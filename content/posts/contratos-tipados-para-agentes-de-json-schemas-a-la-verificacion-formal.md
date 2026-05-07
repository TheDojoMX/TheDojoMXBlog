---
title: "Contratos tipados para agentes: de JSON Schemas a la verificación formal"
date: 2026-03-30
author: "Héctor Patricio"
tags: ['agentes', 'tipos', 'json-schema', 'pydantic', 'verificación-formal', 'llm', 'python', 'diseño-de-software', 'contratos', 'arquitectura']
description: "Exploramos cómo los contratos tipados resuelven el problema de comunicación entre agentes de IA: desde JSON Schemas hasta tipos dependientes y verificación formal con TLA+."
featuredImage: ""
draft: true
---

Un agente de IA produce un JSON con el campo `"action": "delete"` y `"confirmation": false`. El JSON es estructuralmente válido, pasa todas las validaciones del schema, y el sistema lo ejecuta sin quejarse. Resultado: datos borrados, sin confirmación, sin vuelta atrás. Nadie validó el **significado** de la salida, solo su **forma**.

Este es el problema central de la comunicación entre agentes: la validación estructural no es suficiente. Necesitamos **contratos tipados** que garanticen no solo que los datos tienen la forma correcta, sino que su contenido es semánticamente válido. Los tipos y schemas son contratos: acuerdos formales sobre la forma y el significado de los datos intercambiados.

En este artículo vamos a recorrer el espectro completo de soluciones, desde el parsing con regex hasta la verificación formal con TLA+, pasando por JSON Schemas, Pydantic y tipos dependientes. No se trata solo de herramientas: se trata de entender qué nivel de garantía necesitas y cuánto estás dispuesto a pagar por ella.

## De texto libre a structured outputs: la evolución

Hagamos un recorrido por cómo hemos llegado hasta aquí. La historia de la comunicación con LLMs es la historia de ganar control sobre lo impredecible.

### La era del regex y la esperanza

En 2023, la forma estándar de obtener datos estructurados de un LLM era algo como esto:

```python
import re

response = llm.complete("Extrae el nombre y edad del siguiente texto: 'Juan tiene 30 años'")
# response = "El nombre es Juan y la edad es 30 años."

# Parsing con regex... y esperanzas
name_match = re.search(r"nombre es (\w+)", response)
age_match = re.search(r"edad es (\d+)", response)

if name_match and age_match:
    name = name_match.group(1)
    age = int(age_match.group(1))
else:
    # ¿Qué hacemos aquí? Rezar.
    raise ValueError("No pude parsear la respuesta del LLM")
```

Esto funcionaba... a veces. El problema fundamental es que un LLM no tiene obligación de formatear su respuesta de ninguna manera particular. Podía responder "Juan, 30", o "Nombre: Juan. Edad: treinta", o incluso inventar una conversación ficticia. Estábamos en territorio de **best effort**: hacíamos nuestro mejor esfuerzo, pero no teníamos garantías.

### JSON como lingua franca

El siguiente paso fue pedirle al modelo que respondiera en JSON, generalmente con instrucciones en el prompt:

```python
prompt = """Extrae el nombre y edad del siguiente texto.
Responde SOLO con un JSON válido con las claves "name" y "age".
No incluyas ningún otro texto.

Texto: 'Juan tiene 30 años'"""

response = llm.complete(prompt)
data = json.loads(response)  # Puede fallar si el modelo añade texto extra
```

Mejor, pero seguimos en territorio de esperanzas. El modelo puede incluir un preámbulo como "Aquí tienes el JSON:" antes del objeto, puede usar comillas simples, puede generar JSON inválido. Peor aún, puede generar un JSON válido pero con claves diferentes a las que esperamos.

### JSON Schemas: el primer contrato real

Con la llegada de los **Structured Outputs** en las APIs de los proveedores de LLMs, finalmente obtuvimos un mecanismo formal. Para 2026, todos los proveedores principales (Anthropic, Google, OpenAI, Mistral) soportan structured outputs. Le proporcionas un JSON Schema al modelo y la API te **garantiza** que la respuesta se ajustará a ese schema:

