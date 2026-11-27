"""Perfil del alumno: respuestas del formulario inicial (HU1).

El perfil no contiene datos personales: es lo único del alumno que
podrá recibir el Selector de cursos (SPEC, apartado 6).
"""

import psycopg
from fastapi import APIRouter, Depends, HTTPException, status

from .auth import alumno_actual
from .db import get_conn
from .esquemas import PerfilIn, PerfilOut

router = APIRouter(prefix="/api/perfil", tags=["perfil"])

_CAMPOS = "nivel, intereses, objetivo, disponibilidad_min, por_empresa"


@router.get("", response_model=PerfilOut)
def leer_perfil(alumno: dict = Depends(alumno_actual), conn: psycopg.Connection = Depends(get_conn)):
    fila = conn.execute(
        f"SELECT {_CAMPOS} FROM perfil WHERE alumno_id = %s", (alumno["id"],)
    ).fetchone()
    if fila is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Todavía no has completado el formulario")
    return fila


@router.post("", response_model=PerfilOut)
def guardar_perfil(
    datos: PerfilIn,
    alumno: dict = Depends(alumno_actual),
    conn: psycopg.Connection = Depends(get_conn),
):
    """Guarda el perfil. Si ya existía, lo sustituye."""
    conn.execute(
        f"""INSERT INTO perfil (alumno_id, {_CAMPOS})
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (alumno_id) DO UPDATE SET
                nivel = EXCLUDED.nivel,
                intereses = EXCLUDED.intereses,
                objetivo = EXCLUDED.objetivo,
                disponibilidad_min = EXCLUDED.disponibilidad_min,
                por_empresa = EXCLUDED.por_empresa,
                actualizado_en = now()""",
        (
            alumno["id"],
            datos.nivel,
            datos.intereses,
            datos.objetivo,
            datos.disponibilidad_min,
            datos.por_empresa,
        ),
    )
    return datos
