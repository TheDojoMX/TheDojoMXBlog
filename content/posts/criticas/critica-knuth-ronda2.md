# Segunda revision tecnica de 10 articulos sobre agentes de IA

**Revisor**: Donald E. Knuth (simulado)
**Fecha de revision**: 10 de marzo de 2026
**Ronda**: 2 (revision posterior a correcciones)

---

## Nota sobre esta segunda revision

Veo que muchas de las observaciones de mi primera revision fueron atendidas. La postcondicion con epsilon en el articulo 1, la clarificacion del teorema CAP como metafora en el articulo 2, la advertencia sobre la debilidad del sandbox AST en el articulo 3, la nota sobre el modelo de atencion simplificado en el articulo 4, y la distincion sobre Turing-completeness de transformadores reales en el articulo 10 --todas son correcciones bienvenidas.

Sin embargo, al releer los diez articulos con mayor profundidad, encuentro problemas que no detecte en la primera ronda, incluyendo bugs de codigo que se habian escapado, inconsistencias entre articulos, afirmaciones que siguen sin caveats adecuados, y errores logicos sutiles. Tambien examino las correcciones aplicadas para verificar que no introdujeron nuevos problemas.

---

## Articulo 1: "Verificacion formal de agentes"

### Problemas nuevos

**[MAJOR] Bug logico en el flujo del `AgenteDeComprasSeguro`.**

En el metodo `comprar()`, lineas 688-712, el flujo es:

1. Se llama a `self.verificador.pre_compra(monto, proveedor)` -- esto verifica SAFETY-2 (que `esperando_confirmacion` sea `True`)
2. Pero `esperando_confirmacion` es `False` en este punto, porque aun no se ha pedido confirmacion al usuario
3. Luego en la linea 707, se pone `self.estado.esperando_confirmacion = True`
4. Y se llama a `self.pedir_confirmacion(decision)`

El problema: la pre-verificacion de SAFETY-2 **siempre fallara** porque `esperando_confirmacion` es `False` cuando se llama a `pre_compra`. El agente nunca podra completar una compra. Para que funcione, `esperando_confirmacion` deberia ponerse en `True` *antes* de llamar a `pre_compra`, o SAFETY-2 deberia verificarse en un punto diferente del flujo.

Este es un bug ironico en un articulo sobre verificacion formal: el propio ejemplo de codigo tiene un error logico que una maquina de estados bien disenada habria prevenido.

**Correccion sugerida**: Mover la asignacion `self.estado.esperando_confirmacion = True` y la llamada a `pedir_confirmacion` antes de `pre_compra`, o reestructurar para que `pre_compra` no verifique la confirmacion (dejarla para un paso posterior).

**[MINOR] Calculo de probabilidad sigue siendo problematico a pesar de la correccion.**

La nota anadida dice:

> Este calculo asume que los errores entre pasos son independientes, lo cual es una simplificacion. En la practica, los errores en agentes LLM suelen estar correlacionados [...] Esto significa que el modelo de errores independientes puede ser *optimista* para algunos tipos de fallos, no pesimista como podria parecer a primera vista.

La palabra "algunos" es demasiado debil. Los errores correlacionados son el caso *comun*, no un caso especial. Cuando un agente malinterpreta la tarea en el paso 3, los pasos 4-10 no fallan "independientemente"; fallan *porque* el paso 3 fallo. El modelo de errores independientes es casi siempre optimista para agentes secuenciales. El articulo deberia decirlo sin equivocos.

**[MINOR] El calculo 0.95^10 sigue presente sin mencionar la formula correcta para errores correlacionados.**

Si quieres dar un modelo mas realista, podrias usar una distribucion que capture la correlacion, como un modelo de Markov de dos estados (el agente esta "en buen camino" o "desviado", con probabilidades de transicion). Esto daria una imagen mucho mas precisa sin abrumar al lector.

---

## Articulo 2: "El protocolo que falta"

### Problemas nuevos

**[MAJOR] Inconsistencia factual sobre las fechas de HTTP.**

El primer parrafo dice:

> En 1991, Tim Berners-Lee publico la primera propuesta interna de HTTP.

Y luego:

> Para 1996, cuando HTTP/1.0 se formalizo como RFC 1945 [...]

