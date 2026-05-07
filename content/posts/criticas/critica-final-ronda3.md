# Critica final (ronda 3): 10 articulos sobre agentes de IA

**Revisor**: Editor final de consistencia y pulido
**Fecha**: 10 de marzo de 2026
**Ronda**: 3 (revision final posterior a dos rondas de correcciones)
**Enfoque**: Consistencia terminologica, flujo de serie, bugs de codigo residuales, referencias huerfanas, tono, frontmatter, calidad de escritura final.

---

## Nota sobre esta tercera revision

Las dos rondas anteriores (Knuth: precision tecnica; Zinsser/King: estilo editorial; Practitioner: perspectiva de produccion) identificaron y corrigieron problemas sustanciales. Esta tercera revision busca lo que quedo despues de esas correcciones: inconsistencias *entre* articulos, problemas que las correcciones pudieron haber introducido, y detalles de pulido que solo se ven al leer los diez articulos como una unidad.

---

## 1. Inconsistencias terminologicas entre articulos

### 1.1 "Harness" vs "arnes"

- **Articulo 3** (titulo): usa "arnes" como traduccion de harness en el titulo y la apertura. Luego alterna entre "Agent Harness" (en ingles) y "arnes" (en espanol) a lo largo del texto.
- **Articulo 9** (titulo y cuerpo): usa "harness" sin traduccion en el titulo ("protocolos, harness y el problema del consenso"). En el cuerpo habla de "harness multi-agente".
- **Articulo 1**: menciona "guardrails operativos" y "circuit breakers" sin referirse explicitamente al concepto de harness.

**Problema**: No hay criterio uniforme. A veces "harness" se traduce, a veces no. Recomendacion: elegir una convencion (sugerencia: usar "harness" en ingles siempre, ya que es un termino tecnico sin traduccion directa elegante, y el articulo 3 ya lo justifica) y aplicarla en los 10 articulos.

### 1.2 "Guardrails" vs "barreras de contencion"

- **Articulo 3**: define guardrails como "barreras de contencion" en una seccion dedicada. Usa ambos terminos intercambiablemente.
- **Articulo 1**: menciona "guardrails operativos" sin definirlo.
- **Articulo 9**: usa "guardrails" sin referirse a la definicion del articulo 3.
- **Articulo 5**: no usa el termino guardrails; habla de "contratos" y "validadores".

**Problema**: El articulo 3 es el hogar conceptual de "guardrails", pero los otros articulos usan el termino sin referenciar esa definicion. Un lector que lee el articulo 1 primero (posicion 9 en el orden sugerido) encontrara "guardrails" sin contexto.

### 1.3 "Tool use" vs "uso de herramientas" vs "function calling"

- **Articulo 10**: usa "tool use" en ingles y "uso de herramientas" en espanol, mas "function calling" como sinonimo.
- **Articulo 6**: usa "herramientas" y "tools" indistintamente, mas "function calling" una vez.
- **Articulo 4**: usa "tool tax" (acunado en ese articulo) y "herramientas" pero nunca "function calling".
- **Articulo 3**: habla de "herramientas" consistentemente.
- **Articulo 5**: usa "tool calls" y "herramientas" mezclados.

**Problema menor**: La mezcla es natural en texto tecnico bilingue, pero "function calling" y "tool use" son conceptos ligeramente diferentes (function calling es el mecanismo de la API; tool use es el patron de diseno). Los articulos no hacen esta distincion.

### 1.4 "Ventana de contexto" vs "context window"

- Todos los articulos usan "ventana de contexto" en espanol consistentemente. Bien.

### 1.5 "Alucinaciones" vs "hallucinations"

- Todos los articulos usan "alucinaciones" y "alucinar" en espanol consistentemente. Bien.

### 1.6 "Evals" vs "evaluaciones"

- **Articulo 8**: introduce "evals" y lo define como "evaluaciones o 'evals'", luego usa ambos terminos.
- **Articulo 1**: menciona "evals" sin definicion.
- **Articulo 10**: no usa el termino.

**Problema menor**: El articulo 8 define el termino correctamente; los otros articulos que lo usan deberian referenciar esa definicion.

