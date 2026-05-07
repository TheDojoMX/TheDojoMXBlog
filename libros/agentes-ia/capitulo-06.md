# Capitulo 6: Contratos Tipados -- De JSON Schemas a Garantias Formales

> "Si tu agente responde con texto libre, estas rezando para que funcione. Y rezar no es una estrategia de ingenieria."

---

En el Capitulo 5 construimos el harness: guardrails, circuit breakers, rate limiters, sandboxing y observabilidad. El harness controla *que* puede hacer el agente y *cuanto*. Pero hay un problema que el harness no resuelve por si solo: **como se comunica el agente con el resto del sistema**.

Cuando un agente produce una respuesta, esa respuesta debe ser consumida por otro componente: otro agente, una API, una base de datos, una interfaz de usuario. Si la respuesta es texto libre --una cadena de caracteres sin estructura predefinida--, cada componente que la consume necesita interpretarla. Y la interpretacion de texto libre es el terreno fertil donde nacen los bugs mas dificiles de diagnosticar.

Un agente produce un JSON con el campo `"action": "delete"` y `"confirmation": false`. El JSON es estructuralmente valido. Pasa todas las validaciones del schema. El sistema downstream lo ejecuta sin quejarse. Resultado: datos borrados, sin confirmacion, sin vuelta atras. Nadie valido el **significado** de la salida, solo su **forma**.

Este es el problema central de la comunicacion entre agentes y entre un agente y su entorno: la validacion estructural no es suficiente. Necesitamos **contratos tipados** --acuerdos formales sobre la forma *y* el significado de los datos intercambiados-- que garanticen no solo que los datos tienen la estructura correcta, sino que su contenido es semanticamente valido.

En este capitulo vamos a recorrer el espectro completo de soluciones, desde el parsing con regex (nivel cero) hasta la verificacion formal con TLA+ (nivel cinco), pasando por JSON Schemas, Pydantic con validadores semanticos, tipos dependientes simulados y Design by Contract. No se trata solo de herramientas: se trata de entender que nivel de garantia necesitas y cuanto estas dispuesto a pagar por el.

---

## 6.1 De texto libre a structured outputs: la evolucion

Para entender donde estamos, conviene mirar como hemos llegado hasta aqui. La historia de la comunicacion con LLMs es la historia de ganar control sobre lo impredecible.

### La era del regex y la esperanza

En 2023, la forma estandar de obtener datos estructurados de un LLM era algo como esto:

```python
import re

response = llm.complete(
    "Extrae el nombre y edad del siguiente texto: "
    "'Juan tiene 30 anos'"
)
# response = "El nombre es Juan y la edad es 30 anos."

# Parsing con regex... y esperanzas
name_match = re.search(r"nombre es (\w+)", response)
age_match = re.search(r"edad es (\d+)", response)

if name_match and age_match:
    name = name_match.group(1)
    age = int(age_match.group(1))
else:
    # Que hacemos aqui? Rezar.
    raise ValueError("No pude parsear la respuesta del LLM")
```

Esto funcionaba... a veces. El problema fundamental es que un LLM no tiene obligacion de formatear su respuesta de ninguna manera particular. Podia responder "Juan, 30", o "Nombre: Juan. Edad: treinta", o incluso inventar una conversacion ficticia. Estabamos en territorio de **best effort**: haciamos nuestro mejor esfuerzo, pero no teniamos garantias.

El regex es una herramienta poderosa para texto con estructura predecible. Pero la salida de un LLM es, por definicion, impredecible. El espacio de posibles formatos es combinatoriamente explosivo. Para cada nuevo formato que el modelo inventa, necesitas un nuevo patron. Es una carrera que no puedes ganar.

### JSON como lingua franca

El siguiente paso fue pedirle al modelo que respondiera en JSON, generalmente con instrucciones en el prompt:

```python
prompt = """Extrae el nombre y edad del siguiente texto.
Responde SOLO con un JSON valido con las claves "name" y "age".
No incluyas ningun otro texto.

Texto: 'Juan tiene 30 anos'"""

response = llm.complete(prompt)
data = json.loads(response)  # Puede fallar
```

Mejor, pero seguimos en territorio de esperanzas. El modelo puede incluir un preambulo como "Aqui tienes el JSON:" antes del objeto. Puede usar comillas simples en lugar de dobles. Puede generar JSON invalido con comas finales o sin cerrar llaves. Peor aun: puede generar un JSON valido pero con claves diferentes a las que esperamos, como `"nombre"` en lugar de `"name"`.

La instrucion en el prompt es una *sugerencia*, no un *contrato*. Y las sugerencias se ignoran con una frecuencia que crece en proporcion directa a la complejidad de la tarea.

### Structured outputs: el primer contrato real

Con la llegada de los **Structured Outputs** en las APIs de los proveedores de LLMs, finalmente obtuvimos un mecanismo formal. Para 2026, todos los proveedores principales --Anthropic, Google, OpenAI, Mistral-- soportan structured outputs [OpenAI, 2024; Anthropic, 2025]. Le proporcionas un JSON Schema al modelo y la API te **garantiza** que la respuesta se ajustara a ese schema.