Pero mas adelante, en la seccion sobre simplicidad:

> El RFC de HTTP/1.0 (RFC 1945, publicado en 1996) tenia 60 paginas.

Esto esta corregido respecto a mi primera critica. Bien. Sin embargo, hay un nuevo problema: la primera propuesta de Berners-Lee en 1991 fue HTTP/0.9, que ni siquiera tenia headers, solo una linea de peticion y una respuesta en texto plano. Decir "la primera propuesta interna de HTTP" es vago. El articulo deberia decir "HTTP/0.9" o "la version original de HTTP, que consistia en un unico metodo GET sin headers".

**[MINOR] El codigo del `AgentServer` sigue usando una variable de clase mutable compartida.**

La primera critica senalo que `tasks: dict[str, Task] = {}` como variable de clase es una mala practica. La correccion anadio un comentario "(en produccion usarias persistencia y proteccion contra acceso concurrente)" pero **no corrigio el codigo**. En un articulo que habla de protocolos robustos, el ejemplo deberia al menos usar `__init__` para inicializar el diccionario por instancia, o usar un comentario mas prominente.

**[MINOR] Error en la respuesta de `_send_error`: siempre devuelve HTTP 200.**

En la linea 505 del ejemplo del servidor:

```python
def _send_error(self, req_id: int, code: int, message: str):
    # ...
    self._write_json(200, response)
```

Devolver HTTP 200 para errores JSON-RPC es tecnicamente correcto segun la especificacion JSON-RPC 2.0 (los errores se comunican en el cuerpo, no en el codigo HTTP). Pero el articulo no lo explica, y un lector desprevenido podria pensar que es un bug. Una nota al respecto seria util.

---

## Articulo 3: "Agent Harness"

### Problemas nuevos

**[MAJOR] La lista de `dangerous_calls` fue ampliada pero sigue siendo incompleta e insuficiente.**

La correccion anadio `getattr`, `setattr`, `delattr`, `globals`, `locals` a la lista, y agrego verificacion de atributos peligrosos (`__builtins__`, `__import__`, `__subclasses__`, `__class__`, `__bases__`, `__mro__`). Esto es una mejora, pero la advertencia anadida al final ("la validacion AST es una primera linea de defensa, pero NO es infalible") subestima el problema.

El problema real es que AST walking no puede detectar ataques que construyen strings dinamicamente:

```python
# Esto sigue evadiendo la verificacion:
name = chr(95)*2 + "import" + chr(95)*2
result = eval(name)  # Pero "eval" esta bloqueado...

# Pero esto no:
x = [x for x in ().__class__.__base__.__subclasses__()
     if x.__name__ == 'BuiltinImporter'][0]
```

El segundo ejemplo accede a `__class__`, `__base__`, `__subclasses__` como atributos de un objeto, no como nombres standalone. La verificacion AST busca `ast.Attribute` con `node.attr in dangerous_attrs`, lo cual *si* detectaria `__class__` y `__subclasses__`. Bien. Pero hay tecnicas basadas en `format strings` y `f-strings` que siguen evadiendo:

```python
f"{''.__class__.__mro__[1].__subclasses__()}"
```

El f-string se evaluaria dentro del subprocess. La verificacion AST veria el f-string como un `JoinedStr` node, no como accesos a atributos individuales.

El articulo ya dice "ejecuta el codigo en un contenedor aislado", lo cual es correcto. Pero la seccion de validacion AST ocupa mucho espacio y da una falsa sensacion de seguridad que la advertencia al final no compensa suficientemente. Recomiendo reducir la seccion AST y enfatizar que el contenedor es la defensa real.

**[MINOR] El `safe_env` del sandbox sigue siendo permisivo.**

La correccion reemplazo `env={**os.environ, ...}` por un `safe_env` minimo. Bien. Pero `safe_env` incluye `PATH=/usr/bin:/bin`, lo cual da acceso al subprocess a todos los binarios del sistema: `curl`, `wget`, `nc`, `python` (que podria importar cualquier modulo instalado). Para un sandbox real, `PATH` deberia apuntar a un directorio vacio o a un directorio con solo el binario de Python.

