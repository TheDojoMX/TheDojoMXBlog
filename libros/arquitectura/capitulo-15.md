# Capitulo 15: Los grados de diseno como guia practica

> "Antes de resolver, identifica en que nivel esta tu problema."

---

## El mapa que te falta

Imagina que llegas a la oficina un lunes por la manana y te asignan una tarea: "mejorar el rendimiento del catalogo de cursos." Abres tu editor, miras el codigo y te preguntas: por donde empiezo?

Si tu primera reaccion es abrir el archivo del controlador HTTP y buscar queries lentas, estas asumiendo algo. Estas asumiendo que el problema es de codigo -- que la solucion esta en optimizar una consulta SQL o agregar un indice. Quiza tengas razon. Pero quiza el problema no esta en el codigo. Quiza esta en la arquitectura: el catalogo y el motor de busqueda comparten la misma base de datos, y las consultas de busqueda bloquean las del catalogo. O quiza esta mas arriba aun: la decision de usar una sola base de datos relacional para todo -- busqueda, catalogo, analytics -- fue una decision de arquitectura de solucion que ahora esta limitando el sistema.

El mismo sintoma -- "el catalogo es lento" -- puede tener su raiz en cuatro niveles diferentes de diseno. Y la solucion correcta depende enteramente de en que nivel este la causa real.

A lo largo de catorce capitulos hemos trabajado con principios que aplican en todos los niveles: complejidad, modulos profundos, ocultamiento de informacion, abstraccion. Pero no hemos hablado explicitamente de los niveles mismos. Es hora de hacerlo.

En este capitulo vamos a trazar un mapa completo de los cuatro grados de diseno de software -- desde la arquitectura de solucion hasta el diseno de codigo -- y vamos a usarlo como brujula para saber en que nivel necesitas trabajar segun el problema que enfrentas. Es, en cierto sentido, el capitulo que une los catorce anteriores con la practica diaria.

**Takeaway:** Antes de escribir una linea de codigo o dibujar un diagrama, identifica en que grado de diseno se encuentra tu problema. La solucion correcta en el nivel equivocado es peor que no tener solucion.

---

## Los cuatro grados: un mapa completo

El diseno de software opera en cuatro niveles, cada uno con un proposito diferente, un vocabulario diferente y artefactos diferentes. Pensemos en ellos como grados de distancia respecto a la implementacion en codigo.

### Grado 1: Arquitectura de solucion

Es el nivel mas alejado del codigo. Aqui la pregunta no es "como implemento esto" sino "que construyo y por que". Es el nivel donde se toman las decisiones de negocio que enmarcan todo lo demas.

**Proposito:** Definir el alcance, las restricciones y las grandes decisiones sobre que construir.

**Vocabulario:** Stakeholders, objetivos de negocio, restricciones, build vs. buy, compliance, riesgos, presupuesto, roadmap.

**Preguntas tipicas:**
- Cual es el problema de negocio que estamos resolviendo?
- Quienes son los stakeholders y que necesitan?
- Que restricciones tenemos (legales, presupuestarias, de tiempo, de equipo)?
- Que construimos internamente y que compramos o subcontratamos?
- Como medimos el exito?

**Artefactos:**
- Mapa de stakeholders
- Objetivos medibles (OKRs, KPIs)
- Mapa de capacidades del sistema
- Analisis de riesgos con mitigaciones
- Decision de build vs. buy
- Roadmap de alto nivel

**Quien lo hace:** Arquitectos de solucion, CTOs, product managers senior, lideres tecnicos. En equipos pequenos, el tech lead o el CTO asumen este rol.

### Grado 2: Arquitectura de software

Una vez que sabemos *que* construir, la siguiente pregunta es *con que propiedades*. Este es el nivel de los atributos de calidad: latencia, disponibilidad, seguridad, mantenibilidad, operabilidad. Aqui se toman las decisiones estructurales que determinan como el sistema logra esas propiedades.

**Proposito:** Priorizar atributos de calidad y tomar las decisiones estructurales para lograrlos.

**Vocabulario:** Atributos de calidad, escenarios de calidad, ADRs (Architecture Decision Records), SLOs, SLAs, trade-offs, NFRs (Non-Functional Requirements), diagramas C4, contenedores.

