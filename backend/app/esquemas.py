"""Modelos de entrada y salida de la API (Pydantic)."""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

# Opciones del formulario inicial (HU1). Ninguna es un dato personal.
Nivel = Literal["nunca", "algo", "otro_lenguaje"]
Interes = Literal["datos", "web", "automatizar", "ia"]
Objetivo = Literal["empleo", "mejorar_trabajo", "curiosidad"]
Disponibilidad = Literal[15, 30, 60]


class RegistroIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    apellidos: str = Field(min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    es_menor: bool


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class AlumnoOut(BaseModel):
    id: UUID
    nombre: str
    es_menor: bool


class PerfilIn(BaseModel):
    nivel: Nivel
    intereses: list[Interes] = Field(min_length=1, max_length=4)
    objetivo: Objetivo
    disponibilidad_min: Disponibilidad
    por_empresa: bool

    @field_validator("intereses")
    @classmethod
    def sin_repetidos(cls, v: list[str]) -> list[str]:
        if len(set(v)) != len(v):
            raise ValueError("Los intereses no pueden repetirse")
        return v


class PerfilOut(PerfilIn):
    pass