La garantia no es estadistica: es determinista. La API usa constrained decoding --modifica las probabilidades de los tokens durante la generacion para hacer imposible que el modelo produzca una salida que viole el schema-- o valida y reintenta internamente. El resultado es que si defines un schema con un campo `"age"` de tipo `integer`, jamas recibiras un string.

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person_extraction",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 150,
                    },
                },
                "required": ["name", "age"],
                "additionalProperties": False,
            },
        },
    },
    messages=[
        {
            "role": "user",
            "content": "Extrae el nombre y edad: 'Juan tiene 30 anos'",
        }
    ],
)
```

La evolucion es analoga a la de la web: de respuestas de texto libre a formatos estandarizados con contratos claros. En REST, el contrato es la combinacion de URIs, metodos HTTP y tipos de contenido. En agentes, el contrato es el JSON Schema.

> **Nota de produccion**: forzar structured outputs siempre tiene un costo cognitivo. El modelo "gasta capacidad" en formatear correctamente el JSON en lugar de razonar sobre el contenido. En la practica, muchos equipos usan un enfoque hibrido: dejan que el modelo razone en texto libre y luego extraen datos estructurados con un paso de parsing o con un segundo llamado mas pequeno y barato [Pydantic, 2025].

Pero aqui viene la pregunta incomoda: **es suficiente?**

---

## 6.2 JSON Schema como contrato basico: que garantiza y que no

Un JSON Schema te da garantias **estructurales**. Puede asegurarte que:

- Un campo existe y es del tipo correcto
- Un numero esta dentro de un rango
- Un string tiene una longitud minima o maxima
- Un valor pertenece a un conjunto enumerado
- Un objeto tiene exactamente las propiedades requeridas

Esto es poderoso. Pero hay una categoria entera de problemas que un JSON Schema **no puede resolver**: la **validacion semantica**.

### El problema de la validez estructural vs. semantica

Considera este schema para las acciones de un agente:

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["read", "write", "delete"]
    },
    "target": {
      "type": "string"
    },
    "confirmation": {
      "type": "boolean"
    }
  },
  "required": ["action", "target"]
}
```

El siguiente objeto es **estructuralmente valido**:

```json
{
  "action": "delete",
  "target": "/",
  "confirmation": false
}
```

Pasa todas las validaciones del schema. Pero semanticamente, es una instruccion para borrar el directorio raiz del sistema. Y `confirmation` es `false`, pero el agente igual podria ejecutarla porque el campo no es requerido y nada en el schema dice que `delete` necesita `confirmation: true`.

La validacion de estructura no sustituye a la validacion semantica. Un JSON valido puede contener instrucciones peligrosas, igual que un SQL parametrizado puede contener logica maliciosa si no validamos los valores.

### Las limitaciones formales de JSON Schema

Desde la perspectiva de la teoria de tipos, JSON Schema es un lenguaje de validacion estructural con restricciones de primer orden sobre valores individuales. Aunque desde el draft 7 (2017) soporta `if/then/else` para expresar relaciones proposicionales entre campos, la sintaxis es verbosa, fragil y tiene limites duros. No puede expresar:

- **Invariantes temporales**: "el campo `updated_at` debe ser posterior a `created_at`"
- **Restricciones contextuales**: "el agente solo puede ejecutar `delete` si tiene el rol `admin`"
- **Propiedades semanticas**: "el campo `email` debe ser un email real que exista"
- **Relaciones aritmeticas entre campos**: "el campo `discount_price` debe ser menor que `original_price`"
- **Dependencias de estado externo**: "la accion requiere que el usuario tenga saldo suficiente"

Para estas restricciones, necesitamos algo mas expresivo. Aqui es donde entra Pydantic.

---

## 6.3 Pydantic: contratos inteligentes en runtime

Si JSON Schema es un contrato en papel, **Pydantic** es un contrato con un abogado que lo ejecuta en tiempo real. Pydantic es la libreria de validacion de datos mas popular en Python, y se ha convertido en el estandar de facto para definir contratos de datos en sistemas con agentes [Liu, 2024; Pydantic, 2025].

> **Importante**: todos los ejemplos en este capitulo usan **Pydantic v2** (`BaseModel`, `Field`, `model_validator`, `field_validator`). Si tu proyecto aun usa Pydantic v1, migra antes de implementar contratos para agentes. Mezclar APIs de v1 y v2 es una fuente comun de errores en produccion.

### De schemas a modelos ejecutables

La idea fundamental de Pydantic es simple: defines una clase Python con anotaciones de tipo, y Pydantic valida que los datos se ajusten a esas anotaciones al momento de crear la instancia. Pero a diferencia de JSON Schema, puedes agregar logica de validacion arbitraria:

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
from typing import Optional
from datetime import datetime


