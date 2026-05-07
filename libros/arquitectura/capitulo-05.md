# Capitulo 5: El ocultamiento de informacion es tu arma mas poderosa

> "Lo que escondes importa mas de lo que expones."

---

## La funcion que nunca has leido

Cuantas veces has mirado el codigo fuente de `print()` en Python? O de `console.log()` en JavaScript? O de `fmt.Println()` en Go?

Probablemente nunca. Y sin embargo, las usas todos los dias. Las usas con confianza absoluta. Sabes que van a funcionar. Sabes que van a hacer lo que esperas. Y nunca -- ni una sola vez -- necesitaste entender *como* lo hacen.

Ahora piensa en la ultima funcion que escribio un companero de tu equipo. La que necesitaste usar la semana pasada. Pudiste usarla sin leer su codigo fuente? O tuviste que abrirla, leer las 80 lineas, entender que base de datos consultaba, en que formato esperaba las fechas, y que efecto secundario tenia sobre la sesion del usuario?

La diferencia entre `print()` y la funcion de tu companero no es talento. No es experiencia. Es una decision de diseno: `print()` fue disenada para *ocultar* todo lo que no necesitas saber. La funcion de tu companero probablemente no fue disenada en absoluto -- simplemente sucedio.

En el capitulo anterior descubrimos que los mejores modulos son profundos: ocultan mucha funcionalidad detras de una interfaz simple. Pero eso abre una pregunta fundamental: *que* exactamente deben ocultar? No se trata de meter codigo adentro de un modulo y esperar lo mejor. Se trata de identificar con precision las *decisiones de diseno* que deben quedar encapsuladas, y de detectar las *fugas* que rompen ese encapsulamiento.

Este capitulo trata sobre el principio mas importante del diseno de software. No es SOLID. No es DRY. No es ningun acronimo. Es una idea que David Parnas articulo en 1972 y que sigue siendo, medio siglo despues, la herramienta mas poderosa que tienes como disenador de software: el ocultamiento de informacion.

**Takeaway:** Las funciones que usas con mas confianza son las que menos necesitas entender por dentro. Ese no es un accidente: es el resultado del ocultamiento de informacion bien aplicado.

---

## El principio que cambio la historia del software

En 1972, un profesor de informatica llamado David Parnas publico un articulo de apenas ocho paginas que cambio para siempre la forma de pensar sobre el diseno de software. El titulo era sobrio y academico: "On the Criteria To Be Used in Decomposing Systems into Modules" [Parnas, 1972]. El contenido era revolucionario.

Parnas planteo una pregunta que parecia obvia pero que nadie habia respondido con rigor: *que criterio debemos usar para decidir como dividir un sistema en partes?*

En esa epoca, la respuesta convencional era: divide segun el flujo de ejecucion. Primero el sistema lee datos, luego los procesa, luego los almacena, luego genera la salida. Cada paso es un modulo. Es la descomposicion que cualquier persona dibujaría si le pidieras un diagrama de flujo.

Parnas demostro, con un ejemplo concreto (un sistema para generar un indice KWIC), que esa descomposicion era inferior a otra basada en un criterio diferente: **cada modulo debe encapsular una decision de diseno que sea probable que cambie**.

La diferencia entre ambas descomposiciones era dramatica. En la primera (por flujo), cambiar el formato de almacenamiento de los datos requeria modificar casi todos los modulos, porque todos conocian la estructura de los datos. En la segunda (por ocultamiento de informacion), el mismo cambio afectaba un solo modulo, porque solo ese modulo sabia como se almacenaban los datos. Los demas interactuaban con el a traves de una interfaz que no revelaba esos detalles.

Parnas escribio:

> "Cada modulo se caracteriza por su conocimiento de una decision de diseno que oculta de todos los demas. Su interfaz se disena para revelar lo menos posible sobre su funcionamiento interno." [Parnas, 1972]

Esto parece sentido comun hoy. Pero en 1972 era una ruptura radical con la forma en que se ensenaba y practicaba la descomposicion de sistemas. Y lo mas notable es que, cincuenta y cuatro anos despues, la mayoria de los sistemas de software siguen violando este principio todos los dias.

John Ousterhout lo puso en terminos modernos:

> "La idea basica es que cada modulo deberia encapsular algunas piezas de conocimiento, que representen decisiones de diseno." [Ousterhout, 2018]

Nota la palabra *conocimiento*. No "funcionalidad". No "datos". No "operaciones". Conocimiento. Decisiones de diseno. Cosas que podrian cambiar. Cosas que, si cambian, deberian afectar a un solo lugar del sistema.

Ese es el principio del ocultamiento de informacion: **disenar los modulos alrededor de las decisiones de diseno que es probable que cambien, y esconder esas decisiones detras de interfaces estables**.

**Takeaway:** El ocultamiento de informacion no es "meter cosas dentro de una clase". Es identificar las decisiones de diseno que probablemente cambien y encapsularlas en modulos cuyas interfaces no revelen esas decisiones. Es el principio fundamental detras de la mayoria de las buenas practicas de diseno.

---

