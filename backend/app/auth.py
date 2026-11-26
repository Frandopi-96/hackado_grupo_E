"""Registro, inicio y cierre de sesión (HU1).

- Las contraseñas se guardan cifradas con Argon2, nunca en claro.
- La sesión es un token aleatorio que viaja en una cookie HttpOnly
  (el JavaScript de la página no puede leerlo). En la base de datos
  solo se guarda su hash.
"""

import hashlib
import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone

import psycopg
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from .db import get_conn
from .esquemas import AlumnoOut, LoginIn, RegistroIn

router = APIRouter(prefix="/api/auth", tags=["auth"])

_hasher = PasswordHasher()
# Hash de una contraseña cualquiera: se usa para que el login tarde lo mismo
# exista o no el email, y así no se pueda averiguar qué emails están registrados.
_HASH_FALSO = _hasher.hash("contrasena-que-no-existe")

COOKIE_SESION = "sesion"
DURACION_SESION = timedelta(days=7)
# En la demo se entra por HTTP; con HTTPS hay que poner COOKIE_SECURE=true.
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "false").lower() == "true"


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _iniciar_sesion(conn: psycopg.Connection, alumno_id, response: Response) -> None:
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO sesion (token_hash, alumno_id, expira_en) VALUES (%s, %s, %s)",
        (_hash_token(token), alumno_id, datetime.now(timezone.utc) + DURACION_SESION),
    )
    response.set_cookie(
        COOKIE_SESION,
        token,
        max_age=int(DURACION_SESION.total_seconds()),
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE,
        path="/",
    )


def alumno_actual(
    sesion: str | None = Cookie(default=None),
    conn: psycopg.Connection = Depends(get_conn),
) -> dict:
    """Dependencia: devuelve el alumno con sesión iniciada o responde 401."""
    if not sesion:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Inicia sesión para continuar")
    fila = conn.execute(
        """SELECT a.id, a.nombre, a.es_menor
             FROM sesion s JOIN alumno a ON a.id = s.alumno_id
            WHERE s.token_hash = %s AND s.expira_en > now()""",
        (_hash_token(sesion),),
    ).fetchone()
    if fila is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Inicia sesión para continuar")
    return fila


@router.post("/registro", response_model=AlumnoOut, status_code=status.HTTP_201_CREATED)
def registro(datos: RegistroIn, response: Response, conn: psycopg.Connection = Depends(get_conn)):
    alumno_id = uuid.uuid4()
    try:
        conn.execute(
            """INSERT INTO alumno (id, nombre, apellidos, email, password_hash, es_menor)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                alumno_id,
                datos.nombre.strip(),
                datos.apellidos.strip(),
                datos.email.lower(),
                _hasher.hash(datos.password),
                datos.es_menor,
            ),
        )
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe una cuenta con ese email")
    _iniciar_sesion(conn, alumno_id, response)
    return {"id": alumno_id, "nombre": datos.nombre.strip(), "es_menor": datos.es_menor}


@router.post("/login", response_model=AlumnoOut)
def login(datos: LoginIn, response: Response, conn: psycopg.Connection = Depends(get_conn)):
    fila = conn.execute(
        "SELECT id, nombre, es_menor, password_hash FROM alumno WHERE email = %s",
        (datos.email.lower(),),
    ).fetchone()
    try:
        _hasher.verify(fila["password_hash"] if fila else _HASH_FALSO, datos.password)
    except VerifyMismatchError:
        fila = None
    if fila is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email o contraseña incorrectos")
    _iniciar_sesion(conn, fila["id"], response)
    return fila


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    sesion: str | None = Cookie(default=None),
    conn: psycopg.Connection = Depends(get_conn),
):
    if sesion:
        conn.execute("DELETE FROM sesion WHERE token_hash = %s", (_hash_token(sesion),))
    response.delete_cookie(COOKIE_SESION, path="/")
