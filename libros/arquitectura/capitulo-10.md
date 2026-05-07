# Capitulo 10: Cohesion y acoplamiento -- los principios que realmente importan

> "Constantine y Yourdon lo entendieron en 1974. Nosotros seguimos redescubriendolo."

---

## Los principios que estaban ahi desde el principio

En 1968, un joven investigador llamado Larry Constantine estaba intentando resolver un problema que hoy suena familiar: por que algunos programas eran faciles de modificar y otros eran una pesadilla? La programacion estructurada estaba en panales, los lenguajes orientados a objetos no existian, y los equipos de software luchaban contra sistemas que se volvian incomprensibles con cada cambio.

Constantine, junto con Edward Yourdon, desarrollo dos conceptos que publicaron formalmente en 1974 en el IBM Systems Journal y luego expandieron en su libro *Structured Design* de 1979 [Stevens, Myers y Constantine, 1974; Yourdon y Constantine, 1979]. Esos conceptos eran *cohesion* y *acoplamiento*. Y medio siglo despues, siguen siendo las herramientas mas utiles que un disenador de software puede tener.

Lo notable no es que estos conceptos hayan sobrevivido cincuenta anos. Lo notable es que cada decada, la industria los "redescubre" con un nombre nuevo. SOLID es, en gran medida, una reformulacion de cohesion y acoplamiento para la era de la orientacion a objetos. Los microservicios son una aplicacion de cohesion y acoplamiento a la arquitectura distribuida. Domain-Driven Design organiza los bounded contexts alrededor de -- adivina -- cohesion y acoplamiento. Incluso las arquitecturas de modulos de los lenguajes modernos (paquetes en Go, crates en Rust, modulos en JavaScript) son mecanismos para gestionar cohesion y acoplamiento.

Cada vez que la industria inventa un acronimo nuevo para describir "pon las cosas relacionadas juntas y manten separadas las cosas que no lo estan", esta redescubriendo a Constantine y Yourdon.

Este capitulo va a tomarse en serio estos dos conceptos. No como ideas abstractas que se mencionan en el primer dia de un curso de ingenieria de software y luego se olvidan. Como herramientas concretas, medibles, y mas utiles que cualquier principio SOLID individual.

**Takeaway:** Cohesion y acoplamiento fueron articulados en los anos 70 y siguen siendo los indicadores mas confiables de la salud de un diseno de software. Si los dominas, el 80% de las decisiones de diseno se vuelven intuitivas.

---

## Cohesion: que tan relacionadas estan las piezas DENTRO de un modulo

### La definicion precisa

La cohesion es una medida de que tan fuertemente se relacionan entre si los elementos de un modulo. Un modulo tiene *alta cohesion* cuando todos sus elementos contribuyen a un mismo proposito. Tiene *baja cohesion* cuando sus elementos hacen cosas dispares que no tienen relacion conceptual.

Constantine lo definio asi:

> "La cohesion es la medida en que los elementos de un modulo se relacionan entre si." [Constantine y Yourdon, 1979]

"Elementos" puede significar funciones, clases, metodos, variables, tipos -- cualquier cosa que viva dentro de la frontera del modulo. Y "relacionarse" significa que contribuyen a la misma tarea, operan sobre los mismos datos, o participan en el mismo proceso.

La intuicion es simple: un modulo cohesivo es un modulo donde si le preguntas a alguien "de que se trata este modulo?", la respuesta es una sola oracion. "Este modulo maneja las inscripciones." "Este modulo procesa los pagos." "Este modulo genera recomendaciones." Si la respuesta es "este modulo maneja inscripciones, genera reportes y envia notificaciones", la cohesion es baja.

### Por que la cohesion importa

Un modulo con alta cohesion tiene tres propiedades practicas que importan en el dia a dia:

**1. Es mas facil de entender.** Si todos los elementos del modulo trabajan hacia el mismo objetivo, entender uno te da contexto para entender los demas. Cuando lees una funcion en el modulo de pagos, ya sabes que el contexto es pagos. Tu mente no tiene que cambiar de contexto entre "esto es de pagos" y "esto es de notificaciones".

**2. Es mas facil de cambiar.** Cuando un requisito de negocio cambia -- digamos, las reglas de inscripcion ahora requieren verificar la edad del usuario -- sabes exactamente donde hacer el cambio: en el modulo de inscripciones. Si el modulo de inscripciones tambien manejara notificaciones y reportes, tendrias que navegar entre codigo de tres dominios diferentes para encontrar donde agregar la verificacion de edad.

**3. Es mas facil de probar.** Un modulo cohesivo tiene un ambito claro: le das entradas del dominio X y esperas salidas del dominio X. Las pruebas son directas. Un modulo con baja cohesion necesita setup de multiples dominios para cada prueba, porque los elementos estan entrelazados con preocupaciones dispares.

Estas tres propiedades conectan directamente con los tres sintomas de complejidad que identificamos en el capitulo 1: *amplificacion de cambios* (baja cohesion causa que un cambio afecte multiples conceptos), *carga cognitiva* (baja cohesion obliga a mantener multiples contextos en la cabeza), y *desconocidos desconocidos* (baja cohesion aumenta la probabilidad de que un cambio en un dominio afecte otro dominio de forma inesperada).

### Los siete niveles de cohesion

Constantine y Yourdon no se conformaron con decir "alta cohesion buena, baja cohesion mala". Identificaron siete niveles de cohesion, ordenados de peor a mejor. Estos niveles fueron elaborados inicialmente por Constantine en los anos 60 y formalizados en las publicaciones de los 70. Veamoslos con ejemplos modernos.

