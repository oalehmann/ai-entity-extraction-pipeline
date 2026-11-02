
import logging
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from schemas import ExtraccionTecnica


# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configurar el modelo
model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"],
    temperature=0
)


# Definir las instrucciones para el modelo
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Eres un analista especializado en infraestructura y software.

        Analiza el texto técnico recibido y extrae la siguiente información:

        1. tecnologias:
           Identifica las tecnologías mencionadas explícitamente.
           No inventes tecnologías que no estén respaldadas por el texto.

        2. nivel_de_criticidad:
           Clasifica la criticidad como baja, media o alta.
           Considera el impacto, la gravedad y la urgencia descritos.
           No supongas que existe un impacto grave si el texto no lo indica.

        3. resumen_tecnico:
           Resume brevemente el problema técnico principal.

        Utiliza únicamente la información disponible en el texto.
        Si la información es ambigua, evita inventar detalles.
        """
    ),
    (
        "human",
        "Analiza el siguiente texto técnico:\n\n{text}"
    )
])

# Conectar el modelo con el esquema Pydantic
structured_model = model.with_structured_output(
    ExtraccionTecnica,
    include_raw=True
)

# Función de validación de respuesta
def validar_respuesta(resultado):

    if resultado["parsing_error"] is not None:
        raise resultado["parsing_error"]

    if resultado["parsed"] is None:
        raise ValueError("El modelo no devolvió una respuesta válida.")

    return resultado["parsed"]

# Construir la cadena LCEL
chain = (
    prompt
    | structured_model
    | RunnableLambda(validar_respuesta)
).with_retry(
    retry_if_exception_type=(Exception,),
    stop_after_attempt=3
)

# Función pública para procesar textos técnicos

async def process_text(text: str) -> ExtraccionTecnica:
    """Procesa un texto técnico y devuelve una extracción validada."""

    logger.info("Iniciando extracción técnica")

    try:
        resultado = await chain.ainvoke({"text": text})

        logger.info("Extracción técnica completada correctamente")
        return resultado

    except Exception:
        logger.exception("Falló el procesamiento del texto")
        raise