class Action(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


class AgentCommand(BaseModel):
    """Contrato para un comando emitido por un agente.

    Cada campo tiene restricciones estructurales (tipo, rango)
    y los validadores agregan restricciones semanticas que
    JSON Schema no puede expresar.
    """
    action: Action
    target: str = Field(..., min_length=1, max_length=500)
    confirmation: bool = False
    reason: str = Field(
        ...,
        min_length=10,
        description="Justificacion para la accion",
    )

    @field_validator("target")
    @classmethod
    def validate_target(cls, v: str, info) -> str:
        """Prevenir paths peligrosos.

        Esta es una lista de exclusion explicita. En produccion,
        complementa con una lista de inclusion (allowlist) que
        define los paths permitidos.
        """
        dangerous_paths = ["/", "/etc", "/usr", "/var", "/home"]
        if v in dangerous_paths:
            raise ValueError(
                f"El path '{v}' esta en la lista de paths protegidos"
            )
        return v

    @model_validator(mode="after")
    def validate_delete_has_confirmation(self) -> "AgentCommand":
        """Las acciones destructivas requieren confirmacion explicita.

        Este es el tipo de invariante que JSON Schema no puede
        expresar: una relacion condicional entre dos campos
        donde el valor de uno depende del valor del otro.
        """
        if self.action == Action.DELETE and not self.confirmation:
            raise ValueError(
                "Las acciones de tipo DELETE requieren confirmation=True"
            )
        return self
```

Observa lo que hemos ganado con respecto al JSON Schema puro:

1. **Validacion cross-field**: podemos expresar que `delete` requiere `confirmation`
2. **Listas de exclusion**: podemos prohibir ciertos valores especificos con logica arbitraria
3. **Validacion semantica custom**: podemos ejecutar cualquier logica de Python
4. **Documentacion ejecutable**: los mensajes de error explican exactamente que salio mal

Intentemos crear un comando invalido:

```python
try:
    cmd = AgentCommand(
        action="delete",
        target="/",
        confirmation=False,
        reason="Limpieza general del sistema",
    )
except ValidationError as e:
    print(e)
    # 2 validation errors for AgentCommand
    # target
    #   Value error, El path '/' esta en la lista de paths protegidos
    # confirmation
    #   Value error, Las acciones de tipo DELETE requieren confirmation=True
```

Pydantic atrapa ambos errores en una sola pasada. No ejecuta el comando y proporciona mensajes de error que un desarrollador (o un LLM con un bucle de retroalimentacion) puede usar para corregir la respuesta.

### Validadores semanticos avanzados

Los validadores de Pydantic pueden ir mucho mas alla de comparaciones simples. Puedes implementar logica de negocio completa:

```python
class TransferCommand(BaseModel):
    """Contrato para una transferencia de dinero entre cuentas.

    Ilustra validaciones semanticas que requieren conocimiento
    del dominio y que son imposibles de expresar en JSON Schema.
    """
    from_account: str = Field(..., pattern=r"^[A-Z]{2}\d{20}$")
    to_account: str = Field(..., pattern=r"^[A-Z]{2}\d{20}$")
    amount: float = Field(..., gt=0, le=50_000)
    currency: str = Field(..., pattern=r"^[A-Z]{3}$")
    reason: str = Field(..., min_length=10, max_length=500)
    requires_approval: bool = False

    @model_validator(mode="after")
    def validate_transfer_rules(self) -> "TransferCommand":
        # Las cuentas deben ser diferentes
        if self.from_account == self.to_account:
            raise ValueError(
                "No se puede transferir a la misma cuenta"
            )

        # Montos grandes requieren aprobacion
        if self.amount > 10_000 and not self.requires_approval:
            raise ValueError(
                f"Transferencias mayores a 10,000 {self.currency} "
                f"requieren requires_approval=True"
            )

        # Validar pares de moneda permitidos
        allowed_currencies = {"USD", "EUR", "MXN", "BRL", "COP"}
        if self.currency not in allowed_currencies:
            raise ValueError(
                f"Moneda '{self.currency}' no soportada. "
                f"Monedas permitidas: {allowed_currencies}"
            )

        return self

    @field_validator("reason")
    @classmethod
    def reason_not_generic(cls, v: str) -> str:
        """Rechazar justificaciones genericas.

        Un agente que dice 'transferencia de fondos' como razon
        no esta proporcionando informacion util para auditoria.
        """
        generic_reasons = [
            "transferencia",
            "pago",
            "transfer",
            "payment",
            "envio de dinero",
        ]
        if v.lower().strip() in generic_reasons:
            raise ValueError(
                "La justificacion es demasiado generica. "
                "Proporciona contexto especifico para auditoria."
            )
        return v
```

Estos validadores capturan invariantes de negocio que ningun JSON Schema podria expresar. Y lo hacen con Python estandar, sin necesidad de aprender un lenguaje de especificacion nuevo.

### Instructor: Pydantic nativo con LLMs

La libreria **Instructor** de Jason Liu lleva esta idea un paso mas alla: integra Pydantic directamente con las APIs de los LLMs, de forma que el modelo genera objetos Pydantic directamente [Liu, 2024]:

```python
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field


client = instructor.from_openai(OpenAI())


class AnalysisResult(BaseModel):
    sentiment: str = Field(
        ..., pattern=r"^(positive|negative|neutral)$"
    )
    confidence: float = Field(..., ge=0.0, le=1.0)
    key_topics: list[str] = Field(
        ..., min_length=1, max_length=10
    )
    summary: str = Field(..., min_length=20, max_length=500)


# Instructor maneja los reintentos automaticamente
# si el LLM produce un output que no valida
result = client.chat.completions.create(
    model="gpt-4o",
    response_model=AnalysisResult,
    max_retries=3,
    messages=[
        {
            "role": "user",
            "content": (
                "Analiza: 'El producto es excelente "
                "pero el envio fue lento'"
            ),
        }
    ],
)

# result es un AnalysisResult completamente validado
print(result.sentiment)    # "neutral" o "positive"
print(result.confidence)   # 0.75
print(result.key_topics)   # ["producto", "envio", "calidad"]
```

Lo interesante de Instructor es que implementa un **bucle de retroalimentacion**: si la validacion de Pydantic falla, Instructor envia los errores de vuelta al LLM y le pide que corrija su respuesta. Los contratos tipados no solo detectan errores: **guian al sistema hacia respuestas correctas**. Es el mismo principio del loop agentico del Capitulo 3, pero aplicado a la validacion de salidas.

### PydanticAI: el framework de agentes con contratos nativos

El equipo de Pydantic lanzo **PydanticAI**, un framework de agentes que trata los contratos tipados como ciudadanos de primera clase [Pydantic, 2025]. A diferencia de frameworks como LangChain donde la validacion de salida es un paso opcional, en PydanticAI el tipo de salida es parte de la definicion del agente:

```python
from pydantic_ai import Agent
from pydantic import BaseModel, Field


class CityInfo(BaseModel):
    name: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    population: int = Field(..., gt=0)
    notable_fact: str = Field(..., min_length=20)


agent = Agent(
    "openai:gpt-4o",
    result_type=CityInfo,
    system_prompt=(
        "Eres un experto en geografia. Proporciona informacion "
        "precisa y verificable sobre ciudades."
    ),
)

result = agent.run_sync("Dime sobre Tokio")
# result.data es un CityInfo validado
print(result.data.name)        # "Tokio"
print(result.data.population)  # 13960000
```

PydanticAI implementa tres metodos diferentes para obtener datos estructurados del modelo: **Tool Output** (usa tool calls para producir la salida), **Native Output** (requiere que el modelo produzca contenido JSON conforme a un schema) y **Prompted Output** (inyecta el schema deseado en las instrucciones del prompt). El framework selecciona automaticamente el metodo mas apropiado segun las capacidades del modelo.

---

## 6.4 Tipos dependientes y contratos entre agentes

Hasta aqui hemos cubierto lo que la industria usa hoy en produccion. Pero si queremos entender hacia donde va el campo --y como construir sistemas genuinamente robustos--, necesitamos adentrarnos en territorio mas teorico: los **tipos dependientes** y los **refinement types**.

### El problema: tipos demasiado amplios

Considera la siguiente definicion:

```python
class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any]
```

El campo `tool_name` es un `str`. Pero no cualquier string es un nombre de herramienta valido. Y `arguments` es un `dict` generico, pero los argumentos validos dependen de **que herramienta** estas llamando. El tipo `str` es demasiado amplio: permite infinitos valores donde solo unos pocos son validos.

En un sistema de agentes real, esta imprecision de tipos causa errores en cascada. El agente genera `{"tool_name": "serch", "arguments": {"q": "clima"}}` (nota el typo en "serch"), y el sistema falla silenciosamente o lanza una excepcion generica que no ayuda a diagnosticar el problema.

### Tipos dependientes en la teoria

Los tipos dependientes vienen de la teoria de tipos de Martin-Lof y son la base de lenguajes como **Idris**, **Agda** y **Lean** [Martin-Lof, 1984]. La idea fundamental es que los tipos pueden ser funciones de valores. Por ejemplo, un `Vect n a` en Idris es un vector cuyo *tipo* incluye su longitud `n`, de forma que el compilador rechaza en tiempo de compilacion cualquier intento de llamar `head` sobre un vector vacio.

En pseudocodigo inspirado en Liquid Haskell:

```haskell
-- Un tipo refinado: un string que esta en la lista de herramientas
type ToolName = {v: String | v `elem` availableTools}

