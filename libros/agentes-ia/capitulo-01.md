# Capitulo 1: Un Agente No Es un Chatbot con Herramientas

> "Si le preguntas a cinco personas que es un agente de IA, obtendras siete respuestas diferentes. La palabra se ha convertido en un comodin que puede significar desde un chatbot con acceso a herramientas hasta un sistema autonomo que toma decisiones financieras. Resulta que el concepto tiene decadas de historia rigurosa."

---

La palabra "agente" ha sufrido una inflacion semantica brutal. Las startups la usan para vender chatbots con tres endpoints. Los frameworks la usan para justificar su complejidad. Los tutoriales la usan para prometer que cualquiera puede construir uno en 15 minutos.

Pero un agente no es un wrapper de API con un system prompt. Tampoco es un pipeline de RAG con un loop. Y definitivamente no es un chatbot que "a veces" llama funciones.

El concepto de agente en inteligencia artificial tiene mas de 30 anos de historia formal. Mucho antes de que existieran los LLMs, investigadores en IA habian definido, clasificado y debatido extensamente que significa ser un agente. Y esas definiciones clasicas no solo siguen siendo relevantes: son **esenciales** para entender que estamos construyendo hoy y que limitaciones tiene.

En este capitulo vamos a hacer un viaje desde las definiciones formales de los libros de texto hasta los agentes LLM modernos. No porque la teoria sea un requisito academico vacio, sino porque entender los fundamentos te da herramientas para disenar mejores sistemas. Regresar a las definiciones es una de las tecnicas mas poderosas para resolver problemas complejos, como decia Polya.

Empecemos por el principio.

---

## 1.1 La definicion clasica: Russell y Norvig

Stuart Russell y Peter Norvig, en su libro *Artificial Intelligence: A Modern Approach* --el texto de IA mas usado en universidades del mundo desde su primera edicion en 1995--, proponen una definicion elegante y sorprendentemente amplia:

> **Un agente es todo aquello que puede considerarse que percibe su ambiente a traves de sensores y actua sobre ese ambiente a traves de actuadores.** [Russell y Norvig, 2020]

Eso es todo. No se necesita inteligencia, no se necesita lenguaje, no se necesita aprendizaje. Un **termostato** es un agente bajo esta definicion: percibe la temperatura (sensor) y enciende o apaga la calefaccion (actuador). Un ser humano tambien es un agente: percibe con ojos, oidos y tacto, y actua con manos, piernas y voz.

Esta amplitud es intencional. Russell y Norvig querian un marco que permitiera analizar **cualquier** sistema que interactua con un ambiente, desde los mas simples hasta los mas sofisticados. La pregunta interesante no es si algo es un agente --casi todo lo es bajo esta definicion--, sino **que tipo** de agente es.

La definicion tiene dos componentes esenciales que vale la pena desmenuzar:

**Percepcion**: el agente recibe informacion del ambiente. Esto puede ser tan simple como un sensor de temperatura o tan complejo como una camara de video conectada a un modelo de vision por computadora. En el mundo de los LLMs, la "percepcion" incluye el prompt del usuario, los resultados de las herramientas, y todo el contexto que llega a la ventana de contexto del modelo.

**Accion**: el agente hace algo que modifica el ambiente. Puede ser encender una calefaccion, girar un volante, enviar un email o ejecutar una query SQL. En los agentes LLM, las acciones son las tool calls, la generacion de texto, la ejecucion de codigo.

Lo que conecta percepcion y accion es la **funcion del agente**: un mapeo de secuencias de percepciones a acciones. Para un agente racional, esta funcion deberia maximizar alguna medida de rendimiento. La implementacion concreta de esa funcion es lo que llamamos el **programa del agente**.

Podemos modelar esta abstraccion en Python:

```python
from abc import ABC, abstractmethod
from typing import Any


class Agent(ABC):
    """Un agente abstracto: percibe y actua.

    La definicion mas basica posible, siguiendo a Russell y Norvig.
    Todo lo demas se construye sobre esto.
    """

    @abstractmethod
    def perceive(self, percept: Any) -> None:
        """Recibe una percepcion del ambiente."""
        pass

    @abstractmethod
    def act(self) -> Any:
        """Decide y ejecuta una accion."""
        pass


class ThermostatAgent(Agent):
    """El agente mas simple del mundo: un termostato.

    Percibe temperatura, actua encendiendo/apagando calefaccion.
    Es un agente legitimo segun Russell y Norvig.
    """

    def __init__(self, target_temp: float = 22.0):
        self.target_temp = target_temp
        self.current_temp: float | None = None

    def perceive(self, percept: dict) -> None:
        self.current_temp = percept["temperature"]

    def act(self) -> str:
        if self.current_temp is None:
            return "esperar"
        if self.current_temp < self.target_temp - 0.5:
            return "encender_calefaccion"
        elif self.current_temp > self.target_temp + 0.5:
            return "apagar_calefaccion"
        return "mantener"
```