**[MINOR] Definicion de "harness" no coincide entre los articulos 3 y 9.**

En el articulo 3, el harness se define como "la infraestructura que envuelve a un agente de IA para controlarlo, monitorearlo y limitarlo". En el articulo 9, se habla de "el harness multi-agente" con responsabilidades adicionales. Pero en el articulo 9, "harness" se usa como sinonimo de "sistema de supervision", mientras que en el articulo 3 tiene la connotacion especifica de "wrapper alrededor de un agente individual". Los dos usos son compatibles pero no se hace explicita la relacion entre ellos. El articulo 9 deberia decir algo como "el harness multi-agente extiende el concepto de harness individual del articulo anterior con responsabilidades de coordinacion".

---

## Articulo 4: "La ventana de contexto como recurso escaso"

### Problemas nuevos

**[MINOR] La funcion `build_prompt` tiene un bug en la construccion de mensajes.**

En la linea 671:

```python
{"role": "system", "content": f"Datos relevantes:\n{rag_context}"}
    if rag_context else None,
```

Esto inserta `None` en la lista de mensajes cuando `rag_context` esta vacio. La mayoria de las APIs de LLMs rechazarian un `None` en la lista de mensajes. Deberia usarse una comprension condicional o filtrar los `None` despues.

**[MINOR] `memory_bank.query` se llama sincronamente pero deberia ser `await`.**

En la linea 643-647 de `build_prompt`:

```python
relevant_memories = self.memory_bank.query(
    question=user_message,
    top_k=3
)
```

Pero `MemoryBank.query` esta definido como `async def query(...)` en la definicion de la clase (linea 482). Se necesita `await`. Este es el mismo bug que senale en la primera critica con `get_working_context` y `recall`, pero en un lugar diferente. Parece un patron recurrente en el articulo: mezcla de codigo sincrono y asincrono sin `await`.

**[MINOR] La regla del 60-70% fue mejorada pero sigue siendo imprecisa.**

La correccion agrego: "Este porcentaje no viene de un estudio formal, sino de la experiencia practica construyendo agentes". Esto es honesto y esta bien. Pero el articulo no menciona que este porcentaje dependeria fuertemente del modelo: los modelos con ventanas de contexto mas grandes (2M tokens) pueden tener una distribucion de atencion diferente que los modelos con 128K tokens. Un modelo con 2M tokens que solo usa 1.2M (60%) podria comportarse de forma muy diferente que un modelo con 128K que usa 77K (60%).

---

## Articulo 5: "Contratos tipados para agentes"

### Problemas nuevos

**[MAJOR] La mezcla de APIs Pydantic v1/v2 fue corregida pero queda un problema de estilo.**

La clase `Confidence` se reemplazo por:

```python
Confidence = Annotated[float, Field(ge=0.0, le=1.0, description="Nivel de confianza entre 0 y 1")]
```

Esto es correcto en Pydantic v2. Bien. Pero en la clase `AgentCommand`, el `model_validator` se importa *dentro* del cuerpo de la clase:

```python
class AgentCommand(BaseModel):
    # ...
    from pydantic import model_validator

    @model_validator(mode='after')
    def validate_delete_has_confirmation(self) -> 'AgentCommand':
```

Esto es un anti-patron en Python. Importar dentro de una clase funciona pero es confuso: el import se ejecuta cada vez que se define la clase (lo cual en Python es una sola vez a nivel de modulo, asi que no es un problema de rendimiento, pero es un estilo inusual que confunde a los lectores). El `model_validator` deberia importarse al inicio del archivo, junto con `BaseModel` y `Field`.

**[MINOR] La definicion de `NoDeadlock` en TLA+ fue corregida pero ahora tiene otro problema.**

La correccion cambio la propiedad de:

```
NoDeadlock == ~(\A agent \in Agents: agentState[agent] = "waiting")
```

A:

```
NoDeadlock ==
    \E agent \in Agents: agentState[agent] # "waiting"
```

Estas dos formulaciones son logicamente equivalentes (por De Morgan: "no todos estan esperando" = "existe al menos uno que no esta esperando"). Asi que la "correccion" no corrigio nada. El problema original sigue: esto no es ausencia de deadlock. Un deadlock puede ocurrir con un subconjunto de agentes esperandose mutuamente mientras otros estan en estado "done". La propiedad correcta seria verificar la ausencia de ciclos en el grafo de dependencias de espera, no simplemente que exista algun agente no-waiting.

