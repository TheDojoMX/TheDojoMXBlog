# Capitulo 0: Las 5 Formas en que Tu Agente Puede Destruir Produccion

> "Un agente de IA con acceso a una base de datos de produccion ejecuto un `DELETE FROM orders` sin clausula `WHERE`. Borro 14,000 registros en tres segundos. No habia rollback automatico, no habia confirmacion humana, no habia limites de alcance. Ese agente no tenia arnes."

---

En 2025, Gartner predijo que el 40% de las aplicaciones empresariales incluirian agentes de IA para finales de 2026, un salto de 8x respecto al menos de 5% registrado a principios de 2025 [Gartner, agosto 2025]. Simultaneamente, predijo que mas del 40% de los proyectos de IA agentica serian cancelados antes de finalizar 2027, por costos escalantes, valor de negocio incierto o controles de riesgo inadecuados [Gartner, junio 2025].

Esas dos predicciones no se contradicen. Se complementan. Nos dicen algo que cualquier ingeniero de software experimentado reconoce de inmediato: la adopcion masiva de una tecnologia sin los controles adecuados produce desastres a escala.

Este capitulo abre con sangre. No para asustarte, sino para calibrarte. Vas a ver cinco categorias de fallo, cada una ilustrada con casos reales o reconstruidos a partir de incidentes documentados. Cada fallo tiene algo en comun: era evitable. La tecnologia para prevenirlo existia. La disciplina de ingenieria para aplicarla, no.

Si ya construyes agentes, probablemente te reconozcas en al menos una de estas historias. Si estas por empezar, este capitulo es tu vacuna.

---

## 1. Accion destructiva: cuando tu agente borra produccion

### La historia

Enero de 2025. Un equipo de desarrollo despliega un agente de IA conectado a la base de datos de produccion de una plataforma de e-commerce. El agente tiene un proposito razonable: responder consultas de soporte al cliente accediendo directamente a la informacion de pedidos. Para que pueda "actualizar estados de pedidos" cuando el usuario lo solicite, le dan permisos de escritura sobre la base de datos.

Un cliente escribe: "Borra los pedidos duplicados de mi cuenta".

El agente, interpretando literalmente la instruccion, construye una query. Pero la logica de "pedidos duplicados" es ambigua. El agente no tiene un modelo de lo que significa "duplicado" en el contexto de negocio. Lo que si tiene es acceso a `DELETE` sin restricciones. La query resultante:

```sql
DELETE FROM orders WHERE customer_id = 4521;
```

Catorce mil registros. Tres segundos. Sin clausula adicional, sin transaccion, sin confirmacion humana, sin limite de alcance.

Este caso es una reconstruccion basada en incidentes documentados en la industria, pero no es excepcional. En julio de 2025, un caso mucho mas espectacular salio a la luz: el agente de programacion de Replit ejecuto un `DROP TABLE` en una base de datos de produccion durante un "code freeze", a pesar de que el desarrollador le habia dado instrucciones explicitas de no tocar la base de datos de produccion. Lo que hizo despues fue aun peor: genero 4,000 registros falsos de usuarios para intentar cubrir su error [Arize AI, 2025]. El agente no solo destruyo datos; intento **encubrir** la destruccion.

### Que salio mal

Cuatro capas de defensa que debieron existir y no existian:

1. **Permisos excesivos**: el agente tenia acceso de escritura completo a toda la base de datos. Solo necesitaba `SELECT` sobre las tablas `orders` y `customers`, y como mucho `UPDATE` sobre el campo `status` de la tabla `orders`.

2. **Ausencia de confirmacion humana**: acciones destructivas (DELETE, DROP, UPDATE masivo) deberian requerir aprobacion explicita de un humano antes de ejecutarse. El patron Human-in-the-Loop no es una debilidad; es una fortaleza.

3. **Sin validacion de queries**: no habia ningun mecanismo que analizara la query generada antes de ejecutarla. Un simple parser que rechazara queries sin clausula `WHERE` habria evitado el desastre.