**Preguntas tipicas:**
- Cuales son los atributos de calidad mas importantes para nuestro sistema?
- Que latencia es aceptable? Que disponibilidad necesitamos?
- Monolito o microservicios? Sincrono o asincrono?
- Como observamos el sistema en produccion?
- Cuales son los trade-offs de cada decision?

**Artefactos:**
- Escenarios de calidad priorizados (estimulo, fuente, entorno, artefacto, respuesta, medida)
- ADRs (Architecture Decision Records)
- Diagrama C4 Nivel 2 (contenedores)
- Presupuestos de error
- Plan de observabilidad

**Quien lo hace:** Arquitectos de software, tech leads senior. En equipos pequenos, el lider tecnico con input del equipo.

### Grado 3: Diseno de sistemas

Este nivel traduce las decisiones arquitectonicas en una topologia concreta: componentes, contratos, flujos de datos, mecanismos de resiliencia. Es donde la arquitectura se convierte en un plano que los desarrolladores pueden seguir.

**Proposito:** Definir la topologia del sistema -- componentes, datos, contratos y mecanismos de escala y fiabilidad.

**Vocabulario:** APIs, contratos, esquemas de datos, diagramas de secuencia, idempotencia, versionado, rate limits, caches, colas, circuit breakers, backpressure, particionamiento.

**Preguntas tipicas:**
- Cuales son los componentes del sistema y como se comunican?
- Que contratos definen las APIs entre componentes?
- Cual es el modelo de datos? Consistencia fuerte o eventual?
- Como manejamos los picos de carga?
- Que pasa cuando un componente falla?

**Artefactos:**
- Contratos de API (OpenAPI, gRPC, GraphQL schemas)
- Modelo de datos logico
- Diagramas de secuencia de los flujos criticos
- Estrategia de cache
- Mecanismos de resiliencia documentados
- Estimaciones de capacidad y costos

**Quien lo hace:** Desarrolladores senior, tech leads, ingenieros de plataforma. En equipos pequenos, los desarrolladores mas experimentados.

### Grado 4: Diseno de codigo

Es el nivel mas cercano a la implementacion. Aqui es donde aplicamos todo lo que discutimos en los capitulos 4 a 14: modulos profundos, ocultamiento de informacion, cohesion, acoplamiento, composicion, abstraccion, claridad.

**Proposito:** Organizar el codigo en modulos con interfaces claras, alta cohesion, bajo acoplamiento y buenas abstracciones.

**Vocabulario:** Modulos, interfaces, funciones, clases, tipos, patrones de diseno, tests, metricas de complejidad, linters, bounded contexts, vertical slices.

**Preguntas tipicas:**
- Como organizo los modulos de esta funcionalidad?
- Que interfaz expone este modulo?
- Que informacion oculta?
- Es un modulo profundo o superficial?
- La abstraccion captura el concepto correcto?

**Artefactos:**
- Limites de modulo documentados
- Contratos de API interna (firmas de funciones, tipos)
- Estrategia de pruebas
- Metricas de calidad (complejidad ciclomatica, cobertura, acoplamiento)
- Guias de estilo y convenciones

**Quien lo hace:** Todos los desarrolladores del equipo. Es el nivel donde se pasa la mayor parte del tiempo.

---

## Como saber en que grado necesitas trabajar

El error mas comun no es resolver un problema mal en el nivel correcto. Es resolver un problema correctamente en el nivel equivocado. Optimizar una consulta SQL cuando el verdadero problema es que necesitas una base de datos diferente. Refactorizar un modulo cuando el verdadero problema es que dos servicios deberian ser uno solo. Agregar un cache cuando el verdadero problema es que los objetivos de negocio estan mal definidos y el equipo esta construyendo lo que no debe.

Aqui hay cinco heuristicas para identificar en que grado se encuentra tu problema.

### Heuristica 1: Mira la escala del impacto

Si el problema afecta a un archivo o una funcion, probablemente es Grado 4 (diseno de codigo). Si afecta a un componente completo o a la comunicacion entre componentes, probablemente es Grado 3 (diseno de sistemas). Si afecta a las propiedades globales del sistema (disponibilidad, latencia, seguridad), probablemente es Grado 2 (arquitectura de software). Si cuestiona *que* estas construyendo o *por que*, es Grado 1 (arquitectura de solucion).