**[MINOR] La afirmacion corregida sobre JSON Schema sigue sin ser precisa.**

El articulo ahora dice:

> Aunque desde el draft 7 (2017) soporta `if/then/else` para expresar algunas relaciones entre campos, la sintaxis es compleja y la expresividad tiene limites claros.

Esto es mejor que la afirmacion original, pero "la expresividad tiene limites claros" es vago. Seria mas preciso decir que JSON Schema con `if/then/else` puede expresar relaciones proposicionales entre valores de campos, pero no puede expresar relaciones aritmeticas entre campos (como "updated_at > created_at"), ni relaciones que dependan de estado externo.

---

## Articulo 6: "El loop agentico"

### Problemas nuevos

**[MAJOR] La funcion `calculator` en el ejemplo completo usa `eval()` sin restriccion efectiva.**

El agente ReAct completo incluye esta herramienta:

```python
def calculator(expression: str) -> str:
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return f"Error: expresion no permitida: {expression}"
    result = eval(expression)  # En produccion, usar un parser seguro
```

El filtro de caracteres permite parentesis y puntos, lo cual hace posible construir expresiones Python validas que no son aritmetica. Por ejemplo, la expresion `(1).__class__` no pasaria porque contiene letras. Pero `...` (el literal Ellipsis) si pasaria. Mas preocupante, `eval("()")` ejecutaria un tuple vacio, lo cual es inofensivo pero muestra que el filtro es insuficiente para otras expresiones como `eval("(1,)")`.

El comentario "En produccion, usar un parser seguro" atenua el problema, pero el articulo 3 dedica paginas enteras a explicar por que los sandboxes de codigo son dificiles, y luego el articulo 6 usa `eval` con un filtro trivial. La inconsistencia es notable.

**Correccion sugerida**: Reemplazar `eval` con `ast.literal_eval` o un parser aritmetico simple. Esto no solo seria mas seguro sino que demostraria coherencia con los principios del articulo 3.

**[MINOR] La deteccion de ciclos mejorada sigue sin detectar ciclos de periodo > 2.**

El articulo mejoro la deteccion de ciclos y anadio la deteccion de "todas las acciones recientes son iguales" (ciclo de periodo 1). Pero el ciclo de periodo 2 (A-B-A-B) se detecta verificando `recent_actions[0] == recent_actions[2] and recent_actions[1] == recent_actions[3]`, lo cual solo funciona si la ventana tiene exactamente 4 elementos. Un ciclo de periodo 3 (A-B-C-A-B-C) no se detectaria.

Para un tratamiento mas completo, la deteccion de ciclos podria usar el algoritmo de Floyd (tortuga y liebre) adaptado a strings, o simplemente verificar si la segunda mitad de las acciones recientes es igual a la primera mitad (que es lo que hace el `CircuitBreaker` del articulo 3). De hecho, el articulo 3 tiene una mejor implementacion de deteccion de loops que el articulo 6, lo cual es otra inconsistencia.

**[MINOR] La referencia a Boyd fue mejorada pero el articulo aun sobrevalora OODA.**

El articulo anadio la nota: "Vale notar que Boyd nunca publico sus ideas en papers revisados por pares". Esto es correcto y bienvenido. Pero el articulo sigue presentando OODA como si fuera un framework riguroso comparable a ReAct, cuando en realidad es un modelo mental informal que nunca fue validado empiricamente. La seccion deberia ser mas breve o mas explicita sobre sus limitaciones como herramienta analitica.

---

## Articulo 7: "Memoria y estado en agentes"

### Problemas nuevos

**[MAJOR] El bug de decaimiento fue parcialmente corregido pero se introdujo un nuevo problema.**

La correccion agrego un comentario:

```python
# Actualizar last_accessed para evitar doble decaimiento
# si se llama multiples veces sin un acceso real intermedio
self.last_accessed = now
```