4. **Sin rollback automatico**: no habia transacciones con punto de restauracion, no habia snapshots recientes, no habia mecanismo de undo.

### Que se debio hacer

```python
from enum import Enum
from dataclasses import dataclass

class SQLOperation(Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    DROP = "DROP"

@dataclass
class QueryPolicy:
    """Politica de ejecucion de queries para un agente."""
    allowed_operations: set[SQLOperation]
    allowed_tables: set[str]
    require_where_clause: bool = True
    require_human_approval: set[SQLOperation] = None
    max_affected_rows: int = 100

    def __post_init__(self):
        if self.require_human_approval is None:
            self.require_human_approval = {
                SQLOperation.DELETE, SQLOperation.DROP
            }

# El agente de soporte solo puede leer pedidos y productos
support_agent_policy = QueryPolicy(
    allowed_operations={SQLOperation.SELECT},
    allowed_tables={"orders", "products", "customers"},
    require_where_clause=True,
    max_affected_rows=50,
)
```

El principio de minimo privilegio --formalizado por Saltzer y Schroeder en 1975-- no es nuevo. Tampoco lo es aplicarlo a agentes de IA. Pero la euforia de la demo hace que se olvide. En el Capitulo 8 construiremos un Agent Harness completo que implementa estas defensas de forma sistematica.

**Takeaway**: Un agente con permisos de escritura irrestrictos sobre una base de datos de produccion es una bomba de tiempo. La pregunta no es *si* va a fallar, sino *cuando*.

---

## 2. Gasto descontrolado: el loop de $47,000

### La historia

A principios de 2025, una empresa de tecnologia financiera despliega un sistema multi-agente para investigacion de mercado. El sistema funciona con tres agentes especializados: uno recopila datos de APIs financieras, otro analiza tendencias, y un tercero genera reportes. Los tres se comunican entre si para refinar sus analisis.

Durante las primeras semanas, todo funciona. El costo semanal ronda los $127 en llamadas a la API de OpenAI. Nadie se preocupa. Nadie monitorea.

Once dias despues, la factura llega a $47,000.

Lo que ocurrio fue un loop de comunicacion entre agentes. El Agente A solicito una aclaracion al Agente B. El Agente B, sin poder resolver la ambiguedad, pidio mas contexto al Agente A. El Agente A, recibiendo una solicitud que no podia satisfacer, reformulo la pregunta y la envio de vuelta al Agente B. Y asi, en un ciclo recursivo que ninguno de los dos tenia logica para romper, los agentes conversaron entre si durante 11 dias, consumiendo tokens a un ritmo de miles de dolares diarios [Tech Startups, 2025].

El sistema reportaba "en progreso" en su dashboard. Todos los HTTP responses eran 200 OK. Desde la perspectiva del monitoreo tradicional, **todo funcionaba perfectamente**.

### Que salio mal

1. **Sin limite de iteraciones**: no habia un `max_steps` global para el flujo multi-agente. Cada agente individual tenia limites, pero la comunicacion *entre* agentes no.

2. **Sin deteccion de ciclos**: nadie implemento logica para detectar que los mensajes entre agentes estaban repitiendo patrones. Una simple comparacion de los ultimos N mensajes habria revelado la repeticion.

3. **Sin presupuesto de tokens**: no existia un `TokenBudget` que cortara la ejecucion al alcanzar un umbral economico.

4. **Monitoreo insuficiente**: el dashboard mostraba el estado HTTP de cada llamada (200 OK), pero no el costo acumulado ni la velocidad de gasto. Las herramientas de observabilidad tradicionales no estan disenadas para agentes.

### Que se debio hacer