### Heuristica 2: Pregunta quien necesita tomar la decision

Si la decision la puede tomar un desarrollador individual, es Grado 4. Si la necesita validar el equipo, es Grado 3. Si involucra al tech lead y requiere documentacion formal (un ADR), es Grado 2. Si necesita aprobacion de stakeholders no tecnicos, es Grado 1.

### Heuristica 3: Evalua la reversibilidad

Las decisiones de Grado 4 son casi siempre reversibles en horas o dias. Las de Grado 3, en dias o semanas. Las de Grado 2, en semanas o meses. Las de Grado 1 pueden ser irreversibles o requerir meses de trabajo para revertir. Cuanto menos reversible sea la decision, mas arriba en los grados esta el problema.

### Heuristica 4: Escucha el vocabulario

Si el equipo habla de "funciones", "clases", "nombres de variables", estas en Grado 4. Si habla de "APIs", "schemas", "flujos de datos", estas en Grado 3. Si habla de "latencia", "disponibilidad", "trade-offs", estas en Grado 2. Si habla de "usuarios", "presupuesto", "competidores", "regulacion", estas en Grado 1.

### Heuristica 5: Identifica si el problema sube de nivel

A veces empiezas en un grado y descubres que el problema esta mas arriba. Si estas optimizando una consulta (Grado 4) y descubres que el modelo de datos esta mal disenado (Grado 3), sube. Si el modelo de datos esta mal porque el sistema deberia ser asincrono en vez de sincrono (Grado 2), sube otra vez. Si deberia ser asincrono pero no lo es porque el presupuesto no permite la infraestructura necesaria (Grado 1), has llegado a la raiz.

La regla general: **resuelve el problema en el grado mas alto donde se origina, no en el grado mas bajo donde se manifiesta.** Resolver un problema de Grado 2 con una solucion de Grado 4 es como tratar un dolor de muelas con aspirinas: alivias el sintoma, pero la causa sigue ahi.

---

## Artefactos, decisiones y checklists para cada nivel

Para cada grado, hay un conjunto minimo de artefactos que deberias producir, decisiones que deberias documentar, y preguntas que deberias responder antes de considerar que el trabajo esta hecho.

### Checklist de Grado 1: Arquitectura de solucion

- [ ] Los objetivos de negocio estan definidos y son medibles
- [ ] Las restricciones estan documentadas (presupuesto, tiempo, equipo, legales)
- [ ] Los riesgos principales estan identificados con mitigaciones
- [ ] Las decisiones de build vs. buy estan justificadas
- [ ] Los criterios de exito estan definidos (como sabemos que funciono?)
- [ ] El roadmap de alto nivel existe y tiene hitos concretos
- [ ] Los stakeholders han validado el alcance

**Pregunta clave:** Si muestro este documento a alguien que no conoce el proyecto, puede entender *que* construimos y *por que*?

### Checklist de Grado 2: Arquitectura de software

- [ ] Los atributos de calidad estan priorizados (no todo puede ser numero uno)
- [ ] Cada atributo tiene al menos un escenario medible
- [ ] Las decisiones arquitectonicas estan documentadas como ADRs
- [ ] Los trade-offs de cada decision estan explicitos
- [ ] El diagrama C4 Nivel 2 (contenedores) esta actualizado
- [ ] La estrategia de observabilidad esta definida
- [ ] Los presupuestos de error (error budgets) estan cuantificados

**Pregunta clave:** Si un nuevo arquitecto llega al proyecto, puede entender *por que* se tomaron las decisiones estructurales?

### Checklist de Grado 3: Diseno de sistemas

- [ ] Los contratos de API estan definidos y versionados
- [ ] Los flujos criticos tienen diagramas de secuencia
- [ ] El modelo de datos esta documentado con decisiones de consistencia
- [ ] Los mecanismos de resiliencia estan identificados (que pasa cuando X falla?)
- [ ] Las estimaciones de capacidad estan hechas (throughput, picos, almacenamiento)
- [ ] Las estrategias de cache estan documentadas con politicas de invalidacion
- [ ] Los limites de rate limiting estan definidos