> **Nota de producción**: forzar structured outputs siempre tiene un costo cognitivo. El modelo "gasta capacidad" en formatear correctamente el JSON en lugar de razonar sobre el contenido. En la práctica, muchos equipos usan un enfoque híbrido: dejan que el modelo razone en texto libre y luego extraen datos estructurados con un paso de parsing o con un segundo llamado más pequeño.

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
                    "age": {"type": "integer", "minimum": 0, "maximum": 150}
                },
                "required": ["name", "age"],
                "additionalProperties": False
            }
        }
    },
    messages=[
        {"role": "user", "content": "Extrae el nombre y edad: 'Juan tiene 30 años'"}
    ]
)
```

La evolución es análoga a la de la web: de respuestas de texto libre a formatos estandarizados con contratos claros. En REST, el contrato es la combinación de URIs, métodos HTTP y tipos de contenido. En agentes, el contrato es el JSON Schema.

Pero aquí viene la pregunta incómoda: **¿es suficiente?**

## JSON Schema como contrato básico: qué garantiza y qué no

Un JSON Schema te da garantías **estructurales**. Puede asegurarte que:

- Un campo existe y es del tipo correcto
- Un número está dentro de un rango
- Un string tiene una longitud mínima o máxima
- Un valor pertenece a un conjunto enumerado
- Un objeto tiene exactamente las propiedades requeridas

Esto es poderoso. Pero hay una categoría entera de problemas que un JSON Schema **no puede resolver**: la **validación semántica**.

### El problema de la validez estructural vs. semántica

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

El siguiente objeto es **estructuralmente válido**:

```json
{
  "action": "delete",
  "target": "/",
  "confirmation": false
}
```

Pasa todas las validaciones del schema. Pero semánticamente, es una instrucción para borrar el directorio raíz del sistema. Y `confirmation` es `false`, pero el agente igual podría ejecutarla porque el campo no es requerido y nada en el schema dice que `delete` necesita `confirmation: true`.

La validación de estructura no sustituye a la validación semántica. Un JSON válido puede contener instrucciones peligrosas, igual que un SQL parametrizado puede contener lógica maliciosa si no validamos los valores.

### Las limitaciones formales de JSON Schema

Desde la perspectiva de la teoría de tipos, JSON Schema es un lenguaje de validación estructural con restricciones de primer orden sobre valores. Aunque desde el draft 7 (2017) soporta `if/then/else` para expresar relaciones proposicionales entre valores de campos, la sintaxis es compleja y hay límites duros: no puede expresar relaciones aritméticas entre campos (como "updated_at > created_at") ni relaciones que dependan de estado externo. No puede expresar:

- **Invariantes temporales**: "el campo `updated_at` debe ser posterior a `created_at`"
- **Restricciones contextuales**: "el agente solo puede ejecutar `delete` si tiene el rol `admin`"
- **Propiedades semánticas**: "el campo `email` debe ser un email real que exista"
- **Relaciones complejas entre campos**: más allá de las condicionales simples que `if/then/else` permite

Para estas restricciones, necesitamos algo más expresivo. Aquí es donde entra Pydantic.

## Pydantic y los validadores en runtime

Si JSON Schema es un contrato en papel, **Pydantic** es un contrato con un abogado que lo ejecuta en tiempo real. Pydantic es la librería de validación de datos más popular en Python, y se ha convertido en el estándar de facto para definir contratos de datos en sistemas con agentes.

> **Importante**: todos los ejemplos en este artículo usan **Pydantic v2** (`BaseModel`, `Field`, `model_validator`, `field_validator`). Si tu proyecto aún usa Pydantic v1, migra antes de implementar contratos para agentes. Mezclar APIs de v1 y v2 es una fuente común de errores en producción que solo aparecen al resolver dependencias en el entorno de despliegue.

### De schemas a modelos ejecutables

La idea fundamental de Pydantic es simple: defines una clase Python con anotaciones de tipo, y Pydantic valida que los datos se ajusten a esas anotaciones al momento de crear la instancia:

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
from typing import Optional

class Action(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"

class AgentCommand(BaseModel):
    action: Action
    target: str = Field(..., min_length=1, max_length=500)
    confirmation: bool = False
    reason: str = Field(..., min_length=10, description="Justificación para la acción")

    @field_validator('target')
    @classmethod
    def validate_target(cls, v: str, info) -> str:
        # Prevenir paths peligrosos
        dangerous_paths = ['/', '/etc', '/usr', '/var', '/home']
        if v in dangerous_paths:
            raise ValueError(f"El path '{v}' está en la lista de paths protegidos")
        return v

    @model_validator(mode='after')
    def validate_delete_has_confirmation(self) -> 'AgentCommand':
        if self.action == Action.DELETE and not self.confirmation:
            raise ValueError(
                "Las acciones de tipo DELETE requieren confirmation=True"
            )
        return self
```

