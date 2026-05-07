---
title: "Verificación formal de agentes: por qué 'funciona en la demo' no es suficiente"
date: 2026-04-08
author: "Héctor Patricio"
tags: ['agentes', 'verificación-formal', 'llm', 'inteligencia-artificial', 'seguridad', 'formal-methods', 'testing', 'producción', 'arquitectura']
description: "Exploramos por qué los agentes de IA necesitan verificación formal para pasar de demos impresionantes a sistemas confiables en producción. Desde lógica de Hoare hasta herramientas como TLA+ y AgentSpec."
featuredImage: ""
draft: true
---

Imagina que construyes un agente de IA que compra productos en línea por ti.
En la demo funciona perfecto: busca, compara precios, confirma contigo y compra.
Lo presentas ante tu equipo, todos aplauden. Luego lo pones en producción y a las
tres semanas descubres que gastó $4,700 dólares en un pedido duplicado porque el
API del proveedor respondió con un timeout y el agente interpretó eso como
"la compra no se realizó, hay que reintentar". Nadie se dio cuenta hasta que
llegó el estado de cuenta.

Este no es un escenario hipotético rebuscado. Es el tipo de fallo que ocurre
cuando confiamos en que "funciona en la demo" es equivalente a "funciona en
producción". Y con los agentes de IA, la distancia entre esas dos afirmaciones
es un abismo.

Un matiz importante: antes de hablar de verificación formal, hay que reconocer
que la verificación formal es la *última* capa de protección, no la primera.
Si tu agente tiene acceso directo a una API de compras sin límites de gasto,
sin confirmación humana y sin circuit breakers, tu primer problema no es de
verificación formal sino de infraestructura básica. Asegúrate de tener
guardrails operativos, circuit breakers y límites de gasto antes de
considerar verificación formal. La verificación formal te protege de los
fallos que pasan a través de esas capas.

En artículos anteriores hemos explorado los
[patrones de diseño para sistemas con IA](/posts/patrones-de-diseno-para-sistemas-con-ia/)
y las lecciones de llevar
[agentes de la teoría a producción](/posts/de-agentes-teoricos-a-agentes-en-produccion/).
Ahora toca hablar de algo que la industria ha ignorado durante demasiado tiempo:
**cómo demostrar formalmente que un agente se va a comportar correctamente**, no
solo probar que lo hizo en los 50 casos de prueba que se nos ocurrieron.

## ¿Qué es la verificación formal?

Antes de hablar de agentes, necesitamos entender qué significa verificar algo
*formalmente*. Y para eso, hay que regresar a los fundamentos de la ciencia
de la computación.

### La lógica de Hoare: contratos para programas

En 1969, Tony Hoare publicó un artículo seminal que cambió la forma en que
pensamos sobre la corrección de programas. Su idea central es elegante:
un programa se puede describir con un **triple** de la forma:

```
{P} C {Q}
```

Donde **P** es la **precondición** (lo que debe ser cierto antes de ejecutar
el programa), **C** es el **comando** o programa, y **Q** es la **postcondición**
(lo que será cierto después de ejecutarlo). Si puedes demostrar que cada vez que
P es verdadera antes de ejecutar C, Q será verdadera después, entonces tienes
una **prueba de corrección parcial**.

Pensemos en un ejemplo cotidiano. Si tienes una función que divide dos números:

```python
def dividir(a: float, b: float) -> float:
    """
    Precondición: b != 0
    Postcondición: abs(resultado * b - a) < epsilon
    (En aritmética exacta sería resultado * b == a, pero con
    punto flotante IEEE 754, el redondeo impide la igualdad
    estricta. Por ejemplo, 1.0 / 3.0 * 3.0 != 1.0 en Python.)
    """
    return a / b
```

La precondición dice: "solo me llames cuando b no sea cero". La postcondición
dice: "si cumpliste tu parte del contrato, yo te garantizo que el resultado
multiplicado por b te da a, dentro de la tolerancia de la aritmética de punto
flotante". Esto es un **contrato**, y es la base de la verificación formal.

¿Por qué importa esto? Porque la diferencia entre *testing* y *proving*
es fundamental:

- **Testing**: "Probé 10,000 casos y ninguno falló" -- pero no sabes qué
  pasa con el caso 10,001.
- **Proving**: "Demostré matemáticamente que para TODOS los casos posibles,
  el programa se comporta correctamente".

Es la diferencia entre verificar que tu puente aguanta 10 camiones específicos
y demostrar que aguanta cualquier carga hasta 50 toneladas. En el primer caso
estás siendo empírico; en el segundo, estás haciendo ingeniería.

### Invariantes: lo que nunca debe cambiar

Además de precondiciones y postcondiciones, la verificación formal trabaja
con **invariantes**: propiedades que deben mantenerse verdaderas a lo largo
de toda la ejecución de un programa. Piensa en un invariante como una ley
física de tu sistema.

Por ejemplo, en un sistema bancario, un invariante podría ser: "la suma de
todos los saldos siempre es igual al total de depósitos menos el total de
retiros". No importa cuántas transacciones proceses, esta propiedad debe
mantenerse. Si en algún punto se viola, algo está fundamentalmente roto.