-- Los argumentos dependen del nombre de la herramienta
type ToolCall = {
  toolName: ToolName,
  arguments: ArgumentsFor toolName  -- Tipo dependiente
}
```

Observa la magia en `ArgumentsFor toolName`: el **tipo** de los argumentos depende del **valor** del nombre de la herramienta. Esto es un tipo dependiente: un tipo parametrizado por un valor, no solo por otro tipo.

Es elegante, pero en la practica nadie construye agentes de IA con Idris. Lo relevante es la *idea*: si pudieras expresar en el sistema de tipos cosas como "este agente solo puede llamar herramientas de la lista X" y "los argumentos de `search` deben ser un string no vacio de maximo 100 caracteres", eliminarias categorias enteras de errores antes de que lleguen a produccion.

### Aproximaciones practicas en Python: discriminated unions

No necesitas Idris para obtener **algunas** de las garantias de los tipos dependientes. En Python, la combinacion de `Literal`, `Union` y Pydantic te acerca considerablemente:

```python
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field


# Diferentes modelos de argumentos para cada herramienta
class SearchArgs(BaseModel):
    query: str = Field(..., min_length=1, max_length=100)
    max_results: int = Field(default=10, ge=1, le=100)


class CalculateArgs(BaseModel):
    expression: str = Field(
        ..., pattern=r"^[\d\s\+\-\*\/\(\)\.]+$"
    )


class SendEmailArgs(BaseModel):
    to: Annotated[
        str,
        Field(pattern=r"^[a-zA-Z0-9_.+-]+@company\.com$"),
    ]
    subject: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)