Este termostato cumple perfectamente la definicion de agente. Percibe (temperatura), razona (compara con el objetivo) y actua (enciende o apaga). Es el agente mas simple posible, pero es un agente legitimo.

Y eso nos lleva a la pregunta natural: si un termostato y un sistema con GPT-5 son ambos "agentes", que los distingue? La respuesta esta en un marco de cuatro letras.

---

## 1.2 PEAS: el marco para describir cualquier agente

Para hacer operativa su definicion de agente, Russell y Norvig propusieron el marco **PEAS**, un acronimo que describe los cuatro componentes fundamentales:

- **P**erformance (Medida de rendimiento): como evaluamos si el agente esta haciendo un buen trabajo?
- **E**nvironment (Ambiente): en que entorno opera el agente?
- **A**ctuators (Actuadores): que acciones puede realizar el agente?
- **S**ensors (Sensores): que informacion puede percibir el agente?

PEAS es mas que una taxonomia. Es una **herramienta de diseno**. Definir PEAS *antes* de escribir codigo te ahorra semanas de iteracion. He aqui por que cada componente importa:

### Performance (Medida de rendimiento)

Sin una medida clara de exito, no puedes evaluar si tu agente funciona. La medida de rendimiento se traduce directamente en tus evaluaciones automatizadas (evals) y en los criterios de aceptacion de tu sistema.

Parece obvio, pero la mayoria de los equipos lanzan agentes sin una medida de rendimiento explicita. "Que responda bien" no es una medida. "Que resuelva el 85% de las consultas de soporte sin escalamiento a un humano, con un tiempo promedio de resolucion menor a 3 minutos y una satisfaccion del usuario mayor a 4.0/5.0" si lo es.

### Environment (Ambiente)

Definir el ambiente te dice que tan impredecible es el mundo de tu agente. Russell y Norvig clasifican los ambientes en varias dimensiones:

- **Observable vs. parcialmente observable**: puede el agente ver todo el estado del ambiente? Un juego de ajedrez es completamente observable; una negociacion por chat es parcialmente observable.
- **Deterministico vs. estocastico**: el siguiente estado del ambiente esta completamente determinado por el estado actual y la accion del agente? Las APIs son deterministicas; los usuarios son estocasticos.
- **Estatico vs. dinamico**: el ambiente cambia mientras el agente delibera? Una base de datos es relativamente estatica; un mercado financiero es dinamico.
- **Discreto vs. continuo**: hay un numero finito de estados y acciones? Un chatbot tiene acciones discretas (herramientas especificas); un robot tiene acciones continuas (angulos y velocidades).

Estas dimensiones determinan directamente la complejidad de tu agente. Un agente en un ambiente completamente observable, deterministico, estatico y discreto puede ser un simple conjunto de reglas. Un agente en un ambiente parcialmente observable, estocastico, dinamico y continuo necesita planificacion sofisticada, manejo de incertidumbre y adaptacion en tiempo real.

La mayoria de los agentes LLM que construimos hoy operan en ambientes parcialmente observables (el agente no puede ver todo el estado del sistema), estocasticos (los usuarios son impredecibles), dinamicos (los datos cambian) y discretos (las herramientas son un conjunto finito). Eso los coloca en la zona de complejidad media-alta, lo que explica por que son mas dificiles de lo que parecen en la demo.

### Actuators (Actuadores)

Las herramientas que le das a tu agente **son** sus actuadores. Cada herramienta que anades es un actuador mas que necesitas testear, monitorear y controlar.

Esta correspondencia directa es critica: si le das al agente un actuador de "ejecutar SQL arbitrario", acabas de darle el equivalente de un brazo robotico sin articulaciones de seguridad en una fabrica. Si le das un actuador de "ejecutar SELECT sobre la tabla products con limite de 100 filas", acabas de darle un brazo con limites de movimiento bien definidos.

