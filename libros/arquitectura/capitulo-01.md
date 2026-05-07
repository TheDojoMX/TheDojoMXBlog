# Capitulo 1: Tu codigo funciona, pero eso no es suficiente

> "Tu codigo funciona. Todas las pruebas pasan. El cliente esta contento. Entonces, por que cada nueva funcion tarda el doble que la anterior?"

---

## La historia del proyecto que nadie quiere tocar

En alguna empresa -- puede que en la tuya -- existe un sistema al que todos le dicen "el monolito". Nadie recuerda exactamente cuando empezo a ser inmanejable. Lo que si recuerdan es el momento en que dejaron de querer tocarlo.

Ernesto fue el primer desarrollador. Escribio la version inicial en tres meses: un backend en Python con Flask, una base de datos PostgreSQL, y un frontend en React. Todo funcionaba. El formulario de registro funcionaba. El carrito de compras funcionaba. El checkout con Stripe funcionaba. El equipo celebro el lanzamiento con pizza y cerveza.

Seis meses despues, Diana se unio al equipo. Su primera tarea: agregar un campo de "idioma preferido" al perfil de usuario. Parecia sencillo. Cuatro dias despues, Diana seguia encontrando archivos que necesitaban el cambio. El campo de idioma estaba implicito en la forma en que se generaban los correos, en como se construian las URLs, en la logica del buscador, y en un script de reportes que nadie sabia que existia. Cuando finalmente abrio el pull request, tocaba 14 archivos.

Un ano despues, el equipo habia crecido a cinco personas. Ya nadie celebraba lanzamientos. Los estimados eran impredecibles. "Agregar certificados de curso" -- que parecia un proyecto de una semana -- tomo un mes y medio. El deploy del viernes se convirtio en un ritual temido. Y la frase mas escuchada en los stand-ups era: "Esto se tardo porque tuve que entender como funcionaba la parte de [inserte modulo aqui]."

El codigo funcionaba. Nunca dejo de funcionar. Pero se habia convertido en un sistema que era progresivamente mas caro de cambiar.

Esta historia no es excepcional. Es la norma. Segun un analisis de CAST de 2025 que cubrio 47,000 aplicaciones en 3,000 empresas, el rezago acumulado de deuda tecnica a nivel global alcanzo 61 mil millones de dias-hombre de trabajo, una cifra que crece cada trimestre conforme los equipos apilan codigo nuevo sobre cimientos viejos [CAST, 2025]. Gartner estima que para 2026, el 80% de toda la deuda tecnica sera *arquitectonica* -- no algo que un sprint de refactorizacion pueda arreglar, sino algo que requiere rediseno deliberado del sistema [Gartner, 2025].

No es un problema de talento. Es un problema de diseno.

**Takeaway:** El software que "funciona" no es necesariamente software bien disenado. La diferencia se manifiesta con el tiempo, en la velocidad con la que puedes cambiarlo.

---

## Por que el software "que funciona" se vuelve inmanejable

Fred Brooks, en su legendario ensayo "No Silver Bullet" de 1986, establecio una distincion que sigue siendo fundamental: la diferencia entre complejidad *esencial* y complejidad *accidental* [Brooks, 1986].

La complejidad esencial es la inherente al problema que estas resolviendo. Si construyes un sistema de pagos, tienes que lidiar con impuestos, monedas, contracargos, regulaciones PCI, y estados de transaccion. Eso no se puede simplificar. Es la naturaleza del dominio.

La complejidad accidental es todo lo demas: es la complejidad que tu introduces con tus decisiones (o con la ausencia de ellas). Es el archivo de configuracion que duplicaste porque "era mas rapido". Es el modulo que tiene tres responsabilidades porque "de todos modos estan relacionadas". Es la abstraccion que no hiciste porque "todavia no la necesitamos".

La razon por la que el software que funciona se vuelve inmanejable es simple: **la complejidad accidental se acumula silenciosamente.** Cada decision rapida que tomas -- cada atajo, cada copia-pega, cada "despues lo limpio" -- anade una capa delgada de complejidad accidental. Cada capa es casi invisible. Pero como el sedimento en un rio, se acumula hasta que un dia descubres que el cauce esta bloqueado.

Brian Kernighan lo puso de manera aun mas directa:

> "Controlar la complejidad es la esencia de la programacion." [Kernighan & Plauger, 1978]

Los desarrolladores gastan, en promedio, el 33% de su tiempo resolviendo problemas causados por deuda tecnica. En bases de codigo mal mantenidas, esa cifra sube al 50-80% [CAST, 2025]. Para una startup con cinco desarrolladores ganando $100,000 dolares al ano cada uno, eso equivale a $125,000 dolares anuales gastados no en construir valor, sino en pelear contra decisiones pasadas.

Piensalo asi: no es que el software se "pudra" como la fruta. Es que cada decision que tomas reduce o expande el espacio de decisiones futuras. Un buen diseno expande tus opciones. Un mal diseno las contrae. Y cuando tus opciones se contraen lo suficiente, llegas al punto en que "es mas facil hacerlo de nuevo".

Joel Spolsky llamo a esta situacion "lo peor que una empresa de software puede hacer" cuando analizo el caso de Netscape. En el ano 2000, Netscape decidio reescribir su navegador desde cero. Les tomo tres anos. Durante esos tres anos, no pudieron agregar funciones, no pudieron responder a la amenaza de Internet Explorer, y tuvieron que sentarse a ver como Microsoft devoraba su mercado [Spolsky, 2000]. La reescritura completa no es la solucion al mal diseno; es la consecuencia ultima de ignorar el diseno durante demasiado tiempo.

Healthcare.gov es otro caso emblematico. El presupuesto original de $93.7 millones de dolares se inflo a $1.7 mil millones. El lanzamiento en octubre de 2013 fue un desastre: el sistema no podia manejar el trafico, los modulos no se comunicaban entre si, y el login era un cuello de botella peor que el sitio principal. La causa raiz no fue tecnica en el sentido de "no sabian programar". La causa fue arquitectonica: 33 proveedores diferentes, sin un responsable de la arquitectura general, sin pruebas de integracion, sin una vision unificada del sistema [HHS OIG, 2016].

**Takeaway:** La complejidad accidental es silenciosa y acumulativa. No la introduces con una sola decision mala, sino con cientos de pequenas decisiones no reflexionadas.

---

## Disenar es decidir (lo hagas conscientemente o no)

Aqui hay una verdad incomoda: **tu ya estas disenando tu software.** La pregunta no es si disenas o no. La pregunta es si lo haces de forma consciente o inconsciente.

Cada vez que decides donde poner una funcion, como nombrar una variable, que parametros recibe un metodo, que modulo se comunica con cual, o que datos expone una API -- estas tomando decisiones de diseno. Si no las piensas, las tomas por defecto. Y las decisiones por defecto rara vez son buenas.

John Ousterhout, profesor de Stanford y autor de *A Philosophy of Software Design*, lo plantea asi: la tarea principal del desarrollador no es escribir codigo que funcione, sino **disenar sistemas que resistan el cambio** [Ousterhout, 2018]. En una entrevista de abril de 2025 con The Pragmatic Engineer, Ousterhout argumento que el diseno importa *mas* ahora con la inteligencia artificial, no menos. Cuando las herramientas de IA pueden generar codigo a velocidades sin precedente, lo que se vuelve escaso -- y por lo tanto valioso -- es la capacidad de decidir *que* codigo debe existir y *como* debe estar organizado.

El DORA Report 2025 confirma esto con datos empiricos: el 90% de los desarrolladores ya usa alguna forma de asistencia de IA en su trabajo diario, y mas del 80% cree que la IA ha aumentado su productividad. Pero el hallazgo mas revelador es que **la IA no arregla equipos disfuncionales**. La IA actua como amplificador: los equipos con buenos fundamentos de ingenieria mejoran; los que no los tienen, empeoran [DORA, 2025]. La arquitectura, el diseno, las pruebas, y la observabilidad son *mas* importantes que nunca, no menos.

Disenar es decidir. Y las decisiones tienen niveles. No es lo mismo decidir "vamos a usar PostgreSQL" que decidir "esta funcion va a recibir tres parametros en vez de siete". Ambas son decisiones de diseno, pero operan en escalas diferentes.

**Takeaway:** No hay codigo sin diseno. Si no decides conscientemente, las decisiones se toman por inercia -- y la inercia favorece la complejidad.

---

## Los cuatro grados de diseno: de la solucion al codigo

