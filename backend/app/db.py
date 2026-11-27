"""Conexión a PostgreSQL y creación de las tablas."""

import os

import psycopg
from psycopg.rows import dict_row

ESQUEMA = """
CREATE TABLE IF NOT EXISTS alumno (
    id            UUID PRIMARY KEY,
    nombre        TEXT NOT NULL,
    apellidos     TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    es_menor      BOOLEAN NOT NULL,
    creado_en     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sesion (
    token_hash TEXT PRIMARY KEY,
    alumno_id  UUID NOT NULL REFERENCES alumno(id) ON DELETE CASCADE,
    expira_en  TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS perfil (
    alumno_id          UUID PRIMARY KEY REFERENCES alumno(id) ON DELETE CASCADE,
    nivel              TEXT NOT NULL,
    intereses          TEXT[] NOT NULL,
    objetivo           TEXT NOT NULL,
    disponibilidad_min INTEGER NOT NULL,
    por_empresa        BOOLEAN NOT NULL,
    actualizado_en     TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


def datos_conexion() -> dict:
    """Datos de conexión a PostgreSQL, leídos de las variables de entorno."""
    return {
        "host": os.environ.get("DB_HOST", "db"),
        "port": int(os.environ.get("DB_PORT", "5432")),
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "dbname": os.environ["POSTGRES_DB"],
    }


def conectar() -> psycopg.Connection:
    return psycopg.connect(**datos_conexion(), row_factory=dict_row, connect_timeout=3)


def crear_tablas() -> None:
    """Crea las tablas si no existen. Se ejecuta al arrancar el backend."""
    with conectar() as conn:
        conn.execute(ESQUEMA)


def get_conn():
    """Dependencia de FastAPI: una conexión por petición.

    Al salir del bloque se hace commit si todo ha ido bien, o rollback si hubo error.
    """
    with conectar() as conn:
        yield conn