### 1.7 "System prompt" vs "prompt del sistema" vs "instrucciones del sistema"

- **Articulo 10**: usa "instrucciones del sistema (system prompt)" y "system prompt" indistintamente.
- **Articulo 4**: usa "system prompt" sin traduccion.
- **Articulo 7**: usa "prompt del sistema".
- **Articulo 3**: usa "system prompt" sin traduccion.

**Problema**: Tres variantes del mismo concepto. Recomendacion: estandarizar en "system prompt" (sin traduccion) ya que es el termino tecnico establecido.

### 1.8 "Presupuesto de tokens" / "Budget" / "Context budget"

- **Articulo 3**: tiene una clase `Budget`.
- **Articulo 4**: tiene una clase `ContextBudget`.
- **Articulo 6**: menciona presupuesto de tokens sin clase.
- **Articulo 9**: tiene `BudgetManager`.

**Problema** (ya identificado por Knuth en ronda 2): Cuatro implementaciones del mismo concepto en cuatro articulos, con nombres diferentes. Ninguno referencia a los otros. Un lector que busca "como implementar un presupuesto de contexto" encontrara cuatro versiones sin guia sobre cual usar.

---

## 2. Flujo como serie (orden de lectura: 10 -> 6 -> 3 -> 4 -> 7 -> 5 -> 2 -> 8 -> 1 -> 9)

### 2.1 Transiciones entre articulos

**10 -> 6 (Que es un agente -> El loop agentico)**:
Transicion natural. El articulo 10 termina hablando de la estructura Percepcion -> Razonamiento -> Accion, y el articulo 6 abre con "Todo agente de IA [...] se reduce a lo mismo: un loop." La conexion es clara aunque el articulo 6 no referencia explicitamente al 10. **Sugerencia**: agregar una mencion al articulo 10 en la introduccion del 6, algo como "En el articulo anterior definimos que es un agente; ahora veamos su mecanismo central."

**6 -> 3 (El loop agentico -> Agent Harness)**:
Transicion razonable. El articulo 6 habla de construir el loop; el 3 habla de controlarlo. El articulo 3 no referencia al 6. **Sugerencia**: una frase puente en la intro del 3 que diga "Ya sabemos como funciona el loop de un agente; ahora veamos como controlarlo."

**3 -> 4 (Agent Harness -> Ventana de contexto)**:
Transicion algo abrupta. Se pasa de seguridad/control a gestion de recursos. No hay referencia cruzada directa entre estos dos articulos. **Sugerencia**: el articulo 4 podria mencionar que el harness tambien consume contexto (tool definitions de los guardrails, logging).

**4 -> 7 (Ventana de contexto -> Memoria y estado)**:
Transicion natural y bien ejecutada. El articulo 7 abre con el problema de la memoria, que es la extension natural del problema de contexto del articulo 4. Hay solapamiento significativo (ya identificado por Zinsser/King y Knuth): ambos hablan de working memory, short-term memory y bases de datos vectoriales. **El solapamiento persiste y sigue siendo el problema editorial mas grande entre estos dos articulos.**

**7 -> 5 (Memoria y estado -> Contratos tipados)**:
Transicion menos obvia pero funcional. Se pasa de "como gestionar la informacion del agente" a "como validar la informacion que intercambia". El articulo 5 no referencia al 7.

**5 -> 2 (Contratos tipados -> El protocolo que falta)**:
Buena transicion: de validar datos a estandarizar la comunicacion. El articulo 5 habla de contratos individuales; el 2 habla de protocolos de comunicacion. Complementarios.

**2 -> 8 (Protocolos -> Testing)**:
Transicion razonable. Despues de construir la comunicacion, hay que verificar que funciona. El articulo 8 referencia articulos anteriores en su intro.