Para pensar con claridad sobre el diseno, necesitamos un mapa. A lo largo de mi experiencia disenando sistemas y ensenando a otros a hacerlo, he encontrado util dividir las decisiones de diseno en cuatro niveles, ordenados de lo mas abstracto a lo mas concreto. Los llamo *grados de diseno* porque no son categorias rigidas sino puntos en un espectro continuo.

### Grado 1: Arquitectura de soluciones

Este es el nivel mas alto. Aqui las preguntas son: *Que estamos construyendo? Para quien? Con que restricciones?*

No se trata de tecnologia todavia. Se trata de proposito. Las decisiones en este nivel incluyen:

- Construir vs. comprar
- Alcance del producto minimo viable
- Dependencias externas criticas
- Restricciones de presupuesto, regulacion y tiempo

**Ejemplo en DevCourses:** Antes de escribir una sola linea de codigo, hay que decidir si el sistema de video sera propio o usaremos un servicio como Mux o Cloudflare Stream. Hay que decidir si los pagos seran directos (Stripe) o a traves de un marketplace. Estas decisiones definen el campo de juego.

### Grado 2: Arquitectura de software

Aqui decidimos las grandes estructuras del sistema y los atributos de calidad que priorizamos.

Las preguntas son: *Que tan rapido debe responder? Que tan disponible? Que tan seguro? Como se estructura en grandes bloques?*

Las decisiones en este nivel incluyen:

- Monolito modular vs. microservicios
- Sincrono vs. asincrono
- Estrategia de caching y colas
- Observabilidad y monitoreo

**Ejemplo en DevCourses:** Decidimos que sera un monolito modular (no microservicios, porque somos un equipo de seis) con PostgreSQL como base de datos principal, Redis para cache y colas, y S3 para almacenamiento de video. Priorizamos latencia baja en el catalogo (p95 < 200ms) y alta disponibilidad (SLO 99.9%).

### Grado 3: Diseno de sistemas

Aqui definimos la topologia interna: como se comunican los componentes, como fluyen los datos, como se escala.

Las preguntas son: *Que contratos tienen los modulos entre si? Como fluye una solicitud desde el usuario hasta la respuesta?*

Las decisiones en este nivel incluyen:

- Modelos de datos y esquemas
- Contratos de API (endpoints, formatos, versionado)
- Flujos de secuencia para operaciones criticas
- Estrategias de resiliencia (circuit breakers, retries, backpressure)

**Ejemplo en DevCourses:** Definimos que el flujo de "compra de curso" pasa por: autenticacion -> validacion de disponibilidad -> procesamiento de pago -> otorgamiento de acceso -> notificacion. Cada paso tiene un contrato definido. El pago es asincrono con confirmacion via webhook.

### Grado 4: Diseno de codigo

Este es el nivel mas cercano a la implementacion. Aqui es donde la mayoria de los libros de "codigo limpio" se enfocan, pero es solo la punta del iceberg.

Las preguntas son: *Como se organizan los modulos? Que interfaces exponen? Que patrones usamos? Como probamos?*

Las decisiones en este nivel incluyen:

- Organizacion de paquetes y modulos
- Interfaces publicas de cada modulo
- Patrones de diseno especificos
- Estrategia de pruebas
- Convenciones de nombres y estilo

**Ejemplo en DevCourses:** El modulo de pagos expone una interfaz simple: `procesar_pago(usuario_id, curso_id)`. Internamente, resuelve el metodo de pago del usuario, aplica cupones, calcula impuestos, y se comunica con Stripe. Nada de eso lo ve el codigo que lo llama.

### La relacion entre los niveles

Los cuatro grados no son independientes. Fluyen de arriba hacia abajo y de abajo hacia arriba:

```
  Grado 1: Arquitectura de soluciones
       |
       v
  Grado 2: Arquitectura de software
       |
       v
  Grado 3: Diseno de sistemas
       |
       v
  Grado 4: Diseno de codigo
```

Las decisiones de arriba restringen las de abajo. Si en Grado 1 decidiste que el presupuesto es limitado, en Grado 2 no puedes elegir una arquitectura de microservicios con Kubernetes. Si en Grado 2 decidiste un monolito modular, en Grado 3 los contratos entre modulos son llamadas a funciones, no APIs HTTP.

