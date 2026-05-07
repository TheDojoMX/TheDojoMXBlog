# Apendice A: Glosario

Definiciones concisas de los terminos tecnicos utilizados en este libro. Las referencias entre parentesis indican el capitulo donde el concepto se introduce o se trata en mayor profundidad.

---

**A2A (Agent-to-Agent Protocol).** Protocolo abierto desarrollado por Google para la comunicacion entre agentes de IA via HTTPS y JSON-RPC 2.0. Define Agent Cards como mecanismo de descubrimiento y capacidades. (Cap. 12)

**Agente.** Sistema que percibe su ambiente a traves de sensores y actua sobre ese ambiente a traves de actuadores. En el contexto de este libro, un agente de IA es un sistema que usa un LLM como motor de razonamiento, accede a herramientas externas y opera en un loop de retroalimentacion para lograr un objetivo. (Cap. 1)

**Agente basado en metas.** Tipo de agente que toma decisiones comparando estados futuros posibles con un estado objetivo deseado. (Cap. 1)

**Agente basado en modelo.** Tipo de agente que mantiene un modelo interno del mundo para tomar decisiones con informacion parcial. (Cap. 1)

**Agente basado en utilidad.** Tipo de agente que asigna un valor numerico (utilidad) a cada estado posible y selecciona la accion que maximiza la utilidad esperada. (Cap. 1)

**Agente reactivo simple.** Tipo de agente que responde directamente a estimulos del ambiente con reglas condicion-accion, sin mantener estado interno. (Cap. 1)

**Agent Card.** En el protocolo A2A, un documento JSON alojado en `/.well-known/agent.json` que describe las capacidades, endpoint y requisitos de autenticacion de un agente. (Cap. 12)

**Agent Harness (Arnes del Agente).** Capa de infraestructura que envuelve a un agente de IA con controles de seguridad, permisos, guardrails, circuit breakers y observabilidad. El harness restringe y monitorea las acciones del agente. (Cap. 8)

**Alucinacion.** Generacion de informacion por parte de un LLM que suena plausible pero no esta respaldada por hechos reales. Es una propiedad inherente de los modelos generativos, no un bug transitorio. (Cap. 2, 4)

**Audit log.** Registro inmutable de todas las acciones ejecutadas por un agente, utilizado para depuracion, cumplimiento regulatorio y analisis post-incidente. (Cap. 8, 9)

**Backoff exponencial.** Estrategia de reintento donde el tiempo de espera entre intentos crece exponencialmente (2s, 4s, 8s, 16s...) para evitar sobrecargar servicios fallidos. (Cap. 14)

**BDI (Beliefs, Desires, Intentions).** Modelo de arquitectura de agentes propuesto por Bratman, Rao y Georgeff. Los beliefs representan el conocimiento del agente sobre el mundo, los desires sus objetivos, y las intentions los planes comprometidos para alcanzar esos objetivos. (Cap. 1)

**Chain-of-Thought (CoT).** Tecnica de prompting que induce al LLM a generar pasos de razonamiento intermedios antes de producir una respuesta final. Mejora significativamente el rendimiento en tareas que requieren razonamiento. (Cap. 2, 3)

**Chunking.** Proceso de dividir documentos en fragmentos (chunks) de tamano apropiado para almacenamiento vectorial y recuperacion en sistemas RAG. Puede ser por tamano fijo, por parrafos, o semantico. (Cap. 7)

**Circuit breaker.** Patron de resiliencia que detiene la ejecucion de un agente cuando se detectan condiciones anomalas: loops de razonamiento, consumo excesivo de tokens, errores consecutivos o tiempo excesivo. (Cap. 8)

**Consenso bizantino.** Problema de la teoria de sistemas distribuidos que describe la dificultad de alcanzar acuerdo entre nodos cuando algunos de ellos pueden comportarse de forma incorrecta o maliciosa. Aplicado a agentes LLM, se manifiesta cuando multiples agentes con el mismo modelo base comparten los mismos sesgos y confirman mutuamente informacion incorrecta. (Cap. 13)

**Context engineering (Ingenieria de contexto).** Disciplina de disenar, construir y optimizar el contexto que recibe un agente: que informacion incluir, como estructurarla, cuando resumirla y como priorizarla dentro de la ventana de contexto. (Cap. 5)

**Contrato tipado.** Modelo de datos (tipicamente implementado con Pydantic) que define la estructura y las restricciones semanticas de la comunicacion entre agentes, entre un agente y sus herramientas, o entre un agente y el usuario. (Cap. 10)