Los invariantes son especialmente poderosos para agentes porque nos permiten
definir **límites absolutos** sobre su comportamiento: el agente *nunca*
gastará más de X, el agente *siempre* pedirá confirmación antes de acciones
irreversibles, el saldo *nunca* será negativo.

## Por qué los agentes necesitan verificación formal

Ahora que entendemos los fundamentos, la pregunta es: ¿por qué no basta
con hacer testing exhaustivo para agentes de IA? Hay tres razones
fundamentales.

### El no determinismo del LLM

Los programas tradicionales son deterministas: la misma entrada produce la
misma salida. Si tu función `suma(2, 3)` devuelve 5, puedes estar seguro
de que siempre devolverá 5. Pero un LLM es fundamentalmente no determinista.
La misma pregunta puede producir respuestas diferentes cada vez, incluso
con temperatura 0. Aunque con temperatura 0 y greedy decoding la salida *es*
determinista dado el mismo estado del modelo y la misma entrada, en la
práctica la variabilidad aparece por actualizaciones silenciosas del modelo
por parte del proveedor, efectos de batching en GPU y diferencias numéricas
entre hardware.

Esto hace que el testing tradicional sea insuficiente. No puedes probar todas
las posibles respuestas del LLM porque el espacio de posibilidades es
prácticamente infinito. Es como tratar de probar un programa cuya entrada
es un número real: no importa cuántos pruebes, siempre hay infinitos más.

Estos modelos operan mediante reconocimiento de patrones sofisticado, no
mediante reglas deterministas. Esto implica que su comportamiento tiene una
variabilidad inherente que ningún conjunto de pruebas finito puede capturar
completamente.

### Amplificación de errores en cadenas multi-paso

Los agentes modernos no hacen una sola llamada al LLM. Típicamente ejecutan
**cadenas de múltiples pasos**: razonan, planifican, ejecutan herramientas,
observan resultados, ajustan su plan, y repiten. Cada paso introduce una
probabilidad de error.

Si cada paso tiene una probabilidad de éxito del 95% (lo cual es generoso)
y asumimos independencia entre pasos, una cadena de 10 pasos tiene una
probabilidad de éxito de:

```python
probabilidad_exito = 0.95 ** 10  # = 0.5987
```

Menos del 60%. Y en la práctica, los agentes complejos pueden tener 20, 30
o más pasos. Con 20 pasos al 95% de confiabilidad por paso, tu probabilidad
de éxito cae a 35%.

**Una nota importante**: este cálculo asume que los errores entre pasos son
independientes, lo cual es una simplificación significativa. En la práctica,
los errores en agentes LLM están casi siempre correlacionados: si el agente
comete un error de interpretación en el paso 3, los pasos 4 al 10
probablemente serán todos incorrectos, no porque fallen independientemente
sino *porque* el paso 3 falló. Esto significa que el modelo de errores
independientes es generalmente *optimista*, no pesimista como podría
parecer a primera vista. Un modelo más realista sería uno de Markov de dos
estados ("en buen camino" y "desviado"), con probabilidades de transición
entre ellos, pero eso excede el alcance de este artículo.

Guo et al. (Google Research, 2025) cuantificaron este fenómeno en benchmarks
académicos: en sistemas multi-agente independientes (agentes trabajando en
paralelo sin coordinación), los errores se **amplificaron 17.2x**. Incluso
con un orquestador central que actúa como "cuello de botella de validación",
la amplificación fue de 4.4x. En producción, la amplificación varía
dramáticamente según la calidad de la validación intermedia entre pasos:
sistemas con buena validación pueden tener amplificaciones de solo 2x,
mientras que sistemas sin validación pueden llegar a 50x. Las cifras
del paper son un punto de referencia, no una constante universal.

### El problema de la confianza composicional

Este es quizás el problema más sutil y el menos discutido. Supongamos que
tienes tres agentes: A, B y C. El agente A confía en las salidas del agente
B, y B confía en las salidas de C. ¿Puede A confiar transitivamente en C?

En lógica formal, la confianza **no es transitiva** en sistemas no deterministas.
Que A haya verificado que B es confiable (en ciertos contextos) y que B haya
verificado que C es confiable no implica que A pueda confiar en C. Cada
interfaz entre agentes es un punto donde las garantías se pueden degradar.

Piénsalo con una analogía: confías en que tu doctor recete medicamentos
adecuados, y tu doctor confía en la farmacia para surtir correctamente.
Pero si la farmacia contrata a un nuevo proveedor que no conoces, tu
confianza original en el doctor no cubre automáticamente a ese proveedor.
La cadena de confianza se rompe.

En nuestro artículo sobre
[OWASP Top 10 para LLMs](/posts/owasp-top-10-para-llms-las-nuevas-vulnerabilidades/),
discutimos vulnerabilidades como la inyección indirecta de prompts. Este
es exactamente un caso donde la confianza composicional falla: un agente
confía en datos de una fuente que ha sido comprometida, y esa confianza
mal fundamentada se propaga por toda la cadena.

## Propiedades verificables en agentes

La verificación formal clasifica las propiedades de un sistema en categorías
bien definidas. Entender estas categorías nos permite especificar
rigurosamente qué esperamos de un agente.