Observa lo que hemos ganado con respecto al JSON Schema puro:

1. **Validación cross-field**: podemos expresar que `delete` requiere `confirmation`
2. **Listas de exclusión**: podemos prohibir ciertos valores específicos
3. **Validación semántica custom**: podemos ejecutar cualquier lógica de Python
4. **Documentación ejecutable**: los mensajes de error explican exactamente qué salió mal

### El patrón de Output Parsers

Los frameworks de agentes como LangChain y LangGraph popularizaron el patrón de **output parsers**: componentes que toman la salida cruda de un LLM y la transforman en un objeto tipado. Con Pydantic, este patrón se vuelve trivial:

```python
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=AgentCommand)

# El parser genera instrucciones de formato para el prompt
format_instructions = parser.get_format_instructions()

# Y luego valida la respuesta del LLM
try:
    command = parser.parse(llm_response)
    # command es un AgentCommand validado y tipado
    execute_command(command)
except ValidationError as e:
    # Sabemos exactamente qué falló
    handle_invalid_command(e.errors())
```

### Instructor: Pydantic nativo con LLMs

La librería **Instructor** de Jason Liu lleva esta idea un paso más allá: integra Pydantic directamente con las APIs de los LLMs, de forma que el modelo genera objetos Pydantic directamente:

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI())

class AnalysisResult(BaseModel):
    sentiment: str = Field(..., pattern=r'^(positive|negative|neutral)$')
    confidence: float = Field(..., ge=0.0, le=1.0)
    key_topics: list[str] = Field(..., min_length=1, max_length=10)
    summary: str = Field(..., min_length=20, max_length=500)

# Instructor maneja los reintentos automáticamente
# si el LLM produce un output que no valida
result = client.chat.completions.create(
    model="gpt-4o",
    response_model=AnalysisResult,
    max_retries=3,
    messages=[
        {"role": "user", "content": "Analiza: 'El producto es excelente pero el envío fue lento'"}
    ]
)

# result es un AnalysisResult completamente validado
print(result.sentiment)     # "neutral" o "positive"
print(result.confidence)    # 0.75
print(result.key_topics)    # ["producto", "envío", "calidad"]
```

Lo interesante de Instructor es que implementa un **bucle de retroalimentación**: si la validación de Pydantic falla, Instructor envía los errores de vuelta al LLM y le pide que corrija su respuesta. Los contratos tipados no solo detectan errores: guían al sistema hacia respuestas correctas.

### TypeScript: Zod como equivalente

En el mundo TypeScript, el equivalente de Pydantic es **Zod**. La idea es la misma: schemas ejecutables que validan en runtime lo que TypeScript verifica en compilación:

```typescript
import { z } from 'zod';

const AgentCommandSchema = z.object({
  action: z.enum(['read', 'write', 'delete']),
  target: z.string().min(1).max(500),
  confirmation: z.boolean().default(false),
  reason: z.string().min(10).max(1000),
}).refine(
  (data) => {
    if (data.action === 'delete' && !data.confirmation) {
      return false;
    }
    return true;
  },
  { message: "Las acciones DELETE requieren confirmación" }
);

// El tipo se infiere automáticamente del schema
type AgentCommand = z.infer<typeof AgentCommandSchema>;

// Validación en runtime
const parseResult = AgentCommandSchema.safeParse(llmResponse);
if (parseResult.success) {
  const command: AgentCommand = parseResult.data;
  // Totalmente tipado y validado
} else {
  console.error("Errores:", parseResult.error.issues);
}
```

Con Zod tienes lo mejor de ambos mundos: tipos estáticos de TypeScript en compilación **y** validación en runtime. Esto es crucial para agentes, porque los datos vienen de un LLM que, por naturaleza, opera fuera de tu sistema de tipos.

## Tipos dependientes y refinement types: más allá de lo básico

Hasta aquí hemos cubierto lo que la industria usa hoy. Pero si queremos entender hacia dónde va el campo, necesitamos adentrarnos en territorio más teórico: los **tipos dependientes** y los **refinement types**.

### El problema: tipos demasiado amplios

Considera la siguiente definición:

```python
class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any]
```

El campo `tool_name` es un `str`. Pero no cualquier string es un nombre de herramienta válido. Y `arguments` es un `dict` genérico, pero los argumentos válidos dependen de **qué herramienta** estás llamando. El tipo `str` es demasiado amplio: permite infinitos valores donde solo unos pocos son válidos.

En lenguajes con **refinement types**, puedes expresar restricciones más finas sobre los tipos. Por ejemplo, en pseudocódigo inspirado en Liquid Haskell:

```haskell
-- Un tipo refinado: un string que está en la lista de herramientas disponibles
type ToolName = {v: String | v `elem` availableTools}