#### Nivel 7 (peor): Cohesion coincidental

Los elementos del modulo no tienen ninguna relacion entre si. Estan juntos por accidente, tipicamente porque alguien necesitaba un lugar donde poner codigo y este archivo estaba disponible.

```python
# utils.py -- el clasico vertedero de funciones
def formatear_fecha(fecha): ...
def calcular_impuesto(monto, pais): ...
def enviar_email(destinatario, asunto, cuerpo): ...
def generar_thumbnail(imagen, tamano): ...
def validar_tarjeta_credito(numero): ...
```

Cinco funciones que no tienen nada que ver entre si. Si le preguntas a alguien "de que se trata utils.py?", la respuesta es "de todo y de nada". Es el cajon de sastre del software.

**En DevCourses:** El equipo original creo un archivo `helpers.py` con funciones de formateo de fechas, validacion de emails, generacion de IDs, y calculo de precios con descuento. Ninguna relacion entre ellas. La unica razon por la que estaban juntas era que no pertenecian a ningun modulo especifico. Esto es cohesion coincidental: la forma mas debil posible.

#### Nivel 6: Cohesion logica

Los elementos del modulo hacen cosas *similares en naturaleza* pero para propositos completamente diferentes. Estan agrupados por categoria general, no por funcion.

```python
# formateadores.py
def formatear_fecha(fecha): ...
def formatear_moneda(monto, simbolo): ...
def formatear_nombre(nombre, apellido): ...
def formatear_direccion(calle, ciudad, pais): ...
def formatear_telefono(numero, codigo_pais): ...
```

Todas las funciones "formatean" algo. Pero formatear una fecha no tiene nada que ver con formatear un telefono. Si cambian las reglas de formato de moneda, no deberia importarle al formato de fechas. Estan juntas por una coincidencia linguistica (todas son "formateadoras"), no por una relacion funcional.

**En DevCourses:** Un archivo `validaciones.py` que contiene `validar_email()`, `validar_tarjeta_credito()`, `validar_cupon()`, `validar_contrasena()`. Todas "validan" algo, pero los dominios son completamente diferentes. La validacion de cupones pertenece al modulo de pagos. La validacion de contrasenas pertenece al modulo de usuarios. Juntarlas por ser "validaciones" es agrupar por verbo, no por concepto.

#### Nivel 5: Cohesion temporal

Los elementos del modulo se ejecutan al mismo tiempo, pero no se relacionan funcionalmente. Tipicamente son tareas de "inicio" o "limpieza" del sistema.

```python
# startup.py
def inicializar_base_de_datos(): ...
def cargar_configuracion(): ...
def conectar_cache(): ...
def registrar_handlers_de_errores(): ...
def iniciar_worker_de_emails(): ...
```

Todas se ejecutan al arrancar el sistema. Pero no comparten datos, no comparten logica, y si cambias una no afecta a las demas. Estan juntas porque suceden "al mismo tiempo", no porque se relacionen.

Esta es exactamente la *descomposicion temporal* que discutimos en el capitulo 7. Es una de las trampas mas comunes en el diseno de software.

**En DevCourses:** Un modulo `cleanup.py` que al final de cada dia ejecuta: `archivar_sesiones_expiradas()`, `limpiar_cache_de_thumbnails()`, `enviar_reporte_diario()`, `verificar_renovaciones_de_suscripcion()`. Cuatro tareas que suceden al mismo momento pero que no tienen relacion conceptual alguna.

#### Nivel 4: Cohesion procedural

Los elementos del modulo participan en un mismo proceso secuencial, pero cada uno trabaja con datos diferentes y resuelve un problema diferente.

```python
# procesar_pedido.py
def verificar_inventario(producto_id): ...
def calcular_envio(direccion, peso): ...
def procesar_pago(tarjeta, monto): ...
def enviar_confirmacion(email, pedido): ...
```

Estas funciones son los pasos de un proceso ("procesar pedido"), pero cada una opera en un dominio diferente: inventario, logistica, finanzas, comunicacion. Que esten juntas porque son pasos secuenciales del mismo flujo es descomposicion temporal disfrazada.

Sin embargo, hay un matiz importante: si estas funciones comparten *contexto* (el pedido actual) y ese contexto solo tiene sentido dentro de este flujo, la cohesion procedural puede ser aceptable. El problema surge cuando los pasos son reutilizables fuera del flujo -- lo cual es casi siempre el caso.

**En DevCourses:** Este es exactamente el ejemplo del capitulo 7 con `ValidadorInscripcion`, `ProcesadorInscripcion` y `NotificadorInscripcion`. Tres clases que son los pasos de un flujo, pero que comparten contexto y datos. La solucion que encontramos fue unirlas en `ServicioInscripcion` -- un modulo con cohesion funcional.

#### Nivel 3: Cohesion comunicacional

Los elementos del modulo operan sobre los mismos datos. No necesariamente hacen lo mismo, pero comparten la fuente de informacion.

```python
# reporte_usuario.py
def obtener_historial_compras(usuario_id): ...
def calcular_gasto_total(usuario_id): ...
def obtener_cursos_completados(usuario_id): ...
def generar_certificado(usuario_id, curso_id): ...
```

Todas las funciones operan sobre el mismo dato: el usuario. Comparten la fuente de informacion (la base de datos de usuarios y sus actividades). Es una relacion mas fuerte que la procedural porque el vinculo no es temporal ("se ejecutan en secuencia") sino informacional ("operan sobre lo mismo").