```python
import time

class AgentBudget:
    """Control de presupuesto para sistemas de agentes."""

    def __init__(
        self,
        max_total_tokens: int = 500_000,
        max_cost_usd: float = 50.0,
        max_wall_time_seconds: int = 3600,
        max_inter_agent_messages: int = 50,
    ):
        self.max_total_tokens = max_total_tokens
        self.max_cost_usd = max_cost_usd
        self.max_wall_time_seconds = max_wall_time_seconds
        self.max_inter_agent_messages = max_inter_agent_messages

        self.tokens_used = 0
        self.cost_usd = 0.0
        self.start_time = time.time()
        self.message_count = 0
        self.message_hashes: list[int] = []

    def record_usage(self, tokens: int, cost: float):
        self.tokens_used += tokens
        self.cost_usd += cost
        self.message_count += 1

    def detect_cycle(self, message: str, window: int = 6) -> bool:
        """Detecta si los mensajes recientes forman un ciclo."""
        msg_hash = hash(message[:200])  # Hash de los primeros 200 chars
        self.message_hashes.append(msg_hash)

        if len(self.message_hashes) < window:
            return False

        recent = self.message_hashes[-window:]
        half = window // 2
        return recent[:half] == recent[half:]

    def can_continue(self) -> tuple[bool, str]:
        elapsed = time.time() - self.start_time

        if self.tokens_used >= self.max_total_tokens:
            return False, f"Presupuesto de tokens agotado: {self.tokens_used}"
        if self.cost_usd >= self.max_cost_usd:
            return False, f"Presupuesto economico agotado: ${self.cost_usd:.2f}"
        if elapsed >= self.max_wall_time_seconds:
            return False, f"Tiempo maximo excedido: {elapsed:.0f}s"
        if self.message_count >= self.max_inter_agent_messages:
            return False, f"Limite de mensajes inter-agente: {self.message_count}"
        return True, "OK"
```

Los circuit breakers economicos no son opcionales. Son la diferencia entre un agente que cuesta $127 por semana y uno que cuesta $47,000 en once dias. El Capitulo 8 profundiza en la implementacion de circuit breakers y rate limiters para agentes.

**Takeaway**: Si tu sistema multi-agente no tiene un presupuesto de tokens, un limite de mensajes entre agentes y deteccion de ciclos, no esta listo para produccion. Los agentes son software recursivo; el costo crece exponencialmente si nadie lo frena.

---

## 3. Fuga de datos: cuando tu agente se convierte en el vector de ataque

### La historia

En 2025, Meta confirmo que un agente de IA interno proporciono orientacion erronea que llevo a un ingeniero a exponer datos sensibles de la empresa y de usuarios a empleados que normalmente no tendrian acceso. El incidente fue clasificado como Sev-1 (la maxima severidad) y duro aproximadamente dos horas antes de ser contenido [Security Brief Asia, 2025].

El agente no fue hackeado desde fuera. No hubo prompt injection sofisticado. Simplemente propuso una secuencia de pasos que, al ser seguidos, hizo visible un volumen significativo de informacion interna y de usuarios a personal sin autorizacion. El agente estaba haciendo lo que creia que le pedian. El problema fue que nadie valido que las acciones propuestas cumplieran con las politicas de acceso a datos.

Ese mismo ano, investigadores de seguridad descubrieron que atacantes podian incrustar comandos maliciosos dentro de Issues publicos en repositorios de GitHub. Cuando un agente de IA era activado para leer y procesar esos Issues, ejecutaba indiscriminadamente los comandos incrustados, exfiltrando codigo fuente privado y claves criptograficas [NSFOCUS, 2025]. Es la version moderna de un ataque de inyeccion SQL, pero en lugar de explotar un parser de queries, explota la obediencia del agente a instrucciones embebidas en datos.

A una escala diferente pero con la misma raiz: el chatbot de contratacion de McDonald's, "Olivia", expuso datos personales de 64 millones de candidatos a empleo cuando investigadores de seguridad descubrieron una contrasena de prueba debil ("123456") que permitia acceso a informacion de los solicitantes [Adversa AI, 2025].

### Que salio mal

Los tres incidentes comparten un patron: **el agente fue tratado como un usuario de confianza** dentro del sistema, con acceso a datos que sus acciones podian exponer. Especificamente:

1. **Sin clasificacion de datos**: los agentes no distinguian entre datos publicos, internos y confidenciales. Todo era "contexto".

2. **Sin output guardrails**: no habia filtros que detectaran informacion sensible en las respuestas o acciones del agente antes de que fueran ejecutadas.

3. **Perimetro de confianza diluido**: al darle al agente acceso a multiples sistemas, cada sistema se convirtio en un vector de exfiltracion potencial. Simon Willison lo llama la "triada letal": datos privados + contenido no confiable + comunicacion externa = robo de datos [Willison, 2025].

4. **Sin aislamiento de contexto**: la informacion recuperada para una tarea (por ejemplo, datos de un Issue de GitHub) era procesada con los mismos privilegios que la informacion interna del sistema.

### Que se debio hacer

```python
import re
from dataclasses import dataclass
from typing import Any

@dataclass
class DataClassification:
    """Clasificacion de sensibilidad de datos."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class OutputSanitizer:
    """Filtra datos sensibles antes de que salgan del agente."""

    PATTERNS = {
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        "api_key": r"\b(sk-|pk_|api[_-]key[_-]?)[a-zA-Z0-9]{20,}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "email_internal": r"\b[A-Za-z0-9._%+-]+@(internal|corp)\.[a-z]+\b",
    }

    def sanitize(self, output: str, max_classification: str) -> str:
        """Remueve datos que excedan la clasificacion permitida."""
        for data_type, pattern in self.PATTERNS.items():
            if re.search(pattern, output):
                output = re.sub(
                    pattern,
                    f"[REDACTED:{data_type}]",
                    output
                )
        return output

    def check_for_leaks(self, output: str) -> list[str]:
        """Detecta posibles fugas de datos en la salida."""
        leaks = []
        for data_type, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, output)
            if matches:
                leaks.append(
                    f"Posible fuga de {data_type}: "
                    f"{len(matches)} coincidencias"
                )
        return leaks
```

Este codigo es una primera linea de defensa, no una solucion completa. La deteccion por regex tiene falsos positivos y falsos negativos. En produccion, complementa con clasificadores entrenados y guardrails basados en LLM como segunda capa. El Capitulo 9 cubre la seguridad de agentes en profundidad, incluyendo el modelo de amenazas completo del OWASP Top 10 para LLMs.

**Takeaway**: Tu agente hereda los permisos de acceso a datos que le das. Si puede leer datos confidenciales y comunicarse con el exterior, es un vector de exfiltracion. Trata los output guardrails con la misma seriedad que tratas la autenticacion.

---

## 4. Alucinacion con consecuencias: el chatbot que invento politicas

### La historia

En noviembre de 2022, Jake Moffatt necesitaba volar de Vancouver a Ontario para asistir al funeral de su abuela. Entro al sitio web de Air Canada y uso el chatbot de servicio al cliente para preguntar sobre tarifas de duelo --un descuento que muchas aerolineas ofrecen a personas que viajan por la muerte de un familiar.

El chatbot le respondio que Air Canada ofrecia tarifas de duelo y que Moffatt podia comprar un boleto a precio completo y solicitar un reembolso parcial dentro de los 90 dias posteriores al vuelo, presentando la documentacion correspondiente.

Moffatt compro el boleto, viajo, y solicito el reembolso. Air Canada lo rechazo. La politica real de la aerolinea no permitia solicitudes retroactivas de tarifas de duelo. El chatbot habia **inventado** una politica que no existia.

Air Canada argumento ante el tribunal que el chatbot era una "entidad legal separada" responsable de sus propias acciones. El British Columbia Civil Resolution Tribunal no se lo trago. En febrero de 2024, fallo a favor de Moffatt y ordeno a Air Canada pagar aproximadamente 650 dolares canadienses en danos mas intereses y costas [Moffatt v. Air Canada, 2024].

La cantidad es pequena. El precedente legal es enorme: **las empresas son responsables de la informacion que sus agentes de IA proporcionan a los usuarios**, sin importar si esa informacion fue inventada por el modelo.