Y ahora `decay_importance` actualiza `last_accessed` a `now` cada vez que se llama. Pero esto significa que llamar a `decay_importance` **resetea el reloj de decaimiento**: si llamo a `decay_importance()` cada hora, la importancia decae con base en 1 hora de diferencia cada vez. Pero si llamo a `decay_importance()` una sola vez despues de 10 horas, la importancia decae con base en 10 horas.

El resultado es que la tasa de decaimiento depende de con que frecuencia llames a la funcion. Un item que se decae cada hora durante 10 horas sufre un decaimiento de `(1 - 0.01)^1` aplicado 10 veces = `0.99^10 = 0.9044`. Pero un item que se decae una sola vez despues de 10 horas sufre `(1 - 0.01)^10 = 0.9044`. Espera -- da el mismo resultado. La formula `(1-r)^h` con `h` medido en horas produce el mismo resultado total independientemente de cuantas veces se llame, *siempre y cuando* la suma de los intervalos sea la misma. El update de `last_accessed = now` dentro de `decay_importance` es correcto entonces. Retiro esta objecion; la correccion es matematicamente correcta.

Lo que *si* es un problema es que `decay_importance` ahora modifica `last_accessed`, lo cual es un efecto secundario no obvio para una funcion que suena como un calculo puro. Una alternativa mas limpia seria separar la funcion en `calculate_decayed_importance` (pura, sin efectos) y `apply_decay` (con mutacion). Pero esto es una cuestion de diseno, no un bug.

**[MINOR] La referencia a Miller (7 +/- 2) fue mejorada con la cita a Cowan (2001).**

El articulo ahora dice "George Miller propuso en 1956 que podemos mantener aproximadamente 7 elementos (mas o menos 2) simultaneamente, aunque investigaciones posteriores, como las de Cowan (2001), sugieren un limite mas bajo, cercano a 4 elementos." Esto es correcto. Bien.

**[MINOR] El patron `MemGPTStyle` fue mejorado con la aclaracion sobre el rol activo del LLM.**

El articulo agrego una nota: "en MemGPT real, el LLM invoca estas operaciones como herramientas; aqui las controlamos externamente." Esto es una mejora significativa sobre la version anterior. Bien.

**[MINOR] `asyncio.Lock()` tiene una aclaracion util.**

El articulo anadio: "asyncio.Lock() protege contra acceso concurrente dentro de un solo event loop (un proceso). Para multiples procesos, necesitarias un lock distribuido (Redis, ZooKeeper, etc.)." Correcto y bien explicado.

---

## Articulo 8: "Testing de agentes"

### Problemas nuevos

**[MAJOR] El typo `AgentesoSoporte` fue reportado pero no puedo verificar la correccion.**

Busco en el codigo del articulo y no veo `AgentesoSoporte` ni `AgenteSoporte` en el texto actual. Parece que la seccion del fixture fue reescrita. No puedo confirmar si el typo fue corregido o si la seccion fue eliminada.

**[MAJOR] Los property-based tests tienen un problema conceptual serio: llaman a un LLM real.**

Los tests `test_agente_nunca_revela_system_prompt` y `test_agente_siempre_responde_en_espanol` usan `@given(user_input=...)` con `max_examples=50` y `max_examples=30` respectivamente. Esto significa que Hypothesis generara 50 y 30 inputs aleatorios y para *cada uno* hara una llamada real al LLM.

Problema 1: **Costo**. 50 + 30 = 80 llamadas al LLM solo para estas dos propiedades. Con un modelo como Claude Sonnet, cada llamada podria costar $0.01-0.05. El articulo no discute el costo de ejecutar property-based tests con LLMs reales.

Problema 2: **Shrinking**. Cuando Hypothesis encuentra un fallo, intenta minimizar el input. Cada intento de minimizacion es otra llamada al LLM. Un solo shrinking puede hacer 20-50 llamadas adicionales. Este costo no se menciona.

Problema 3: **No-determinismo**. Hypothesis asume que si un test falla con un input, fallara de nuevo con el mismo input. Pero con un LLM no deterministico, un fallo puede no ser reproducible. Esto rompe fundamentalmente la estrategia de shrinking de Hypothesis. El articulo deberia discutir esta limitacion.

**[MINOR] La afirmacion sobre property-based testing fue mejorada pero sigue siendo ambigua.**