# "Tipo dependiente" simulado con discriminated unions
class SearchCall(BaseModel):
    tool_name: Literal["search"]
    arguments: SearchArgs


class CalculateCall(BaseModel):
    tool_name: Literal["calculate"]
    arguments: CalculateArgs


class SendEmailCall(BaseModel):
    tool_name: Literal["send_email"]
    arguments: SendEmailArgs


# La union discriminada vincula tool_name con
# el tipo de argumentos correcto
ToolCall = Union[SearchCall, CalculateCall, SendEmailCall]


def execute_tool_call(raw_data: dict) -> str:
    """Ejecuta un tool call con validacion de tipos dependientes.

    Pydantic automaticamente selecciona el modelo correcto
    basandose en el valor de tool_name (discriminated union).
    Si tool_name es 'search', valida que arguments sea SearchArgs.
    Si es 'calculate', valida que sea CalculateArgs. Y asi.
    """
    from pydantic import TypeAdapter

    adapter = TypeAdapter(ToolCall)
    call = adapter.validate_python(raw_data)

    match call:
        case SearchCall():
            return search(call.arguments.query, call.arguments.max_results)
        case CalculateCall():
            return calculate(call.arguments.expression)
        case SendEmailCall():
            return send_email(
                call.arguments.to,
                call.arguments.subject,
                call.arguments.body,
            )
```

Lo que estamos haciendo es simular tipos dependientes con el sistema de tipos existente. No es tan expresivo como Idris, pero en la practica cubre la mayoria de los casos que necesitamos en sistemas de agentes. El beneficio clave: si el agente genera `{"tool_name": "search", "arguments": {"expression": "2+2"}}`, Pydantic rechaza la entrada porque los argumentos no coinciden con el schema de `SearchArgs`.

### Contratos entre agentes en un pipeline

En un sistema multi-agente, cada agente es un componente con una interfaz. Los contratos tipados definen esas interfaces:

```python
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Annotated
from datetime import datetime


# Tipo compartido para nivel de confianza
Confidence = Annotated[
    float,
    Field(ge=0.0, le=1.0, description="Nivel de confianza"),
]


class Source(BaseModel):
    """Fuente de informacion con metadatos de confiabilidad."""
    url: str = Field(..., pattern=r"^https?://.+")
    title: str = Field(..., min_length=1, max_length=300)
    retrieved_at: datetime
    reliability_score: Confidence


# === Contrato: Investigador -> Analista ===

class ResearchResult(BaseModel):
    """Contrato de salida del Agente Investigador.

    Define exactamente que produce el investigador y que
    puede esperar el analista. Si el investigador produce
    algo que no cumple este contrato, la validacion falla
    ANTES de que el analista lo procese.
    """
    query: str = Field(
        ..., min_length=5, description="La consulta original"
    )
    sources: list[Source] = Field(..., min_length=1, max_length=20)
    raw_findings: list[str] = Field(..., min_length=1)
    confidence: Confidence
    timestamp: datetime = Field(default_factory=datetime.now)

    @model_validator(mode="after")
    def findings_need_sources(self) -> "ResearchResult":
        """Cada hallazgo debe estar respaldado por fuentes."""
        if len(self.raw_findings) > len(self.sources) * 3:
            raise ValueError(
                f"Demasiados hallazgos ({len(self.raw_findings)}) "
                f"para {len(self.sources)} fuentes. "
                f"Maximo 3 hallazgos por fuente."
            )
        return self


# === Contrato: Analista -> Escritor ===

class Insight(BaseModel):
    claim: str = Field(..., min_length=10, max_length=500)
    evidence: list[str] = Field(..., min_length=1)
    confidence: Confidence
    category: Literal[
        "trend", "anomaly", "correlation", "prediction"
    ]


class AnalysisResult(BaseModel):
    """Contrato de salida del Agente Analista."""
    research_query: str
    insights: list[Insight] = Field(
        ..., min_length=1, max_length=10
    )
    overall_confidence: Confidence
    limitations: list[str] = Field(..., min_length=1)
    recommended_actions: list[str] = Field(
        default_factory=list, max_length=5
    )

    @model_validator(mode="after")
    def confidence_consistent(self) -> "AnalysisResult":
        """La confianza general no puede exceder la mas alta."""
        if self.insights:
            max_conf = max(i.confidence for i in self.insights)
            if self.overall_confidence > max_conf + 0.1:
                raise ValueError(
                    f"overall_confidence ({self.overall_confidence}) "
                    f"no puede exceder significativamente el insight "
                    f"mas confiable ({max_conf})"
                )
        return self


# === Orquestador con validacion en cada paso ===

class ContractOrchestrator:
    """Orquestador que valida contratos entre cada par de agentes.

    Si la validacion falla en cualquier paso, el error se
    propaga con informacion clara de que contrato se violo
    y por que. No hay ejecucion silenciosa de datos invalidos.
    """

    async def run_pipeline(self, query: str) -> dict:
        # Paso 1: Investigacion
        raw_research = await self.researcher.run(query)
        research = ResearchResult.model_validate(raw_research)

        # Paso 2: Analisis
        raw_analysis = await self.analyst.run(
            research.model_dump()
        )
        analysis = AnalysisResult.model_validate(raw_analysis)

        # Paso 3: Escritura
        raw_report = await self.writer.run(
            analysis=analysis.model_dump(),
            sources=[s.model_dump() for s in research.sources],
        )
        report = FinalReport.model_validate(raw_report)

        return report.model_dump()