**8 -> 1 (Testing -> Verificacion formal)**:
**Esta es la transicion mas problematica.** Los articulos 8 y 1 cubren terreno muy similar (property-based testing con Hypothesis, espectro de testing a verificacion formal, TLA+). Un lector que sigue el orden sugerido leera primero el articulo 8 (testing practico) y luego el 1 (verificacion formal), y encontrara repeticion sustancial. La diferencia conceptual (testing vs proving) esta clara en el articulo 1, pero la repeticion de ejemplos de Hypothesis y TLA+ no se resolvio en las correcciones anteriores.

**1 -> 9 (Verificacion formal -> Orquestacion multi-agente)**:
Transicion funcional como cierre de la serie. El articulo 9 intenta sintetizar temas de los articulos 2, 3 y 8 en el contexto multi-agente.

### 2.2 Referencias cruzadas: inventario

Las siguientes referencias cruzadas apuntan a articulos **externos a la serie de 10** (articulos del blog que no estan en el grupo de los 10). Verifique que todas las rutas parecen validas dentro de la estructura del blog:

- Multiples articulos referencian `/posts/patrones-de-diseno-para-sistemas-con-ia/` -- este es uno de los posts nuevos no publicados (en `content/posts/`). OK.
- Multiples articulos referencian `/posts/de-agentes-teoricos-a-agentes-en-produccion/` -- mismo caso. OK.
- Multiples articulos referencian `/posts/como-razonan-los-llms-de-turing-a-inference-time-scaling/` -- mismo caso. OK.
- Multiples articulos referencian `/posts/owasp-top-10-para-llms-las-nuevas-vulnerabilidades/` -- mismo caso. OK.
- Multiples articulos referencian `/posts/rag-en-2026-la-paradoja-de-la-simplicidad/` -- mismo caso. OK.

**Problema potencial**: Todos estos posts referenciados tambien estan en estado `draft: true`. Si se publican los 10 articulos sin publicar tambien estos posts de soporte, habra links rotos. Los 10 articulos de la serie asumen que estos otros posts existen.

**Referencia a articulo antiguo del blog**: El articulo 10 referencia `/2019/09/27/el-arte-de-resolver-problemas-la-heuristica/`, el articulo 6 referencia `/2019/10/03/el-arte-de-resolver-problemas-la-heuristica.html` y `/2019/09/27/tecnicas-para-resolver-problemas.html`. Estos usan formato de URL diferente (sin `/posts/`). Presumiblemente son posts existentes y publicados. No puedo verificar que los URLs son correctos, pero la inconsistencia de formato (`.html` vs sin extension) sugiere que al menos uno de los dos formatos es incorrecto.

---

## 3. Bugs de codigo residuales

### 3.1 Articulo 4: `build_prompt` sigue teniendo el problema de None en la lista de mensajes

En la funcion `build_prompt` del `ContextManagedAgent`, las lineas 667-674:

```python
messages = [
    {"role": "system", "content": history_context},
]
if rag_context:
    messages.append(
        {"role": "system", "content": f"Datos relevantes:\n{rag_context}"}
    )
messages.append({"role": "user", "content": user_message})
```

La correccion de la ronda 2 noto que la version anterior insertaba `None` en la lista. La version actual corrige esto usando un `if` separado. **Corregido.** Sin embargo, `memory_bank.query` en la linea 645 se llama con `await` correctamente. Verifique que `build_prompt` es `async def` (lo es). OK.

### 3.2 Articulo 6: `eval()` en `calculator` sigue presente

La herramienta `calculator` en el ejemplo completo del agente ReAct sigue usando `eval()` con filtro de caracteres:

```python
allowed = set("0123456789+-*/.() ")
if not all(c in allowed for c in expression):
    return f"Error: expresion no permitida: {expression}"
result = eval(expression)
```

Tiene el comentario "En produccion, usar un parser seguro", pero la inconsistencia con el articulo 3 (que dedica paginas a explicar por que `eval` es peligroso) persiste. **No se corrigio entre rondas.**

### 3.3 Articulo 1: El flujo de `AgenteDeComprasSeguro` fue corregido

Revise el codigo del articulo 1. El flujo ahora es:
1. `pre_compra_sin_confirmacion()` -- verifica Safety 1, 3, 4 (no verifica confirmacion)
2. `self.estado.esperando_confirmacion = True`
3. `pedir_confirmacion()`
4. `verificar_confirmacion()` -- verifica Safety 2