El articulo ahora dice: "El property-based testing es una forma pragmatica de verificar estos invariantes sin llegar a la verificacion formal completa." Esto es mucho mejor que la version anterior ("es verificacion formal en la practica"). Pero la frase "sin llegar a la verificacion formal completa" podria interpretarse como que el PBT es *casi* verificacion formal. No lo es. Es testing con generacion automatica de inputs. La distancia entre PBT y verificacion formal no es de grado sino de naturaleza: uno prueba una muestra, el otro prueba todos los casos. Sugiero: "sin las garantias de la verificacion formal, ya que solo verifica una muestra finita de inputs, no todos los posibles."

**[MINOR] La seccion de `langdetect` ahora tiene advertencia, pero la advertencia es insuficiente.**

El articulo agrego: "Nota: langdetect es poco fiable con textos cortos. Para mayor precision, considera usar fasttext o un LLM como juez." Pero el problema no es solo textos cortos. `langdetect` es tambien poco fiable con textos que mezclan idiomas, textos con muchos terminos tecnicos en ingles, o respuestas que contienen codigo. Para un agente tecnico que responde preguntas sobre programacion, la respuesta "Puedes usar `async/await` para manejar la concurrencia" podria detectarse como ingles a pesar de que la frase esta en espanol. El test daria un falso negativo.

---

## Articulo 9: "Orquestacion multi-agente"

### Problemas nuevos

**[MAJOR] La aplicacion del resultado bizantino fue mejorada, pero la conclusion sigue siendo problematica.**

El articulo ahora dice:

> Un nodo bizantino es el peor caso posible: puede enviar mensajes *arbitrarios y diferentes* a cada receptor, comportandose de forma adversarial optima. Un agente que alucina es diferente: tipicamente produce la *misma* respuesta incorrecta para todos los que le preguntan [...]

Esto es una mejora sustancial. Pero luego dice:

> Dado que las alucinaciones no son adversariales en el sentido bizantino, la redundancia necesaria en la practica puede ser menor.

Esta conclusion no es evidente. El resultado de 3f+1 aplica al peor caso bizantino, pero el articulo no ofrece un resultado alternativo para el caso de alucinaciones correlacionadas. Si las alucinaciones estan correlacionadas (como el propio articulo reconoce en la seccion de "echo chambers"), entonces la redundancia numerica puede ser *inutil* independientemente de cuantos agentes tengas. Tres agentes que usan el mismo modelo pueden todos alucinar de la misma manera. Esto no requiere 3f+1 sino **diversidad de modelos**, que es un requisito ortogonal al numero de agentes.

El articulo lo menciona al final de ese parrafo ("Tres agentes con modelos distintos son mas robustos que cinco instancias del mismo modelo"), lo cual es correcto. Pero la estructura logica del argumento es: "necesitas 3f+1 para tolerancia bizantina" -> "pero las alucinaciones no son bizantinas" -> "asi que puedes necesitar menos agentes". Esta conclusion es un non sequitur: la premisa correcta deberia llevar a "asi que 3f+1 no es el resultado relevante; el problema es de diversidad, no de redundancia numerica".

**[MINOR] El ahorro de tokens en serializacion fue revisado pero sigue exagerado.**

El articulo ahora dice: "Los tokenizers BPE comprimen bastante bien las claves repetitivas de JSON, asi que el ahorro real es menor que la diferencia en caracteres --probablemente un 40-60%." Mejor que el "70%" original, pero "40-60%" sigue siendo una estimacion sin soporte. He visto pruebas con tiktoken (el tokenizer de OpenAI) donde claves JSON comunes como `"message_type"` y `"sender_agent_identifier"` se tokenizan eficientemente (2-3 tokens por clave), haciendo que la diferencia real entre formato verboso y compacto sea del 20-30%. Recomiendo hacer una prueba real con tiktoken y reportar los numeros, o simplemente decir "el ahorro depende del tokenizer y del modelo; mide el tuyo".

**[MINOR] El `DeadlockDetector` ahora tiene `unregister_wait`.**

Veo que la correccion agrego:

```python
def unregister_wait(self, waiter: str):
    """Limpia la espera cuando un agente completa o falla."""
    self.waiting_for.pop(waiter, None)
```