**En DevCourses:** El modulo de perfil de usuario que agrupa: `obtener_perfil()`, `actualizar_preferencias()`, `calcular_progreso_general()`, `obtener_certificados()`. Todas operan sobre datos del usuario. La cohesion es comunicacional porque comparten la misma fuente de datos, aunque las funciones hacen cosas conceptualmente diferentes (presentacion, configuracion, analisis, certificacion).

#### Nivel 2: Cohesion secuencial

Los elementos del modulo estan conectados porque la salida de uno es la entrada del siguiente. Forman un pipeline de transformacion.

```python
# pipeline_video.py
def extraer_audio(video_raw) -> audio: ...
def normalizar_volumen(audio) -> audio_normalizado: ...
def generar_subtitulos(audio_normalizado) -> subtitulos: ...
def combinar(video_raw, audio_normalizado, subtitulos) -> video_final: ...
```

Cada funcion toma la salida de la anterior. Los datos fluyen en una cadena de transformaciones. Esto es mas cohesivo que la cohesion comunicacional porque no solo comparten datos, sino que los datos se *transforman* progresivamente hacia un resultado.

**En DevCourses:** El pipeline de procesamiento de videos que los instructores suben: `validar_formato()` -> `transcodificar()` -> `generar_thumbnails()` -> `extraer_preview()` -> `publicar_en_cdn()`. Cada paso toma la salida del anterior y la transforma. La cohesion es alta porque las funciones no solo comparten datos, sino que participan en una transformacion progresiva del mismo artefacto.

#### Nivel 1 (mejor): Cohesion funcional

Todos los elementos del modulo contribuyen a una unica funcion bien definida. Si le preguntas a alguien "de que se trata este modulo?", la respuesta es una oracion corta y sin "y".

```python
# autenticacion.py
class Autenticacion:
    def iniciar_sesion(self, credenciales) -> Token: ...
    def cerrar_sesion(self, token) -> None: ...
    def verificar_token(self, token) -> Usuario: ...
    def refrescar_token(self, token) -> Token: ...
    def _hashear_contrasena(self, contrasena) -> str: ...
    def _validar_credenciales(self, credenciales) -> bool: ...
```

Todas las funciones contribuyen a un unico objetivo: gestionar la autenticacion. Cada funcion publica es una operacion de autenticacion. Cada funcion privada es un detalle de implementacion de la autenticacion. Si cambias las reglas de autenticacion, todo el cambio esta contenido aqui. Si buscas algo relacionado con autenticacion, todo esta aqui.

**En DevCourses:** El `ServicioInscripcion` que disenamos en capitulos anteriores tiene cohesion funcional: todo lo que contiene contribuye a un unico proposito (inscribir usuarios en cursos). La validacion, el cobro, el registro y la notificacion son pasos de una sola funcion cohesiva, no responsabilidades independientes.

### El espectro en la practica

Constantine y Yourdon descubrieron, y estudios posteriores de Steve McConnell y otros confirmaron, que los dos niveles inferiores (coincidental y logico) son definitivamente problematicos [McConnell, 2004]. La cohesion comunicacional y secuencial son buenas. Y la cohesion funcional es la meta a la que debes aspirar.

En la practica, la mayoria de los modulos bien disenados caen entre cohesion comunicacional y funcional. Eso esta bien. No necesitas perfeccion; necesitas estar en la parte alta del espectro. Y lo mas importante: si identificas modulos con cohesion coincidental o logica en tu sistema, esos son los candidatos prioritarios para reorganizacion.

**Takeaway:** Los siete niveles de cohesion proporcionan un vocabulario preciso para evaluar tus modulos. La meta es cohesion funcional (todo contribuye a un proposito), pero cohesion comunicacional y secuencial son aceptables. Si tus modulos tienen cohesion coincidental o logica, es hora de reorganizar.

---

## Acoplamiento: cuanto necesitas saber de otro modulo para entender este

### La definicion operativa

El acoplamiento mide el grado de interdependencia entre modulos. La pregunta clave es:

> "Cuanto necesitas saber de un modulo para entender otro?" [Constantine y Yourdon, 1979]

Si para modificar el modulo de inscripciones necesitas entender como funciona internamente el modulo de pagos, esos dos modulos estan altamente acoplados. Si puedes modificar inscripciones sin siquiera saber que existe un modulo de pagos (porque interactuas con el a traves de una interfaz simple), el acoplamiento es bajo.

El acoplamiento ideal seria cero: modulos completamente independientes. Pero eso es imposible en la practica. Un sistema donde los modulos no se comunican en absoluto es un sistema que no hace nada. El objetivo realista es *minimizar* el acoplamiento, no eliminarlo.

### Los seis niveles de acoplamiento

Asi como la cohesion tiene un espectro, el acoplamiento tambien. Constantine y Yourdon identificaron niveles que van del peor al mejor:

#### Nivel 6 (peor): Acoplamiento de contenido

Un modulo accede directamente a las estructuras internas de otro. Lee sus variables privadas, modifica su estado interno, o salta a codigo en medio de otro modulo.

```python
# modulo_reportes.py
from modulo_usuarios import _cache_interna_usuarios  # Accede a implementacion privada

def generar_reporte():
    # Accede directamente al estado interno del modulo de usuarios
    for usuario in _cache_interna_usuarios.values():
        if usuario._contrasena_hash.startswith("bcrypt"):  # Accede a campo privado
            ...
```

Esto es la forma mas daninayla de acoplamiento. Si el modulo de usuarios cambia su estructura interna -- renombra la cache, cambia el formato del hash -- el modulo de reportes se rompe. Y nadie lo ve venir, porque la dependencia esta en los detalles internos, no en la interfaz publica.