-- Los argumentos dependen del nombre de la herramienta
type ToolCall = {
  toolName: ToolName,
  arguments: ArgumentsFor toolName  -- Tipo dependiente
}
```

Observa la magia en `ArgumentsFor toolName`: el **tipo** de los argumentos depende del **valor** del nombre de la herramienta. Esto es un **tipo dependiente**: un tipo que depende de un valor.

### Tipos dependientes en la teoría

Los tipos dependientes vienen de la teoría de tipos de Martin-Löf y son la base de lenguajes como **Idris**, **Agda** y **Lean**. La idea fundamental es que los tipos pueden ser funciones de valores: por ejemplo, un `Vect n a` en Idris es un vector cuyo *tipo* incluye su longitud `n`, de forma que el compilador rechaza en tiempo de compilación cualquier intento de llamar `head` sobre un vector vacío. Es elegante, pero en la práctica nadie construye agentes de IA con Idris. Lo relevante es la idea: si pudieras expresar en el sistema de tipos cosas como:

- "Este agente solo puede llamar herramientas de la lista X"
- "Los argumentos de `search` deben ser un string no vacío de máximo 100 caracteres"
- "La respuesta de un agente de resumen debe ser más corta que el texto de entrada"
- "Un agente con rol `viewer` solo puede ejecutar acciones de tipo `read`"

### Aproximaciones prácticas en Python y TypeScript

No necesitas Idris para obtener **algunas** de las garantías de los tipos dependientes. En Python, la librería `Annotated` de `typing` junto con Pydantic te acerca:

```python
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field

# Diferentes modelos de argumentos para diferentes herramientas
class SearchArgs(BaseModel):
    query: str = Field(..., min_length=1, max_length=100)
    max_results: int = Field(default=10, ge=1, le=100)

class CalculateArgs(BaseModel):
    expression: str = Field(..., pattern=r'^[\d\s\+\-\*\/\(\)\.]+$')

class SendEmailArgs(BaseModel):
    to: Annotated[str, Field(pattern=r'^[a-zA-Z0-9_.+-]+@company\.com$')]
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

# La unión discriminada vincula tool_name con el tipo de argumentos correcto
ToolCall = Union[SearchCall, CalculateCall, SendEmailCall]
```

En TypeScript, esto es aún más natural con **discriminated unions**:

```typescript
type SearchCall = {
  tool_name: 'search';
  arguments: {
    query: string;
    max_results?: number;
  };
};

type CalculateCall = {
  tool_name: 'calculate';
  arguments: {
    expression: string;
  };
};

type SendEmailCall = {
  tool_name: 'send_email';
  arguments: {
    to: `${string}@company.com`;  // Template literal type
    subject: string;
    body: string;
  };
};

type ToolCall = SearchCall | CalculateCall | SendEmailCall;