Como vimos en el Capitulo 0, la diferencia entre un agente que funciona en produccion y uno que borra 14,000 registros esta directamente en el diseno de sus actuadores.

### Sensors (Sensores)

Los sensores determinan que informacion entra al contexto del agente. Si no defines tus sensores explicitamente, terminas con agentes que reciben demasiada o muy poca informacion.

Demasiada informacion satura la ventana de contexto y degrada la calidad de las respuestas (ver Capitulo 5). Muy poca informacion obliga al agente a alucinar lo que no sabe. El diseno de los sensores --que datos le llegan al agente, en que formato, con que frecuencia-- es tan importante como el diseno del prompt.

### PEAS en codigo

```python
from dataclasses import dataclass


@dataclass
class PEAS:
    """Descripcion formal de un agente segun Russell y Norvig.

    Define PEAS antes de escribir codigo. Es la especificacion
    mas concisa y util de tu sistema.
    """
    performance: str          # Como mides el exito
    environment: str          # Donde opera el agente
    actuators: list[str]      # Que puede hacer
    sensors: list[str]        # Que puede percibir


# Ejemplo 1: agente de soporte al cliente
support_agent = PEAS(
    performance=(
        "Resolver 85%+ de consultas sin escalamiento humano. "
        "Tiempo promedio < 3 min. Satisfaccion > 4.0/5.0"
    ),
    environment=(
        "Conversaciones con usuarios via chat. "
        "Base de conocimiento de productos. "
        "Sistema de tickets Zendesk. "
        "Ambiente: parcialmente observable, estocastico, dinamico"
    ),
    actuators=[
        "responder_al_usuario",
        "buscar_en_base_de_conocimiento",
        "crear_ticket",
        "escalar_a_humano",
    ],
    sensors=[
        "mensaje_del_usuario",
        "historial_de_conversacion",
        "perfil_del_cliente",
        "estado_del_pedido",
    ],
)


# Ejemplo 2: agente de analisis de datos
data_agent = PEAS(
    performance=(
        "Generar analisis correctos en 90%+ de los casos. "
        "Tiempo < 60 segundos. Costo < $0.50 por consulta"
    ),
    environment=(
        "Base de datos PostgreSQL de solo lectura. "
        "Datos de ventas de los ultimos 2 anos. "
        "Ambiente: completamente observable, deterministico, estatico"
    ),
    actuators=[
        "ejecutar_query_sql_select",
        "generar_grafico",
        "responder_con_resumen",
    ],
    sensors=[
        "pregunta_del_usuario",
        "esquema_de_la_base_de_datos",
        "resultados_de_queries",
    ],
)


# Ejemplo 3: agente de trading (alto riesgo)
trading_agent = PEAS(
    performance=(
        "Retorno ajustado por riesgo (Sharpe > 1.5). "
        "Drawdown maximo < 5%. "
        "Latencia de decision < 100ms"
    ),
    environment=(
        "Mercado financiero en tiempo real. "
        "Multiples exchanges. "
        "Ambiente: parcialmente observable, estocastico, "
        "altamente dinamico, continuo"
    ),
    actuators=[
        "colocar_orden_compra",
        "colocar_orden_venta",
        "cancelar_orden",
        "ajustar_stop_loss",
    ],
    sensors=[
        "precios_en_tiempo_real",
        "volumen_de_operaciones",
        "indicadores_tecnicos",
        "noticias_del_mercado",
        "posiciones_actuales",
    ],
)
```

Observa como la complejidad del agente escala con la complejidad del ambiente. El agente de datos opera en un ambiente observable, deterministico y estatico; puede ser relativamente simple. El agente de trading opera en un ambiente parcialmente observable, estocastico, dinamico y continuo; necesita una arquitectura sofisticada y controles rigurosos.

La proxima vez que escuches "estamos construyendo un agente de IA", pregunta por cada componente de PEAS. La cantidad de claridad --o la falta de ella-- te dira mucho sobre la madurez del proyecto.

### Ejercicio: Define PEAS para tu sistema

Antes de continuar, toma 10 minutos para definir el PEAS de un agente que te gustaria construir. Usa esta plantilla:

```python
mi_agente = PEAS(
    performance="___",   # Como sabes si funciona?
    environment="___",   # Donde opera? Observable? Deterministico?
    actuators=[],        # Que puede hacer? (se especifico)
    sensors=[],          # Que informacion recibe?
)
```