**En DevCourses:** Un caso que encontramos en el capitulo 6: el controlador de la API accedia directamente a la URL de S3 para los videos, en vez de pedirle al modulo de video que generara la URL. Si el esquema de almacenamiento en S3 cambiaba, el controlador se rompia.

#### Nivel 5: Acoplamiento comun (global)

Dos modulos comparten datos globales: variables globales, singletons mutables, bases de datos compartidas sin interfaz.

```python
# globals.py
estado_sistema = {"modo": "produccion", "usuarios_activos": 0}

# modulo_a.py
from globals import estado_sistema
estado_sistema["usuarios_activos"] += 1

# modulo_b.py
from globals import estado_sistema
if estado_sistema["usuarios_activos"] > 1000:
    activar_modo_alto_trafico()
```

Ambos modulos dependen de la misma variable global. Si A la modifica, B se comporta diferente. Si alguien agrega un campo nuevo o cambia el formato, ambos modulos se ven afectados. El estado compartido mutable es una de las fuentes mas comunes de bugs en sistemas grandes.

**En DevCourses:** Antes de la reorganizacion, el modulo de reportes y el modulo de facturacion accedian directamente a las mismas tablas de la base de datos sin pasar por interfaces. Cuando el esquema cambio (agregar el campo `idioma` a los cursos), ambos modulos necesitaron actualizarse porque ambos tenian queries SQL que asumian la estructura de la tabla.

#### Nivel 4: Acoplamiento de control

Un modulo le dice a otro *como* comportarse, pasandole un parametro que altera su flujo de control.

```python
def procesar_datos(datos, modo="normal"):
    if modo == "normal":
        return transformar_normal(datos)
    elif modo == "legacy":
        return transformar_legacy(datos)
    elif modo == "debug":
        return transformar_debug(datos)
```

El modulo que llama a `procesar_datos` necesita conocer los modos internos de la funcion. Necesita saber que existe un modo "legacy" y que hace. Eso es conocimiento sobre la implementacion interna que esta fugando a traves de la interfaz.

**En DevCourses:** El modulo de catalogo tenia una funcion `buscar_cursos(query, tipo_busqueda="texto")` donde `tipo_busqueda` podia ser "texto", "categoria", "instructor" o "avanzada". El modulo que llamaba a `buscar_cursos` necesitaba conocer los cuatro tipos de busqueda y sus diferencias. Es mejor ofrecer funciones separadas con nombres claros: `buscar_por_texto()`, `buscar_por_categoria()`, `buscar_por_instructor()`.

#### Nivel 3: Acoplamiento de sello (stamp)

Un modulo pasa a otro una estructura de datos completa cuando solo necesita una parte.

```python
def enviar_confirmacion(usuario: Usuario):
    # Solo necesita el email, pero recibe todo el objeto Usuario
    email.enviar(
        destinatario=usuario.email,
        asunto="Inscripcion confirmada"
    )
```

`enviar_confirmacion` recibe un objeto `Usuario` completo pero solo usa `usuario.email`. Ahora `enviar_confirmacion` esta acoplado a la estructura de `Usuario`. Si `Usuario` cambia (agrega un campo obligatorio al constructor, cambia el nombre del atributo `email` a `correo`), la funcion podria verse afectada aunque no use esos campos.

La alternativa es pasar solo lo que se necesita:

```python
def enviar_confirmacion(email_destinatario: str):
    email.enviar(
        destinatario=email_destinatario,
        asunto="Inscripcion confirmada"
    )
```

Ahora la funcion no sabe ni le importa que existe un tipo `Usuario`. Solo necesita una cadena de texto con una direccion de email.

Hay un matiz: el acoplamiento de sello no siempre es malo. Si la estructura de datos pasada es estable y la funcion usa la mayoria de sus campos, pasar el objeto completo es mas limpio que pasar diez parametros individuales. El problema surge cuando pasas objetos grandes y solo usas un fragmento.

**En DevCourses:** El modulo de notificaciones recibia un objeto `Curso` completo para generar un email de bienvenida, pero solo usaba `curso.nombre` y `curso.instructor_nombre`. Refactorizamos para que recibiera un `MensajeBienvenida` con solo los datos necesarios.

#### Nivel 2: Acoplamiento de datos

Los modulos se comunican a traves de parametros simples: tipos primitivos, estructuras de datos minimas, valores concretos. Cada dato pasado es necesario y suficiente.

```python
def calcular_precio(monto_base: Decimal, porcentaje_descuento: int) -> Decimal:
    return monto_base * (1 - porcentaje_descuento / 100)
```

La funcion recibe exactamente lo que necesita: dos valores simples. No hay dependencia en estructuras complejas, no hay parametros de control, no hay datos globales. El acoplamiento es minimo.

Este es el tipo de acoplamiento al que debes aspirar. No siempre es posible (a veces necesitas pasar objetos complejos), pero cuando puedes reducir la interfaz a datos simples, hazlo.

#### Nivel 1 (mejor): Sin acoplamiento directo (mensajes)

Los modulos se comunican a traves de mensajes, eventos, o interfaces completamente desacopladas. Un modulo emite un evento; otro lo consume. Ninguno sabe de la existencia del otro.

```python
# modulo_inscripcion.py
def inscribir(usuario_id, curso_id):
    inscripcion = crear_inscripcion(usuario_id, curso_id)
    eventos.emitir("inscripcion_completada", {
        "usuario_id": usuario_id,
        "curso_id": curso_id
    })

# modulo_notificaciones.py (en otro lugar, no conoce a inscripcion)
@eventos.escuchar("inscripcion_completada")
def enviar_bienvenida(datos):
    enviar_email(datos["usuario_id"], "Bienvenido al curso")
```