## Ocultamiento de informacion vs. encapsulacion: no son lo mismo

Hay una confusion generalizada que necesitamos despejar antes de avanzar. Muchos desarrolladores usan "ocultamiento de informacion" y "encapsulacion" como sinonimos. No lo son. Entender la diferencia es crucial.

**Encapsulacion** es un mecanismo. Es la capacidad de agrupar datos y operaciones en una unidad (una clase, un modulo, un paquete) y controlar el acceso a sus partes internas. En Java, es poner `private` delante de un atributo. En Python, es usar el prefijo `_` por convencion. En Go, es usar minusculas en el nombre de una funcion para que sea privada al paquete.

**Ocultamiento de informacion** es un principio de diseno. Es la *decision* de que ciertas piezas de conocimiento no deben ser accesibles -- ni necesarias -- para los usuarios de un modulo. No se trata de poner `private` en un atributo. Se trata de disenar el modulo de tal forma que el atributo ni siquiera necesite existir en la mente de quien lo usa.

La diferencia es sutil pero profunda. Puedes tener encapsulacion sin ocultamiento de informacion. Y puedes tener ocultamiento de informacion sin encapsulacion formal.

### Encapsulacion sin ocultamiento de informacion

Considera esta clase en Java:

```java
public class Usuario {
    private String stripeCustomerId;

    public String getStripeCustomerId() {
        return stripeCustomerId;
    }

    public void setStripeCustomerId(String id) {
        this.stripeCustomerId = id;
    }
}
```

El atributo `stripeCustomerId` es privado. La clase esta "encapsulada" en el sentido tecnico: los datos estan detras de metodos de acceso. Pero el ocultamiento de informacion es nulo. Cualquier codigo que use esta clase *sabe* que el usuario tiene un ID de Stripe. Sabe que el sistema de pagos es Stripe. Si manana migras a otra pasarela, todos los consumidores de `getStripeCustomerId()` necesitan cambiar.

El getter y el setter crean la *ilusion* de encapsulamiento. Pero el conocimiento -- "este usuario tiene una relacion directa con Stripe" -- esta expuesto a todo el sistema. Encapsulaste los datos; no ocultaste la informacion.

### Ocultamiento de informacion sin encapsulacion formal

Ahora considera un modulo en Python (un lenguaje sin `private` real):

```python
# modulo: procesador_pagos.py

def cobrar(usuario_id: str, monto: Decimal, moneda: str,
           descripcion: str) -> ResultadoPago:
    """
    Cobra al usuario usando su metodo de pago configurado.
    """
    metodo = _obtener_metodo_pago(usuario_id)
    procesador = _obtener_procesador(metodo.tipo)
    return procesador.cobrar(monto, moneda, metodo.token, descripcion)
```

Python no tiene `private`. Nada impide tecnicamante que alguien importe `_obtener_metodo_pago` directamente. No hay barrera de compilacion ni de runtime. Pero el diseno del modulo oculta informacion efectivamente: quien llama a `cobrar()` no necesita saber que procesador se usa, como se obtiene el metodo de pago, ni que estructura tiene el token. El conocimiento esta oculto por diseno, no por restriccion del lenguaje.

### La relacion correcta

Piensa en ello asi: la encapsulacion es el *mecanismo* y el ocultamiento de informacion es el *principio*. La encapsulacion facilita el ocultamiento de informacion, pero no lo garantiza. Puedes tener el mecanismo sin el principio (getters y setters que exponen todo), y puedes tener el principio sin el mecanismo (modulos bien disenados en lenguajes sin `private`).

Un buen diseno usa la encapsulacion *al servicio* del ocultamiento de informacion. Cada atributo privado, cada funcion interna, cada detalle oculto deberia existir no porque "las buenas practicas dicen que los atributos deben ser privados", sino porque ocultar esa decision de diseno reduce la complejidad del sistema.

**Takeaway:** La encapsulacion es como construir una pared alrededor de un jardin. El ocultamiento de informacion es asegurarte de que nadie *necesite* saber que hay detras de la pared para poder transitar por la calle. Si todo el mundo sabe que detras de la pared hay rosas rojas y planifica su ruta en funcion de eso, la pared no te sirve de nada.

---

## Fugas de informacion: cuando la implementacion se escapa

Si el ocultamiento de informacion es el ideal, las fugas de informacion son su opuesto. Una fuga de informacion ocurre cuando una decision de diseno que deberia estar encapsulada en un modulo se *refleja* en otros modulos del sistema.

Ousterhout define las fugas con claridad:

> "Una fuga de informacion sucede cuando una decision de diseno se ve reflejada en multiples modulos." [Ousterhout, 2018]

Las fugas no siempre son obvias. A veces son tan sutiles que nadie las nota hasta que un cambio aparentemente simple se convierte en una pesadilla. Vamos a examinar los tipos mas comunes.

### Fuga tipo 1: La estructura de datos que se escapa

Esta es la fuga mas clasica. Un modulo expone su estructura de datos interna, y otros modulos empiezan a depender de ella.

Ejemplo: tu modulo de catalogo devuelve los cursos como diccionarios con esta estructura:

```python
{
    "id": "curso_123",
    "titulo": "Python Avanzado",
    "precio_centavos": 4999,
    "s3_video_key": "videos/curso_123/intro.mp4",
    "postgres_created_at": "2024-03-15T10:30:00+00:00"
}
```

Observa `s3_video_key` y `postgres_created_at`. Esos nombres revelan decisiones de implementacion: los videos estan en S3 y la base de datos es PostgreSQL. Cualquier modulo que consuma estos datos *sabe* esas cosas. Si migras el video a Cloudflare Stream o la base de datos a MongoDB, todos los consumidores necesitan cambiar.

La version sin fuga seria:

```python
{
    "id": "curso_123",
    "titulo": "Python Avanzado",
    "precio_centavos": 4999,
    "video_url": "https://cdn.devcourses.com/curso_123/intro",
    "creado_en": "2024-03-15T10:30:00+00:00"
}
```

Ahora los consumidores no saben ni necesitan saber donde estan los videos ni que base de datos usas.

### Fuga tipo 2: El formato que cruza fronteras

Esta fuga sucede cuando dos modulos comparten conocimiento sobre un formato de datos sin que ningun modulo lo "posea".

Un caso real que se repite en miles de proyectos: el backend almacena fechas en formato ISO 8601 (`"2024-03-15T10:30:00+00:00"`) y el frontend las parsea directamente con `new Date(string)`. Parece inofensivo. Pero el formato de la fecha es una decision de diseno del backend que ahora *tambien* conoce el frontend. Si el backend cambia el formato (digamos, empieza a usar timestamps Unix), el frontend se rompe.

La solucion es que un modulo sea el *dueno* del formato. El backend define el contrato: "las fechas se envian en formato ISO 8601". El frontend no parsea directamente; usa una funcion `parsearFechaAPI(string)` que encapsula el conocimiento del formato. Si el formato cambia, solo esa funcion necesita actualizarse.

### Fuga tipo 3: La decision duplicada

Esta es la fuga mas insidiosa. Sucede cuando dos modulos implementan independientemente la misma decision de diseno.

En DevCourses, el modulo de pagos calcula descuentos asi:

```python
# En el modulo de pagos
precio_final = precio * (1 - descuento_porcentaje / 100)
```

Y el modulo de reportes financieros calcula el mismo descuento asi:

```python
# En el modulo de reportes
monto_descontado = precio_original * (1 - porcentaje / 100)
```

Mismo calculo. Misma decision de diseno ("como se aplica un descuento porcentual"). Dos implementaciones. Si el equipo de negocio decide que los descuentos deben redondearse a dos decimales, o que nunca pueden exceder el 50%, o que deben calcularse sobre el precio con impuestos, hay que cambiar *ambos* modulos. Y dado que nadie sabe que estan duplicados, es casi seguro que alguien se olvide de uno.

### Fuga tipo 4: La interfaz que revela el mecanismo

Esta fuga sucede cuando el nombre o la firma de una funcion revelan *como* hace su trabajo, en vez de *que* hace.

Considera estas dos interfaces para un modulo de notificaciones:

```python
# Version con fuga
def enviar_email_ses(destinatario, asunto, cuerpo_html):
    ...

def enviar_push_firebase(usuario_id, titulo, mensaje):
    ...

# Version sin fuga
def notificar(usuario_id, tipo_evento, datos):
    ...
```

La primera version revela que los emails se envian con Amazon SES y las notificaciones push con Firebase. Si migras a SendGrid o a OneSignal, cada llamada a estas funciones necesita cambiar. La segunda version oculta el mecanismo: el modulo de notificaciones decide internamente como enviar cada notificacion.

### Como detectar fugas

Ousterhout sugiere una pregunta poderosa para detectar fugas:

> "Si cambio la implementacion interna de este modulo completamente, que codigo externo se rompe?" [Ousterhout, 2018]

Todo lo que se rompe es una fuga. Cada pieza de codigo externo que depende de tu implementacion interna -- tu formato de datos, tu proveedor, tu algoritmo, tu esquema de base de datos -- es un punto donde la informacion se escapo.

Otra pregunta util: "Si le doy este modulo a otro equipo y les digo 'pueden reescribir la implementacion como quieran, pero la interfaz debe mantenerse', pueden hacerlo?" Si la respuesta es no -- si la interfaz *implica* la implementacion -- tienes una fuga.

**Takeaway:** Las fugas de informacion son el enemigo silencioso del buen diseno. No causan errores inmediatos. No aparecen en los tests. Se manifiestan meses despues, cuando un cambio que deberia ser local se convierte en una operacion que toca veinte archivos. Aprende a verlas y sellarlas.

---

## Descomposicion temporal: el error mas comun al dividir codigo

Hay un tipo especifico de fuga de informacion que es tan comun que merece su propia seccion. Ousterhout la llama *descomposicion temporal*, y es probablemente el error de diseno mas frecuente que cometen los desarrolladores cuando intentan modularizar su codigo.

La descomposicion temporal sucede cuando **divides el codigo segun el orden en que las operaciones ocurren en el tiempo**, en vez de segun el conocimiento que cada parte necesita.

