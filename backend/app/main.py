"""API del prototipo de 480 Academy (FastAPI).

Documentación automática (OpenAPI) en /api/docs.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from . import auth, perfil
from .db import conectar, crear_tablas


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield


app = FastAPI(
    title="480 Academy API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(perfil.router)


@app.get("/api/health", tags=["infraestructura"])
def health():
    """Comprueba que el backend responde y que la base de datos está accesible."""
    try:
        with conectar() as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "db": "ok"}
    except Exception:
        # No se devuelve el detalle del error para no exponer datos internos.
        return JSONResponse(
            status_code=503, content={"status": "error", "db": "unreachable"}
        )