**Este flujo es logicamente correcto.** El bug reportado por Knuth en ronda 2 fue corregido: la verificacion de confirmacion ahora ocurre despues de pedir la confirmacion, no antes. La funcion `pre_compra_sin_confirmacion` ya no verifica SAFETY-2. Bien.

### 3.4 Articulo 5: propiedad `NoDeadlock` en TLA+ sigue siendo incompleta

La propiedad ahora dice:

```
NoDeadlock ==
    \A agent \in Agents:
        agentState[agent] = "waiting" =>
            \E other \in Agents:
                waitingFor[agent] = other /\ agentState[other] # "waiting"
```

Esto verifica que todo agente en espera esta esperando a uno que no esta en "waiting". **Pero no detecta ciclos de longitud > 2**: si A espera a B, B espera a C, y C espera a A, los tres estan en "waiting" pero cada uno espera a un agente diferente. Esta propiedad no los detecta.

El articulo anade una nota explicando que es una simplificacion y que una spec completa verificaria ciclos en el grafo de espera. **Aceptable como sketch didactico**, pero la nota deberia ser mas prominente. Actualmente es un parrafo despues del bloque de codigo que un lector rapido podria saltar.

### 3.5 Articulo 8: Typo `AgentesoSoporte`

Busque en el texto del articulo 8. Los imports de los tests unitarios dicen:

```python
from agente.prompt_builder import construir_prompt
from agente.parser import extraer_tool_call
```

No encontre `AgentesoSoporte` ni `AgenteSoporte` en el texto actual. **Parece que la seccion del fixture fue reescrita y el typo se elimino junto con el codigo que lo contenia.** Sin embargo, los imports a `agente.prompt_builder` y `agente.parser` siguen apuntando a modulos que no se definen en el articulo. Esto sigue siendo un problema para un articulo sobre testing: los tests no se pueden ejecutar.

### 3.6 Articulo 7: `apply_decay` y `calculate_decayed_importance`

La correccion de la ronda 2 se implemento correctamente: ahora hay dos metodos separados (`apply_decay` con mutacion y `calculate_decayed_importance` sin mutacion), con docstrings que explican el efecto secundario. Bien.

### 3.7 Articulo 2: `_send_error` devuelve HTTP 200

Se anadio el comentario explicativo:

```python
# HTTP 200 es correcto aqui: en JSON-RPC 2.0, los errores de
# aplicacion se comunican en el cuerpo JSON (campo "error"),
# no mediante codigos HTTP.
```

**Bien explicado.** Aunque el comentario es largo para un bloque de codigo, la claridad justifica la extension.

---

## 4. Contenido huerfano y referencias dangling

### 4.1 El articulo 5 menciona "futuros articulos" que no existen

La conclusion del articulo 5 dice:

> "En futuros articulos exploraremos como implementar verificacion formal completa para protocolos de agentes y como integrar estos contratos con observabilidad y monitoreo en produccion."

Esto podria referirse a los articulos 1 (verificacion formal) y 3 (observabilidad), que ya existen en la serie. **La referencia deberia ser a articulos existentes, no a "futuros articulos".** Reemplazar con links directos a los articulos 1 y 3.

### 4.2 El articulo 9 referencia articulos de la serie sin usar links

El articulo 9 dice cosas como "Como discutimos en el articulo sobre harness..." pero no siempre incluye el link. En una serie de blog, cada referencia cruzada deberia ser un hipervinculo.

### 4.3 Articulo 7: titulo en frontmatter vs titulo en el texto

El frontmatter dice:

```
title: "Memoria y estado en agentes: el problema central de la ingenieria agentica"
```

Pero la critica de Zinsser/King (ronda 1) noto que el titulo original era "el problema **mas dificil**" y sugirio moderarlo. El titulo actual usa "central" en vez de "mas dificil". Sin embargo, en el cuerpo del articulo, el primer parrafo dice "uno de los mas dificiles de resolver en la ingenieria agentica" -- esta version moderada ("uno de los mas dificiles") es consistente con el titulo moderado ("central"). **Bien resuelto.**