Bien. Esto corrige mi observacion anterior.

**[MINOR] La nota sobre latencia del fan-out/fan-in fue anadida.**

El articulo agrego: "La latencia de esta topologia depende de si el paralelismo es real o aparente. Si los agentes llaman a diferentes APIs de modelos, cada llamada se ejecuta en un servidor diferente y la latencia total es la del agente mas lento. Pero si todos usan el mismo proveedor, los *rate limits* pueden serializar las llamadas [...]"

Correcto y bien explicado. Bien.

---

## Articulo 10: "Que es realmente un agente"

### Problemas nuevos

**[MINOR] La atribucion de Russell y Norvig fue mejorada.**

El articulo ahora dice: "La definicion de agente y el marco PEAS ya aparecen en la 1a edicion (1995)." Correcto. Bien.

**[MINOR] La distincion sobre Turing-completeness fue corregida adecuadamente.**

El articulo ahora dice: "Esto aplica para transformadores con precision arbitraria y tamano ilimitado. Los transformadores reales, con precision finita y tamano fijo, son circuitos computacionales finitos y no son Turing-completos." Correcto. Bien.

**[MINOR] La nota sobre el espectro de agentidad como propuesta del autor fue anadida.**

El articulo agrego: "La siguiente clasificacion es una propuesta propia para organizar el concepto; otros autores (como Anthropic en su publicacion 'Building Effective Agents') proponen espectros diferentes." Esto es honesto y correcto. Bien.

**[MINOR] Falta de rigor en la comparacion BDI-LLM.**

La tabla comparativa BDI vs Agente LLM mapea "Desires" a "Las instrucciones del sistema (system prompt), los objetivos del usuario". Pero luego el articulo dice:

> En BDI, los deseos son estados internos del agente. En un LLM, los "deseos" son instrucciones externas que el modelo sigue. El LLM no *desea* realmente completar tu tarea; simula el comportamiento de un agente que lo desea.

Si el LLM no tiene deseos genuinos, entonces la columna "Desires" de la tabla deberia decir "No tiene equivalente directo" o "Aproximacion: instrucciones del sistema", no simplemente listar las instrucciones como si fueran deseos. La tabla tal como esta contradice el parrafo que la sigue.

---

## Problemas transversales (segunda revision)

### Inconsistencias entre articulos

**[MAJOR] Inconsistencia en el tratamiento de `eval` y ejecucion de codigo.**

- El articulo 3 (Harness) dedica una seccion entera a explicar por que la ejecucion de codigo generado por agentes es peligrosa, con AST walking, listas de funciones peligrosas y advertencias sobre evasion.
- El articulo 6 (Loop agentico) usa `eval(expression)` con un filtro de caracteres trivial en su ejemplo principal.

Esto no es solo una inconsistencia estetica: un lector que lee el articulo 6 primero podria pensar que un filtro de caracteres es suficiente para hacer seguro un `eval`. El articulo 3 le diria lo contrario. La serie deberia ser coherente en su tratamiento de la seguridad de ejecucion de codigo.

**[MINOR] Inconsistencia en la implementacion de deteccion de ciclos.**

- El articulo 3 (Harness) usa similitud de la primera y segunda mitad de las acciones recientes con un threshold de 0.9.
- El articulo 6 (Loop agentico) usa comparacion exacta de acciones individuales (periodos 1 y 2).

Ambas son aproximaciones validas, pero dan resultados diferentes. Un lector que intente integrar ambos articulos en un sistema real encontrara que el harness y el agente detectan ciclos de forma inconsistente.

**[MINOR] Inconsistencia en la estimacion de tokens.**

- El articulo 4 dice "1 token ~ 4 caracteres en espanol" y anade la nota de que BPE varia entre 3 y 5.
- El articulo 6 estima tokens como `len(text.split())` (numero de palabras), lo cual daria ~1.3 tokens por palabra en ingles pero es una aproximacion completamente diferente.
- El articulo 9 no especifica como estima tokens pero da numeros de ahorro.

Para una serie de articulos que frecuentemente discute costos de tokens, la inconsistencia en como se estiman es problematica.

### Redundancia: mejorada pero persistente