**Pregunta clave:** Si tengo que implementar el flujo mas critico del sistema, puedo hacerlo sin preguntar a nadie como deberia funcionar?

### Checklist de Grado 4: Diseno de codigo

- [ ] Los limites de modulo estan definidos (que es responsabilidad de quien)
- [ ] Cada modulo tiene una interfaz documentada
- [ ] Cada modulo oculta al menos una decision de diseno importante
- [ ] La estrategia de pruebas esta definida (que se prueba, como, a que nivel)
- [ ] Las metricas de calidad se monitorean (complejidad, cobertura, acoplamiento)
- [ ] Las convenciones de nombrado y estilo estan documentadas y automatizadas
- [ ] El vocabulario del dominio es consistente en todo el codigo

**Pregunta clave:** Si un nuevo desarrollador se une al equipo, puede hacer su primer cambio significativo en menos de una semana sin romper nada?

---

## La interaccion entre niveles

Los cuatro grados no son compartimentos estancos. Se alimentan mutuamente en ambas direcciones.

### Top-down: las decisiones bajan

Una decision de Grado 1 -- "necesitamos soportar pagos en multiples monedas" -- genera restricciones en todos los grados inferiores:

- **Grado 2:** El sistema necesita un atributo de calidad nuevo: precision en el manejo de divisas. Esto puede requerir un ADR sobre como almacenar cantidades monetarias (nunca en punto flotante).
- **Grado 3:** Las APIs de pago necesitan aceptar un parametro de moneda. El modelo de datos necesita una tabla de tipos de cambio. El flujo de pago necesita un paso de conversion.
- **Grado 4:** Los modulos que manejan dinero necesitan usar `Decimal` en lugar de `float`. Los tests necesitan verificar precision en operaciones aritmeticas. Las interfaces necesitan exponer la moneda como parte del contrato.

### Bottom-up: las restricciones suben

A veces, un descubrimiento en Grado 4 obliga a reconsiderar decisiones de grados superiores. Si al implementar el modulo de video descubres que la latencia de streaming desde S3 no cumple el SLO de Grado 2, esa restriccion tecnica sube hasta Grado 2 y potencialmente hasta Grado 1 (quiza necesitemos un CDN, lo cual tiene implicaciones de presupuesto).

### La gobernanza entre niveles

Para mantener la coherencia entre grados, tres practicas son esenciales:

**1. Documentacion viva.** Los artefactos de cada grado deben estar versionados y actualizados. Un ADR que dice "usamos PostgreSQL porque es gratis" pero que fue escrito hace dos anos no sirve si ahora estamos pagando licencias enterprise. La documentacion viva -- docs-as-code, ADRs con cadencia de revision, tech radar interno -- mantiene la coherencia.

**2. Revisiones periodicas.** Una revision arquitectonica trimestral que recorra los cuatro grados: los objetivos de negocio siguen siendo los mismos? Los atributos de calidad siguen priorizados correctamente? Los contratos de API siguen siendo coherentes? El codigo sigue respetando los limites de modulo?

**3. Back-propagation de cambios.** Cuando una decision cambia en un grado, los grados inferiores deben actualizarse. Si un ADR se modifica, los contratos y el codigo que dependian de la decision anterior deben revisarse. Esto no es burocracia; es consistencia.

---

## Proyecto guia: DevCourses recorre los cuatro grados

Vamos a tomar DevCourses -- nuestro companero de viaje durante todo el libro -- y recorrer explicitamente los cuatro grados de diseno, mostrando como cada nivel informa al siguiente y como las decisiones se propagan entre ellos.

### Grado 1: La arquitectura de solucion de DevCourses

Recordemos el contexto del capitulo 1. DevCourses es una plataforma de cursos en linea para desarrolladores. El equipo es de seis personas. El presupuesto es acotado. El mercado es competitivo.

Las decisiones de Grado 1 que enmarcaron todo lo demas:

**Objetivo de negocio:** Alcanzar 50,000 usuarios activos al mes en 12 meses, con una tasa de conversion de prueba gratuita a suscripcion del 8%.

