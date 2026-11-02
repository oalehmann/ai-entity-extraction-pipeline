
from enum import Enum

from pydantic import BaseModel, Field


class NivelCriticidad(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class ExtraccionTecnica(BaseModel):
    tecnologias: list[str] = Field(
        min_length=1,
        description="Lista de tecnologías identificadas en el texto."
    )

    nivel_de_criticidad: NivelCriticidad = Field(
        description="Nivel de criticidad: baja, media o alta."
    )

    resumen_tecnico: str = Field(
        min_length=1,
        description="Resumen breve del problema técnico."
    )