// TypeScript verifica que los argumentos coincidan con la herramienta
function executeToolCall(call: ToolCall) {
  switch (call.tool_name) {
    case 'search':
      // TypeScript sabe que call.arguments es SearchCall['arguments']
      return search(call.arguments.query, call.arguments.max_results);
    case 'calculate':
      return calculate(call.arguments.expression);
    case 'send_email':
      return sendEmail(call.arguments.to, call.arguments.subject, call.arguments.body);
  }
}
```

Lo que estamos haciendo es simular tipos dependientes con el sistema de tipos existente. No es tan expresivo como Idris, pero en la práctica cubre la mayoría de los casos que necesitamos en sistemas de agentes.

## Hacia la verificación formal de contratos entre agentes

Ahora entramos en el territorio más ambicioso. Hasta aquí hemos validado **datos individuales**. Pero en un sistema multi-agente, lo que realmente queremos verificar son **protocolos**: secuencias de interacciones que deben cumplir ciertas propiedades.

### Design by Contract: las ideas de Bertrand Meyer

En 1986, Bertrand Meyer introdujo el concepto de **Design by Contract** (Diseño por Contrato) en el lenguaje Eiffel. La idea es que cada componente de software tiene un contrato explícito con tres partes:

- **Precondiciones**: qué debe ser verdad antes de llamar a una función
- **Postcondiciones**: qué será verdad después de que la función retorne
- **Invariantes**: qué debe ser verdad siempre

Aplicado a agentes, esto se traduce directamente:

```python
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class ToolContract:
    """Contrato para una herramienta que un agente puede invocar."""
    name: str
    preconditions: list[Callable[[dict], bool]]
    postconditions: list[Callable[[dict, Any], bool]]
    invariants: list[Callable[[], bool]]

    def validate_call(self, arguments: dict) -> bool:
        """Verifica precondiciones antes de ejecutar."""
        for pre in self.preconditions:
            if not pre(arguments):
                raise ContractViolation(
                    f"Precondición violada para {self.name}: {pre.__doc__}"
                )
        return True

    def validate_result(self, arguments: dict, result: Any) -> bool:
        """Verifica postcondiciones después de ejecutar."""
        for post in self.postconditions:
            if not post(arguments, result):
                raise ContractViolation(
                    f"Postcondición violada para {self.name}: {post.__doc__}"
                )
        return True

# Ejemplo: contrato para una herramienta de base de datos
db_query_contract = ToolContract(
    name="database_query",
    preconditions=[
        lambda args: "query" in args,                          # Debe tener query
        lambda args: "SELECT" in args["query"].upper(),        # Solo SELECT
        lambda args: "DROP" not in args["query"].upper(),      # Nunca DROP
        lambda args: args.get("limit", 100) <= 1000,           # Límite razonable
    ],
    postconditions=[
        lambda args, result: isinstance(result, list),         # Resultado es lista
        lambda args, result: len(result) <= args.get("limit", 100),  # Respeta el límite
    ],
    invariants=[
        lambda: database_connection.is_alive(),                # La BD sigue viva
    ]
)
```

El contrato **es** la interfaz del módulo: una superficie simple que oculta la complejidad de la implementación detrás.

En producción, este patrón se aplica directamente a las herramientas de un agente. Considera una herramienta de transferencia de dinero:

```python
def transfer_money(amount: float, from_account: str, to_account: str):
    # Precondiciones explícitas
    assert amount > 0, "Precondición: el monto debe ser positivo"
    assert from_account != to_account, "Precondición: las cuentas deben ser diferentes"
    balance = get_balance(from_account)
    assert balance >= amount, "Precondición: saldo insuficiente"

    # Ejecución
    old_balance = balance
    execute_transfer(amount, from_account, to_account)

    # Postcondiciones
    assert get_balance(from_account) == old_balance - amount, \
        "Postcondición: el saldo no se actualizó correctamente"
```

Las `assert` aquí no son validaciones de input del usuario: son contratos del módulo. Si una postcondición falla, hay un bug en la implementación, no en los datos.

### Pre/post condiciones para tool calls

En un sistema multi-agente real, cada herramienta debería declarar su contrato. Esto permite que el orquestador verifique antes de ejecutar:

```python
class ContractAwareAgent:
    def __init__(self, tools: dict[str, ToolContract]):
        self.tools = tools
        self.call_history: list[dict] = []

    def execute_tool(self, tool_name: str, arguments: dict) -> Any:
        contract = self.tools.get(tool_name)
        if not contract:
            raise ValueError(f"Herramienta desconocida: {tool_name}")

        # 1. Verificar invariantes
        for inv in contract.invariants:
            if not inv():
                raise ContractViolation("Invariante del sistema violada")

        # 2. Verificar precondiciones
        contract.validate_call(arguments)

        # 3. Ejecutar
        result = self._run_tool(tool_name, arguments)

        # 4. Verificar postcondiciones
        contract.validate_result(arguments, result)

        # 5. Registrar para auditoría
        self.call_history.append({
            "tool": tool_name,
            "arguments": arguments,
            "result_type": type(result).__name__,
            "timestamp": datetime.now().isoformat()
        })

        return result
