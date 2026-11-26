"""Tests de la HU1: registro, inicio de sesión y formulario inicial.

Se ejecutan dentro del contenedor del backend, contra la base de datos de Docker:
    docker compose exec backend python -m pytest tests -q -p no:cacheprovider

Cada test usa un email único (test-...@ejemplo.com) y al final se borran
todas las cuentas de prueba.
"""

import uuid

import pytest
from fastapi.testclient import TestClient

from app.db import conectar
from app.main import app

PASSWORD = "contrasena-segura-1"
PERFIL_VALIDO = {
    "nivel": "nunca",
    "intereses": ["datos", "web"],
    "objetivo": "empleo",
    "disponibilidad_min": 30,
    "por_empresa": False,
}


def _email() -> str:
    return f"test-{uuid.uuid4().hex[:12]}@ejemplo.com"


def _registro(client, email=None, password=PASSWORD, es_menor=False):
    return client.post(
        "/api/auth/registro",
        json={
            "nombre": "Ana",
            "apellidos": "Prueba",
            "email": email or _email(),
            "password": password,
            "es_menor": es_menor,
        },
    )


@pytest.fixture(scope="module", autouse=True)
def limpiar_cuentas_de_prueba():
    yield
    with conectar() as conn:
        conn.execute("DELETE FROM alumno WHERE email LIKE 'test-%%@ejemplo.com'")


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


# --- Registro e inicio de sesión ---------------------------------------------

def test_registro_crea_cuenta_e_inicia_sesion(client):
    r = _registro(client)
    assert r.status_code == 201
    assert "sesion" in r.cookies
    # Recién registrado todavía no tiene perfil
    assert client.get("/api/perfil").status_code == 404


def test_registro_no_devuelve_datos_sensibles(client):
    datos = _registro(client).json()
    assert set(datos) == {"id", "nombre", "es_menor"}


def test_contrasena_guardada_cifrada(client):
    email = _email()
    _registro(client, email=email)
    with conectar() as conn:
        fila = conn.execute(
            "SELECT password_hash FROM alumno WHERE email = %s", (email,)
        ).fetchone()
    assert fila["password_hash"] != PASSWORD
    assert fila["password_hash"].startswith("$argon2")


def test_registro_email_repetido(client):
    email = _email()
    assert _registro(client, email=email).status_code == 201
    assert _registro(client, email=email.upper()).status_code == 409


def test_registro_contrasena_corta(client):
    assert _registro(client, password="corta").status_code == 422


def test_login_correcto(client):
    email = _email()
    _registro(client, email=email)
    client.cookies.clear()
    r = client.post("/api/auth/login", json={"email": email, "password": PASSWORD})
    assert r.status_code == 200
    assert "sesion" in r.cookies


def test_login_contrasena_incorrecta(client):
    email = _email()
    _registro(client, email=email)
    client.cookies.clear()
    r = client.post("/api/auth/login", json={"email": email, "password": "otra-distinta"})
    assert r.status_code == 401


def test_login_email_inexistente_mismo_error(client):
    r = client.post("/api/auth/login", json={"email": _email(), "password": PASSWORD})
    assert r.status_code == 401
    assert r.json()["detail"] == "Email o contraseña incorrectos"


def test_logout_cierra_la_sesion(client):
    _registro(client)
    token = client.cookies.get("sesion")
    assert client.post("/api/auth/logout").status_code == 204
    client.cookies.set("sesion", token)
    assert client.get("/api/perfil").status_code == 401


# --- Formulario inicial (perfil) ---------------------------------------------

def test_perfil_sin_sesion(client):
    assert client.get("/api/perfil").status_code == 401
    assert client.post("/api/perfil", json=PERFIL_VALIDO).status_code == 401


def test_perfil_guardar_y_leer(client):
    _registro(client)
    r = client.post("/api/perfil", json=PERFIL_VALIDO)
    assert r.status_code == 200
    assert client.get("/api/perfil").json() == PERFIL_VALIDO


def test_perfil_se_puede_rehacer(client):
    _registro(client)
    client.post("/api/perfil", json=PERFIL_VALIDO)
    nuevo = {**PERFIL_VALIDO, "nivel": "otro_lenguaje", "disponibilidad_min": 60}
    client.post("/api/perfil", json=nuevo)
    assert client.get("/api/perfil").json() == nuevo


def test_perfil_no_contiene_datos_personales(client):
    _registro(client)
    client.post("/api/perfil", json=PERFIL_VALIDO)
    datos = client.get("/api/perfil").json()
    assert not {"nombre", "apellidos", "email", "id"} & set(datos)


@pytest.mark.parametrize(
    "cambio",
    [
        {"nivel": "experto"},
        {"intereses": []},
        {"intereses": ["datos", "datos"]},
        {"intereses": ["cocina"]},
        {"disponibilidad_min": 45},
        {"objetivo": None},
    ],
)
def test_perfil_respuestas_no_validas(client, cambio):
    _registro(client)
    r = client.post("/api/perfil", json={**PERFIL_VALIDO, **cambio})
    assert r.status_code == 422