El modulo de inscripcion no sabe que existe un modulo de notificaciones. El modulo de notificaciones no sabe que existe un modulo de inscripcion. Solo comparten un contrato: el formato del evento "inscripcion_completada".

Este nivel de acoplamiento es poderoso pero tiene un costo: la indirreccion hace que el flujo sea mas dificil de seguir. Si algo falla en las notificaciones, rastrear el origen del problema requiere entender el sistema de eventos. Usa este patron cuando el desacoplamiento genuinamente importa, no como patron universal.

### Los cuatro factores que afectan el acoplamiento

Constantine identifico cuatro factores que determinan que tan acoplados estan dos modulos [Constantine y Yourdon, 1979]:

1. **Tipo de conexion.** Como se conectan los modulos? A traves de una interfaz publica (bajo acoplamiento), a traves de datos compartidos (medio), o accediendo directamente a las estructuras internas del otro (alto)?

2. **Complejidad de la interfaz.** Cuantos parametros, cuantos tipos, cuantos conceptos se necesitan para que un modulo llame a otro? Menos es mejor.

3. **Tipo de informacion transmitida.** Se pasan datos simples (bajo acoplamiento), estructuras complejas (medio), o flags de control que alteran el comportamiento del otro modulo (alto)?

4. **Momento de la conexion.** La dependencia se resuelve en tiempo de compilacion (tipicamente bajo), en tiempo de ejecucion (medio), o dinamicamente en cualquier momento (alto)?

Evaluar estos cuatro factores para cada par de modulos te da un mapa preciso del acoplamiento en tu sistema.

**Takeaway:** El acoplamiento se mide por cuanto necesitas saber de un modulo para usar o entender otro. Los niveles van desde acoplamiento de contenido (el peor: acceso directo a internos) hasta comunicacion por mensajes (el mejor: ningun modulo sabe del otro). El objetivo practico es mantenerse en los niveles de acoplamiento de datos o mejor.

---

## La relacion inversa: mas cohesion implica menos acoplamiento

Constantine y Yourdon descubrieron una relacion que parece obvia en retrospectiva pero que tiene implicaciones profundas:

> "A mayor cohesion de los modulos individuales en el sistema, menor sera el acoplamiento." [Constantine y Yourdon, 1979]

La logica es esta: si un modulo contiene todo lo necesario para cumplir su funcion (alta cohesion), no necesita buscar piezas en otros modulos. Es autocontenido. Y un modulo autocontenido, por definicion, tiene menos conexiones con el exterior.

Inversamente, si un modulo tiene baja cohesion -- si contiene funcionalidades dispares -- necesita importar datos y funciones de multiples lugares para cada una de esas funcionalidades. Mas funcionalidades dispares significan mas dependencias externas.

Considera el ejemplo de DevCourses. Si el modulo de catalogo tiene cohesion funcional -- contiene todo lo relacionado con buscar, filtrar y listar cursos -- no necesita saber como funcionan las inscripciones, los pagos o las notificaciones. Solo expone una interfaz simple: "dame los cursos que cumplan estos criterios".

Pero si el modulo de catalogo tambien maneja "cursos recomendados basados en tus inscripciones", ahora necesita acceder al modulo de inscripciones. Y si tambien muestra "cursos que tus amigos estan tomando", necesita acceder al modulo social. Cada funcionalidad ajena que agregas al catalogo es una dependencia nueva con un modulo externo. La cohesion bajo; el acoplamiento subio.

La relacion inversa no es perfecta -- puedes tener un modulo cohesivo con alto acoplamiento si su interfaz esta mal disenada. Pero como heuristica general, funciona: **si mejoras la cohesion de tus modulos, el acoplamiento tiende a bajar automaticamente**.

Esto explica por que cohesion y acoplamiento son mas utiles en la practica que SOLID. SOLID te da cinco principios independientes que a veces se contradicen entre si. Cohesion y acoplamiento te dan dos medidas que se refuerzan mutuamente. Mejorar una tiende a mejorar la otra. Es un sistema coherente, no una coleccion de reglas.

**Takeaway:** Alta cohesion y bajo acoplamiento se refuerzan mutuamente. Mejorar la cohesion de tus modulos tiende a reducir el acoplamiento automaticamente. Es un sistema que se retroalimenta positivamente.

---

## Por que cohesion y acoplamiento son mas utiles que SOLID

Dejemos de lado la diplomacia y digamoslo con claridad: para las decisiones de diseno del dia a dia, cohesion y acoplamiento son mas utiles que SOLID. Hay cinco razones concretas.

### 1. Son medibles

Puedes contar las dependencias entre modulos (acoplamiento). Puedes evaluar si los elementos de un modulo trabajan hacia el mismo objetivo (cohesion). Son propiedades observables que no dependen de la interpretacion del observador.

Compara con SRP: "una sola responsabilidad" es subjetivo. Lo que para un desarrollador es una responsabilidad, para otro son tres. No hay forma de resolver el desacuerdo porque "responsabilidad" no es un termino tecnico definido.

Compara con OCP: "abierto para extension, cerrado para modificacion" requiere predecir el futuro. No puedes medir si tu modulo esta "abierto" hasta que llegue el cambio.

Cohesion y acoplamiento se pueden evaluar *ahora*, con el codigo que tienes *hoy*, sin necesidad de predecir cambios futuros.

### 2. No se contradicen entre si

