
# AI Entity Extraction Pipeline

## 1. Descripción del proyecto

Pipeline de procesamiento de textos técnicos desarrollado con Python, LangChain y Pydantic.

Su objetivo es analizar descripciones de arquitecturas de software, incidentes y errores técnicos para extraer información estructurada y validada.

## 2. Información extraída

El pipeline genera tres campos:

- **tecnologias:** lista de tecnologías identificadas en el texto.
- **nivel_de_criticidad:** clasificación en baja, media o alta.
- **resumen_tecnico:** descripción breve del problema técnico principal.

## 3. Arquitectura

El procesamiento sigue esta secuencia:

1. Recepción del texto técnico.
2. Construcción del prompt mediante ChatPromptTemplate.
3. Procesamiento con un modelo de OpenAI.
4. Generación de una respuesta estructurada según el esquema Pydantic.
5. Validación de los datos.
6. Reintentos automáticos ante excepciones.

La cadena se implementa mediante LCEL (LangChain Expression Language).

## 4. Estructura del proyecto

```text
ai-entity-extraction-pipeline/
│
├── ai-entity-extraction-pipeline.ipynb
├── schemas.py
├── chain.py
├── test_pipeline.py
├── requirements.txt
└── README.md
```

## 5. Requisitos e instalación

Se requiere Python 3.12 y una API Key de OpenAI.

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## 6. Configuración

Configurar la variable de entorno:

```bash
OPENAI_API_KEY=tu_api_key
```

No compartir ni publicar la API Key en el repositorio.

## 7. Uso

Ejemplo de utilización:

```python
import asyncio
from chain import process_text

texto = """
La aplicación FastAPI presenta errores de conexión con PostgreSQL.
El pool de conexiones se agota durante los períodos de alta demanda,
provocando interrupciones en el servicio.
"""

resultado = asyncio.run(process_text(texto))

print(resultado.model_dump_json(indent=2))
```

## 8. Ejemplo de salida

```json
{
  "tecnologias": [
    "FastAPI",
    "PostgreSQL"
  ],
  "nivel_de_criticidad": "alta",
  "resumen_tecnico": "La aplicación presenta problemas de conexión con PostgreSQL debido al agotamiento del pool de conexiones, provocando interrupciones del servicio."
}
```

## 9. Validación y resiliencia

El esquema Pydantic valida:

- Que la lista de tecnologías no esté vacía.
- Que el nivel de criticidad pertenezca al enum definido.
- Que el resumen técnico no esté vacío.

La cadena utiliza `with_retry` para reintentar automáticamente ante excepciones, con un máximo de tres intentos.

## 10. Testing

Ejecutar las pruebas mediante:

```bash
python test_pipeline.py
```

La prueba verifica que el pipeline devuelva un objeto `ExtraccionTecnica` con los campos requeridos.