### Propiedades de seguridad (Safety)

Una propiedad de seguridad dice: **"algo malo NUNCA sucede"**. Es una
restricción sobre todos los estados posibles del sistema.

Ejemplos para agentes:

- El agente **nunca** ejecuta una compra sin confirmación del usuario.
- El agente **nunca** accede a datos de usuarios que no tienen relación con
  la tarea actual.
- El agente **nunca** gasta más de $500 en una sola transacción.
- El agente **nunca** ejecuta código destructivo (DROP TABLE, rm -rf, etc.).

Las propiedades de seguridad son las más importantes en producción porque
sus violaciones pueden ser catastróficas e irreversibles. Si tu agente
borra una base de datos, no importa que lo haya hecho solo una vez en un
millón de ejecuciones.

En lógica temporal, una propiedad de seguridad se expresa como:
**G(not peligro)** -- "globalmente, en todos los estados, la condición
peligrosa es falsa". La **G** (globally) es un operador de la lógica
temporal lineal (LTL) que significa "en todos los momentos futuros".

### Propiedades de vivacidad (Liveness)

Una propiedad de vivacidad dice: **"algo bueno EVENTUALMENTE sucede"**. No
dice cuándo, pero garantiza que el sistema no se queda atascado para siempre.

Ejemplos para agentes:

- El agente **eventualmente** completa la tarea asignada o escala a un humano.
- El agente **eventualmente** libera los recursos que reservó.
- El agente **eventualmente** responde al usuario (no se queda en un loop
  infinito de "pensamiento").

En lógica temporal: **F(completado)** -- "en algún momento futuro, la tarea
estará completada". La **F** (finally/future) es otro operador de LTL.

La distinción entre safety y liveness es elegante. Safety dice "nunca cruzamos
la línea roja". Liveness dice "eventualmente llegamos a la meta". Un buen
sistema necesita ambas: un agente que nunca hace nada malo pero tampoco hace
nada útil no sirve, y un agente que siempre completa la tarea pero a veces
borra tu disco tampoco.

### Propiedades de equidad (Fairness)

Las propiedades de equidad son más sutiles. Dicen: **"el sistema no favorece
injustamente ciertas opciones sobre otras"**. En el contexto de agentes,
esto es crítico:

- El agente no favorece consistentemente a un proveedor sobre otros en
  decisiones de compra.
- El agente no discrimina basándose en características protegidas al
  procesar solicitudes.
- El agente distribuye recursos de manera equitativa entre usuarios.

Las propiedades de fairness generalmente se verifican con model checking:
un explorador automático que examina todos los estados posibles del sistema
buscando violaciones. El model checker verifica exhaustivamente si existe
*algún* camino de ejecución donde la propiedad se viola.

El model checking enfrenta el problema de la explosión de estados: el número
de estados posibles crece exponencialmente con el tamaño del sistema. Pero
existen técnicas como el model checking simbólico y la abstracción que hacen
el problema manejable para sistemas de tamaño práctico.

## Herramientas y técnicas actuales

Los fundamentos están claros. Ahora la pregunta práctica: ¿qué herramientas
tenemos disponibles hoy para verificar agentes?

### TLA+ para especificar protocolos de agentes

TLA+ (Temporal Logic of Actions Plus) es un lenguaje de especificación formal
creado por Leslie Lamport (sí, el mismo del algoritmo de Lamport, los
relojes lógicos y LaTeX). TLA+ permite modelar sistemas concurrentes y
distribuidos de manera precisa, y viene con un model checker llamado TLC que
verifica automáticamente propiedades de tu especificación.

¿Por qué TLA+ es relevante para agentes? Porque un sistema multi-agente es,
en esencia, un sistema distribuido: múltiples entidades autónomas
que se comunican, toman decisiones independientes y deben coordinarse.
Amazon, Microsoft y otros gigantes usan TLA+ para verificar sus sistemas
distribuidos. El mismo enfoque aplica para protocolos de agentes.

Imaginemos una especificación simplificada de un agente de compras en
pseudo-TLA+. Si nunca has visto TLA+, piénsalo como un lenguaje para
describir máquinas de estados con reglas: cada bloque define una acción
posible, sus precondiciones (las líneas con `/\` son conjunciones, es
decir, "y") y cómo cambia el estado (las variables con `'` representan
el valor *después* de la acción). Las propiedades al final son las
garantías que el model checker TLC verificará exhaustivamente:

```
---- MODULE AgenteDeCompras ----
VARIABLES saldo, estado, historial, esperando_confirmacion

Invariante ==
    /\ saldo >= 0                          \* nunca saldo negativo
    /\ estado \in {"idle", "buscando",     \* estados válidos
                   "confirmando", "comprando",
                   "completado", "error"}

IniciarCompra(monto) ==
    /\ estado = "idle"
    /\ monto <= saldo
    /\ monto <= LIMITE_POR_TRANSACCION
    /\ estado' = "confirmando"
    /\ esperando_confirmacion' = TRUE

ConfirmarCompra ==
    /\ estado = "confirmando"
    /\ esperando_confirmacion = TRUE
    /\ estado' = "comprando"

EjecutarCompra(monto) ==
    /\ estado = "comprando"
    /\ saldo' = saldo - monto
    /\ estado' = "completado"
    /\ historial' = Append(historial, monto)

\* PROPIEDAD: Nunca se compra sin confirmación previa
SeguroSinConfirmacion == [](estado = "comprando" =>
                            esperando_confirmacion = TRUE)

\* PROPIEDAD: Eventualmente se completa o reporta error
EventualmenteTermina == <>(estado \in {"completado", "error"})
====
```