```

### TLA+ y la verificación de protocolos de agentes

Pero los contratos individuales no son suficientes para verificar que un **protocolo** completo funciona correctamente. Aquí es donde entran herramientas como **TLA+**, el lenguaje de especificación formal creado por Leslie Lamport.

TLA+ permite modelar sistemas concurrentes y verificar que cumplen ciertas propiedades. Podemos usarlo para modelar la interacción entre agentes:

```tla
---- MODULE AgentProtocol ----
EXTENDS Integers, Sequences

VARIABLES
    agentState,      \* Estado de cada agente
    messageQueue,    \* Cola de mensajes entre agentes
    toolCallCount,   \* Contador de llamadas a herramientas
    waitingFor       \* Grafo de espera: waitingFor[a] = b si a espera a b

\* Los agentes pueden estar en estos estados
AgentStates == {"idle", "thinking", "calling_tool", "waiting", "done", "error"}

\* Invariante: ningún agente puede hacer más de 10 llamadas a herramientas
ToolCallLimit == \A agent \in Agents: toolCallCount[agent] <= 10

\* Invariante: si un agente está en estado "error", no puede llamar herramientas
ErrorBlocksTools ==
    \A agent \in Agents:
        agentState[agent] = "error" =>
            ~(\E msg \in messageQueue: msg.from = agent /\ msg.type = "tool_call")

\* Propiedad de liveness: todo agente eventualmente llega a "done" o "error"
EventualTermination ==
    \A agent \in Agents:
        <>(agentState[agent] \in {"done", "error"})

\* Propiedad de seguridad: ningún subconjunto de agentes se espera mutuamente
\* (simplificación: todo agente en "waiting" espera a uno que no está en "waiting")
\* En una spec completa, verificarías la ausencia de ciclos en el grafo de espera.
NoDeadlock ==
    \A agent \in Agents:
        agentState[agent] = "waiting" =>
            \E other \in Agents:
                waitingFor[agent] = other /\ agentState[other] # "waiting"

====
```

Este es un **sketch** de especificación, no una spec completa de TLA+ (faltan las definiciones de `Init`, `Next` y la especificación completa). Pero ilustra la idea: TLA+ puede explorar **todos** los estados posibles del sistema y verificar que las propiedades se cumplen siempre. No es un test que ejecutas con algunos inputs: es una prueba exhaustiva de todos los escenarios posibles.

Nota que `NoDeadlock` modela la ausencia de deadlock verificando que todo agente en espera está esperando a un agente que no está bloqueado. En una especificación completa, verificarías la ausencia de ciclos en el grafo de espera (A espera a B, B espera a C, C espera a A), lo cual requiere una definición transitiva. Para este sketch, la propiedad simplificada es suficiente para ilustrar el concepto.

¿Es práctico usar TLA+ para sistemas de agentes hoy? Siendo honestos, para la mayoría de equipos es excesivo. Pero para sistemas críticos donde la comunicación incorrecta entre agentes puede causar pérdidas financieras o daño real, la verificación formal empieza a justificarse. Y la tendencia va claramente en esa dirección.

## El espectro de garantías

Ahora podemos visualizar el panorama completo. Piensa en las garantías de comunicación entre agentes como un espectro:

Si tu agente solo genera texto para un chatbot interno, el **Nivel 0** (texto libre con regex) puede bastarte durante un prototipo. Pero en cuanto llegas a producción, necesitas al menos el **Nivel 1** (JSON Schema): estructura correcta y tipos básicos, con soporte nativo en las APIs de los LLMs.

Cuando tu agente maneja datos sensibles o toma decisiones que afectan a usuarios, sube al **Nivel 2** (Pydantic, Zod): validación semántica en runtime, relaciones entre campos y mensajes de error claros. Este es el punto óptimo para la mayoría de sistemas hoy.

Si tienes un sistema multi-agente con decenas de herramientas, el **Nivel 3** (discriminated unions, tipos literales) te permite expresar en el sistema de tipos que los argumentos de cada herramienta son diferentes. El compilador o el runtime atrapan errores que de otra forma llegarían a producción.

Cuando los errores tienen consecuencias serias (dinero, datos de usuarios, acciones irreversibles), el **Nivel 4** (Design by Contract) añade pre/postcondiciones e invariantes explícitas a cada operación.

Y para sistemas críticos en finanzas, salud o infraestructura, el **Nivel 5** (TLA+, Alloy, theorem provers) verifica propiedades sobre todas las ejecuciones posibles del protocolo. El costo es alto, pero la alternativa es descubrir los bugs en producción.

La industria hoy se mueve entre los niveles 1 y 2. Los frameworks más maduros como Instructor están en nivel 2. Los sistemas más avanzados de empresas como Anthropic y Google están explorando los niveles 3 y 4. El nivel 5 es mayormente académico por ahora, pero es cuestión de tiempo antes de que las herramientas sean lo suficientemente accesibles para adoptarlo más ampliamente.

## Ejemplo práctico: contratos tipados para un sistema multi-agente

Vamos a juntar todo lo que hemos discutido en un ejemplo concreto. Imagina un sistema de tres agentes:

1. **Agente Investigador**: busca información
2. **Agente Analista**: analiza datos y produce insights
3. **Agente Escritor**: genera reportes

Cada agente necesita comunicarse con los otros a través de contratos tipados. Veamos cómo implementarlo:

```python
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Union, Annotated
from datetime import datetime
from enum import Enum