**Cuantizacion.** Tecnica de compresion de modelos que reduce la precision numerica de los pesos (de FP32 a FP16, INT8 o INT4) para reducir el tamano en memoria y la latencia de inferencia, con una degradacion controlada de la calidad. (Cap. 15)

**Defensa en profundidad.** Estrategia de seguridad que implementa multiples capas de proteccion independientes, asumiendo que cada una puede ser evadida individualmente. (Cap. 9)

**Embedding.** Representacion numerica (vector) de texto, generada por un modelo de embeddings, que captura el significado semantico. Se usa en RAG para busqueda por similitud. (Cap. 7)

**Eval (Evaluacion).** Test sistematico que mide la calidad de las salidas de un agente o LLM contra un dataset de referencia con criterios de evaluacion definidos. (Cap. 11)

**Fallback deterministico.** Comportamiento predefinido basado en reglas que se activa cuando el LLM falla, el circuit breaker se activa o la confianza del agente es insuficiente. (Cap. 8, 14)

**Function calling (Tool calling).** Mecanismo por el cual un LLM genera una llamada estructurada a una funcion externa, especificando el nombre de la funcion y sus argumentos en formato JSON. (Cap. 3, 8)

**Grounding.** Tecnica de anclar las respuestas de un LLM en datos verificados y fuentes de verdad externas, en lugar de depender unicamente del conocimiento de entrenamiento del modelo. (Cap. 7)

**Guardrail.** Mecanismo de proteccion que valida las entradas o salidas de un agente contra criterios de seguridad, formato, coherencia o cumplimiento. Los input guardrails validan lo que entra al agente; los output guardrails validan lo que sale. (Cap. 8)

**Halting problem (Problema de la parada).** Resultado teorico de Alan Turing (1936) que demuestra que es imposible construir un algoritmo general que determine si un programa arbitrario va a terminar. En agentes, motiva el uso de heuristicas practicas de terminacion. (Cap. 3)

**Handoff.** En el OpenAI Agents SDK, mecanismo por el cual un agente delega la conversacion a otro agente mas especializado, transfiriendo el contexto. (Cap. 15)

**Human-in-the-Loop (HITL).** Patron de diseno donde acciones criticas o de alto riesgo requieren aprobacion explicita de un humano antes de ejecutarse. (Cap. 8, 13)

**Idempotencia.** Propiedad de una operacion que produce el mismo resultado sin importar cuantas veces se ejecute. Esencial para prevenir duplicados causados por retries automaticos. (Cap. 14)

**Inference-time scaling.** Tecnica que asigna mas computo durante la inferencia (en lugar de en el entrenamiento) para mejorar la calidad de las respuestas. Incluye chain-of-thought, tree-of-thought y busqueda con MCTS. (Cap. 2)

**JSON Schema.** Especificacion para definir la estructura esperada de un documento JSON. Usado para definir los parametros de herramientas y para structured outputs. (Cap. 10)

**LATS (Language Agent Tree Search).** Variante del loop agentico que aplica Monte Carlo Tree Search al razonamiento del agente, explorando multiples caminos y seleccionando el mejor. Significativamente mas costoso que ReAct. (Cap. 3)

**LLM (Large Language Model).** Modelo de lenguaje de gran escala entrenado sobre grandes cantidades de texto. Genera texto prediciendo el siguiente token mas probable dado un contexto. En este libro, es el motor de razonamiento del agente, no el agente en si. (Cap. 2)

**Loop agentico.** Ciclo fundamental de operacion de un agente: percibir, razonar, actuar, observar, repetir. Variantes incluyen ReAct, Reflexion, LATS y Plan-and-Execute. (Cap. 3)

**MCP (Model Context Protocol).** Protocolo abierto desarrollado por Anthropic (donado a la Linux Foundation) para conectar agentes de IA con herramientas, datos y servicios externos. Define un estandar de comunicacion entre el agente y los servidores de herramientas. (Cap. 12)

**Memoria episodica.** En agentes, almacenamiento de experiencias pasadas (ejecuciones anteriores, errores, soluciones) que el agente puede consultar para informar decisiones futuras. (Cap. 6)

**Memoria de trabajo.** En agentes, la informacion activa en la ventana de contexto durante una ejecucion: el prompt del sistema, el historial de la conversacion, los resultados de herramientas. (Cap. 6)