**Nota**: esto es pseudo-TLA+, no una especificación compilable por TLC.
Una especificación real necesitaría definiciones de `Init`, `Next` y otros
elementos. El propósito aquí es ilustrar el *tipo* de propiedades que se
pueden expresar. Dicho esto, esta especificación captura invariantes y
propiedades temporales que TLC puede verificar exhaustivamente explorando
todos los estados posibles.
Si existe alguna secuencia de eventos que viola estas propiedades, TLC la
encontrará y te mostrará el contraejemplo exacto.

Investigaciones recientes han explorado cómo integrar TLA+ con esquemas
formales de herramientas de agentes (como los schemas de MCP), incrustando
precondiciones y postcondiciones formales directamente en las definiciones
de las herramientas que los agentes pueden usar.

### Property-based testing: el puente pragmático

Si TLA+ te parece demasiado para tu contexto, hay un punto intermedio
muy poderoso: el **property-based testing**. La idea es simple pero elegante:
en vez de escribir pruebas con casos específicos, defines *propiedades* que
tu sistema debe cumplir, y una herramienta genera automáticamente cientos
o miles de casos de prueba buscando violaciones.

En Python, la biblioteca **Hypothesis** es la herramienta estrella para
esto. Veamos cómo usarla para verificar propiedades de un agente:

```python
from hypothesis import given, strategies as st, settings
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant

class AgenteDeComprasStateMachine(RuleBasedStateMachine):
    """
    Modelo de estados del agente de compras.
    Hypothesis explorará automáticamente secuencias
    de acciones buscando violaciones de invariantes.
    """
    def __init__(self):
        super().__init__()
        self.saldo = 1000.0
        self.compras = []
        self.confirmacion_pendiente = False
        self.limite_por_transaccion = 500.0

    @rule(monto=st.floats(min_value=0.01, max_value=1000.0))
    def solicitar_compra(self, monto):
        """El agente solicita una compra."""
        if monto <= self.saldo and monto <= self.limite_por_transaccion:
            self.confirmacion_pendiente = True
            self.monto_pendiente = monto

    @rule()
    def confirmar_compra(self):
        """El usuario confirma la compra."""
        if self.confirmacion_pendiente:
            self.saldo -= self.monto_pendiente
            self.compras.append(self.monto_pendiente)
            self.confirmacion_pendiente = False

    @rule()
    def cancelar_compra(self):
        """El usuario cancela la compra."""
        self.confirmacion_pendiente = False

    # INVARIANTES que Hypothesis verificará en cada estado
    @invariant()
    def saldo_nunca_negativo(self):
        assert self.saldo >= 0, f"Saldo negativo: {self.saldo}"

    @invariant()
    def limite_respetado(self):
        for compra in self.compras:
            assert compra <= self.limite_por_transaccion, \
                f"Compra {compra} excede límite {self.limite_por_transaccion}"

    @invariant()
    def saldo_consistente(self):
        esperado = 1000.0 - sum(self.compras)
        assert abs(self.saldo - esperado) < 0.01, \
            f"Saldo inconsistente: {self.saldo} vs esperado {esperado}"

# Hypothesis ejecutará miles de secuencias de acciones aleatorias
# buscando una que viole algún invariante
TestAgenteDeCompras = AgenteDeComprasStateMachine.TestCase
```

Lo brillante de Hypothesis es que no solo encuentra fallos: cuando los
encuentra, **minimiza** el caso de prueba para darte el ejemplo más simple
posible que reproduce el problema. Si tu agente falla después de una
secuencia de 47 acciones, Hypothesis te dirá cuáles son las 3 acciones
mínimas necesarias para reproducir el fallo.

El property-based testing no es verificación formal completa (no demuestra
que la propiedad se cumple para *todos* los casos), pero es mucho más
poderoso que el testing tradicional y mucho más accesible que la verificación
formal. Es un excelente punto de partida pragmático.

### Runtime verification: verificación en producción

Hay un enfoque que ha ganado mucha tracción recientemente: en lugar de
(o además de) verificar el agente antes de desplegarlo, **verificar su
comportamiento en tiempo real** mientras ejecuta en producción.

**Importante antes de continuar**: las herramientas que describo a
continuación (AgentSpec, VeriGuard y Pro2Guard) son propuestas de
investigación con prototipos académicos, *no* herramientas de producción
que puedas adoptar hoy. Si buscas herramientas maduras para verificación
en producción, las opciones reales en 2026 son TLA+ (para especificar
protocolos antes de implementarlos), Hypothesis (para property-based
testing) y frameworks de guardrails como Guardrails AI o NeMo Guardrails
de NVIDIA para runtime enforcement. Dicho esto, estas propuestas de
investigación son valiosas porque señalan hacia dónde se dirige el campo.