Preguntas guia:
- Tu medida de rendimiento es medible automaticamente?
- Tu ambiente es parcialmente observable? Si lo es, que informacion le falta al agente?
- Cada actuador tiene limites claros? O hay actuadores "abiertos" como "ejecutar codigo arbitrario"?
- Tus sensores le dan al agente informacion suficiente para tomar decisiones, sin saturar su contexto?

Si no puedes responder alguna de estas preguntas, tienes un problema de diseno que ningun framework ni ningun modelo va a resolver por ti.

---

## 1.3 Taxonomia de agentes: de lo simple a lo sofisticado

Russell y Norvig no se quedaron con una definicion plana. Propusieron una **taxonomia** de agentes organizada por complejidad creciente, donde cada nivel agrega capacidades sobre el anterior. Esta clasificacion sigue siendo una de las mas utiles para entender donde caen los diferentes sistemas que construimos.

### Agentes reactivos simples

El tipo mas basico. Un agente reactivo simple selecciona acciones basandose **unicamente** en la percepcion actual, sin memoria ni modelo del mundo. Es esencialmente una tabla de lookup: "si ves X, haz Y".

```python
class SimpleReflexAgent(Agent):
    """Agente que reacciona solo a la percepcion actual.

    Sin memoria, sin modelo del mundo. Pura tabla de reglas.
    El termostato es el ejemplo canonico.
    """

    def __init__(self, rules: dict):
        self.rules = rules  # {condicion: accion}
        self.current_percept = None

    def perceive(self, percept: Any) -> None:
        self.current_percept = percept

    def act(self) -> Any:
        for condition, action in self.rules.items():
            if condition(self.current_percept):
                return action
        return "no_action"
```

Nuestro termostato es exactamente esto. No recuerda que temperatura habia hace cinco minutos ni predice hacia donde va la temperatura. Solo reacciona al momento presente.

Puede parecer primitivo, pero hay escenarios de produccion donde un agente reactivo simple es la solucion correcta. Un filtro de spam basado en reglas, un clasificador de tickets con logica if-then, un router que envia consultas al modelo correcto basandose en patrones de texto: todos son agentes reactivos simples, y no hay nada malo en eso. La complejidad innecesaria es el enemigo, no la simplicidad.

### Agentes reactivos basados en modelo

Agregan algo crucial: **estado interno**. El agente mantiene un modelo de como funciona el mundo y usa ese modelo para interpretar percepciones parciales. Esto le permite operar en ambientes **parcialmente observables**, donde no puede ver todo a la vez.

```python
class ModelBasedAgent(Agent):
    """Agente con estado interno y modelo del mundo.

    Puede operar en ambientes parcialmente observables porque
    recuerda lo que ha visto antes y tiene un modelo de como
    cambia el mundo.
    """

    def __init__(self):
        self.state: dict = {}       # Modelo interno del mundo
        self.last_action = None

    def perceive(self, percept: Any) -> None:
        # Actualiza el estado usando lo que ya sabia + lo nuevo
        self.state = self._update_state(self.state, percept)

    def _update_state(self, state: dict, percept: Any) -> dict:
        """Combina conocimiento previo con percepcion nueva."""
        new_state = state.copy()
        if isinstance(percept, dict):
            new_state.update(percept)
        return new_state

    def act(self) -> Any:
        # Usa el estado completo, no solo la percepcion actual
        action = self._select_action(self.state)
        self.last_action = action
        return action

    def _select_action(self, state: dict) -> str:
        """Logica de decision basada en el estado completo."""
        raise NotImplementedError
```

Un ejemplo concreto: un robot que navega por una casa. No puede ver todas las habitaciones al mismo tiempo, pero mantiene un mapa interno que actualiza con cada percepcion. Sabe que hay una pared detras de el aunque no la este viendo en este momento.

En el mundo de los LLMs, un agente basado en modelo es cualquier agente que mantiene estado entre turnos de conversacion. La ventana de contexto *es* el estado interno. Los resultados de herramientas anteriores *son* el modelo del mundo. Cuando un agente de soporte recuerda que el usuario ya menciono su numero de pedido tres turnos atras, esta funcionando como un agente basado en modelo.

### Agentes basados en objetivos