```

El patron es claro: cada transicion entre agentes pasa por una barrera de validacion. Los datos nunca fluyen sin validar de un agente a otro. Si el Agente Investigador produce algo que no cumple el contrato `ResearchResult`, el error se detecta *antes* de que el Agente Analista lo procese. Esto es defensa en profundidad aplicada a la comunicacion entre componentes.

---

## 6.5 Design by Contract: las ideas de Bertrand Meyer aplicadas a agentes

En 1986, Bertrand Meyer introdujo el concepto de **Design by Contract** en el lenguaje Eiffel [Meyer, 1997]. La idea es que cada componente de software tiene un contrato explicito con tres partes:

- **Precondiciones**: que debe ser verdad antes de llamar a una funcion
- **Postcondiciones**: que sera verdad despues de que la funcion retorne
- **Invariantes**: que debe ser verdad siempre

Aplicado a las herramientas de un agente, este concepto se traduce directamente:

```python
from dataclasses import dataclass
from typing import Callable, Any


class ContractViolation(Exception):
    """Excepcion que indica que un contrato fue violado.

    A diferencia de ValueError (que indica datos incorrectos),
    ContractViolation indica un fallo en la logica del sistema:
    o bien la precondicion no se verifico correctamente, o
    bien la implementacion de la herramienta tiene un bug.
    """
    pass


@dataclass
class ToolContract:
    """Contrato para una herramienta que un agente puede invocar.

    El contrato especifica que debe ser verdad antes de ejecutar
    (precondiciones), que sera verdad despues (postcondiciones),
    y que debe ser verdad siempre (invariantes del sistema).
    """
    name: str
    preconditions: list[Callable[[dict], bool]]
    postconditions: list[Callable[[dict, Any], bool]]
    invariants: list[Callable[[], bool]]

    def validate_call(self, arguments: dict) -> bool:
        """Verifica precondiciones antes de ejecutar."""
        for pre in self.preconditions:
            if not pre(arguments):
                raise ContractViolation(
                    f"Precondicion violada para {self.name}: "
                    f"{pre.__doc__}"
                )
        return True

    def validate_result(
        self, arguments: dict, result: Any
    ) -> bool:
        """Verifica postcondiciones despues de ejecutar."""
        for post in self.postconditions:
            if not post(arguments, result):
                raise ContractViolation(
                    f"Postcondicion violada para {self.name}: "
                    f"{post.__doc__}"
                )
        return True

    def check_invariants(self) -> bool:
        """Verifica que los invariantes del sistema se mantienen."""
        for inv in self.invariants:
            if not inv():
                raise ContractViolation(
                    f"Invariante violada: {inv.__doc__}"
                )
        return True


# Ejemplo: contrato para una herramienta de base de datos
db_query_contract = ToolContract(
    name="database_query",
    preconditions=[
        lambda args: "query" in args,
        # """La consulta debe existir"""
        lambda args: "SELECT" in args["query"].upper(),
        # """Solo queries de lectura (SELECT)"""
        lambda args: "DROP" not in args["query"].upper(),
        # """Nunca DROP"""
        lambda args: args.get("limit", 100) <= 1000,
        # """Limite de resultados razonable"""
    ],
    postconditions=[
        lambda args, result: isinstance(result, list),
        # """El resultado debe ser una lista"""
        lambda args, result: len(result) <= args.get("limit", 100),
        # """Respeta el limite solicitado"""
    ],
    invariants=[
        lambda: True,  # Placeholder: verificar conexion a BD
        # """La base de datos esta disponible"""
    ],
)
```

Las `assert` y verificaciones de contrato no son validaciones de input del usuario: son contratos del modulo. Si una postcondicion falla, hay un bug en la implementacion, no en los datos. Esta distincion es fundamental y viene directamente de Meyer: las precondiciones son responsabilidad del **llamador** (el agente), las postcondiciones son responsabilidad del **proveedor** (la herramienta).

### El agente con contratos

Un agente que ejecuta herramientas con contratos verifica antes y despues de cada accion:

```python
class ContractAwareAgent:
    """Agente que verifica contratos en cada tool call.

    El flujo es: verificar invariantes -> verificar
    precondiciones -> ejecutar -> verificar postcondiciones.
    Si cualquier paso falla, la excepcion ContractViolation
    proporciona contexto claro para diagnostico.
    """

    def __init__(self, tools: dict[str, ToolContract]):
        self.tools = tools
        self.call_history: list[dict] = []

    def execute_tool(
        self, tool_name: str, arguments: dict
    ) -> Any:
        contract = self.tools.get(tool_name)
        if not contract:
            raise ValueError(f"Herramienta desconocida: {tool_name}")

        # 1. Verificar invariantes del sistema
        contract.check_invariants()

        # 2. Verificar precondiciones
        contract.validate_call(arguments)

        # 3. Ejecutar la herramienta
        result = self._run_tool(tool_name, arguments)

        # 4. Verificar postcondiciones
        contract.validate_result(arguments, result)

        # 5. Registrar para auditoria
        self.call_history.append({
            "tool": tool_name,
            "arguments": arguments,
            "result_type": type(result).__name__,
            "timestamp": datetime.now().isoformat(),
        })

        return result

    def _run_tool(self, tool_name: str, arguments: dict) -> Any:
        """Ejecuta la herramienta real. En produccion, esto
        delega al runtime del agente."""
        raise NotImplementedError