---

## 5. Consistencia de tono

### 5.1 Aperturas: la variacion mejoro pero persiste un patron

Las aperturas post-correccion:

| # | Apertura | Patron |
|---|----------|--------|
| 1 | "Imagina que construyes un agente..." | Imagina que... |
| 2 | HTTP/0.9 en 1991 | Historica |
| 3 | Incidente de DELETE FROM orders | Incidente real |
| 4 | Sistemas embebidos con 2KB de RAM | Experiencia directa |
| 5 | JSON con action delete y confirmation false | Escenario tecnico concreto |
| 6 | "Todo agente de IA [...] se reduce a lo mismo: un loop" | Afirmacion directa |
| 7 | "Cada manana, el agente despierta en blanco" | Narrativa antropomorfica |
| 8 | Test que falla la vez 11 | Escenario reconocible |
| 9 | Sistema de trading que pierde $2.3M | Incidente real |
| 10 | "Todo el mundo habla de agentes..." | Observacion directa |

La critica de Zinsser/King identifico 7 de 10 aperturas como variantes de "Imagina que...". Despues de las correcciones, **solo el articulo 1 conserva "Imagina que..."**. Los articulos 3, 5 y 9 ahora abren con escenarios concretos sin la muleta de "imagina". El articulo 7 sigue usando una apertura narrativa antropomorfica ("el agente despierta en blanco") pero no es un "imagina que". **Mejora significativa.** El unico remanente es el articulo 1.

### 5.2 Secciones que suenan a "autor diferente"

Las notas aclaratorias anadidas en las rondas de correccion a veces rompen el flujo narrativo. Ejemplos:

- **Articulo 1**, parrafo sobre errores correlacionados: la nota "Una nota importante: este calculo asume..." se siente insertada, no integrada. El parrafo que la precede fluye con confianza; la nota frena el ritmo con caveats y citaciones.

- **Articulo 4**, seccion sobre la regla del 60-70%: la version corregida tiene un parrafo largo que alterna entre "mi regla practica" (voz personal, segura) y "este porcentaje depende fuertemente del modelo" y "mide la calidad de las respuestas de tu modelo" (voz tutorial, generica). Las dos voces no estan integradas.

- **Articulo 6**, nota sobre OODA: "Vale notar que Boyd nunca publico sus ideas en papers revisados por pares" se siente como un parentesis defensivo insertado en respuesta a una critica (que es exactamente lo que es). Integrarlo mejor: "Boyd desarrollo OODA en briefings y documentos internos, no en papers revisados por pares, lo que le da un caracter mas de modelo mental que de framework riguroso."

En general, las correcciones de ronda 1 y 2 se implementaron como *inserciones* en vez de *reescrituras*. El texto original fluye bien; las correcciones se sienten como parches. **El resultado es funcional pero no transparente**: un lector atento nota las costuras.

### 5.3 Cierre de los articulos

Varios articulos terminan con una seccion de "Referencias y fuentes clave" precedida por una conclusion. La recomendacion de Zinsser/King de eliminar los resumenes finales se implemento parcialmente:

- **Articulos 4, 6, 10**: tienen conclusiones concisas sin resumen repetitivo. Bien.
- **Articulos 1, 2, 5**: las conclusiones siguen siendo algo extensas y repiten puntos del cuerpo.
- **Articulo 9**: tiene una seccion "Conclusion" que sintetiza de forma original (no repite). Bien.

---

## 6. Frontmatter

### 6.1 Fechas

**Todos los 10 articulos tienen fecha `2026-03-15`.** Esto fue senalado en la ronda 1 por Knuth como problematico (publicar 10 articulos el mismo dia sugiere contenido generado en lote) y reiterado en la ronda 2. **No se corrigio.**

Recomendacion: espaciar las fechas en intervalos de 3-5 dias, siguiendo el orden de lectura sugerido:

| Orden | Articulo | Fecha sugerida |
|-------|----------|---------------|
| 1 | Art. 10 (Que es un agente) | 2026-03-15 |
| 2 | Art. 6 (Loop agentico) | 2026-03-18 |
| 3 | Art. 3 (Agent Harness) | 2026-03-21 |
| 4 | Art. 4 (Ventana de contexto) | 2026-03-24 |
| 5 | Art. 7 (Memoria y estado) | 2026-03-27 |
| 6 | Art. 5 (Contratos tipados) | 2026-03-30 |
| 7 | Art. 2 (Protocolos) | 2026-04-02 |
| 8 | Art. 8 (Testing) | 2026-04-05 |
| 9 | Art. 1 (Verificacion formal) | 2026-04-08 |
| 10 | Art. 9 (Orquestacion multi-agente) | 2026-04-11 |

### 6.2 Tags

Los tags son razonablemente consistentes pero hay variaciones:

- `'IA'` vs `'inteligencia-artificial'`: ambos se usan. Los articulos 1, 4, 7 usan ambos simultaneamente; el articulo 6 usa solo `'inteligencia-artificial'`.
- `'llm'` vs `'llms'`: el articulo 10 usa `'llms'`, el articulo 6 usa `'llm'`, el articulo 2 usa `'llms'`. Estandarizar a uno.
- `'diseño-de-software'` aparece en articulos 3, 4, 5, 7, 9. Bien.
- `'ciencias-de-la-computación'` aparece solo en articulos 6 y 10. Deberia estar tambien en articulos 1 (verificacion formal), 5 (teoria de tipos) y 9 (sistemas distribuidos).
- `'agentes'` aparece en todos. Bien.
- `'arquitectura'` aparece en articulos 3, 4, 6, 9, 10. Deberia estar tambien en articulos 2 y 7.

### 6.3 Draft status

Todos los articulos tienen `draft: true`. Obvio ya que no estan publicados, pero es un recordatorio de que hay que cambiar a `false` antes de publicar.

### 6.4 FeaturedImage

Todos los articulos tienen `featuredImage: ""` (vacio). Si el blog requiere imagenes destacadas, esto producira problemas visuales.

### 6.5 Author

Todos usan `author: "Hector Patricio"`. Consistente. El acento en "Hector" esta presente en todos (`Héctor`). Bien.

---

## 7. Calidad de escritura final

### 7.1 Cliches residuales

Despues de dos rondas de correccion, la mayoria de los cliches senalados por Zinsser/King fueron eliminados o atenuados. Los que persisten:

- **Articulo 1**: "la distancia entre esas dos afirmaciones es un abismo" -- dramatico pero funcional para la apertura. Aceptable.

- **Articulo 3**: "cada accion autonoma es una caida potencial" -- mezclado con la metafora del arnes de escalada. Funciona en contexto.

- **Articulo 7**: "procesan informacion, pero no acumulan experiencia" -- correcto y conciso. No es un cliche sino una descripcion precisa.

- **Articulo 9**: "Tres agentes, cero disidencia, perdida total." -- Esta estructura de tres frases cortas y contundentes es efectiva en la apertura. No es un cliche; es ritmo narrativo deliberado.

**No encontre cliches problematicos residuales.** Las correcciones fueron efectivas.

### 7.2 Voz pasiva residual

La voz pasiva fue reducida significativamente. Persisten casos aislados:

- Art. 4: "la informacion que necesitamos procesar" -- La critica sugirio "la informacion que debemos procesar". **No se corrigio.**
- Art. 4: "No existe un mecanismo automatico de paginacion" -- La critica sugirio "La ventana de contexto no pagina automaticamente". **No se corrigio.**

Estos son menores y no afectan la legibilidad.

### 7.3 Redundancias inter-articulo que persisten

Este es el problema de calidad de escritura mas grande que queda. Las siguientes repeticiones fueron senaladas en rondas anteriores y siguen presentes:

1. **Property-based testing con Hypothesis**: codigo extenso en articulos 1, 5 y 8. El articulo 8 es el tratamiento mas completo. Los articulos 1 y 5 deberian referenciar al 8 y reducir sus ejemplos.