Pero la informacion tambien fluye hacia arriba. Si en Grado 4 descubres que dos modulos siempre se cambian juntos, eso retroalimenta al Grado 3 (quizas deberian ser un solo modulo) y potencialmente al Grado 2 (quizas la frontera que definiste no era la correcta).

**La mayoria de los equipos operan casi exclusivamente en el Grado 4**, y luego se sorprenden cuando su sistema tiene problemas arquitectonicos. Es como intentar construir un edificio decidiendo solo que ladrillos usar, sin planos.

**Takeaway:** El diseno de software opera en cuatro niveles, desde las decisiones de negocio hasta la organizacion del codigo. Operar solo en el nivel del codigo es como navegar mirando unicamente el suelo.

---

## Presentando DevCourses: el proyecto que nos acompanara

A lo largo de este libro, vamos a disenar y redisenar un sistema real: **DevCourses**, una plataforma de cursos en linea para desarrolladores.

Este no es un ejemplo de juguete. DevCourses enfrenta los mismos problemas que enfrenta cualquier aplicacion web con usuarios reales: escalabilidad, pagos, contenido multimedia, busqueda, y la presion constante de "agregar features".

### El contexto

- **Equipo:** 6 desarrolladores (2 senior, 2 mid, 2 junior)
- **Usuarios:** 50,000 activos al mes, con picos de 10x durante lanzamientos de cursos populares
- **Presupuesto:** Limitado. Es una startup con financiamiento seed.
- **Stack inicial:** Python/FastAPI + PostgreSQL + Redis + S3 para video
- **Presion de mercado:** Time-to-market corto. Competencia con Udemy, Platzi, Coursera.

### Los modulos del sistema

1. **Catalogo de cursos:** Listado, busqueda, filtros, recomendaciones basicas
2. **Reproduccion de video:** Streaming adaptativo, progreso del estudiante, marcadores
3. **Pagos y suscripciones:** Compra individual, suscripcion mensual/anual, cupones
4. **Usuarios y perfiles:** Registro, autenticacion, perfil, historial de aprendizaje
5. **Comentarios y discusiones:** Foros por leccion, respuestas anidadas, moderacion
6. **Notificaciones:** Email, push, in-app
7. **Panel de instructor:** Creacion de contenido, subida de video, analytics de audiencia

### El estado actual: DevCourses v0.1

Ernesto, nuestro primer desarrollador, lanzo la primera version en tres meses. Funciona. Pero el codigo vive en una estructura como esta:

```
devcourses/
    app.py              # 2,200 lineas. Rutas, logica de negocio, queries SQL, todo junto.
    models.py           # 800 lineas. Todos los modelos en un archivo.
    utils.py            # 1,100 lineas. "Utilidades" que van desde formateo de fechas
                        # hasta calculo de precios con descuento.
    templates/          # 45 archivos HTML con logica de negocio en los templates.
    static/             # CSS, JS, imagenes.
    config.py           # 30 lineas. Lo unico razonablemente organizado.
```

La funcion principal del archivo `app.py` se ve mas o menos asi:

```python
@app.post("/comprar-curso")
def comprar_curso():
    usuario_id = session["usuario_id"]
    curso_id = request.form["curso_id"]

    # Verificar que el curso existe
    curso = db.execute("SELECT * FROM cursos WHERE id = %s", curso_id)
    if not curso:
        return error("Curso no encontrado")

    # Verificar que no lo haya comprado ya
    compra = db.execute(
        "SELECT * FROM compras WHERE usuario_id = %s AND curso_id = %s",
        usuario_id, curso_id
    )
    if compra:
        return error("Ya tienes este curso")

    # Obtener precio (con descuento si aplica)
    precio = curso["precio"]
    cupon = request.form.get("cupon")
    if cupon:
        desc = db.execute("SELECT * FROM cupones WHERE codigo = %s", cupon)
        if desc and desc["activo"] and desc["usos"] < desc["max_usos"]:
            precio = precio * (1 - desc["porcentaje"] / 100)
            db.execute("UPDATE cupones SET usos = usos + 1 WHERE id = %s", desc["id"])

    # Cobrar con Stripe
    try:
        charge = stripe.Charge.create(
            amount=int(precio * 100),
            currency="usd",
            customer=get_stripe_customer(usuario_id),
        )
    except stripe.error.CardError as e:
        return error("Error en el pago: " + str(e))

    # Registrar compra
    db.execute(
        "INSERT INTO compras (usuario_id, curso_id, monto, stripe_id, fecha) "
        "VALUES (%s, %s, %s, %s, NOW())",
        usuario_id, curso_id, precio, charge["id"]
    )

    # Dar acceso
    db.execute(
        "INSERT INTO accesos (usuario_id, curso_id, fecha_inicio) "
        "VALUES (%s, %s, NOW())",
        usuario_id, curso_id
    )

    # Notificar
    enviar_email(usuario_id, "compra_exitosa", {"curso": curso["titulo"], "monto": precio})
    enviar_push(usuario_id, f"Ya tienes acceso a {curso['titulo']}")

    # Analytics
    registrar_evento("compra", {"usuario": usuario_id, "curso": curso_id, "monto": precio})

    return redirect("/mis-cursos")
```