```

Este patron conecta directamente con el harness del Capitulo 5: los contratos de herramientas son una forma de guardrail que opera a nivel de interfaz, no de contenido. El guardrail dice "no puedes enviar contenido sensible"; el contrato dice "esta herramienta solo acepta queries SELECT con limite menor a 1000".

---

## 6.6 Hacia la verificacion formal: TLA+ y el futuro

Los contratos individuales garantizan que cada interaccion entre un agente y una herramienta es correcta. Pero en un sistema multi-agente, lo que realmente queremos verificar son **protocolos**: secuencias de interacciones que deben cumplir ciertas propiedades globales. Aqui es donde entran herramientas como **TLA+**, el lenguaje de especificacion formal creado por Leslie Lamport [Lamport, 2002].

### Que es TLA+ y por que importa

TLA+ permite modelar sistemas concurrentes y verificar que cumplen ciertas propiedades en **todos** los estados posibles. No es un test que ejecutas con algunos inputs: es una prueba exhaustiva de todos los escenarios posibles dentro del modelo. Si defines correctamente tu sistema en TLA+ y el model checker no encuentra violaciones, puedes tener certeza matematica de que las propiedades se cumplen.

Podemos usarlo para modelar la interaccion entre agentes:

```tla
---- MODULE AgentProtocol ----
EXTENDS Integers, Sequences

VARIABLES
    agentState,      \* Estado de cada agente
    toolCallCount,   \* Contador de llamadas a herramientas
    totalCostUSD     \* Costo acumulado del sistema

\* Los agentes pueden estar en estos estados
AgentStates == {
    "idle", "thinking", "calling_tool",
    "waiting", "done", "error"
}

\* INVARIANTE: ningun agente puede hacer mas de 10
\* llamadas a herramientas por tarea
ToolCallLimit ==
    \A agent \in Agents:
        toolCallCount[agent] <= 10

\* INVARIANTE: el costo total nunca excede el presupuesto
BudgetRespected ==
    totalCostUSD <= MAX_BUDGET_USD

\* INVARIANTE: si un agente esta en "error",
\* no puede llamar herramientas
ErrorBlocksTools ==
    \A agent \in Agents:
        agentState[agent] = "error" =>
            agentState[agent] # "calling_tool"

\* PROPIEDAD DE LIVENESS: todo agente eventualmente
\* llega a "done" o "error" (terminacion garantizada)
EventualTermination ==
    \A agent \in Agents:
        <>(agentState[agent] \in {"done", "error"})