# === Tipos base compartidos ===

Confidence = Annotated[float, Field(ge=0.0, le=1.0, description="Nivel de confianza entre 0 y 1")]

class Source(BaseModel):
    url: str = Field(..., pattern=r'^https?://.+')
    title: str = Field(..., min_length=1, max_length=300)
    retrieved_at: datetime
    reliability_score: float = Field(..., ge=0.0, le=1.0)

# === Contrato: Investigador → Analista ===

class ResearchResult(BaseModel):
    """Contrato de salida del Agente Investigador."""
    query: str = Field(..., min_length=5, description="La consulta original")
    sources: list[Source] = Field(..., min_length=1, max_length=20)
    raw_findings: list[str] = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)

    @model_validator(mode='after')
    def findings_need_sources(self) -> 'ResearchResult':
        """Cada hallazgo debe estar respaldado por al menos una fuente."""
        if len(self.raw_findings) > len(self.sources) * 3:
            raise ValueError(
                f"Demasiados hallazgos ({len(self.raw_findings)}) "
                f"para el número de fuentes ({len(self.sources)}). "
                f"Máximo 3 hallazgos por fuente."
            )
        return self

# === Contrato: Analista → Escritor ===

class Insight(BaseModel):
    claim: str = Field(..., min_length=10, max_length=500)
    evidence: list[str] = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    category: Literal["trend", "anomaly", "correlation", "prediction"]

class AnalysisResult(BaseModel):
    """Contrato de salida del Agente Analista."""
    research_query: str
    insights: list[Insight] = Field(..., min_length=1, max_length=10)
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    limitations: list[str] = Field(..., min_length=1)
    recommended_actions: list[str] = Field(default_factory=list, max_length=5)

    @model_validator(mode='after')
    def confidence_consistent(self) -> 'AnalysisResult':
        """La confianza general no puede ser mayor que la más alta de los insights."""
        if self.insights:
            max_insight_conf = max(i.confidence for i in self.insights)
            if self.overall_confidence > max_insight_conf + 0.1:
                raise ValueError(
                    f"overall_confidence ({self.overall_confidence}) no puede "
                    f"exceder significativamente el insight más confiable "
                    f"({max_insight_conf})"
                )
        return self

# === Contrato: Escritor → Output final ===

class ReportSection(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=50)
    sources_cited: list[int] = Field(default_factory=list)

class FinalReport(BaseModel):
    """Contrato de salida del Agente Escritor."""
    title: str = Field(..., min_length=10, max_length=200)
    executive_summary: str = Field(..., min_length=100, max_length=1000)
    sections: list[ReportSection] = Field(..., min_length=2, max_length=8)
    sources: list[Source]
    generated_at: datetime = Field(default_factory=datetime.now)
    confidence_disclaimer: str = Field(..., min_length=20)

    @model_validator(mode='after')
    def all_citations_valid(self) -> 'FinalReport':
        """Todas las citas deben referir a fuentes existentes."""
        max_idx = len(self.sources) - 1
        for section in self.sections:
            for cite_idx in section.sources_cited:
                if cite_idx < 0 or cite_idx > max_idx:
                    raise ValueError(
                        f"Cita [{cite_idx}] en '{section.title}' no tiene "
                        f"fuente correspondiente (máximo: {max_idx})"
                    )
        return self