**AgentSpec**, presentado en 2025, es un lenguaje de dominio específico
(DSL) diseñado exactamente para esto. Permite definir reglas de ejecución
con tres componentes:

1. **Triggers** (disparadores): eventos que activan una regla. Por ejemplo,
   "cuando el agente intente ejecutar una transacción financiera".
2. **Predicados**: condiciones que se evalúan. Por ejemplo, "si el monto
   excede el umbral predefinido".
3. **Enforcements** (acciones de cumplimiento): lo que sucede cuando la
   regla se dispara. Por ejemplo, "requerir confirmación del usuario antes
   de ejecutar".

Los resultados son impresionantes: AgentSpec previene ejecuciones inseguras
en más del 90% de los casos con agentes de código, elimina todas las
acciones peligrosas en tareas de agentes embodied, y logra 100% de
cumplimiento en vehículos autónomos. Todo esto con overhead de milisegundos.

Otro framework notable es **VeriGuard**, que usa una arquitectura de doble
etapa: primero sintetiza una política de comportamiento a partir de las
especificaciones, y luego la somete tanto a testing como a verificación
formal para demostrar que cumple con las reglas de seguridad. Es como
tener un guardia de seguridad que no solo te revisa, sino que puede
*demostrar* matemáticamente que sus criterios de revisión son correctos.

Más recientemente, **Pro2Guard** incorpora model checking probabilístico
para hacer cumplimiento *proactivo*: en lugar de esperar a que el agente
intente algo peligroso, predice la probabilidad de acciones inseguras y
actúa preventivamente.

## El espectro de verificación

No es un mundo binario de "testing informal" versus "prueba formal completa".
Existe un espectro continuo, y es crucial entender dónde estamos y a dónde
podemos llegar pragmáticamente.

### Nivel 1: Testing manual ad-hoc

"Probé mi agente con 20 prompts y funcionó bien". Esto es donde está la
mayoría de la industria hoy. Es mejor que nada, pero las garantías son
mínimas. Si tu agente es un prototipo interno o un asistente de bajo
riesgo, quizás sea suficiente por ahora.

### Nivel 2: Testing automatizado con casos predefinidos

Suites de pruebas con cientos de escenarios, incluyendo edge cases.
Regresión automatizada. Si tu agente responde preguntas o genera contenido
sin efectos secundarios, este nivel te da una base sólida. Pero sigue
siendo una muestra finita de un espacio infinito.

### Nivel 3: Property-based testing y fuzzing

Hypothesis, fuzzing de entradas, generación aleatoria de escenarios.
Aquí empiezas a encontrar los fallos que no imaginaste. Si tu agente
interactúa con APIs externas o toma decisiones con cierta autonomía,
este es el punto de partida mínimo razonable.

### Nivel 4: Runtime verification con especificaciones formales

AgentSpec, VeriGuard, guardrails con propiedades formalmente definidas.
No demuestras que el agente *siempre* se portará bien, pero garantizas
que si intenta portarse mal, será detenido. Si tu agente maneja datos de
usuarios o ejecuta acciones con consecuencias reales, necesitas estar aquí.

### Nivel 5: Model checking parcial

TLA+, Alloy o herramientas similares para verificar propiedades específicas
del protocolo del agente (no del LLM subyacente, sino de la lógica de
orquestación). Si tu agente mueve dinero, gestiona infraestructura o toma
decisiones médicas, las garantías matemáticas de este nivel son necesarias
para las propiedades críticas.

### Nivel 6: Verificación formal completa

Pruebas matemáticas en sistemas como Lean, Coq o Agda de que el sistema
completo cumple sus especificaciones. Este es el estándar de oro, pero
actualmente es impracticable para agentes completos por la complejidad del
LLM. Sin embargo, puedes verificar formalmente la capa de orquestación y
los guardrails, dejando al LLM como un componente "no confiable" contenido
por una capa de seguridad formalmente verificada.

### ¿Dónde deberían estar los agentes en producción?

Mi recomendación: **mínimo nivel 3, idealmente nivel 4**, para agentes
en producción. Si tu agente maneja dinero, datos personales o acciones
irreversibles, deberías aspirar al nivel 5 para las propiedades críticas.

La clave es entender que no necesitas verificar todo formalmente. Puedes
usar un enfoque por capas: verificación formal para las propiedades de
seguridad críticas, property-based testing para propiedades funcionales
importantes, y testing automatizado para el resto.

## Ejemplo práctico: especificando invariantes para un agente de compras

Vamos a poner todo junto con un ejemplo concreto y completo. Diseñaremos
las especificaciones formales para un agente que compra productos en
línea en nombre de un usuario.

### Definiendo las propiedades

Nuestro agente debe cumplir las siguientes propiedades verificables:

**Propiedades de Safety (nunca):**

1. El agente **nunca** gasta más de $500 por transacción.
2. El agente **nunca** ejecuta una compra sin confirmación explícita
   del usuario.
3. El agente **nunca** compra del mismo proveedor más de 3 veces
   consecutivas (anti-favoritismo).