**Restricciones:**
- Presupuesto mensual de infraestructura: maximo $3,000 USD
- Equipo de 6 desarrolladores full-stack
- Time-to-market: MVP en 3 meses
- Regulacion: GDPR para usuarios europeos, facturacion electronica para LATAM

**Decisiones build vs. buy:**
- Build: catalogo, inscripciones, panel de instructor (core del negocio)
- Buy: procesamiento de pagos (Stripe), CDN para video (Cloudflare Stream), autenticacion (Auth0), email transaccional (Postmark)

**Riesgos identificados:**
1. *Picos de carga x10 en lanzamientos de cursos populares.* Mitigacion: diseno para escala horizontal desde el inicio.
2. *Dependencia de Stripe para ingresos.* Mitigacion: abstraer procesador de pagos para poder integrar alternativas.
3. *GDPR compliance.* Mitigacion: aislamiento de datos personales, mecanismo de borrado.

**Criterio de exito:** El MVP permite a un usuario registrarse, suscribirse, explorar el catalogo y ver un curso completo en un flujo ininterrumpido.

Estas decisiones no son de codigo. No mencionan Python, PostgreSQL ni FastAPI. Son decisiones de negocio que restringen el espacio de soluciones tecnicas.

### Grado 2: La arquitectura de software de DevCourses

Con las restricciones del Grado 1 definidas, el equipo toma las decisiones estructurales.

**Atributos de calidad priorizados:**

1. *Disponibilidad:* SLO 99.9% (maximo 43 minutos de downtime al mes).
2. *Latencia:* p95 < 200ms para el catalogo, p95 < 2s para inicio de reproduccion de video.
3. *Mantenibilidad:* Un nuevo feature de complejidad media (agregar un tipo de contenido) en menos de 2 semanas.
4. *Seguridad:* Datos de pago nunca tocan nuestros servidores (PCI DSS delegado a Stripe). Datos personales aislados y borrables.

**ADRs iniciales:**

*ADR-001: Monolito modular, no microservicios.*
- Contexto: Equipo de 6, time-to-market de 3 meses, presupuesto acotado.
- Decision: Un monolito con modulos bien definidos. Los limites de modulo se refuerzan por convenciones y pruebas.
- Alternativa rechazada: Microservicios. Razon: overhead operacional excesivo para el tamano del equipo.
- Consecuencias: Menor complejidad operacional. Mayor riesgo de acoplamiento si no se respetan los limites de modulo.

*ADR-002: PostgreSQL como base de datos principal.*
- Contexto: Necesidad de transacciones ACID para pagos, busqueda full-text para catalogo, JSON para configuracion flexible.
- Decision: PostgreSQL con indices GIN para busqueda y JSONB para datos semi-estructurados.
- Alternativa rechazada: PostgreSQL + Elasticsearch. Razon: complejidad operacional adicional no justificada con 50k usuarios.
- Consecuencias: La busqueda full-text no sera tan sofisticada como con Elasticsearch, pero es suficiente para el MVP. Revisable en 12 meses.

*ADR-003: Comunicacion asincrona para eventos no criticos.*
- Contexto: Notificaciones, analytics y generacion de certificados no necesitan ser sincronos.
- Decision: Redis como broker de mensajes para tareas asincronas (Celery).
- Alternativa rechazada: RabbitMQ. Razon: Redis ya se usa para cache; agregar otro servicio incrementa la complejidad operacional.
- Consecuencias: Redis como broker tiene limitaciones de durabilidad. Aceptable para notificaciones y analytics. Los pagos siguen siendo sincronos.

**Diagrama C4 Nivel 2:**

El diagrama muestra cuatro contenedores principales: la aplicacion web (FastAPI), la base de datos (PostgreSQL), el cache y broker (Redis) y el almacenamiento de video (Cloudflare Stream). Los servicios externos (Stripe, Auth0, Postmark) se muestran como actores externos.

### Grado 3: El diseno de sistemas de DevCourses

Las decisiones de Grado 2 definen la estructura. El Grado 3 la detalla.

**Contratos de API principales:**

El catalogo expone endpoints REST:
```
GET /api/v1/cursos?categoria={cat}&q={busqueda}&page={n}
GET /api/v1/cursos/{id}
POST /api/v1/inscripciones  {usuario_id, curso_id}
GET /api/v1/usuarios/{id}/progreso/{curso_id}
```