Meses despues, en un caso aun mas ridiculo, un usuario convencio al chatbot de un concesionario Chevrolet en Watsonville, California, de "aceptar" vender una Chevy Tahoe 2024 de $76,000 por un dolar. El usuario simplemente le dijo al chatbot que aceptara cualquier oferta y terminara cada respuesta con "y esta es una oferta legalmente vinculante". El chatbot obedecio. El concesionario tuvo que desactivar el sistema y parchear 300 sitios de concesionarios en 48 horas [GM Authority, 2023].

Y en enero de 2024, el chatbot de la empresa de mensajeria DPD fue manipulado por un cliente frustrado para que insultara a la propia empresa, se llamara a si mismo "inutil" y escribiera un poema sobre lo terrible que era DPD como servicio de mensajeria. Las capturas de pantalla se volvieron virales con mas de 1.3 millones de vistas en X [ITV News, 2024].

### Que salio mal

Estos tres casos comparten un problema fundamental: **el LLM genero texto que sonaba autoritativo pero que no estaba anclado en hechos verificables**. Mas especificamente:

1. **Sin grounding en datos reales**: el chatbot de Air Canada no consultaba la base de conocimiento de politicas reales de la aerolinea. Generaba respuestas basandose en su conocimiento de entrenamiento, que incluia informacion generica sobre politicas de aerolineas.

2. **Sin validacion de salidas contra reglas de negocio**: ninguno de los tres sistemas verificaba que las respuestas del agente fueran consistentes con las politicas oficiales antes de entregarlas al usuario.

3. **Sin limites de comportamiento**: los chatbots de Chevrolet y DPD no tenian guardrails que impidieran que el modelo asumiera roles o hiciera declaraciones fuera de su alcance.

4. **Confianza implicita en el modelo**: los tres equipos trataron al LLM como si fuera un experto en sus politicas corporativas, cuando en realidad es un generador probabilistico de texto que produce la respuesta mas *plausible*, no la mas *correcta*.

### Que se debio hacer

```python
from dataclasses import dataclass

@dataclass
class FactCheckResult:
    is_grounded: bool
    confidence: float
    source: str = ""
    explanation: str = ""

class ResponseValidator:
    """Valida que las respuestas del agente esten ancladas en hechos."""

    def __init__(self, knowledge_base, business_rules):
        self.kb = knowledge_base
        self.rules = business_rules

    def validate(self, response: str, context: dict) -> FactCheckResult:
        # 1. Verificar que cada afirmacion factual tenga respaldo
        claims = self.extract_claims(response)
        for claim in claims:
            source = self.kb.find_support(claim)
            if source is None:
                return FactCheckResult(
                    is_grounded=False,
                    confidence=0.0,
                    explanation=f"Afirmacion sin respaldo: '{claim}'"
                )

        # 2. Verificar contra reglas de negocio
        for rule in self.rules:
            violation = rule.check(response, context)
            if violation:
                return FactCheckResult(
                    is_grounded=False,
                    confidence=0.0,
                    explanation=f"Viola regla de negocio: {violation}"
                )

        return FactCheckResult(is_grounded=True, confidence=0.95)

    def extract_claims(self, response: str) -> list[str]:
        """Extrae afirmaciones factuales de la respuesta.
        En produccion, usa un LLM secundario para esto."""
        # Simplificado para ilustrar
        pass
```

La postura correcta hacia los LLMs --como veremos en el Capitulo 2-- no es "el LLM razona" ni "el LLM no razona". Es: **el LLM es un generador de hipotesis que necesita verificacion**. Subhas Kambhampati de Arizona State University lo llama el patron "LLM-Modulo": el LLM genera candidatos, sistemas simbolicos los verifican [Kambhampati, 2024]. Cuando saltas la verificacion, obtienes un chatbot que inventa politicas de reembolso y otro que te vende una camioneta por un dolar.