4. El gasto total acumulado **nunca** excede el presupuesto mensual.

**Propiedades de Liveness (eventualmente):**

5. El agente **eventualmente** completa la tarea o escala a un humano
   (no se queda en un loop infinito).
6. El agente **eventualmente** libera cualquier lock sobre el carrito
   de compras.

**Propiedades de Fairness:**

7. Si hay múltiples proveedores con precio similar (dentro de 5%),
   el agente **no siempre** elige el mismo.

### Implementación con guardias y monitoreo

Ahora implementemos estas propiedades como un sistema de runtime
verification en Python:

```python
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("agent_verifier")


@dataclass
class InvarianteViolado(Exception):
    """Excepción que se lanza cuando un invariante es violado."""
    propiedad: str
    contexto: dict


@dataclass
class EstadoAgente:
    """Estado observable del agente de compras."""
    saldo_disponible: float
    presupuesto_mensual: float
    gasto_mensual: float = 0.0
    compras_realizadas: list = field(default_factory=list)
    proveedor_consecutivo: list = field(default_factory=list)
    esperando_confirmacion: bool = False
    tarea_iniciada: Optional[datetime] = None
    timeout_tarea: timedelta = timedelta(minutes=30)


class VerificadorDeAgente:
    """
    Monitor de runtime que verifica invariantes en cada
    transición de estado del agente.
    """

    def __init__(self, estado: EstadoAgente):
        self.estado = estado

    def pre_compra_sin_confirmacion(self, monto: float, proveedor: str) -> None:
        """
        Verificaciones ANTES de pedir confirmación al usuario.
        Verifica Safety 1, 3 y 4 (todo excepto confirmación).
        Lanza InvarianteViolado si alguna propiedad se viola.
        """
        # Safety 1: Límite por transacción
        if monto > 500:
            raise InvarianteViolado(
                propiedad="SAFETY-1: Límite por transacción",
                contexto={"monto": monto, "limite": 500}
            )

        # Safety 3: Anti-favoritismo
        ultimos_proveedores = self.estado.proveedor_consecutivo[-3:]
        if (len(ultimos_proveedores) == 3 and
                all(p == proveedor for p in ultimos_proveedores)):
            raise InvarianteViolado(
                propiedad="SAFETY-3: Mismo proveedor 3 veces consecutivas",
                contexto={
                    "proveedor": proveedor,
                    "historial": ultimos_proveedores
                }
            )

        # Safety 4: Presupuesto mensual
        if self.estado.gasto_mensual + monto > self.estado.presupuesto_mensual:
            raise InvarianteViolado(
                propiedad="SAFETY-4: Excede presupuesto mensual",
                contexto={
                    "gasto_actual": self.estado.gasto_mensual,
                    "monto_nuevo": monto,
                    "presupuesto": self.estado.presupuesto_mensual
                }
            )

    def verificar_confirmacion(self) -> None:
        """
        Verifica SAFETY-2: que el usuario haya confirmado la compra.
        Se llama DESPUÉS de obtener la confirmación, ANTES de ejecutar.
        """
        if not self.estado.esperando_confirmacion:
            raise InvarianteViolado(
                propiedad="SAFETY-2: Compra sin confirmación",
                contexto={"estado": "no confirmado"}
            )

    def verificar_liveness(self) -> Optional[str]:
        """
        Verifica propiedades de liveness.
        Retorna acción correctiva si es necesaria.
        """
        # Liveness 5: Timeout de tarea
        if self.estado.tarea_iniciada:
            tiempo_transcurrido = datetime.now() - self.estado.tarea_iniciada
            if tiempo_transcurrido > self.estado.timeout_tarea:
                logger.warning(
                    "LIVENESS-5: Tarea excedió timeout, escalando a humano"
                )
                return "ESCALAR_A_HUMANO"

        return None

    def post_compra(self, monto: float, proveedor: str) -> None:
        """
        Actualiza estado y verifica invariantes post-compra.
        """
        self.estado.gasto_mensual += monto
        self.estado.compras_realizadas.append(monto)
        self.estado.proveedor_consecutivo.append(proveedor)
        self.estado.esperando_confirmacion = False

        # Verificar invariante global: saldo consistente
        assert self.estado.saldo_disponible >= 0, \
            "INVARIANTE GLOBAL: Saldo negativo detectado"


# Uso del verificador como wrapper del agente
class AgenteDeComprasSeguro:
    """
    Agente de compras con verificación de invariantes integrada.
    El agente real (basado en LLM) está envuelto por el verificador.
    """

    def __init__(self, agente_llm, presupuesto_mensual: float):
        self.agente_llm = agente_llm
        self.estado = EstadoAgente(
            saldo_disponible=presupuesto_mensual,
            presupuesto_mensual=presupuesto_mensual
        )
        self.verificador = VerificadorDeAgente(self.estado)

    async def comprar(self, descripcion: str) -> dict:
        self.estado.tarea_iniciada = datetime.now()

        # El LLM decide qué comprar
        decision = await self.agente_llm.decidir(descripcion)

        # Verificar liveness
        accion_correctiva = self.verificador.verificar_liveness()
        if accion_correctiva == "ESCALAR_A_HUMANO":
            return {"status": "ESCALADO", "razon": "Timeout de tarea"}

        # Verificar Safety 1, 3 y 4 ANTES de pedir confirmación
        # (no verificamos SAFETY-2 aquí; eso se verifica después
        # de obtener la confirmación del usuario)
        try:
            self.verificador.pre_compra_sin_confirmacion(
                monto=decision["monto"],
                proveedor=decision["proveedor"]
            )
        except InvarianteViolado as e:
            logger.error(f"Invariante violado: {e.propiedad}")
            return {
                "status": "BLOQUEADO",
                "razon": e.propiedad,
                "contexto": e.contexto
            }

        # Pedir confirmación al usuario (SAFETY-2)
        self.estado.esperando_confirmacion = True
        confirmado = await self.pedir_confirmacion(decision)

        if not confirmado:
            self.estado.esperando_confirmacion = False
            return {"status": "CANCELADO", "razon": "Usuario canceló"}

        # Ahora sí verificamos SAFETY-2: confirmar que el usuario aprobó
        try:
            self.verificador.verificar_confirmacion()
        except InvarianteViolado as e:
            logger.error(f"Invariante violado: {e.propiedad}")
            return {
                "status": "BLOQUEADO",
                "razon": e.propiedad,
                "contexto": e.contexto
            }

        # Ejecutar la compra
        resultado = await self.agente_llm.ejecutar_compra(decision)

        # DESPUÉS de ejecutar: actualizar estado y verificar
        self.verificador.post_compra(
            monto=decision["monto"],
            proveedor=decision["proveedor"]
        )

        return {"status": "COMPLETADO", "resultado": resultado}
```