Los cinco principios SOLID pueden entrar en tension. Aplicar ISP (segregar interfaces) puede violar SRP (al crear mas clases de las necesarias). Aplicar DIP (invertir dependencias) puede violar el consejo de simplicidad de OCP (al crear capas de abstraccion innecesarias).

Cohesion y acoplamiento nunca se contradicen. Mejorar uno mejora el otro. Son dimensiones complementarias de la misma cualidad: la salud estructural del sistema.

### 3. Aplican independientemente del paradigma

SOLID fue formulado para la programacion orientada a objetos. Sus ejemplos usan clases, herencia e interfaces. En un lenguaje funcional, en un lenguaje de scripting, o en una arquitectura de microservicios, la traduccion de SOLID no es directa.

Cohesion y acoplamiento aplican a cualquier modulo, en cualquier paradigma, en cualquier nivel de abstraccion. Una funcion puede tener alta o baja cohesion. Un microservicio puede tener alto o bajo acoplamiento. Un archivo de configuracion puede estar cohesivo o no. Los conceptos son universales.

### 4. Guian la accion

Cuando identifiques baja cohesion en un modulo, la accion es clara: mueve los elementos no relacionados a donde pertenecen. Cuando identifiques alto acoplamiento entre dos modulos, la accion es clara: introduce una interfaz mas simple entre ellos, o reorganiza para que no necesiten comunicarse tanto.

SOLID te dice *que* esta mal, pero no siempre *que* hacer. "Tu clase viola SRP" es un diagnostico. "Tu modulo tiene cohesion logica; deberia tener cohesion funcional" es un diagnostico *y* una prescripcion.

### 5. Fueron validados empiricamente

Multiples estudios academicos a lo largo de las decadas han confirmado que alta cohesion y bajo acoplamiento correlacionan con menor densidad de bugs, mayor facilidad de mantenimiento, y menor costo de cambio [Briand, Daly y Wust, 1999; Al Dallal y Briand, 2012]. SOLID carece de evidencia empirica comparable. Sus beneficios son argumentados teoricamente pero rara vez medidos.

**Takeaway:** Cohesion y acoplamiento son mas utiles que SOLID porque son medibles, no se contradicen, aplican a cualquier paradigma, guian la accion directamente, y tienen soporte empirico. Para las decisiones de diseno del dia a dia, son la herramienta de primera linea.

---

## Checklist: evalua la salud de tus modulos

Usa esta checklist para evaluar cualquier modulo de tu sistema. No es una metrica exacta; es una herramienta de diagnostico rapido.

### Cohesion (evalua cada modulo individualmente)

**Pregunta 1: Puedo describir el proposito del modulo en una oracion sin usar "y"?**
- Si: cohesion probablemente alta.
- No ("maneja usuarios *y* genera reportes *y* envia notificaciones"): cohesion probablemente baja.

**Pregunta 2: Si elimino un elemento del modulo, los demas siguen teniendo sentido juntos?**
- Si para todos los elementos: puede haber elementos que no pertenecen.
- No, la eliminacion rompe la logica: los elementos estan genuinamente relacionados.

**Pregunta 3: Cuando cambio un requisito de negocio, cuantos modulos necesito tocar?**
- Uno: alta cohesion (todo lo relevante esta junto).
- Tres o mas: baja cohesion (la funcionalidad esta esparcida).

**Pregunta 4: En cual de los siete niveles de cohesion cae este modulo?**
- Funcional o secuencial: excelente.
- Comunicacional: bueno, pero podria mejorar.
- Procedural o temporal: hay oportunidad de reorganizar.
- Logico o coincidental: necesita reorganizacion urgente.

### Acoplamiento (evalua cada par de modulos)

**Pregunta 5: Si cambio la implementacion interna de un modulo (sin cambiar su interfaz), cuantos otros modulos se rompen?**
- Cero: bajo acoplamiento (bueno).
- Uno o dos: acoplamiento moderado (aceptable).
- Tres o mas: acoplamiento alto (problematico).

**Pregunta 6: Cuanto necesito saber del modulo B para entender el modulo A?**
- Nada, solo su interfaz publica: acoplamiento bajo.
- Algunos detalles de implementacion: acoplamiento moderado.
- Tengo que leer el codigo fuente de B: acoplamiento alto.

**Pregunta 7: Que tipo de datos pasan entre los modulos?**
- Tipos primitivos o estructuras simples: acoplamiento de datos (bueno).
- Objetos complejos donde solo se usa una parte: acoplamiento de sello (mejorable).
- Flags que controlan el comportamiento del otro: acoplamiento de control (problematico).

**Pregunta 8: Los modulos comparten estado mutable (variables globales, singletons, bases de datos sin interfaz)?**
- No: bien.
- Si: acoplamiento comun (peligroso). Introduce una interfaz entre los modulos y los datos compartidos.

### Tabla resumen rapida

| Indicador | Bueno | Malo |
|---|---|---|
| Descripcion del modulo | Una oracion sin "y" | Parrafo completo |
| Cambio de requisito | Toca 1 modulo | Toca 3+ modulos |
| Modulos afectados por cambio interno | 0 | 3+ |
| Tipo de datos entre modulos | Primitivos, DTOs simples | Objetos complejos, flags |
| Estado compartido | No | Variables globales, singletons |
| Nivel de cohesion | Funcional, secuencial | Logico, coincidental |

---

## Proyecto guia: midiendo cohesion y acoplamiento en DevCourses

Vamos a aplicar la checklist a los siete modulos de DevCourses en su estado actual, despues de las reorganizaciones de los capitulos anteriores.

### Tabla de evaluacion