> "En descomposicion temporal, la estructura de un sistema corresponde al orden en el tiempo en el que las operaciones ocurriran." [Ousterhout, 2018]

### El ejemplo clasico

Ousterhout describe un ejercicio que ponia a sus alumnos de Stanford: implementar el protocolo HTTP. Muchos equipos creaban dos clases separadas: una para *recibir* el mensaje HTTP de la red, y otra para *leerlo y parsearlo*. La logica era temporal: primero recibes, luego lees. Dos momentos, dos clases.

El problema: para recibir un mensaje HTTP, *necesitas leerlo parcialmente* (al menos los headers, para saber el Content-Length y determinar cuando termina el body). Asi que la logica de lectura del formato HTTP estaba en *ambas* clases. La decision de diseno -- "como se estructura un mensaje HTTP" -- se fugo de un modulo al otro. Si el formato cambiaba, habia que modificar las dos clases.

La solucion correcta era tener un solo modulo responsable de todo lo relacionado con el formato HTTP: recibir, leer, parsear. Un solo lugar donde vive el conocimiento de "como se estructura un mensaje HTTP".

### El patron en la practica

La descomposicion temporal se manifiesta frecuentemente en estos escenarios:

**Leer y escribir archivos.** Un equipo crea una clase para leer archivos de configuracion y otra para escribirlos. Ambas clases necesitan conocer el formato del archivo (JSON, YAML, INI, o lo que sea). El conocimiento del formato esta duplicado. La solucion: un solo modulo `ConfiguracionArchivo` que sepa leer *y* escribir.

**Validar y procesar.** Un equipo crea un modulo `ValidadorInscripcion` y otro modulo `ProcesadorInscripcion`. El validador verifica que el usuario tenga derecho a inscribirse; el procesador ejecuta la inscripcion. Pero ambos necesitan conocer las reglas de inscripcion: quien puede inscribirse, cuales son las restricciones, que excepciones existen. El conocimiento de las reglas esta duplicado. La solucion: un solo modulo `Inscripcion` que valide *y* procese.

**Antes y despues.** Un equipo crea funciones `preparar_pago()` y `confirmar_pago()` como dos modulos separados. Pero ambos necesitan entender la estructura de una transaccion: que campos tiene, que estados son validos, como se relacionan con el procesador de pagos. El conocimiento esta duplicado.

### Descomposicion temporal en la composicion funcional

En lenguajes funcionales, la composicion de funciones es una herramienta elegante. Pero puede llevar a descomposicion temporal cuando se abusa de ella. Considera este pipeline en Elixir:

```elixir
"datos"
  |> MiModulo.paso_1
  |> MiModulo.paso_2
  |> MiModulo.paso_3
```

Si `paso_1`, `paso_2` y `paso_3` siempre se usan en esa secuencia, nunca de forma independiente, y cada una depende del formato de salida de la anterior, tienes descomposicion temporal disfrazada de elegancia funcional. Tres funciones que comparten el mismo conocimiento (el formato de los datos intermedios) y que solo existen separadas porque reflejan el *orden* en que suceden las cosas, no las *decisiones de diseno* que encapsulan.

La solucion propuesta por Ousterhout es directa:

> "Concentra todas las operaciones relacionadas con una decision de diseno en un modulo." [Ousterhout, 2018]

Si el conocimiento del formato de los datos solo es relevante internamente, todo el pipeline puede ser una sola funcion que oculte los pasos intermedios. La interfaz es la entrada y la salida; los pasos son un detalle de implementacion.

### Como distinguir buena separacion de descomposicion temporal

No toda separacion secuencial es descomposicion temporal. La pregunta clave es: **las partes comparten conocimiento que deberia estar en un solo lugar?**

Si dos funciones se llaman en secuencia pero cada una encapsula un conocimiento *diferente* e *independiente*, la separacion esta bien. `autenticar_usuario()` seguido de `cargar_dashboard()` no es descomposicion temporal, porque cada funcion encapsula un dominio de conocimiento distinto.

Pero si dos funciones se llaman en secuencia y ambas necesitan conocer la misma estructura de datos, las mismas reglas de negocio, o el mismo formato -- entonces probablemente estan separadas por razon temporal (primero una, luego la otra) y deberian estar juntas.

**Takeaway:** La descomposicion temporal es la trampa de dividir el codigo segun *cuando* suceden las cosas en vez de segun *que conocimiento* encapsulan. Es el error mas comun porque el flujo temporal es lo primero que vemos cuando analizamos un sistema. Pero el criterio correcto no es el tiempo; es el conocimiento.

---

## Disenar modulos alrededor de conocimiento, no de flujo

Todo lo que hemos visto en este capitulo converge en una idea central que vale la pena hacer explicita: **los modulos deben disenarse alrededor de decisiones de diseno (conocimiento), no alrededor de flujos de ejecucion**.

La diferencia es profunda. Cuando disenas alrededor del flujo, preguntas: "Que pasos sigue el sistema para procesar una compra?" y creas un modulo por paso. Cuando disenas alrededor del conocimiento, preguntas: "Que decisiones de diseno podrian cambiar?" y creas un modulo por decision.