Lo importante aquí es el patrón: **el LLM puede decidir lo que quiera,
pero sus decisiones pasan por un verificador determinista antes de
ejecutarse**. El LLM es el cerebro creativo; el verificador es la jaula
de seguridad. Esta separación entre "inteligencia" y "garantías" es
fundamental, y conecta directamente con el patrón que discutimos en
[Patrones de diseño para sistemas con IA](/posts/patrones-de-diseno-para-sistemas-con-ia/)
sobre separar la inteligencia de la lógica de negocio.

### Verificando con Hypothesis

Ahora, ¿cómo sabemos que nuestro verificador es correcto? Usemos
property-based testing para verificar al verificador:

```python
from hypothesis import given, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant


class TestVerificadorCompras(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.estado = EstadoAgente(
            saldo_disponible=2000.0,
            presupuesto_mensual=2000.0
        )
        self.verificador = VerificadorDeAgente(self.estado)
        self.total_gastado = 0.0

    @rule(
        monto=st.floats(min_value=0.01, max_value=600.0),
        proveedor=st.sampled_from(["Amazon", "MercadoLibre", "Walmart"])
    )
    def intentar_compra(self, monto, proveedor):
        try:
            self.verificador.pre_compra_sin_confirmacion(monto, proveedor)
            # Simular confirmación del usuario
            self.estado.esperando_confirmacion = True
            self.verificador.verificar_confirmacion()
            # Si no lanzó excepción, la compra es válida.
            # Verificar que realmente cumple las propiedades:
            assert monto <= 500, "Debió bloquear: excede límite"
            assert self.estado.gasto_mensual + monto <= 2000.0, \
                "Debió bloquear: excede presupuesto"
            # Ejecutar
            self.verificador.post_compra(monto, proveedor)
            self.total_gastado += monto
        except InvarianteViolado:
            # Compra bloqueada correctamente
            pass

    @invariant()
    def gasto_dentro_de_presupuesto(self):
        assert self.estado.gasto_mensual <= self.estado.presupuesto_mensual

    @invariant()
    def saldo_no_negativo(self):
        assert self.estado.saldo_disponible >= 0

    @invariant()
    def consistencia_gasto(self):
        assert abs(self.total_gastado - self.estado.gasto_mensual) < 0.01


TestVerificador = TestVerificadorCompras.TestCase
```

Hypothesis ejecutará automáticamente miles de secuencias de acciones,
buscando cualquier combinación que viole los invariantes. Si nuestro
verificador tiene un bug (digamos, un error de punto flotante que
permite que el gasto exceda el presupuesto por una fracción), Hypothesis
lo encontrará y nos dará el caso mínimo que lo reproduce.

## La verificación formal como necesidad, no como lujo

Hay un argumento recurrente contra la verificación formal: "es demasiado
cara, demasiado lenta, solo sirve para sistemas críticos como aviones
y reactores nucleares". Ese argumento tenía cierto peso hace 10 años.
Hoy ya no se sostiene, por tres razones.

**Primero**, los agentes de IA *son* sistemas críticos. Cuando un agente
maneja tu dinero, tus datos médicos o tus decisiones legales, las
consecuencias de un fallo son comparables a las de un sistema embebido
en un avión. La diferencia es que los ingenieros aeronáuticos llevan
décadas usando verificación formal, y la industria de IA apenas está
descubriendo que la necesita.