| Modulo | Proposito (1 oracion) | Cohesion (1-7) | Acoplamiento con otros | Evaluacion |
|---|---|---|---|---|
| **Catalogo** | Buscar, filtrar y listar cursos disponibles | 6 (funcional) | Bajo: solo expone `buscar_cursos()`, `obtener_curso()` | Bien. Reorganizado en cap. 7 |
| **Inscripcion** | Inscribir usuarios en cursos | 7 (funcional) | Bajo: depende de repo, notificador, precios via interfaces | Bien. Modulo profundo |
| **Pagos** | Cobrar a los usuarios | 6 (funcional) | Bajo: interfaz `ProcesadorPagos` con 3 implementaciones | Bien. DIP justificado |
| **Video** | Almacenar y servir contenido en video | 5 (secuencial) | Medio: depende de S3, pero la dependencia esta encapsulada | Aceptable |
| **Usuarios** | Gestionar perfiles y autenticacion | 5 (comunicacional) | Medio: otros modulos consultan datos de usuario frecuentemente | Mejorable |
| **Comentarios** | Manejar discusiones en cursos | 4 (comunicacional) | Alto: accede directamente a datos de usuarios y cursos | Problematico |
| **Notificaciones** | Enviar mensajes por multiples canales | 5 (funcional) | Bajo: recibe datos minimos, envia por canal configurado | Aceptable |

### Los tres puntos criticos

**Punto critico 1: El modulo de Comentarios.**

El modulo de comentarios tiene el peor acoplamiento del sistema. Para mostrar un comentario, necesita:
- El texto del comentario (suyo).
- El nombre del usuario que comento (del modulo de usuarios).
- El nombre del curso donde se comento (del modulo de catalogo).
- Si el usuario es instructor del curso (del modulo de usuarios + catalogo).

Actualmente, el modulo de comentarios accede directamente a las tablas de usuarios y cursos. Si la estructura de la tabla de usuarios cambia, el modulo de comentarios se rompe.

**Solucion:** El modulo de comentarios deberia almacenar la informacion que necesita como datos desnormalizados: `autor_nombre`, `curso_nombre`, `es_instructor`. Cuando se crea un comentario, estos datos se copian. El comentario se vuelve autocontenido. Si el nombre del usuario cambia, un proceso de sincronizacion actualiza los comentarios. Esto reduce el acoplamiento de "comun" a "datos".

```python
# Antes: alto acoplamiento
class Comentario:
    def mostrar(self):
        usuario = db.obtener_usuario(self.usuario_id)  # Dependencia directa
        curso = db.obtener_curso(self.curso_id)  # Dependencia directa
        return f"{usuario.nombre} en {curso.titulo}: {self.texto}"

# Despues: bajo acoplamiento
class Comentario:
    def __init__(self, texto, autor_nombre, curso_titulo, es_instructor):
        self.texto = texto
        self.autor_nombre = autor_nombre
        self.curso_titulo = curso_titulo
        self.es_instructor = es_instructor

    def mostrar(self):
        return f"{self.autor_nombre} en {self.curso_titulo}: {self.texto}"
```

**Punto critico 2: El modulo de Usuarios como cuello de botella.**

Casi todos los modulos necesitan datos de usuarios: el nombre para comentarios, el email para notificaciones, las preferencias para la interfaz, el historial para las recomendaciones. El modulo de usuarios se ha convertido en un punto central con muchas flechas entrantes.

El problema no es que otros modulos dependan de usuarios -- eso es inevitable. El problema es *como* dependen. Si dependen de la interfaz publica (`obtener_perfil(id)`, `obtener_email(id)`), el acoplamiento es bajo. Si dependen de la estructura interna de la tabla de usuarios, el acoplamiento es alto.

**Solucion:** Verificar que todos los modulos accedan a datos de usuarios *unicamente* a traves de la interfaz publica del modulo de usuarios. Eliminar cualquier acceso directo a la base de datos de usuarios desde otros modulos.

**Punto critico 3: Cohesion del modulo de Usuarios.**

El modulo de usuarios actualmente hace dos cosas conceptualmente diferentes: gestion de perfiles (nombre, foto, preferencias) y autenticacion (login, tokens, contrasenas). Estas dos funcionalidades tienen razones de cambio diferentes: los perfiles cambian cuando el producto evoluciona; la autenticacion cambia cuando hay requisitos de seguridad.

**Solucion:** Separar en dos modulos: `perfiles` (datos del usuario) y `autenticacion` (credenciales, sesiones, tokens). Esto incrementa la cohesion de cada modulo sin agregar acoplamiento significativo entre ellos.

### Plan de mejora priorizado

1. **Inmediato:** Desnormalizar datos de usuario y curso en el modulo de comentarios. Reduce el acoplamiento mas problematico del sistema.

2. **Corto plazo:** Auditar todos los accesos directos a la base de datos de usuarios desde otros modulos. Reemplazar con llamadas a la interfaz publica del modulo de usuarios.

3. **Medio plazo:** Separar el modulo de usuarios en perfiles y autenticacion. Incrementa la cohesion de ambos modulos.

4. **Continuo:** En cada nuevo feature, aplicar la checklist antes de integrarlo. Evaluar si el nuevo codigo mantiene la cohesion del modulo receptor y no incrementa el acoplamiento con otros modulos.

### Mapa de dependencias resultante

```
  Catalogo ←---------- Inscripcion
     ↑                     |
     |                     ↓
     |                   Pagos
     |
  Perfiles ←----------- Notificaciones
     ↑
     |
  Comentarios           Autenticacion
  (autocontenido)
     ↑
     |
    Video
```