Este codigo funciona. Puedes comprarlo, deployarlo, cobrarle a usuarios reales. Pero observa todo lo que sabe esta sola funcion:

- Como se estructura la tabla de cursos
- Como se estructura la tabla de compras
- La logica de validacion de cupones
- Los detalles de la API de Stripe
- La estructura de la tabla de accesos
- Como enviar emails y notificaciones push
- Como registrar eventos de analytics
- El formato de las URLs de redireccion

Esta funcion tiene *conocimiento de todo el sistema*. Y eso es exactamente lo que hace que el sistema sea dificil de cambiar. Cuando necesites agregar "suscripciones" ademas de compras individuales, vas a tener que modificar esta funcion y probablemente otras quince como ella.

### La evolucion planeada

A lo largo de este libro, DevCourses va a evolucionar:

- **Capitulos 1-3:** Diagnosticamos el monolito sin estructura y entendemos por que duele.
- **Capitulos 4-6:** Lo descomponemos en modulos, definimos interfaces y ocultamos informacion.
- **Capitulos 7-9:** Profundizamos los modulos, aplicamos cohesion y acoplamiento, decidimos que juntar y que separar.
- **Capitulos 10-12:** Aplicamos patrones, manejamos dependencias, y refinamos las abstracciones.
- **Capitulos 13-15:** Integramos capas, conectamos con el mundo exterior, y pulimos la arquitectura.
- **Capitulo 16:** El sistema completo, revisado, con lecciones aprendidas.

No vamos a pretender que el diseno perfecto existe desde el dia uno. Vamos a disenar, equivocarnos, aprender, y redisenar. Porque asi funciona en la realidad.

**Takeaway:** DevCourses es deliberadamente imperfecto al inicio. El objetivo del libro es mostrarte *como pensar* para mejorarlo progresivamente, no darte una receta que puedas copiar.

---

## Ejercicio: diagnostica tu proyecto actual

Antes de seguir leyendo, toma 15 minutos y haz este ejercicio con tu propio proyecto (o el proyecto mas reciente en el que trabajaste). Necesitas una hoja de papel o un documento en blanco.

### Paso 1: Dibuja el mapa (3 minutos)

Dibuja los modulos principales de tu sistema como cajas. Conectalas con flechas que representen dependencias ("A usa B", "C llama a D"). No te preocupes por que sea bonito o preciso. El objetivo es tener una imagen mental de la estructura.

### Paso 2: Identifica el dolor (5 minutos)

Responde estas preguntas:

1. **El ultimo cambio "sencillo":** Piensa en el cambio mas reciente que parecia facil pero tardo mas de lo esperado. Que lo hizo dificil? Cuantos archivos tocaste?

2. **El modulo temido:** Hay un modulo, archivo, o clase al que todos le tienen miedo? Que tiene de especial? Por que nadie quiere tocarlo?

3. **La pregunta sin respuesta:** Si un desarrollador nuevo se uniera a tu equipo hoy y te preguntara "que pasa si cambio X?", podrias responder con confianza para cualquier parte del sistema? Donde *no* podrias?

### Paso 3: Clasifica (5 minutos)

Para cada problema que identificaste, intenta clasificarlo:

- **Complejidad esencial:** "Esto es dificil porque el dominio es dificil." (Ejemplo: la logica de impuestos internacionales.)
- **Complejidad accidental:** "Esto es dificil porque tomamos una mala decision, o no tomamos ninguna." (Ejemplo: toda la logica de negocio esta en un solo archivo.)

### Paso 4: Cuantifica (2 minutos)

Estima, de manera aproximada:

- Que porcentaje de tu tiempo de desarrollo se va en pelear con el sistema existente (vs. construir cosas nuevas)?
- Si pudieras redisenar una sola parte del sistema, cual seria?

Guarda tus respuestas. Vamos a regresar a ellas a lo largo del libro.

**Takeaway:** La autoconciencia es el primer paso del buen diseno. No puedes mejorar lo que no has diagnosticado.

---

## Aplica esto el lunes

Estas son tres acciones concretas que puedes ejecutar el proximo dia laboral. No requieren permiso de nadie ni cambios en el proceso del equipo.

### 1. Haz la "prueba del campo nuevo"

Piensa en un dato que seria razonable agregarle a tu entidad principal (un campo de "idioma" a un usuario, un "tag" a un producto, una "prioridad" a un ticket). Sin escribir codigo, traza mentalmente todos los archivos que tendrias que modificar. Si son mas de cinco, tienes un problema de amplificacion de cambios. Anotalo.

### 2. Escribe la "hoja de induccion"

Escoge el modulo mas complejo de tu sistema. Escribe en un documento todo lo que alguien nuevo necesitaria saber para hacer un cambio seguro en ese modulo. Incluye: que archivos tocar, que otros modulos se afectan, que cosas no son obvias, y que puede salir mal. Si el documento excede media pagina, tienes un problema de carga cognitiva. Si no puedes completar el documento porque *tu mismo* no sabes todo lo que hace el modulo, tienes desconocidos desconocidos.

### 3. Pregunta "y si cambio esto?"

En tu proximo stand-up o conversacion con un companero, escoge un componente del sistema y pregunta: "Si yo cambio la forma en que funciona X, que mas se rompe?" Escucha la respuesta. Si es "no se" o "muchas cosas", documenta eso como un riesgo. Si la respuesta es precisa y corta, felicidades: esa parte del sistema esta bien disenada.

---

## Resumen del capitulo

- El software que funciona no es necesariamente software bien disenado. La diferencia se manifiesta con el tiempo.
- La complejidad accidental se acumula silenciosamente a traves de cientos de decisiones pequenas.
- Disenar es decidir. Si no decides conscientemente, las decisiones se toman por inercia.
- El diseno opera en cuatro grados: arquitectura de soluciones, arquitectura de software, diseno de sistemas, y diseno de codigo. La mayoria de los equipos solo operan en el ultimo.
- DevCourses sera nuestro caso de estudio: una plataforma de cursos con problemas reales que resolveremos progresivamente.
- La autoconciencia es el primer paso. Antes de mejorar tu diseno, necesitas diagnosticarlo.

En el siguiente capitulo, vamos a darle nombre y forma a ese enemigo silencioso que hemos estado describiendo. Vamos a aprender a ver la complejidad, medirla, y entender de donde viene. Porque no puedes combatir lo que no puedes ver.

---

### Referencias

- [Brooks, 1986] Brooks, F. "No Silver Bullet -- Essence and Accident in Software Engineering." *Proceedings of the IFIP Tenth World Computing Conference*, 1986.
- [CAST, 2025] CAST Software. "Coding in the Red: The State of Global Technical Debt, 2025."
- [DORA, 2025] Google Cloud. "2025 DORA Report: State of AI-Assisted Software Development." dora.dev, 2025.
- [Gartner, 2025] Gartner. "Technical Debt and IT Budgets." Market Analysis, 2025.
- [HHS OIG, 2016] U.S. Dept. of Health and Human Services, Office of Inspector General. "HealthCare.gov: Case Study of CMS Management of the Federal Marketplace." 2016.
- [Kernighan & Plauger, 1978] Kernighan, B. W. y Plauger, P. J. *The Elements of Programming Style.* McGraw-Hill, 1978.
- [Ousterhout, 2018] Ousterhout, J. *A Philosophy of Software Design.* Yaknyam Press, 2018.
- [Spolsky, 2000] Spolsky, J. "Things You Should Never Do, Part I." Joel on Software, abril 2000.