Agregan algo que los anteriores no tenian: un **objetivo explicito**. El agente no solo reacciona al mundo; tiene una meta y planifica como alcanzarla. Esto requiere capacidad de **busqueda y planificacion**: el agente puede simular secuencias de acciones y evaluar cual lo acerca mas a su objetivo.

La diferencia es sutil pero profunda. Un agente reactivo en un laberinto seguiria la regla "siempre gira a la derecha". Un agente basado en objetivos podria explorar el laberinto, construir un mapa mental y planificar la ruta mas corta hacia la salida.

En el mundo de los LLMs, los agentes basados en objetivos son los que usan el patron **Plan-and-Execute** (que veremos en detalle en el Capitulo 3): primero generan un plan para alcanzar el objetivo, luego ejecutan cada paso del plan.

### Agentes basados en utilidad

Van un paso mas alla: no solo tienen objetivos, sino una **funcion de utilidad** que les permite evaluar que tan "bueno" es cada estado posible. Esto les permite tomar decisiones cuando hay multiples objetivos en conflicto o cuando hay incertidumbre.

Un agente basado en objetivos para un taxi autonomo solo necesita "llegar al destino". Un agente basado en utilidad puede balancear multiples factores: llegar rapido, consumir poca gasolina, mantener al pasajero comodo y respetar las leyes de transito. La funcion de utilidad codifica las preferencias y permite tomar decisiones en situaciones de compromiso.

En los agentes LLM, la funcion de utilidad rara vez es explicita, pero existe implicitamente. Cuando un agente de servicio al cliente decide entre resolver una consulta rapidamente (eficiencia) o dar una respuesta exhaustiva (completitud), esta haciendo un trade-off de utilidad. El problema es que este trade-off esta codificado en el prompt y en los pesos del modelo, no en una funcion matematica que puedas inspeccionar y ajustar.

### Agentes que aprenden

Finalmente, la corona de la taxonomia: agentes que **mejoran su rendimiento con la experiencia**. Russell y Norvig definen cuatro componentes conceptuales:

1. **Elemento de rendimiento**: selecciona acciones (es cualquiera de los agentes anteriores).
2. **Elemento de aprendizaje**: modifica el elemento de rendimiento para mejorar.
3. **Critico**: evalua como esta funcionando el agente respecto a la medida de rendimiento.
4. **Generador de problemas**: sugiere acciones exploratorias para descubrir informacion nueva.

Los agentes LLM son una mezcla curiosa respecto al aprendizaje. El modelo subyacente fue entrenado con datos (aprendio), pero no aprende *durante la ejecucion* de una tarea individual. Sin embargo, hay mecanismos para simular aprendizaje: el patron **Reflexion** (que veremos en el Capitulo 3) permite al agente criticar sus propios intentos y mejorar en reintentos sucesivos. Y los sistemas de memoria a largo plazo (Capitulo 6) permiten que el agente "recuerde" experiencias pasadas y las aplique en situaciones futuras.

### Tabla comparativa

| Tipo de agente | Memoria | Objetivos | Planificacion | Aprendizaje | Ejemplo LLM |
|---|---|---|---|---|---|
| Reactivo simple | No | No | No | No | Clasificador de intenciones |
| Basado en modelo | Si (estado) | No | No | No | Chatbot con historial |
| Basado en objetivos | Si | Si | Si | No | Agente con Plan-and-Execute |
| Basado en utilidad | Si | Si (multiples) | Si | No | Agente con router de modelos |
| Que aprende | Si | Si | Si | Si | Agente con Reflexion + memoria |

La mayoria de los agentes LLM que se construyen hoy caen en la categoria de **agentes basados en objetivos** o **agentes basados en modelo**, dependiendo de si implementan planificacion explicita o simplemente reaccionan al contexto acumulado. Los agentes verdaderamente autonomos con aprendizaje en linea son todavia raros en produccion.

---

## 1.4 BDI: creencias, deseos e intenciones

Hay otra forma de pensar sobre los agentes que viene no de la ingenieria sino de la **filosofia de la mente**. En los anos 80, el filosofo Michael Bratman desarrollo una teoria sobre como los seres humanos razonan y toman decisiones. Los investigadores Anand Rao y Michael Georgeff la adaptaron en 1995 como una arquitectura de software para agentes [Rao y Georgeff, 1995].

La arquitectura **BDI** (Beliefs, Desires, Intentions) propone que un agente racional tiene tres componentes mentales:

### Beliefs (Creencias)