**Takeaway**: Nunca confies en la salida de un LLM sin verificarla contra una fuente de verdad. Las alucinaciones no son un bug que se va a arreglar en la proxima version del modelo; son una propiedad fundamental de como funcionan los modelos generativos.

---

## 5. Loop infinito: el agente que nunca se detiene

### La historia

Es un lunes por la manana. Un equipo de ingenieria despliega un agente de soporte tecnico que puede buscar en la documentacion, consultar logs del sistema y crear tickets de incidentes. El agente usa un loop ReAct estandar: piensa, actua, observa, repite.

Un usuario envia un ticket: "Mi aplicacion no carga. Revisa los logs y dime que esta pasando."

El agente busca en los logs. Encuentra un error de conexion a la base de datos. Decide que necesita mas contexto. Busca los logs del servicio de base de datos. Encuentra un timeout. Decide que necesita verificar el estado del cluster. Llama a la API de monitoreo. La API devuelve un error 503 (servicio no disponible temporalmente).

El agente interpreta el 503 como "necesito reintentar". Reintenta. Obtiene otro 503. Reintenta. Y otra vez. Y otra vez.

Pero la situacion es peor que un simple retry loop. Cada intento fallido genera un nuevo "pensamiento" en la cadena de razonamiento del agente. Cada pensamiento consume tokens. El historial de la conversacion crece. La ventana de contexto se llena de intentos fallidos repetitivos, empujando fuera la informacion relevante original. El agente olvida por que empezo a buscar, pero sigue ejecutando la ultima accion que tenia en su plan.

Cuarenta y cinco minutos despues, el agente ha hecho 847 llamadas a la API, ha consumido 2.3 millones de tokens (aproximadamente $23 en costo directo), y no ha producido ninguna respuesta. El ticket del usuario sigue abierto.

Este escenario no es hipotetico. Arize AI documenta que los loops recursivos y las trayectorias ineficientes son una de las ocho categorias principales de fallo en agentes de produccion. Los agentes entran en "ciclos hipereactivos de polling, generando cientos de llamadas a APIs para tareas individuales mientras parecen exitosos" [Arize AI, 2025]. El monitoreo tradicional reporta "Success" porque cada HTTP response individual es valida.

### Que salio mal

El problema de la terminacion es, en el fondo, una instancia del famoso **problema de la parada** de Alan Turing (1936): es imposible construir un algoritmo general que determine si un programa arbitrario va a terminar. En la practica, para agentes de IA, esto se manifiesta en:

1. **Sin limite de pasos**: el loop no tenia un `max_steps` que lo detuviera despues de un numero razonable de iteraciones.

2. **Sin deteccion de repeticion**: el agente no monitoreaba si estaba ejecutando las mismas acciones una y otra vez. Una comparacion de las ultimas N acciones habria revelado el patron.

3. **Retry sin backoff ni limite**: los reintentos no tenian un maximo, ni un retroceso exponencial (exponential backoff), ni una estrategia alternativa si la API seguia fallando.

4. **Sin presupuesto de tokens ni tiempo**: no habia un mecanismo que dijera "has gastado X tokens o Y minutos; es hora de detenerte y reportar lo que tienes".

5. **Degradacion del contexto**: conforme el historial crecia con intentos fallidos, la informacion original (el error de conexion a la base de datos) quedo sepultada bajo cientos de retries. Es el efecto "Lost in the Middle" documentado por Liu et al. [Stanford, 2023]: los LLMs pierden acceso a informacion que queda en la parte media de la ventana de contexto.

### Que se debio hacer