Las flechas indican "depende de". Los modulos con menos flechas entrantes y salientes tienen menor acoplamiento. El objetivo es que cada modulo tenga como maximo dos o tres dependencias directas, y que todas esas dependencias sean a traves de interfaces publicas simples.

**Takeaway:** Medir cohesion y acoplamiento en DevCourses revelo tres problemas concretos: acoplamiento directo a datos en comentarios, el modulo de usuarios como cuello de botella, y baja cohesion por mezclar perfiles con autenticacion. Cada problema tiene una solucion clara y priorizable.

---

## La conexion con todo lo anterior

Cohesion y acoplamiento no son conceptos aislados. Son la lente unificadora a traves de la cual todos los principios que hemos explorado cobran sentido.

**Modulos profundos** (capitulo 5): Un modulo profundo tiene alta cohesion (toda su funcionalidad contribuye a un proposito) y bajo acoplamiento (su interfaz simple minimiza las dependencias del exterior).

**Ocultamiento de informacion** (capitulo 6): Ocultar informacion es la tecnica principal para reducir el acoplamiento. Si un modulo no expone sus detalles internos, los otros modulos no pueden depender de ellos.

**Separar o juntar** (capitulo 7): Los criterios para decidir si dos piezas de codigo deberian estar juntas o separadas son, en esencia, criterios de cohesion. Si comparten informacion y se usan juntas, su cohesion es alta y deberian estar juntas. Si operan en niveles de abstraccion diferentes, su cohesion es baja y deberian estar separadas.

**SOLID** (capitulo 8): SRP es cohesion. OCP es estabilidad de interfaces (que reduce acoplamiento). ISP es minimizar el acoplamiento innecesario. DIP es desacoplar niveles de abstraccion. Los cinco principios son variantes de "alta cohesion, bajo acoplamiento".

**LSP, ISP, DIP** (capitulo 9): Los tres principios que acabamos de analizar son casos particulares de gestion de acoplamiento. LSP dice "no rompas el contrato al que otros estan acoplados". ISP dice "no acoples a otros con lo que no necesitan". DIP dice "acopla a abstracciones, no a implementaciones".

Todo converge en el mismo lugar. Constantine y Yourdon lo vieron en 1974. Parnas lo vio en 1972. Ousterhout lo articulo en 2018 con un vocabulario fresco. Pero la idea es la misma: **pon las cosas relacionadas juntas, minimiza las conexiones entre cosas no relacionadas, y oculta los detalles detras de interfaces simples**.

Si llevas una sola idea de los primeros diez capitulos de este libro, que sea esta. No necesitas memorizar acronimos. No necesitas recitar principios. Necesitas desarrollar la intuicion para reconocer cuando algo esta en el lugar equivocado (baja cohesion) y cuando algo sabe demasiado sobre otra cosa (alto acoplamiento). Esa intuicion se construye con practica, no con teoria.

**Takeaway:** Cohesion y acoplamiento son el hilo conductor de todos los principios de diseno. Modulos profundos, ocultamiento de informacion, SOLID, separacion de niveles -- todos son expresiones de la misma idea fundamental. Si dominas cohesion y acoplamiento, los demas principios se vuelven intuitivos.

---

## Aplica esto el lunes

1. **Dibuja un mapa de dependencias de tus modulos.** Para cada modulo, traza una flecha hacia cada otro modulo del que depende. Donde estan los puntos con mas flechas entrantes y salientes? Esos son tus puntos de mayor acoplamiento. Investiga: las dependencias son a traves de interfaces publicas o de accesos directos a datos internos?

2. **Para tu modulo mas importante, evalua la cohesion con los siete niveles.** Preguntate: todos los elementos contribuyen a un unico proposito? Si encuentras elementos que no pertenecen, anotales. Cada uno es un candidato para moverse a donde conceptualmente pertenezca.

3. **Aplica la checklist a tres modulos.** Responde las ocho preguntas para tus tres modulos mas criticos. Si alguno tiene cohesion logica o coincidental, o acoplamiento de contenido o comun, es tu prioridad de refactorizacion.

4. **Busca un caso de estado compartido mutable.** Variables globales, singletons con estado, tablas de base de datos accedidas directamente desde multiples modulos. Cada caso es acoplamiento comun esperando a causar un bug. Introduce una interfaz publica que mediaticea el acceso.

5. **La proxima vez que digas "este modulo hace demasiado", se preciso.** No digas "viola SRP". Di "tiene cohesion logica porque agrupa funcionalidades por verbo (todas son 'validaciones') en vez de por concepto (validaciones de pago deberian estar en el modulo de pagos)". La precision del diagnostico determina la calidad de la solucion.

---

## Referencias del capitulo

- Al Dallal, J. y Briand, L. C. (2012). "An Object-Oriented High-Level Design-Based Class Cohesion Metric." *Information and Software Technology*, 54(12).
- Briand, L. C., Daly, J. W. y Wust, J. K. (1999). "A Unified Framework for Coupling Measurement in Object-Oriented Systems." *IEEE Transactions on Software Engineering*, 25(1).
- Constantine, L. y Yourdon, E. (1979). *Structured Design: Fundamentals of a Discipline of Computer Program and Systems Design*. Prentice-Hall.
- McConnell, S. (2004). *Code Complete*. 2nd Edition. Microsoft Press.
- Ousterhout, J. (2018). *A Philosophy of Software Design*. Yaknyam Press.
- Parnas, D. (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 15(12).
- Stevens, W., Myers, G. y Constantine, L. (1974). "Structured Design." *IBM Systems Journal*, 13(2).