Lo que el agente **cree** que es verdad sobre el mundo. Las creencias pueden ser incorrectas o incompletas; eso es parte del modelo. Un agente BDI no tiene acceso a la verdad absoluta, sino a su mejor aproximacion.

Las creencias se actualizan conforme el agente percibe nueva informacion, pero tambien pueden actualizarse por **inferencia**: si creo que "todos los gatos son mamiferos" y percibo un gato, puedo inferir que es un mamifero sin haberlo verificado directamente.

### Desires (Deseos)

Lo que el agente **quiere** lograr. Los deseos representan estados del mundo que el agente considera deseables. Pueden ser multiples y hasta contradictorios. Un agente puede desear "llegar rapido" y "conducir seguro" al mismo tiempo, aunque a veces estos deseos entren en conflicto.

### Intentions (Intenciones)

Los planes a los que el agente se ha **comprometido**. Las intenciones son el puente entre los deseos y las acciones. De todos sus deseos, el agente selecciona algunos, forma planes para lograrlos y se compromete con esos planes. Las intenciones son estables (no cambian a cada momento) pero revisables (si la situacion cambia lo suficiente, el agente puede abandonar una intencion).

Bratman enfatizo que la distincion entre deseos e intenciones es crucial. Puedo desear ir a Japon y a Italia este verano, pero solo puedo intentar hacer uno de los dos (a menos que tenga tiempo y dinero ilimitados). El acto de **comprometerse** con un plan es lo que convierte un deseo en una intencion.

### BDI en codigo

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class Belief:
    """Una creencia sobre el estado del mundo."""
    subject: str
    predicate: str
    confidence: float = 1.0

    def __str__(self):
        return f"{self.subject} {self.predicate} ({self.confidence:.0%})"


@dataclass
class Desire:
    """Un estado deseado del mundo."""
    description: str
    priority: float = 0.5

    def __str__(self):
        return f"Deseo: {self.description} (prioridad: {self.priority})"


@dataclass
class Intention:
    """Un plan comprometido para lograr un deseo."""
    goal: Desire
    plan: list[str]
    current_step: int = 0
    active: bool = True

    def next_action(self) -> Optional[str]:
        if self.current_step < len(self.plan):
            action = self.plan[self.current_step]
            self.current_step += 1
            return action
        return None


class BDIAgent:
    """Un agente con arquitectura BDI.

    Ciclo: percibir -> actualizar creencias -> deliberar
    (seleccionar deseos) -> planificar (formar intenciones)
    -> ejecutar -> reconsiderar.
    """

    def __init__(self):
        self.beliefs: list[Belief] = []
        self.desires: list[Desire] = []
        self.intentions: list[Intention] = []

    def update_beliefs(self, percept: dict):
        """Actualiza creencias con nueva percepcion."""
        for key, value in percept.items():
            existing = [b for b in self.beliefs if b.subject == key]
            if existing:
                existing[0].predicate = str(value)
            else:
                self.beliefs.append(
                    Belief(subject=key, predicate=str(value))
                )

    def deliberate(self):
        """Selecciona que deseos perseguir (genera intenciones)."""
        sorted_desires = sorted(
            self.desires, key=lambda d: d.priority, reverse=True
        )
        for desire in sorted_desires:
            if not self._already_intending(desire):
                plan = self._plan_for(desire)
                if plan:
                    self.intentions.append(
                        Intention(goal=desire, plan=plan)
                    )

    def execute(self) -> Optional[str]:
        """Ejecuta la siguiente accion de la intencion activa."""
        active = [i for i in self.intentions if i.active]
        if active:
            action = active[0].next_action()
            if action is None:
                active[0].active = False
            return action
        return None

    def reconsider(self):
        """Debo cambiar mis intenciones?

        Esta es la fase mas critica y la que los agentes LLM
        hacen peor: son notoriamente malos para abandonar
        un plan que ya no funciona.
        """
        for intention in self.intentions:
            if intention.active and not self._still_viable(intention):
                intention.active = False

    def _already_intending(self, desire: Desire) -> bool:
        return any(
            i.goal.description == desire.description and i.active
            for i in self.intentions
        )

    def _plan_for(self, desire: Desire) -> Optional[list[str]]:
        """Genera un plan para lograr un deseo."""
        # En un sistema real, aqui iria un planificador
        return [f"paso_para_{desire.description}"]

    def _still_viable(self, intention: Intention) -> bool:
        """Verifica si una intencion sigue siendo alcanzable."""
        return True  # Simplificado