====
```

Este es un **sketch** de especificacion, no una spec completa (faltan `Init`, `Next` y la especificacion completa de transiciones). Pero ilustra la idea: TLA+ puede explorar todos los estados posibles del sistema y verificar que las propiedades se cumplen siempre.

### Agent Behavioral Contracts: la investigacion reciente

En 2025, investigadores formalizaron el concepto de **Agent Behavioral Contracts** (ABC), un framework que lleva los principios de Design by Contract a los agentes autonomos [Varios, 2025]. Un contrato ABC se define como `C = (P, I, G, R)`:

- **P** (Preconditions): que debe ser verdad antes de que el agente actue
- **I** (Invariants): que debe ser verdad siempre durante la ejecucion
- **G** (Governance): politicas que restringen el comportamiento
- **R** (Recovery): mecanismos de recuperacion cuando algo sale mal

Este framework es compatible con la implementacion que hemos construido en este capitulo: nuestro `ToolContract` cubre P e I, el harness del Capitulo 5 cubre G (guardrails, circuit breakers) y R (fallbacks, escalacion humana). La contribucion de ABC es formalizar la relacion entre estos componentes como un todo coherente.

Martin Kleppmann ha argumentado que la IA hara que la verificacion formal se vuelva mainstream [Kleppmann, 2025]. Su tesis es que los LLMs pueden generar especificaciones formales a partir de descripciones en lenguaje natural, democratizando el acceso a herramientas que antes requeran formacion matematica especializada. Si esta prediccion se cumple, la verificacion formal de agentes dejara de ser un lujo academico para convertirse en una practica estandar de ingenieria.

### Es practico usar verificacion formal hoy?

Siendo honestos: para la mayoria de equipos, la verificacion formal completa con TLA+ es excesiva. El costo de aprender TLA+, modelar el sistema correctamente y mantener la especificacion actualizada es alto. Pero para sistemas criticos donde la comunicacion incorrecta entre agentes puede causar perdidas financieras o dano real, empieza a justificarse.

La recomendacion practica es esta: usa el nivel de verificacion proporcional al riesgo. No necesitas TLA+ para un chatbot de soporte. Si necesitas algo mas fuerte que Pydantic para un sistema que maneja transferencias bancarias.

---

## 6.7 El espectro de garantias: elige tu nivel

Ahora podemos visualizar el panorama completo. Piensa en las garantias de comunicacion entre agentes como un espectro con seis niveles:

| Nivel | Herramienta | Garantia | Costo | Cuando usarlo |
|-------|-------------|----------|-------|---------------|
| 0 | Texto libre + regex | Ninguna formal | Casi nulo | Prototipos rapidos |
| 1 | JSON Schema | Estructura correcta | Bajo | Cualquier produccion |
| 2 | Pydantic/Zod | Semantica en runtime | Medio | Datos sensibles, decisiones |
| 3 | Discriminated unions | Tipos dependientes (parcial) | Medio | Multi-herramienta, multi-agente |
| 4 | Design by Contract | Pre/post/invariantes | Medio-alto | Acciones irreversibles |
| 5 | TLA+/Alloy/Lean | Garantias matematicas | Alto | Sistemas criticos |

Si tu agente solo genera texto para un chatbot interno, el Nivel 0 puede bastarte durante un prototipo. Pero en cuanto llegas a produccion, necesitas al menos el Nivel 1: estructura correcta y tipos basicos, con soporte nativo en las APIs de los LLMs.

Cuando tu agente maneja datos sensibles o toma decisiones que afectan a usuarios, sube al Nivel 2. Este es el punto optimo para la mayoria de sistemas hoy: validacion semantica en runtime, relaciones entre campos, mensajes de error claros.

Si tienes un sistema multi-agente con decenas de herramientas, el Nivel 3 te permite expresar en el sistema de tipos que los argumentos de cada herramienta son diferentes. El compilador o el runtime atrapan errores que de otra forma llegarian a produccion.

Cuando los errores tienen consecuencias serias --dinero, datos de usuarios, acciones irreversibles--, el Nivel 4 anade pre/postcondiciones e invariantes explicitas a cada operacion. Es el minimo para sistemas financieros.

Y para sistemas criticos en finanzas, salud o infraestructura, el Nivel 5 verifica propiedades sobre todas las ejecuciones posibles del protocolo. El costo es alto, pero la alternativa es descubrir los bugs en produccion con dinero real.

La industria en 2026 se mueve entre los niveles 1 y 2. Los frameworks mas maduros como Instructor y PydanticAI estan en nivel 2. Los sistemas mas avanzados de empresas como Anthropic y Google estan explorando los niveles 3 y 4. El nivel 5 es mayormente academico, pero la tendencia --impulsada por herramientas como Lean y por la capacidad de los LLMs para generar especificaciones formales-- va claramente en esa direccion.

### Checklist: que nivel necesitas

Antes de implementar contratos tipados, responde estas preguntas:

1. **Las acciones del agente son reversibles?** Si no -> Nivel 4 minimo
2. **Hay dinero real involucrado?** Si -> Nivel 3 minimo
3. **Multiples agentes se comunican entre si?** Si -> Nivel 3
4. **El agente maneja datos personales?** Si -> Nivel 2 minimo
5. **Estas en produccion?** Si -> Nivel 1 minimo
6. **Es un prototipo interno?** Si -> Nivel 0 es aceptable temporalmente

---

## Resumen del capitulo

La validacion estructural no es suficiente. Un JSON valido puede contener instrucciones peligrosas, y un schema que valida la forma de los datos no dice nada sobre su significado.

El camino desde texto libre hasta verificacion formal es un espectro con trade-offs claros. La mayoria de los sistemas en produccion hoy deberian estar en Nivel 2 (Pydantic con validadores semanticos) como minimo. Los sistemas multi-agente con herramientas deberian aspirar al Nivel 3 (discriminated unions). Los sistemas criticos necesitan Nivel 4 (Design by Contract) o superior.

Los contratos tipados no son solo una defensa: son una herramienta de diseno. Definir el contrato *antes* de implementar el agente te obliga a pensar en los modos de fallo, las invariantes del negocio y las dependencias entre componentes. Es la misma disciplina que hace que las interfaces bien disenadas produzcan software mas robusto.

En el proximo capitulo abordaremos un tema que conecta directamente con los contratos: la seguridad. Porque de nada sirve un contrato perfecto si un atacante puede inyectar instrucciones maliciosas que el agente ejecuta diligentemente.

---

### Referencias del capitulo

- [Anthropic, 2025] Anthropic. "Tool Use Documentation." 2025.
- [Kleppmann, 2025] Kleppmann, M. "Prediction: AI will make formal verification go mainstream." Blog, diciembre 2025.
- [Lamport, 2002] Lamport, L. *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Addison-Wesley, 2002.
- [Liu, 2024] Liu, J. "Instructor: Structured outputs for LLMs." GitHub, 2024. https://github.com/jxnl/instructor
- [Martin-Lof, 1984] Martin-Lof, P. *Intuitionistic Type Theory*. Bibliopolis, 1984.
- [Meyer, 1997] Meyer, B. *Object-Oriented Software Construction*. 2nd ed. Prentice Hall, 1997.
- [OpenAI, 2024] OpenAI. "Introducing Structured Outputs in the API." Blog, agosto 2024.
- [Pydantic, 2025] Pydantic. "How to Use Pydantic for LLMs: Schema, Validation & Prompts." 2025. https://pydantic.dev/articles/llm-intro
- [Varios, 2025] "Agent Behavioral Contracts: Formal Specification and Runtime Enforcement for Reliable Autonomous AI Agents." arXiv:2602.22302, 2025.
