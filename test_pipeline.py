
import asyncio

from schemas import ExtraccionTecnica
from chain import process_text


async def test_process_text():

    texto = """
    La aplicación FastAPI presenta errores de conexión con PostgreSQL.
    El pool de conexiones se agota durante los períodos de alta demanda,
    provocando interrupciones en el servicio.
    """

    resultado = await process_text(texto)

    assert isinstance(resultado, ExtraccionTecnica)
    assert len(resultado.tecnologias) > 0
    assert resultado.nivel_de_criticidad.value in ["baja", "media", "alta"]
    assert len(resultado.resumen_tecnico) > 0

    print("Todas las verificaciones fueron superadas.")


if __name__ == "__main__":
    asyncio.run(test_process_text())