2. **Pseudo-TLA+**: aparece en articulos 1, 5 y 9. Tres versiones de pseudo-codigo TLA+ con tres niveles de detalle, sin que ninguno sea una spec completa. Deberia haber un solo ejemplo completo (en el articulo 1 o el 5) y los demas deberian referenciarlo.

3. **Presupuesto de contexto/tokens**: cuatro implementaciones en articulos 3, 4, 6 y 9 (ya mencionado arriba).

4. **Solapamiento articulos 4 y 7**: ambos discuten working memory, bases de datos vectoriales, y la analogia con la RAM de un sistema operativo. El articulo 4 lo hace desde la perspectiva de la ventana de contexto; el 7 desde la perspectiva de la memoria persistente. La distincion es conceptualmente clara pero en la practica muchos parrafos podrian estar en cualquiera de los dos articulos.

---

## Resumen de hallazgos

### Problemas que requieren correccion antes de publicar

| Prioridad | Problema | Articulo(s) |
|-----------|----------|-------------|
| ALTA | Todas las fechas son 2026-03-15 | Todos |
| ALTA | El articulo 5 referencia "futuros articulos" que ya existen en la serie | 5 |
| MEDIA | `eval()` en calculator contradice principios del articulo 3 | 6 |
| MEDIA | Tags `'llm'` vs `'llms'`, `'IA'` duplicado con `'inteligencia-artificial'` | Varios |
| MEDIA | Posts referenciados tambien en `draft: true` (links rotos si no se publican juntos) | Todos |
| MEDIA | Inconsistencia en formato de URLs de articulos antiguos (`.html` vs sin extension) | 6, 10 |
| BAJA | `harness` vs `arnes`: sin criterio uniforme | 3, 9 |
| BAJA | `system prompt` vs `prompt del sistema` vs `instrucciones del sistema` | Varios |
| BAJA | Notas correctivas se sienten como parches, no como texto integrado | 1, 4, 6 |
| BAJA | FeaturedImage vacio en todos los articulos | Todos |
| BAJA | Articulo 1 sigue abriendo con "Imagina que..." | 1 |

### Lo que funciona bien

1. **Las correcciones tecnicas de las rondas 1 y 2 fueron implementadas correctamente.** La postcondicion con epsilon, la clarificacion del teorema CAP como metafora, la distincion sobre Turing-completeness de transformadores, el flujo corregido del `AgenteDeComprasSeguro`, la separacion `apply_decay`/`calculate_decayed_importance` -- todo funciona.

2. **El tono general es consistente.** La voz del autor (conversacional-tecnica, con humor seco y analogias bien elegidas) se mantiene a traves de los 10 articulos. Las mejores lineas siguen intactas: "detras de toda la magia no hay mas que un `while True` bien pensado" (art. 6), el concepto de "tool tax" (art. 4), la tabla BDI->LLM (art. 10).

3. **Las aperturas mejoraron significativamente.** Solo queda un "Imagina que..." de los siete originales.

4. **Los articulos 6 (Loop agentico), 10 (Que es un agente) y 4 (Ventana de contexto) son los mas solidos de la serie** y no requieren cambios sustanciales.

5. **Las secciones "Cuando NO" se anadieron al articulo 9 (multi-agente) y al 10 (agentes en general).** Esto era la recomendacion #1 de la critica de produccion. Bien ejecutado.

6. **El prompt caching se anadio al articulo 4.** Era la recomendacion de la critica de produccion sobre la optimizacion de produccion mas importante. Bien integrado.

### Veredicto final

La serie esta en buena forma despues de dos rondas de correccion. Los problemas restantes son de *consistencia editorial* (fechas, tags, terminologia entre articulos, redundancia) y *pulido fino* (integrar mejor las notas correctivas, resolver la referencia a "futuros articulos"). No hay errores tecnicos criticos pendientes. Los bugs de codigo residuales son menores (el `eval()` del articulo 6 es el mas notable pero esta claramente marcado como ejemplo didactico).

La accion mas impactante antes de publicar: **espaciar las fechas** y **verificar que todos los posts referenciados estan tambien listos para publicar**. Sin esto, la serie tendra links rotos desde el primer dia.