Cada endpoint tiene un contrato formal: parametros, tipos, codigos de respuesta, errores posibles, limites de rate. El contrato es el acuerdo entre el frontend y el backend. Cambiarlo requiere un proceso de versionado.

**Flujo critico: inscripcion y pago.**

El diagrama de secuencia del flujo mas importante del sistema:

1. El usuario selecciona un curso y hace clic en "Inscribirme".
2. El frontend envia `POST /api/v1/inscripciones`.
3. El servicio de inscripcion verifica que el usuario tiene acceso (suscripcion activa o pago directo).
4. Si necesita pago, delega al servicio de pagos que crea una sesion de Stripe Checkout.
5. El usuario completa el pago en Stripe.
6. Stripe envia un webhook al backend.
7. El servicio de pagos confirma el pago y emite un evento `pago_completado`.
8. El servicio de inscripcion crea la inscripcion y emite `inscripcion_completada`.
9. Los consumidores asincronos envian email de bienvenida, actualizan analytics y generan acceso al contenido.

**Modelo de datos (decisiones clave):**

- Las cantidades monetarias se almacenan como enteros en centavos (`INTEGER`, no `NUMERIC` ni `FLOAT`).
- La moneda se almacena junto al monto en cada registro (no como configuracion global).
- Los datos personales estan en tablas separadas para facilitar el borrado GDPR.
- El progreso del curso se almacena como registros individuales por leccion (no como porcentaje agregado), como disenamos en el capitulo 14.

**Mecanismos de resiliencia:**

- Cache de catalogo en Redis con TTL de 5 minutos. Invalidacion por eventos de creacion/actualizacion de cursos.
- Circuit breaker para la comunicacion con Stripe. Si Stripe falla, los pagos se encolan y se reintentan con backoff exponencial.
- Rate limiting de 100 requests/minuto por usuario autenticado, 20/minuto para anonimos.
- Health check endpoint que verifica conexion a PostgreSQL, Redis y Cloudflare.

### Grado 4: El diseno de codigo de DevCourses

Finalmente, el nivel donde hemos pasado la mayor parte del libro. Las decisiones de Grado 4 son las que convierten el diseno en codigo funcional.

**Estructura de modulos:**

```
devcourses/
    catalogo/         # Busqueda, listado, categorias, recomendaciones
    inscripciones/    # Inscripcion, acceso, progreso
    pagos/            # Procesamiento, webhooks, facturas
    usuarios/         # Perfiles, autenticacion, preferencias
    video/            # Streaming, progreso de reproduccion
    notificaciones/   # Canales, formateadores, preferencias
    instructor/       # Panel, analytics, gestion de contenido
    compartido/       # Eventos, tipos comunes, utilidades
```

Cada modulo es un paquete de Python con una interfaz publica explicita (un archivo `__init__.py` que exporta solo lo que otros modulos necesitan) y una implementacion privada.

**Limites de modulo en la practica:**

El modulo de catalogo expone:
```python
# catalogo/__init__.py
from catalogo.servicio import ServicioCatalogo
from catalogo.tipos import CursoResumen, CursoDetalle, FiltrosCatalogo
```

El resto -- repositorios, logica de indexacion, algoritmo de busqueda -- es interno. El modulo de pagos no importa nada que no este en `catalogo/__init__.py`. Si lo intenta, es una violacion de limites que las pruebas de arquitectura atrapan.

**Patrones aplicados (solo donde se justifican):**

- *Strategy* para el ordenamiento del catalogo (por popularidad, fecha, relevancia) -- porque hay tres algoritmos que cambian en tiempo de ejecucion segun el usuario.
- *Adapter* para los procesadores de pago (Stripe, MercadoPago) -- porque la decision de Grado 1 identifico el riesgo de dependencia de Stripe.
- *Facade* para la inscripcion -- porque el proceso involucra cinco componentes internos que el controlador no necesita conocer.
- *Observer* (via EventBus) para efectos secundarios de inscripcion -- porque notificaciones, analytics y acceso son independientes y opcionales.
- Ningun *Singleton*, ningun *Abstract Factory*, ningun *Builder*. No porque sean malos, sino porque no resuelven problemas reales en este sistema.