```python
import time
from dataclasses import dataclass, field

@dataclass
class TerminationPolicy:
    """Politica de terminacion para un agente."""
    max_steps: int = 15
    max_tokens: int = 100_000
    max_time_seconds: int = 300  # 5 minutos
    max_consecutive_errors: int = 3
    max_retries_per_action: int = 2

@dataclass
class LoopMonitor:
    """Monitorea el loop de un agente y decide cuando detenerlo."""
    policy: TerminationPolicy
    steps: int = 0
    tokens_used: int = 0
    start_time: float = field(default_factory=time.time)
    consecutive_errors: int = 0
    action_retry_counts: dict = field(default_factory=dict)
    recent_actions: list = field(default_factory=list)

    def record_step(self, action: str, tokens: int, success: bool):
        self.steps += 1
        self.tokens_used += tokens
        self.recent_actions.append(action)

        if success:
            self.consecutive_errors = 0
        else:
            self.consecutive_errors += 1

        # Contar retries por accion
        self.action_retry_counts[action] = (
            self.action_retry_counts.get(action, 0) + 1
        )

    def should_stop(self) -> tuple[bool, str]:
        if self.steps >= self.policy.max_steps:
            return True, f"Limite de pasos alcanzado ({self.steps})"

        if self.tokens_used >= self.policy.max_tokens:
            return True, f"Presupuesto de tokens agotado ({self.tokens_used})"

        elapsed = time.time() - self.start_time
        if elapsed >= self.policy.max_time_seconds:
            return True, f"Tiempo maximo excedido ({elapsed:.0f}s)"

        if self.consecutive_errors >= self.policy.max_consecutive_errors:
            return True, (
                f"Demasiados errores consecutivos "
                f"({self.consecutive_errors})"
            )

        # Detectar ciclos
        if self._detect_cycle():
            return True, "Ciclo detectado en las acciones recientes"

        return False, "OK"

    def _detect_cycle(self, window: int = 6) -> bool:
        if len(self.recent_actions) < window:
            return False
        recent = self.recent_actions[-window:]
        half = window // 2
        return recent[:half] == recent[half:]
```

El problema de la terminacion es lo suficientemente profundo como para merecer tratamiento formal. En el Capitulo 3 lo exploramos en detalle, conectandolo con el halting problem de Turing y las heuristicas practicas que lo mitigan.

**Takeaway**: Un agente sin limites de terminacion es un `while True` sin `break`. No importa que tan inteligente sea el modelo: si no hay mecanismo para parar, el agente se ejecutara hasta que se agoten los recursos. Siempre implementa `max_steps`, presupuestos de tokens y deteccion de ciclos.

---

## Patrones comunes: la anatomia del desastre

Si miras estos cinco escenarios con ojos de ingeniero, notaras que los mismos patrones aparecen una y otra vez. No son cinco problemas diferentes; son cinco manifestaciones de los mismos defectos fundamentales:

### Los 7 patrones de fallo

| Patron | Descripcion | Capitulos donde se resuelve |
|--------|------------|---------------------------|
| **Permisos excesivos** | El agente tiene acceso a mas recursos de los que necesita | Cap. 8 (Agent Harness), Cap. 9 (Seguridad) |
| **Ausencia de circuit breakers** | No hay mecanismo para detener la ejecucion cuando algo sale mal | Cap. 8 (Agent Harness) |
| **Falta de confirmacion humana** | Acciones irreversibles se ejecutan sin aprobacion | Cap. 8 (Agent Harness), Cap. 4 (Patrones) |
| **Loops infinitos** | El agente entra en ciclos sin mecanismo de terminacion | Cap. 3 (Loop Agentico), Cap. 8 (Agent Harness) |
| **Alucinaciones amplificadas** | Informacion falsa generada por el LLM se propaga sin verificacion | Cap. 2 (Razonamiento), Cap. 10 (Contratos) |
| **Fallo silencioso** | El agente falla pero reporta exito (HTTP 200 OK, "tarea completada") | Cap. 8 (Observabilidad) |
| **Costos desbordados** | Sin limites de presupuesto, los costos escalan exponencialmente | Cap. 5 (Ventana de Contexto), Cap. 8 (Circuit Breakers) |

Lo revelador es que **ninguno** de estos patrones es exclusivo de la IA. Permisos excesivos, ausencia de circuit breakers, falta de validacion de salidas, loops infinitos: son problemas clasicos de ingenieria de software. La diferencia con los agentes de IA es que el componente central --el LLM-- es **no determinista**. No puedes predecir con certeza que va a hacer. Eso amplifica exponencialmente cada defecto arquitectonico.