```

### Es un agente LLM un agente BDI?

El mapeo es tentador y productivo como herramienta de diseno, pero tiene diferencias profundas:

| BDI | Agente LLM | Diferencia clave |
|-----|-----------|-----------------|
| **Beliefs** | Ventana de contexto + resultados de herramientas + conocimiento del entrenamiento | En BDI, las creencias persisten entre sesiones. En un LLM, desaparecen cuando el contexto se llena o la sesion termina. |
| **Desires** | Instrucciones del sistema + objetivo del usuario | En BDI, los deseos son estados internos. En un LLM, son instrucciones externas que el modelo "sigue" (simula seguir). El LLM no *desea* completar tu tarea. |
| **Intentions** | Secuencia de tool calls planificada | En BDI, las intenciones son estables pero revisables. Los agentes LLM son notoriamente malos para reconsiderar: tienden a seguir adelante con un plan incluso cuando deberian detenerse y replantear. |

La analogia entre BDI y agentes LLM es util como herramienta de diseno, no como descripcion literal. Cuando disenas un agente, pensar en terminos de "que cree, que desea, que intenta hacer" te ayuda a estructurar el system prompt, las herramientas y los guardrails. Pero no te enganes pensando que tu agente LLM tiene creencias genuinas o deseos autonticos. Es un generador probabilistico de texto que simula extraordinariamente bien el comportamiento de un agente con creencias y deseos.

---

## 1.5 Donde encajan los agentes LLM en todo esto

Con los fundamentos clasicos claros, podemos ahora responder la pregunta mas practica: que es y que *no es* un agente de IA basado en LLMs?

### La definicion convergente

Despues de anos de debate, la comunidad ha convergido en una definicion razonablemente precisa. Simon Willison la articula de forma limpia: un agente es "un LLM que ejecuta herramientas en un loop para lograr un objetivo" [Willison, 2025]. Anthropic, en su guia "Building Effective Agents", distingue entre **workflows** (orquestacion de LLMs con flujos predefinidos) y **agentes verdaderos** (sistemas donde el LLM dirige autonomamente su propio proceso) [Anthropic, 2024].

La definicion que usaremos en este libro combina ambas perspectivas:

> **Un agente de IA es un sistema de software que usa un modelo de lenguaje para percibir informacion, razonar sobre ella, seleccionar autonomamente acciones (incluyendo el uso de herramientas), y ejecutar esas acciones en un loop de retroalimentacion hasta alcanzar un objetivo.**

Tres criterios minimos hacen a un sistema un agente:

1. **Autonomia en la seleccion de acciones**: el sistema decide *que* hacer en cada paso, no sigue un script fijo.
2. **Uso de herramientas**: el sistema puede actuar sobre el mundo (no solo generar texto).
3. **Loop de retroalimentacion**: el sistema observa el resultado de sus acciones y ajusta su comportamiento.

### Que NO es un agente

La definicion se clarifica mirando lo que queda fuera:

**Un chatbot** no es un agente. Un chatbot recibe texto y genera texto. No selecciona acciones autonomamente, no usa herramientas, y no tiene loop de retroalimentacion. Es un pipe: texto entra, texto sale.

**Un pipeline de RAG** no es un agente. Un sistema que busca documentos, los inyecta en un prompt y genera una respuesta esta siguiendo un flujo fijo: buscar -> inyectar -> generar. No hay autonomia en la seleccion de acciones. Es un workflow, no un agente.

**Un wrapper de API** no es un agente. Llamar a un LLM con un system prompt bonito no lo convierte en un agente. Si el flujo es siempre el mismo (usuario pregunta -> LLM responde -> fin), no hay loop ni autonomia.

**Un workflow con LLMs** no es un agente (generalmente). Una cadena de LLMs donde el output de uno es el input de otro es un pipeline. Puede ser sofisticado y util, pero si el flujo esta predefinido, no es un agente. Es la distincion que Anthropic hace entre workflows y agentes.

La frontera no siempre es nitida. Un sistema de RAG que *decide autonomamente* si necesita buscar mas documentos y *elige* que consultas hacer podria calificar como agente. Lo que importa no es la etiqueta, sino la presencia de los tres criterios: autonomia, herramientas y retroalimentacion.

### El mapeo clasico -> moderno

Para cerrar el circulo, mapeemos los conceptos clasicos a sus equivalentes en agentes LLM:

| Concepto clasico | Equivalente en agente LLM |
|---|---|
| Sensor | Prompt del usuario, resultados de herramientas, contexto del sistema |
| Actuador | Tool calls (function calling), generacion de texto, ejecucion de codigo |
| Funcion del agente | El LLM + su system prompt + la logica del loop |
| Estado interno | Ventana de contexto (working memory) + memoria persistente (si existe) |
| Medida de rendimiento | Evals: metricas automatizadas de calidad |
| Ambiente | El conjunto de APIs, datos, usuarios y restricciones con los que interactua |
| PEAS - Performance | Evals, KPIs del sistema, SLAs |
| PEAS - Environment | APIs disponibles, datos accesibles, tipo de usuarios, restricciones legales |
| PEAS - Actuators | Herramientas registradas en el agente |
| PEAS - Sensors | Inputs: prompt, tool results, datos de contexto |

### Checklist: Es tu sistema realmente un agente?

Usa esta lista para evaluar si lo que estas construyendo es un agente o algo mas simple (que no tiene nada de malo):

- [ ] **Seleccion autonoma de acciones**: El sistema decide que hacer en cada paso sin un flujo predefinido?
- [ ] **Uso de herramientas**: El sistema puede ejecutar acciones que afectan al mundo (APIs, bases de datos, archivos)?
- [ ] **Loop de retroalimentacion**: El sistema observa el resultado de sus acciones y ajusta su comportamiento?
- [ ] **Condicion de terminacion**: El sistema decide cuando ha terminado (no un flujo fijo de N pasos)?
- [ ] **Multiples caminos posibles**: Ante la misma entrada, el sistema podria tomar caminos diferentes dependiendo del contexto?

Si marcaste todos los puntos, tienes un agente. Si no, probablemente tienes un workflow o un chatbot --y eso esta perfectamente bien. No todo necesita ser un agente. De hecho, como veremos a lo largo de este libro, **la mayoria de los sistemas deberian empezar como workflows y evolucionar a agentes solo cuando la complejidad lo justifique**.

---

## Takeaway del capitulo

Un agente no es magia. Es un sistema que percibe, razona y actua. Las definiciones de Russell y Norvig de hace 30 anos siguen siendo la mejor base para disenar agentes hoy. El marco PEAS te obliga a pensar con claridad sobre lo que estas construyendo antes de escribir una sola linea de codigo. La arquitectura BDI te da un vocabulario para pensar en las "creencias", "deseos" e "intenciones" de tu agente, aunque sean simulados.

Antes de construir tu proximo agente, define PEAS. Si no puedes llenar los cuatro campos con precision, no estas listo para escribir codigo. Y si lo que necesitas es un chatbot o un pipeline de RAG, construye eso. No todo problema requiere un agente, y forzar una solucion agentica donde no se necesita es la forma mas segura de acabar en el Capitulo 0.

En el proximo capitulo exploraremos como "razonan" los LLMs que estan en el corazon de estos agentes. Entender los limites de ese razonamiento es fundamental para disenar agentes que funcionen cuando las consecuencias son reales.

---

### Notas y referencias

- [Russell y Norvig, 2020] Stuart Russell, Peter Norvig. *Artificial Intelligence: A Modern Approach*, 4th Ed. Pearson. Capitulo 2: Intelligent Agents.
- [Rao y Georgeff, 1995] Anand S. Rao, Michael P. Georgeff. "BDI Agents: From Theory to Practice." Proceedings of the First International Conference on Multi-Agent Systems (ICMAS-95).
- [Bratman, 1987] Michael E. Bratman. *Intention, Plans, and Practical Reason*. Harvard University Press.
- [Anthropic, 2024] "Building Effective Agents." Anthropic Research, diciembre 2024.
- [Willison, 2025] Simon Willison. "I think 'agent' may finally have a widely enough agreed upon definition."
- [Weng, 2023] Lilian Weng. "LLM Powered Autonomous Agents." OpenAI Blog, junio 2023.
- [Huyen, 2025] Chip Huyen. "Agents." Enero 2025. Adaptado de *AI Engineering* (O'Reilly).
- [Shankar et al., 2025] "Measuring Agents in Production." 306 practicantes encuestados: 68% de agentes ejecutan maximo 10 pasos; 70% usan prompting sobre fine-tuning.
