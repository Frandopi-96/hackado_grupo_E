"""API del prototipo de 480 Academy (FastAPI).

De momento solo expone /api/health para comprobar que el backend
y la base de datos están conectados. La documentación automática
(OpenAPI) queda en /api/docs.
"""

import os

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="480 Academy API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)


def _datos_conexion() -> dict:
    """Datos de conexión a PostgreSQL, leídos de las variables de entorno."""
    return {
        "host": os.environ.get("DB_HOST", "db"),
        "port": int(os.environ.get("DB_PORT", "5432")),
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "dbname": os.environ["POSTGRES_DB"],
    }


@app.get("/api/health")
def health():
    """Comprueba que el backend responde y que la base de datos está accesible."""
    try:
        with psycopg.connect(**_datos_conexion(), connect_timeout=3) as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "db": "ok"}
    except Exception:
        # No se devuelve el detalle del error para no exponer datos internos.
        return JSONResponse(
            status_code=503, content={"status": "error", "db": "unreachable"}
        )