**Memoria semantica.** En agentes, conocimiento general almacenado en forma de embeddings y recuperable por similitud semantica. Tipicamente implementada con bases de datos vectoriales. (Cap. 6)

**Minimo privilegio.** Principio de seguridad (Saltzer y Schroeder, 1975) que establece que cada componente debe tener acceso unicamente a los recursos estrictamente necesarios para su funcion. (Cap. 8, 9)

**OODA (Observe, Orient, Decide, Act).** Loop de decision desarrollado por John Boyd, aplicable a la estructura del ciclo agentico. (Cap. 3)

**OWASP Top 10 para LLMs.** Lista de las diez vulnerabilidades mas criticas en aplicaciones basadas en LLMs, publicada por OWASP. Incluye prompt injection, fuga de datos, envenenamiento de datos de entrenamiento, entre otras. (Cap. 9)

**PEAS (Performance, Environment, Actuators, Sensors).** Marco de Russell y Norvig para describir formalmente un agente: que medida de desempeno tiene, en que ambiente opera, que actuadores usa y que sensores tiene. (Cap. 1)

**Plan-and-Execute.** Variante del loop agentico que separa la fase de planificacion (generar un plan completo) de la fase de ejecucion (ejecutar cada paso del plan). (Cap. 3)

**Prompt injection.** Ataque donde un usuario o una fuente de datos inserta instrucciones maliciosas en el contexto del agente para alterar su comportamiento. Puede ser directo (en el input del usuario) o indirecto (embebido en datos que el agente procesa). (Cap. 9)

**Property-based testing.** Tecnica de testing que verifica que invariantes (propiedades) del sistema se cumplen para un gran numero de inputs generados automaticamente, en lugar de verificar casos especificos. (Cap. 11)

**RAG (Retrieval-Augmented Generation).** Patron que combina un sistema de recuperacion de informacion con un LLM: primero se recuperan documentos relevantes de una base de conocimiento, luego se incluyen en el contexto del LLM para generar una respuesta anclada en datos reales. (Cap. 7)

**Rate limiter.** Mecanismo que limita la cantidad de peticiones o acciones que un agente o usuario puede realizar por unidad de tiempo, previniendo abuso y costos desbordados. (Cap. 8)

**ReAct (Reasoning and Acting).** Patron canonico del loop agentico para LLMs (Yao et al., 2022): el agente genera un pensamiento (Thought), ejecuta una accion (Action) y observa el resultado (Observation), repitiendo hasta alcanzar una respuesta final. (Cap. 3)

**Red teaming.** Practica de evaluar un sistema asumiendo el rol de un adversario que intenta romperlo. Para agentes, incluye intentos de prompt injection, exfiltracion de datos, abuso de herramientas y evasion de guardrails. (Cap. 11)

**Reflexion.** Variante del loop agentico donde el agente evalua criticamente su propia respuesta y reintenta si detecta errores, aprendiendo de sus fallos sin actualizar los pesos del modelo. (Cap. 3)

**Sandboxing.** Tecnica de aislamiento donde el agente ejecuta acciones (especialmente ejecucion de codigo) en un entorno contenido sin acceso a la red ni al filesystem del host. (Cap. 8)

**Structured output.** Capacidad de un LLM de generar respuestas en un formato estructurado (JSON, XML) que se ajusta a un esquema predefinido, facilitando el parsing y la validacion. (Cap. 10)

**Token.** Unidad basica de procesamiento de un LLM. Aproximadamente equivale a 3/4 de una palabra en ingles o 1/2 de una palabra en espanol. Los costos de API se miden en tokens consumidos. (Cap. 2, 5)

**Topologia multi-agente.** Patron de organizacion de un sistema de multiples agentes: centralizada (orquestador), descentralizada (peer-to-peer), jerarquica, pipeline o fan-out/fan-in. (Cap. 13)

**Tracing distribuido.** Tecnica de observabilidad que registra cada paso de una ejecucion del agente como un "span" dentro de un "trace", permitiendo reconstruir y analizar el flujo completo. (Cap. 14)

**Validacion semantica.** Validacion que verifica no solo la estructura de un dato (formato correcto, tipos correctos) sino su significado en el contexto del dominio (coherencia con reglas de negocio, consistencia con restricciones del mundo real). (Cap. 10)

**Ventana de contexto.** Cantidad maxima de tokens que un LLM puede procesar en una sola llamada. Es un recurso finito que requiere gestion deliberada: que informacion incluir, que resumir, que descartar. (Cap. 5)

---