En DevCourses, las decisiones de diseno que son probables que cambien incluyen:

1. **Que procesador de pagos usamos.** Hoy es Stripe y MercadoPago. Manana podria ser PayPal, Conekta, o una solucion propia.
2. **Como se almacenan los videos.** Hoy es S3. Manana podria ser Cloudflare Stream, Mux, o un CDN propio.
3. **Como se calculan los precios.** Hoy es precio base menos cupon. Manana podria incluir impuestos por region, descuentos por volumen, o precios dinamicos.
4. **Como se envian las notificaciones.** Hoy son emails y push. Manana podria incluir SMS, Slack, o notificaciones in-app.
5. **Que formato tiene el contenido de un curso.** Hoy son videos. Manana podria incluir articulos interactivos, quizzes, y ejercicios de codigo.

Cada una de estas decisiones deberia vivir en *un solo modulo*. Y la interfaz de ese modulo deberia ser tal que, si la decision cambia, ningun otro modulo necesite enterarse.

Esto es exactamente lo que Parnas propuso en 1972:

> "Comienza con una lista de decisiones de diseno dificiles o decisiones que es probable que cambien. Cada modulo se disena para ocultar tal decision de los demas." [Parnas, 1972]

No empieces con un diagrama de flujo. Empieza con una lista de decisiones.

**Takeaway:** La pregunta correcta al disenar modulos no es "que pasos tiene este proceso?" sino "que decisiones de diseno podrian cambiar y como las aislamos?" Los modulos son recipientes de conocimiento, no estaciones en una linea de ensamblaje.

---

## Proyecto guia: detectando fugas de informacion en DevCourses

Volvamos a DevCourses. Despues del rediseno del capitulo anterior, el modulo de pagos es mucho mas profundo. Pero el sistema en general todavia tiene fugas de informacion que necesitamos detectar y sellar. Vamos a hacer una auditoria sistematica.

### Fuga 1: El controlador sabe que los videos estan en S3

El controlador que maneja la pagina del curso tiene esta logica:

```python
@app.get("/curso/{curso_id}/leccion/{leccion_id}")
def ver_leccion(curso_id: str, leccion_id: str):
    leccion = catalogo.obtener_leccion(leccion_id)

    # Generar URL firmada de S3
    video_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': 'devcourses-videos',
            'Key': leccion["s3_key"]
        },
        ExpiresIn=3600
    )

    return render("leccion.html", leccion=leccion, video_url=video_url)
```

**Diagnostico:** El controlador conoce tres decisiones de implementacion: (1) que los videos estan en S3, (2) el nombre del bucket, y (3) que se usan URLs firmadas con expiracion de una hora. Si migramos a Cloudflare Stream, este controlador -- y todos los que generen URLs de video -- necesitan cambiar.

**Solucion:** Mover la responsabilidad de generar URLs de video al modulo de video:

```python
@app.get("/curso/{curso_id}/leccion/{leccion_id}")
def ver_leccion(curso_id: str, leccion_id: str):
    leccion = catalogo.obtener_leccion(leccion_id)
    video_url = video.obtener_url_reproduccion(leccion.video_id)
    return render("leccion.html", leccion=leccion, video_url=video_url)
```

Ahora el controlador no sabe nada sobre S3, buckets, ni URLs firmadas. Solo sabe que puede pedir una URL de reproduccion dado un `video_id`. El modulo de video oculta como genera esa URL.

### Fuga 2: El frontend parsea directamente el formato de fecha de la base de datos

Los templates HTML de DevCourses tienen este patron:

```html
<span class="fecha">
    {{ curso.created_at | datetime_format("%d/%m/%Y") }}
</span>
```

El filtro `datetime_format` asume que `created_at` es un objeto `datetime` de Python, que a su vez viene directamente de PostgreSQL. Si cambias la forma en que almacenas las fechas (por ejemplo, a timestamps Unix), o si cambias el serializador de la API (por ejemplo, a strings ISO 8601), los templates se rompen.

**Solucion:** El modulo de catalogo deberia devolver las fechas ya formateadas, o al menos como objetos con un metodo `para_mostrar()`:

```python
# En el modulo de catalogo
class Curso:
    @property
    def fecha_publicacion(self) -> str:
        """Devuelve la fecha de publicacion formateada para el usuario."""
        return self._created_at.strftime("%d/%m/%Y")
```

O, si necesitas flexibilidad en el frontend:

```python
class Curso:
    @property
    def fecha_publicacion(self) -> FechaPublicacion:
        """Devuelve un objeto fecha independiente del almacenamiento."""
        return FechaPublicacion(self._created_at)
```

El template usa `{{ curso.fecha_publicacion }}` o `{{ curso.fecha_publicacion.formato_corto }}` sin saber nada sobre PostgreSQL, `datetime`, ni formatos de serializacion.

### Fuga 3: Dos modulos saben como calcular descuentos