# === Orquestador con contratos ===

class MultiAgentOrchestrator:
    """Orquestador que usa contratos tipados para coordinar agentes."""

    async def run_pipeline(self, query: str) -> FinalReport:
        # Paso 1: Investigación
        raw_research = await self.researcher.run(query)
        research = ResearchResult.model_validate(raw_research)
        # Si la validación falla, obtenemos un error claro antes de continuar

        # Paso 2: Análisis
        raw_analysis = await self.analyst.run(research.model_dump())
        analysis = AnalysisResult.model_validate(raw_analysis)

        # Paso 3: Escritura
        raw_report = await self.writer.run(
            analysis=analysis.model_dump(),
            sources=[s.model_dump() for s in research.sources]
        )
        report = FinalReport.model_validate(raw_report)

        return report
```

Observa cómo cada paso del pipeline tiene un contrato explícito. Si el agente investigador produce datos inválidos, el error se detecta **antes** de pasarlos al analista. Si el analista produce insights con confianza inconsistente, eso se detecta antes de escribir el reporte. Y si el escritor cita fuentes que no existen, el reporte no se genera.

Esto es la esencia del diseño por contratos aplicado a agentes: **fallar rápido y con información clara**, en lugar de propagar errores silenciosamente a través del sistema.

Los contratos tipados son el pegamento que hace que la orquestación sea confiable.

## Conclusión

Sin contratos tipados, la comunicación entre agentes falla de formas que no puedes detectar hasta que ya causaron daño. Un JSON estructuralmente válido pero semánticamente peligroso pasa todas las validaciones del schema y se propaga silenciosamente por todo el sistema.

La evolución es clara: de texto libre a JSON, de JSON a JSON Schema, de JSON Schema a validación runtime con Pydantic y Zod, de ahí a tipos refinados y Design by Contract, y eventualmente a verificación formal. Cada paso añade garantías, pero también añade costo y complejidad. La clave es elegir el nivel correcto para tu caso de uso.

Para la mayoría de los sistemas hoy, la combinación de **Structured Outputs** (nivel 1) + **Pydantic/Zod con validadores custom** (nivel 2) es el punto óptimo. Es relativamente fácil de implementar, las herramientas están maduras, y te da garantías suficientes para la mayoría de los escenarios.

Pero si estás construyendo sistemas donde la comunicación incorrecta entre agentes puede causar daño real, los niveles 3-5 no son opcionales: son necesarios. Y las herramientas para llegar ahí ya existen. Solo falta que la industria las adopte.

En otros artículos de esta serie exploramos la [verificación formal completa para agentes](/2026/04/08/verificacion-formal-de-agentes-por-que-funciona-en-la-demo-no-es-suficiente/) y el [*harness* que integra contratos con observabilidad y monitoreo en producción](/2026/03/21/agent-harness-el-arnes-que-controla-a-tu-agente-de-ia/).

### Referencias y fuentes clave

- **"Object-Oriented Software Construction"** - Bertrand Meyer (1988). El libro que introdujo Design by Contract.
- **"Types and Programming Languages"** - Benjamin C. Pierce (2002). La referencia estándar en teoría de tipos.
- **"Specifying Systems"** - Leslie Lamport (2002). TLA+ y verificación formal de sistemas concurrentes.
- **JSON Schema Specification** - [json-schema.org](https://json-schema.org/). Especificación oficial de JSON Schema.
- **Pydantic Documentation** - [docs.pydantic.dev](https://docs.pydantic.dev/). Documentación oficial de Pydantic v2.
- **Instructor Library** - [github.com/jxnl/instructor](https://github.com/jxnl/instructor). Structured outputs con Pydantic para LLMs.
- **Zod Documentation** - [zod.dev](https://zod.dev/). Validación de schemas en TypeScript.
- **"Practical TLA+"** - Hillel Wayne (2018). Introducción práctica a TLA+ para ingenieros de software.
- **OpenAI Structured Outputs** - [platform.openai.com](https://platform.openai.com/docs/guides/structured-outputs). Documentación de structured outputs.
- **"Dependent Types at Work"** - Ana Bove y Peter Dybjer (2009). Introducción a tipos dependientes con Agda.
- **"Programming in Idris"** - Edwin Brady (2017). Tipos dependientes en la práctica con Idris.