**Segundo**, las herramientas se han vuelto mucho más accesibles. No
necesitas un doctorado en lógica para usar Hypothesis, AgentSpec o
incluso TLA+. Martin Kleppmann, autor de "Designing Data-Intensive
Applications", ha argumentado recientemente que la IA misma hará que la
verificación formal sea mainstream: los LLMs pueden ayudar a escribir
especificaciones formales, reduciendo la barrera de entrada.

**Tercero**, el costo de *no* verificar está creciendo exponencialmente.
A medida que los agentes toman decisiones más autónomas y con mayores
consecuencias, un solo fallo no detectado puede costar más que meses de
esfuerzo en verificación. El framework de seguridad para sistemas
agénticos publicado en 2025 argumenta que las aproximaciones empíricas
y reactivas (identificar y parchear vulnerabilidades conforme se
descubren) simplemente no son suficientes para proporcionar garantías
formales de seguridad.

### Cuándo vale la pena (y cuándo no)

La verificación formal tiene un costo real. Escribir especificaciones TLA+
para un protocolo de agentes toma 2-4 semanas de un ingeniero senior.
Configurar property-based testing con Hypothesis para un agente completo
toma 1-2 semanas. No tiene sentido invertir ese esfuerzo en todos los
agentes por igual. Aquí hay una guía:

- **Riesgo bajo, uso bajo** (ej. un chatbot interno de clasificación de
  tickets): testing manual y automatizado (niveles 1-2) es suficiente.
  No necesitas TLA+ para esto.
- **Riesgo bajo, uso alto** (ej. un agente de generación de contenido):
  property-based testing (nivel 3) te da buena cobertura sin sobreingeniería.
- **Riesgo alto, uso bajo** (ej. un agente de administración de
  infraestructura): runtime verification (nivel 4) con propiedades de safety
  bien definidas. El costo se justifica aunque el volumen sea bajo.
- **Riesgo alto, uso alto** (ej. un agente que mueve dinero o toma decisiones
  médicas): model checking parcial (nivel 5) para las propiedades críticas.
  Aquí cada peso invertido en verificación te ahorra potencialmente miles
  en incidentes.

La regla general: la inversión en verificación debe ser proporcional al
costo potencial de un fallo multiplicado por la frecuencia de uso.

### Un camino pragmático hacia adelante

No tienes que hacer todo de golpe. Aquí hay un camino incremental:

1. **Hoy**: Identifica las 3-5 propiedades de seguridad más críticas
   de tu agente. Impleméntalas como runtime checks (nivel 4).

2. **Esta semana**: Agrega property-based testing con Hypothesis para
   verificar que tus runtime checks son correctos y completos (nivel 3).

3. **Este mes**: Especifica el protocolo de tu agente en TLA+ o un
   lenguaje similar, al menos la máquina de estados de alto nivel
   (nivel 5).

4. **Este trimestre**: Implementa un framework de runtime verification
   completo con AgentSpec o similar, con logging, alertas y
   escalamiento automático a humanos.

Cada paso te da más confianza. Y cada paso te acerca más a poder decir
con honestidad: "mi agente funciona en producción", no solo "funciona
en la demo".

## Referencias y fuentes clave

1. Hoare, C.A.R. "An Axiomatic Basis for Computer Programming."
   *Communications of the ACM*, 12(10), 576-580, 1969.

2. Lamport, L. "Specifying Systems: The TLA+ Language and Tools for
   Hardware and Software Engineers." Addison-Wesley, 2002.

3. Sistla, A.P. "Safety, Liveness and Fairness in Temporal Logic."
   *Formal Aspects of Computing*, 6, 495-511, 1994.

4. Mu, Y. et al. "AgentSpec: Customizable Runtime Enforcement for
   Safe and Reliable LLM Agents." arXiv:2503.18666, 2025.

5. Mei, K. et al. "VeriGuard: Enhancing LLM Agent Safety via
   Verified Code Generation." arXiv:2510.05156, 2025.

6. Chen, J. et al. "Pro2Guard: Proactive Runtime Enforcement of LLM
   Agent Safety via Probabilistic Model Checking." arXiv:2508.00500,
   2025.

7. Guo, Z. et al. "Towards Verifiably Safe Tool Use for LLM Agents."
   arXiv:2601.08012, 2026.

8. Guo, Z. et al. "Towards a Science of Scaling Agent Systems: When
   and Why Agent Systems Work." Google Research, 2025.

9. Kleppmann, M. "Prediction: AI Will Make Formal Verification Go
   Mainstream." Blog post, diciembre 2025.

10. Li, Y. et al. "Formalizing the Safety, Security, and Functional
    Properties of AI Agents." arXiv:2510.14133, 2025.

11. MacLeod, B. et al. "A Safety and Security Framework for Real-World
    Agentic Systems." arXiv:2511.21990, 2025.

12. Wei, J. et al. "Chain-of-Thought Prompting Elicits Reasoning in
    Large Language Models." *NeurIPS*, 2022.

13. Alpern, B. y Schneider, F.B. "Defining Liveness." *Information
    Processing Letters*, 21(4), 181-185, 1985.

14. Clarke, E.M., Emerson, E.A. y Sifakis, J. "Model Checking:
    Algorithmic Verification and Debugging." *Communications of the
    ACM*, 52(11), 74-84, 2009. (Premio Turing 2007).