Como vimos antes, tanto el modulo de pagos como el modulo de reportes financieros implementan la logica de descuentos. Pero hay una tercera fuga que no habíamos detectado: el panel de instructor *tambien* calcula descuentos para mostrar el "ingreso estimado por venta".

```python
# En el panel de instructor
def calcular_ingreso_estimado(curso):
    precio = curso["precio"]
    # Asumir descuento promedio del 15%
    precio_con_descuento = precio * 0.85
    comision_plataforma = precio_con_descuento * 0.30
    return precio_con_descuento - comision_plataforma
```

Tres modulos. Tres implementaciones de "como se aplica un descuento". Tres lugares que necesitan cambiar cuando la politica de precios evolucione.

**Solucion:** Crear un modulo `precios` que sea el unico responsable de todo lo relacionado con calculos de dinero:

```python
# modulo: precios.py

def calcular_precio_final(producto, cupon=None, usuario=None) -> PrecioCalculado:
    """Calcula el precio final considerando descuentos y region."""
    ...

def calcular_ingreso_instructor(producto, precio_final) -> Decimal:
    """Calcula cuanto recibe el instructor despues de comisiones."""
    ...

def calcular_descuento(precio_base, cupon) -> Decimal:
    """Aplica las reglas de descuento vigentes."""
    ...
```

Un solo modulo posee el conocimiento de como funcionan los precios. Los reportes, el panel de instructor, y el modulo de pagos lo consultan en vez de reimplementar la logica.

### Fuga 4: El orden de llamadas entre modulos esta hardcodeado

En varios endpoints del sistema, el flujo de "comprar un curso" esta disperso con un orden implicito:

```python
# En el controlador
validar_disponibilidad(curso_id)
verificar_no_duplicado(usuario_id, curso_id)
precio = calcular_precio(curso_id, cupon)
pago = procesar_pago(usuario_id, precio)
registrar_compra(usuario_id, curso_id, pago)
dar_acceso(usuario_id, curso_id)
enviar_email_confirmacion(usuario_id, curso_id)
registrar_analytics(usuario_id, curso_id, precio)
```

El controlador *sabe* el orden exacto de ocho operaciones. Si necesitas agregar un paso (por ejemplo, "verificar limite de fraude" entre `calcular_precio` y `procesar_pago`), tienes que modificar todos los controladores que implementen este flujo.

**Solucion:** La funcion `comprar()` del modulo de pagos que disenamos en el capitulo anterior ya resolvio esto. Todo el flujo es interno al modulo. El controlador solo llama:

```python
resultado = compras.comprar(usuario_id, producto_id, cupon_codigo)
```

El orden de las operaciones es un detalle de implementacion del modulo de compras, no algo que el controlador necesite conocer.

### El patron: pregunta "quien posee este conocimiento?"

En cada una de las cuatro fugas, la raiz del problema es la misma: un conocimiento que deberia pertenecer a *un solo* modulo esta disperso en multiples lugares.

La pregunta de auditoria mas potente que puedes hacer es: **"Quien posee este conocimiento?"** Si la respuesta es "varios modulos", tienes una fuga. Si la respuesta es "un solo modulo y los demas lo consultan", tienes un diseno saludable.

**Takeaway:** Las fugas de informacion se detectan preguntando "si esta decision de diseno cambia, cuantos modulos necesitan cambiar?" Si la respuesta es mas de uno, la informacion se fugo. La solucion siempre es la misma: centralizar el conocimiento en un solo modulo y exponer una interfaz que no revele la decision.

---

## Recomendaciones practicas para ocultar informacion

Hasta aqui hemos hablado de la teoria. Ahora veamos recomendaciones concretas que puedes aplicar inmediatamente para mejorar el ocultamiento de informacion en tu codigo.

### 1. Exponer estructuras de datos abstractas, no internas

Nunca devuelvas directamente filas de base de datos, respuestas de APIs externas, o estructuras internas del modulo. Siempre transforma a una representacion que tenga sentido para el consumidor *sin revelar la implementacion*.

```python
# Mal: expone la estructura de la tabla
def obtener_curso(curso_id):
    row = db.execute("SELECT * FROM cursos WHERE id = %s", curso_id)
    return dict(row)  # Devuelve todas las columnas, incluidas las internas

# Bien: devuelve una representacion abstracta
def obtener_curso(curso_id) -> Curso:
    row = db.execute("SELECT * FROM cursos WHERE id = %s", curso_id)
    return Curso(
        id=row["id"],
        titulo=row["titulo"],
        precio=Precio(row["precio_centavos"]),
        publicado=row["status"] == "published"
    )
```

La segunda version oculta que los precios se almacenan en centavos, que hay una columna `status` con un valor string, y que la base de datos tiene mas columnas de las que el consumidor necesita.

### 2. Disenar defaults inteligentes

La mejor interfaz es la que funciona sin que el usuario tenga que pensar. Los defaults inteligentes ocultan las decisiones de configuracion que la mayoria de los usuarios no necesita tomar.