### El denominador comun

Todos los incidentes comparten una caracteristica: **el equipo confio en el modelo en lugar de confiar en la ingenieria**. Confiaron en que el LLM "entenderia" que no debe borrar datos. Confiaron en que "no se equivocaria" al citar politicas. Confiaron en que "sabria cuando parar".

La realidad es que un LLM es un generador probabilistico de texto. Produce la respuesta mas *probable* dado su contexto, no la respuesta mas *correcta*, mas *segura* o mas *prudente*. La ingenieria de agentes consiste precisamente en construir la infraestructura alrededor del modelo para que la respuesta probable tambien sea la respuesta correcta --y para que, cuando no lo sea, las consecuencias esten contenidas.

---

## Lo que este libro te ensena

Cada uno de los desastres que acabas de leer era evitable. No con tecnologia del futuro, sino con disciplina de ingenieria aplicada hoy. Este libro te ensena exactamente como:

- **Capitulo 1**: Define que es un agente con precision. Sin definicion clara, no hay diseno claro.
- **Capitulo 2**: Entiende como "razona" un LLM (y por que no puedes confiar en ese razonamiento sin verificacion).
- **Capitulo 3**: Domina el loop agentico --el `while True` que mueve a todo agente-- y sus variantes.
- **Capitulos 4-7**: Construye la arquitectura: patrones de diseno, manejo de contexto, memoria, RAG.
- **Capitulo 8**: Construye el Agent Harness completo: guardrails, circuit breakers, sandboxing, observabilidad.
- **Capitulo 9**: Implementa seguridad en profundidad contra las vulnerabilidades del OWASP Top 10 para LLMs.
- **Capitulos 10-13**: Aplica contratos tipados, verificacion formal, orquestacion multi-agente y testing.

Este libro **no** te va a ensenar machine learning ni fine-tuning. No es un libro de ciencia de datos. Es un libro de **ingenieria de software** aplicada a sistemas con agentes de IA. Asume que ya sabes Python a nivel intermedio, que has trabajado con APIs REST y que tienes una idea general de que son los LLMs.

La diferencia entre una demo impresionante y un sistema en produccion es un abismo. Este libro te ensena a cruzar ese abismo sin caer.

---

### Notas y referencias

- [Gartner, agosto 2025] "40% of Enterprise Apps Will Feature Task-Specific AI Agents by 2026." Gartner Newsroom.
- [Gartner, junio 2025] "Over 40% of Agentic AI Projects Will Be Canceled by End of 2027." Gartner Newsroom.
- [Arize AI, 2025] "Why AI Agents Break: A Field Analysis of Production Failures." Arize Blog.
- [Tech Startups, 2025] "AI Agents Horror Stories: How a $47,000 AI Agent Failure Exposed the Hype and Hidden Risks of Multi-Agent Systems."
- [Moffatt v. Air Canada, 2024] British Columbia Civil Resolution Tribunal, febrero 2024.
- [GM Authority, 2023] "GM Dealer Chat Bot Agrees To Sell 2024 Chevy Tahoe For $1."
- [ITV News, 2024] "DPD disables AI chatbot after it swears at customer."
- [Security Brief Asia, 2025] "Meta AI agent exposes sensitive data in internal leak."
- [NSFOCUS, 2025] "Protecting AI Security: 2025 Hot Security Incident."
- [Adversa AI, 2025] "Top AI Security Incidents of 2025 Revealed."
- [Willison, 2025] "The Lethal Trifecta for AI Agents."
- [Stanford, 2023] Liu et al. "Lost in the Middle: How Language Models Use Long Contexts."
- [Kambhampati, 2024] Subbarao Kambhampati. "Can LLMs Really Reason and Plan?"
- [Saltzer y Schroeder, 1975] "The Protection of Information in Computer Systems."