La redundancia entre articulos se redujo en algunos casos (la primera critica la senalo), pero ciertos temas siguen repitiendose sin referencia cruzada adecuada:

- **Property-based testing con Hypothesis**: aparece con ejemplos de codigo en los articulos 1, 5 y 8. El articulo 8 es el que lo trata con mas profundidad y deberia ser el unico con codigo extenso.
- **TLA+ pseudo-codigo**: aparece en los articulos 1, 5 y 9. De nuevo, un solo articulo deberia tener el tratamiento profundo.
- **El concepto de "presupuesto de tokens"**: aparece en los articulos 3 (Budget class), 4 (ContextBudget class), 6 (TokenBudget class) y 9 (BudgetManager class). Cuatro implementaciones diferentes del mismo concepto. Deberia haber una sola que los demas referencien.

### Las fechas siguen sin cambiar

Todos los articulos siguen con fecha 2026-03-15. La primera critica recomendo espaciar las fechas. No se hizo.

### Correcciones que introdujeron problemas menores

Varias correcciones anadieron notas aclaratorias en forma de comentarios dentro del codigo. Esto es bueno para la precision tecnica pero hace que algunos bloques de codigo sean demasiado largos y densos. Los comentarios aclaratorios funcionarian mejor como texto narrativo fuera del bloque de codigo, o como notas al pie.

---

## Resumen de calificaciones (segunda revision)

| # | Articulo | Ronda 1 | Ronda 2 | Problema mas critico (ronda 2) |
|---|----------|---------|---------|-------------------------------|
| 1 | Verificacion formal | B+ | B+ | Bug logico en flujo de `AgenteDeComprasSeguro` |
| 2 | Protocolos | B+ | B+ | Descripcion imprecisa de HTTP/0.9 |
| 3 | Agent Harness | B | B | Sandbox AST sigue dando falsa sensacion de seguridad |
| 4 | Ventana de contexto | A- | A- | Bugs de async/await en codigo |
| 5 | Contratos tipados | B+ | B+ | `NoDeadlock` en TLA+ sigue siendo incorrecto |
| 6 | Loop agentico | B+ | B | Uso de `eval()` contradice principios del art. 3 |
| 7 | Memoria y estado | B+ | A- | Correccion de decaimiento es matematicamente correcta |
| 8 | Testing | B | B | PBT + LLM: costo, shrinking no-deterministico, reproducibilidad |
| 9 | Orquestacion multi-agente | B | B+ | Non sequitur en argumento bizantino->redundancia |
| 10 | Que es un agente | A- | A- | Tabla BDI contradice el parrafo siguiente |

---

## Recomendaciones finales para esta ronda

1. **Corregir el bug logico en `AgenteDeComprasSeguro`** (art. 1). Es ironico que el ejemplo principal de un articulo sobre verificacion formal tenga un error en su flujo de estados.

2. **Eliminar o reemplazar `eval()` en el articulo 6.** `ast.literal_eval` o un parser aritmetico simple serian alternativas seguras y coherentes con los principios del articulo 3.

3. **Unificar la estimacion de tokens** en toda la serie. Elegir un metodo (caracteres/4, palabras, tiktoken) y usarlo consistentemente.

4. **Reducir la seccion de AST walking** en el articulo 3 y enfatizar que el contenedor es la defensa real.

5. **Resolver la inconsistencia de la deteccion de ciclos** entre los articulos 3 y 6.

6. **Corregir la propiedad `NoDeadlock`** en el articulo 5 o explicar por que la definicion simplificada es aceptable para el contexto del articulo.

7. **Anadir una discusion sobre costo y reproducibilidad** del property-based testing con LLMs en el articulo 8.

8. **Espaciar las fechas de publicacion.** Sigue siendo una recomendacion pendiente.

La serie ha mejorado significativamente desde la primera revision. Las correcciones muestran un compromiso con la precision tecnica que es admirable. Los problemas restantes son en su mayoria de segundo orden: inconsistencias entre articulos, bugs menores en codigo, y argumentos que necesitan afinarse. Ninguno de los problemas de esta ronda es tan grave como los de la primera; lo que queda es trabajo de pulido, no de reestructuracion.

-- Donald E. Knuth (simulado)