**Estrategia de pruebas:**

- Tests unitarios para invariantes de dominio (reglas de inscripcion, calculo de precios, verificacion de acceso).
- Tests de contrato para las interfaces entre modulos (el catalogo devuelve lo que inscripciones espera).
- Tests de integracion para los flujos criticos (inscripcion completa, pago con webhook).
- Sin mocks excesivos: los repositorios usan una base de datos de prueba, no mocks de la interfaz.

### El recorrido completo: como los grados se conectan

Observa como cada grado alimento al siguiente:

- **Grado 1** dijo: "presupuesto acotado, equipo de 6, picos x10". Eso descarto microservicios (Grado 2) y soluciones caras como Elasticsearch (Grado 3).
- **Grado 2** dijo: "monolito modular, PostgreSQL, Redis". Eso definio la topologia del sistema (Grado 3) y la estructura de modulos (Grado 4).
- **Grado 3** dijo: "contratos REST, eventos asincronos, cache con TTL". Eso guio las interfaces de los modulos (Grado 4) y los patrones a usar.
- **Grado 4** dijo: "el modulo de video tiene latencia inaceptable con S3 directo". Eso subio a Grado 2 (necesitamos un CDN) y a Grado 1 (eso incrementa el presupuesto mensual en $200).

Los grados no son un flujo lineal de arriba hacia abajo. Son un dialogo continuo entre niveles. Las decisiones bajan, las restricciones suben, y el diseno se refina en cada iteracion.

---

## Errores comunes por grado

### Grado 1: Decidir tecnologia antes de entender el problema

"Vamos a usar Kubernetes" no es una decision de arquitectura de solucion. Es una decision de infraestructura que pertenece a los Grados 2-3. En Grado 1, la pregunta es "necesitamos escalar horizontalmente?" y la respuesta deberia basarse en los objetivos de negocio, no en la moda tecnologica.

### Grado 2: Confundir arquitectura con eleccion de framework

"Nuestra arquitectura es FastAPI + React" no es arquitectura de software. Es una lista de herramientas. La arquitectura de software responde preguntas sobre propiedades del sistema: latencia, disponibilidad, mantenibilidad. El framework es una herramienta que puede o no ayudar a lograr esas propiedades.

### Grado 3: Copiar recetas sin entender los trade-offs

"Vamos a usar Event Sourcing porque lo usa Netflix" es el equivalente de copiar la tarea del alumno mas inteligente sin entender la materia. Event Sourcing resuelve problemas especificos (auditoria, reconstruccion de estado, multiples vistas) y crea problemas nuevos (complejidad de queries, eventual consistency). Si no tienes los problemas que resuelve, solo tendras los que crea.

### Grado 4: Sobreingeniar el codigo sin necesidad real

El anti-patron de Pattern-itis que discutimos en el capitulo 13. Aplicar patrones de diseno por el gusto de usarlos, no porque resuelvan un problema concreto. Seis clases y una factory para responder "esta inscrito este usuario en este curso?" cuando una funcion de tres lineas hace lo mismo.

---

## El grado como filtro de complejidad

Hay una forma de pensar en los grados que resulta especialmente util en la practica diaria: cada grado actua como un filtro de complejidad para los grados inferiores.

Una buena decision de Grado 1 reduce la complejidad que enfrenta el Grado 2. Si defines bien los objetivos de negocio, el Grado 2 no tiene que adivinar que atributos de calidad priorizar. Una buena decision de Grado 2 reduce la complejidad del Grado 3. Si el ADR dice "monolito modular", el Grado 3 no tiene que disenar comunicacion entre servicios distribuidos. Una buena decision de Grado 3 reduce la complejidad del Grado 4. Si los contratos de API estan bien definidos, los modulos de codigo pueden implementarse de forma independiente.

La complejidad que no se filtra en un grado se acumula en los grados inferiores. Si Grado 1 no define restricciones de presupuesto, Grado 2 no sabe si puede proponer soluciones costosas. Si Grado 2 no documenta los trade-offs, Grado 3 toma decisiones a ciegas. Si Grado 3 no define contratos, Grado 4 sufre con integraciones fragiles.