```python
# Interfaz con demasiadas decisiones expuestas
def crear_curso(titulo, descripcion, precio, moneda="USD",
                formato_video="mp4", calidad_maxima="1080p",
                idioma="es", permite_descarga=False,
                tipo_licencia="standard", ...):
    ...

# Interfaz con defaults inteligentes
def crear_curso(titulo: str, descripcion: str,
                precio: Precio) -> Curso:
    """
    Crea un curso con la configuracion por defecto de la plataforma.
    La moneda, idioma y configuracion de video se derivan del
    perfil del instructor y las politicas de la plataforma.
    """
    ...
```

En la segunda version, el modulo resuelve internamente la moneda (basandose en la region del instructor), el formato de video (basandose en las politicas de la plataforma), y todas las demas configuraciones. Si el usuario necesita personalizarlas, puede hacerlo *despues* de crear el curso, a traves de interfaces especificas. Pero el caso comun -- crear un curso -- es simple.

### 3. Aislar el conocimiento incluso dentro de los modulos

El ocultamiento de informacion no solo aplica entre modulos. Tambien aplica *dentro* de un modulo. Si tienes una clase con diez metodos, no todos los metodos necesitan conocer todos los detalles internos.

```python
class ProcesadorPagos:
    def cobrar(self, usuario_id, monto, moneda, descripcion):
        metodo = self._obtener_metodo_pago(usuario_id)
        procesador = self._seleccionar_procesador(metodo)
        return procesador.cobrar(monto, moneda, metodo.token, descripcion)

    def _obtener_metodo_pago(self, usuario_id):
        # Solo este metodo sabe como se almacenan los metodos de pago
        ...

    def _seleccionar_procesador(self, metodo):
        # Solo este metodo sabe que procesadores existen y como elegir
        ...
```

Cada metodo privado oculta un aspecto del conocimiento. `cobrar()` no sabe como se almacenan los metodos de pago ni como se seleccionan los procesadores. Solo sabe que puede pedirlos.

### 4. No ocultar informacion que se necesita afuera

Hay un error sutil que es el *opuesto* de la fuga de informacion: ocultar demasiado. Si un modulo oculta informacion que sus usuarios legitimamente necesitan, los obliga a obtenerla de formas tortuosas -- lo cual es peor que no haberla ocultado.

```python
# Demasiado oculto: el usuario necesita el monto para mostrar un recibo
class ResultadoCompra:
    def __init__(self, exito):
        self.exito = exito
        # El monto, la moneda y el ID de transaccion
        # estan ocultos "por buenas practicas"

# Correctamente equilibrado: expone lo que el usuario necesita
class ResultadoCompra:
    def __init__(self, exito, monto, moneda, transaccion_id):
        self.exito = exito
        self.monto = monto
        self.moneda = moneda
        self.transaccion_id = transaccion_id
```

El criterio es: **oculta las decisiones de diseno que podrian cambiar. Expone la informacion que el consumidor necesita para hacer su trabajo.** El monto de una compra no es una decision de diseno; es un dato del negocio que el consumidor necesita. Ocultarlo no reduce la complejidad; la aumenta.

### 5. Nombrar sin revelar mecanismos

Los nombres son parte de la interfaz. Un nombre que revela el mecanismo interno es una fuga:

```python
# Nombres con fuga
enviar_email_ses(...)        # Revela que usamos Amazon SES
guardar_en_postgres(...)     # Revela la base de datos
cache_redis(...)             # Revela la tecnologia de cache

# Nombres sin fuga
notificar(...)               # Que hace, no como
persistir(...)               # Que hace, no donde
cachear(...)                 # Que hace, no con que
```

Los nombres deben comunicar *que* hace el modulo, no *como* lo hace. El "como" es un detalle de implementacion que deberia poder cambiar sin afectar a los usuarios del modulo.

**Takeaway:** Ocultar informacion en la practica requiere disciplina en cinco frentes: exponer datos abstractos (no estructuras internas), disenar defaults inteligentes, aislar conocimiento incluso dentro de los modulos, no ocultar lo que legitimamente se necesita afuera, y nombrar sin revelar mecanismos.

---

## Ejercicio: Auditoria de fugas en tu proyecto

Este ejercicio te tomara entre 20 y 30 minutos. Hazlo con papel y lapiz, o en una pizarra si lo haces con tu equipo.

### El checklist de las 10 preguntas

Para cada modulo principal de tu sistema, responde estas diez preguntas. Cada respuesta afirmativa es una posible fuga de informacion.

1. **Si cambio la base de datos, que otros modulos se rompen?** (Fuga de tecnologia de almacenamiento.)
2. **Si cambio el proveedor externo (pagos, email, cloud), que otros modulos se rompen?** (Fuga de dependencia externa.)
3. **Hay algun nombre de funcion o variable que mencione una tecnologia especifica?** (Fuga en los nombres.)
4. **Dos o mas modulos implementan el mismo calculo o regla de negocio?** (Fuga por duplicacion.)
5. **Algun consumidor de mi modulo necesita leer mi codigo fuente para poder usarlo?** (Fuga en la interfaz informal.)
6. **Devuelvo filas de base de datos directamente, sin transformar?** (Fuga de estructura interna.)
7. **Mis tests prueban detalles de implementacion o solo comportamiento?** (Fuga hacia los tests.)
8. **Hay funciones que siempre se llaman en una secuencia especifica?** (Posible descomposicion temporal.)
9. **Si reescribo un modulo desde cero manteniendo su interfaz, algo externo se rompe?** (Fuga general.)
10. **Hay conocimiento que "todo el equipo sabe" pero que no esta encapsulado en ningun modulo?** (Fuga hacia el conocimiento tribal.)