Esto conecta directamente con el principio de ocultamiento de informacion del capitulo 6. Cada grado oculta un tipo de complejidad del grado inferior:

- Grado 1 oculta la complejidad de negocio (por que construimos esto).
- Grado 2 oculta la complejidad estructural (por que esta arquitectura y no otra).
- Grado 3 oculta la complejidad de integracion (como se comunican los componentes).
- Grado 4 oculta la complejidad de implementacion (como se resuelve cada problema internamente).

Cuando cada grado hace bien su trabajo de filtrado, los desarrolladores en Grado 4 pueden enfocarse en escribir buen codigo sin preocuparse por decisiones que estan fuera de su alcance. Cuando un grado falla, la complejidad se derrama hacia abajo y todos sufren.

---

## Cuando un problema cruza grados

Los problemas mas dificiles en el diseno de software son los que cruzan grados. "El catalogo es lento" puede ser un problema de Grado 4 (query mal escrita), de Grado 3 (cache mal disenado), de Grado 2 (la decision de usar PostgreSQL para busqueda full-text no escala) o de Grado 1 (los objetivos de latencia nunca se definieron formalmente).

La estrategia para abordar problemas multi-grado es la misma que usaria un medico con un paciente complejo: empieza por el diagnostico antes de prescribir tratamiento.

1. **Identifica los sintomas en cada grado.** En Grado 4: queries N+1? En Grado 3: cache sin invalidacion? En Grado 2: SLO sin definir? En Grado 1: prioridad del catalogo vs. otras funcionalidades?

2. **Encuentra la causa raiz en el grado mas alto posible.** La causa raiz es la decision (o la ausencia de decision) que genera los sintomas en los grados inferiores.

3. **Resuelve de arriba hacia abajo.** Corrige la decision de alto nivel primero. Luego deja que la correccion se propague hacia abajo.

4. **Aplica soluciones temporales si es necesario.** A veces no puedes arreglar la causa raiz inmediatamente (quiza cambiar de base de datos es un proyecto de meses). En ese caso, aplica soluciones en grados inferiores como medida temporal, pero documenta la causa raiz y planifica la correccion real.

Esta es la version macro del principio de Polya que veremos en el capitulo final: entender el problema antes de resolverlo. Los grados son el marco que te ayuda a entender *donde* esta el problema antes de intentar resolverlo.

---

## Aplica esto el lunes

1. **Identifica el grado de tu problema actual.** Toma la tarea mas importante de tu sprint. En que grado se encuentra el problema que estas resolviendo? Estas trabajando en el grado correcto o estas aplicando una solucion de Grado 4 a un problema de Grado 2?

2. **Audita un grado completo.** Escoge un grado (recomiendo empezar por el 2, que es el mas frecuentemente ignorado) y responde las preguntas del checklist. Cuantas puedes responder con confianza? Las que no puedes responder son vacios en tu diseno.

3. **Dibuja el mapa de grados de tu sistema.** En una pagina, escribe las decisiones principales de cada grado para tu sistema actual. Estan conectadas? Las decisiones de Grado 1 informan a Grado 2? Las de Grado 3 son coherentes con las de Grado 2?

4. **Identifica una decision que esta en el grado equivocado.** Busca una decision que se tomo en Grado 4 (por ejemplo, "usamos Redis para esto") que en realidad es una decision de Grado 3 o Grado 2. Deberia estar documentada como ADR? Deberia tener un analisis de trade-offs?

5. **Practica el diagnostico multi-grado.** La proxima vez que alguien reporte un problema, antes de abrir el editor de codigo, preguntate: en que grado se origina este problema? Subelo lo mas alto que puedas antes de empezar a resolverlo.

---

## Referencias del capitulo

- Bass, L., Clements, P., y Kazman, R. (2021). *Software Architecture in Practice*. 4th Edition. Addison-Wesley.
- Fowler, M. (2003). "Who Needs an Architect?" *IEEE Software*, 20(5), 11-13.
- Ousterhout, J. (2018). *A Philosophy of Software Design*. Yaknyam Press.
- Parnas, D. L. (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 15(12), 1053-1058.
- Richards, M. y Ford, N. (2020). *Fundamentals of Software Architecture*. O'Reilly Media.