### Documenta lo que encuentres

Para cada fuga que detectes, escribe:

- **Que modulo la tiene:** (Ejemplo: "Controlador de lecciones")
- **Que conocimiento se fugo:** (Ejemplo: "Sabe que los videos estan en S3")
- **A donde se fugo:** (Ejemplo: "Al template HTML y al modulo de analytics")
- **Riesgo:** Que pasa si la decision de diseno cambia? (Ejemplo: "Habria que modificar 8 archivos si migramos de S3")
- **Solucion propuesta:** (Ejemplo: "Mover la generacion de URLs de video al modulo de video")

No necesitas arreglar todas las fugas inmediatamente. El valor del ejercicio esta en *ver* las fugas. Una vez que las ves, no puedes dejar de verlas. Y cada vez que toques uno de esos modulos, puedes sellar una fuga de paso.

**Takeaway:** Una auditoria de fugas es la forma mas efectiva de mejorar la calidad arquitectonica de un sistema existente. No requiere reescritura. Solo requiere ver donde se escapo la informacion y decidir como contenerla.

---

## Aplica esto el lunes

### 1. La prueba del reemplazo

Escoge un modulo de tu sistema -- el que quieras. Hazte esta pregunta: "Si reemplazo la implementacion completa de este modulo (diferente algoritmo, diferente base de datos, diferente proveedor), pero mantengo la misma interfaz, que codigo externo se rompe?" Cada pieza de codigo que se rompe es una fuga de informacion. Anota las fugas. No necesitas arreglarlas ahora. Solo anotalas.

### 2. Revisa las estructuras de datos que cruzam fronteras

Busca en tu codigo los lugares donde un modulo devuelve datos a otro. Esos datos son una representacion abstracta (independiente de la implementacion) o son una copia directa de la estructura interna (filas de base de datos, respuestas de APIs externas)? Si son lo segundo, tienes una fuga. Disenala de nuevo para que sea independiente de la implementacion.

### 3. Busca descomposicion temporal

Identifica dos funciones en tu codigo que siempre se llaman una despues de la otra. Preguntate: comparten conocimiento que deberia estar en un solo lugar? Si ambas necesitan entender el mismo formato de datos, las mismas reglas de negocio, o la misma estructura interna, probablemente son un caso de descomposicion temporal. Considera fusionarlas en un solo modulo.

---

## Resumen del capitulo

- El ocultamiento de informacion, propuesto por David Parnas en 1972, es el principio fundamental del diseno de software: cada modulo debe encapsular decisiones de diseno que es probable que cambien, y su interfaz debe revelar lo menos posible sobre su funcionamiento interno.
- El ocultamiento de informacion y la encapsulacion no son lo mismo. La encapsulacion es un mecanismo (agrupar datos y operaciones). El ocultamiento de informacion es un principio de diseno (asegurar que nadie *necesite* conocer los detalles internos). Puedes tener encapsulacion sin ocultamiento de informacion, y viceversa.
- Las fugas de informacion ocurren cuando una decision de diseno se refleja en multiples modulos. Los tipos mas comunes son: estructuras de datos internas que se exponen, formatos que cruzan fronteras, decisiones duplicadas en multiples modulos, e interfaces que revelan el mecanismo.
- La descomposicion temporal -- dividir el codigo segun el orden de ejecucion en vez de segun el conocimiento que encapsula -- es la fuente mas comun de fugas de informacion. La solucion es concentrar todo el conocimiento de una decision de diseno en un solo modulo.
- Los modulos deben disenarse alrededor de *conocimiento* (decisiones de diseno que podrian cambiar), no alrededor de *flujo* (pasos en un proceso). Empieza con una lista de decisiones, no con un diagrama de flujo.
- En la practica, el buen ocultamiento de informacion requiere: exponer datos abstractos, disenar defaults inteligentes, aislar conocimiento dentro de los modulos, no ocultar lo que se necesita afuera, y nombrar sin revelar mecanismos.

En el siguiente capitulo, vamos a explorar una dimension complementaria del diseno modular: que tan *generales* deben ser los modulos. No se trata solo de ocultar informacion, sino de decidir si tu modulo resuelve *un* problema o *una clase* de problemas. Veremos por que los modulos "algo generales" son casi siempre mejores que los ultra-especificos, y como encontrar el punto justo de generalidad.

---

### Referencias

- [Parnas, 1972] Parnas, D. L. "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 15(12), 1053-1058, 1972.
- [Ousterhout, 2018] Ousterhout, J. *A Philosophy of Software Design.* Yaknyam Press, 2018.
- [Baeldung, 2023] Baeldung. "Difference Between Information Hiding and Encapsulation." baeldung.com, 2023.
