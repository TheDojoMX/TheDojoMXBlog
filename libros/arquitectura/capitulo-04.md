# Capitulo 4: Los modulos profundos ocultan mas de lo que muestran

> "La mejor interfaz es la que parece simple pero resuelve algo dificil."

---

## Una linea de codigo que esconde un universo

Escribe esta linea en cualquier lenguaje de la familia Unix y observa lo que sucede:

```python
archivo = open("notas.txt", "w")
```

Una linea. Dos parametros. Un resultado.

Detras de esa linea, tu sistema operativo acaba de hacer lo siguiente:

1. Busco el archivo `notas.txt` en el directorio actual, recorriendo la estructura de inodos del sistema de archivos.
2. Verifico que tu proceso tiene permisos de escritura sobre ese archivo (o sobre el directorio, si el archivo no existe).
3. Si el archivo no existia, creo un nuevo inodo, asigno bloques de almacenamiento, y actualizo el directorio.
4. Si el archivo existia, trunco su contenido a cero bytes (porque el modo es `"w"`).
5. Busco la entrada mas baja disponible en la tabla de descriptores de archivo de tu proceso.
6. Creo una entrada en la tabla global de archivos abiertos del kernel, apuntando al inodo correcto.
7. Configuro el cursor de escritura en la posicion 0 del archivo.
8. Te devolvio un objeto que representa todo eso como un simple descriptor.

Son ocho operaciones complejas, cada una con sus propios casos de error, sus propias estructuras de datos, y sus propias dependencias con el hardware. Y tu no tuviste que saber *nada* de eso. Solo escribiste una linea.

Esto es un modulo profundo.

Ahora compara con la experiencia de leer un archivo en Java clasico:

```java
FileInputStream fis = new FileInputStream("notas.txt");
InputStreamReader isr = new InputStreamReader(fis, "UTF-8");
BufferedReader br = new BufferedReader(isr);
String linea = br.readLine();
br.close();
```

Cinco lineas. Tres objetos intermedios. Necesitas saber que existe un `FileInputStream` (que lee bytes), un `InputStreamReader` (que convierte bytes a caracteres usando un encoding), y un `BufferedReader` (que agrega buffering y permite leer por lineas). Cada capa "envuelve" a la anterior. Para leer una linea de un archivo, necesitas entender la jerarquia de decoradores de Java I/O.

Esto es un conjunto de modulos superficiales.

La diferencia entre ambos enfoques no es cosmetica. Es fundamental. Es la diferencia entre un sistema que absorbe complejidad y te protege de ella, y un sistema que la redistribuye y te la pone enfrente. Y es la idea central de este capitulo: **los mejores modulos ocultan mucho mas de lo que muestran** [Ousterhout, 2018].

**Takeaway:** Un modulo profundo ofrece una interfaz simple que oculta una implementacion poderosa. Un modulo superficial te obliga a hacer el trabajo que el deberia hacer por ti.

---

## Que es un modulo (definicion amplia)

Antes de hablar de profundidad, necesitamos un vocabulario compartido. En este libro, usamos "modulo" en el sentido mas amplio posible:

> Un modulo es cualquier construccion de software que agrupe codigo detras de una interfaz [Ousterhout, 2018].

Esto incluye:

| Construccion | Lenguaje / contexto |
|---|---|
| Funcion | Todos |
| Clase | Python, Java, C#, Ruby |
| Paquete / modulo | Python, Go, JavaScript |
| Biblioteca | C, C++, Rust |
| Aplicacion OTP | Erlang, Elixir |
| Microservicio | Arquitectura distribuida |
| API HTTP | Cualquiera |

Un modulo puede ser tan pequeno como una funcion de tres lineas o tan grande como un servicio completo con su propia base de datos. El tamano no importa. Lo que importa es que tiene dos partes:

1. **La interfaz:** Lo que el modulo muestra al exterior. Los parametros que recibe, los valores que devuelve, los errores que puede lanzar, y las convenciones que sus usuarios deben seguir.

2. **La implementacion:** Lo que el modulo esconde. Los algoritmos, las estructuras de datos, las conexiones externas, los casos especiales, y las optimizaciones que hacen que todo funcione.

La calidad de un modulo se mide por la relacion entre estas dos partes.

**Takeaway:** Un modulo es cualquier cosa que tenga interfaz e implementacion. Funciones, clases, paquetes, servicios -- todos son modulos. Los principios de este capitulo aplican a todos por igual.

---

## La interfaz: formal e informal

La interfaz de un modulo tiene dos dimensiones que son igualmente importantes, y una de ellas suele ser invisible.

### La interfaz formal

Es la parte explicita, declarada, verificable por el compilador o el runtime:

- **El nombre** de la funcion, clase, o endpoint.
- **Los parametros** que recibe (nombres, tipos, valores por defecto).
- **El tipo de retorno** (cuando el lenguaje lo permite).
- **Las excepciones** que puede lanzar (en lenguajes con checked exceptions).
- **La firma HTTP** en APIs (metodo, ruta, formato del body, codigos de respuesta).

La interfaz formal de `open()` en Python es: recibe un string (la ruta), un string opcional (el modo, default `"r"`), y retorna un objeto archivo. Simple, explicita, documentada.

### La interfaz informal

Es todo lo que necesitas saber para usar el modulo correctamente pero que *no esta declarado* en la firma:

- **Precondiciones:** "Debes llamar a `inicializar()` antes de llamar a `procesar()`."
- **Postcondiciones:** "Despues de llamar a `cerrar()`, no puedes llamar a ningun otro metodo."
- **Efectos secundarios:** "Esta funcion modifica la base de datos ademas de retornar un valor."
- **Convenciones de formato:** "Las fechas deben venir en formato ISO 8601."
- **Restricciones de concurrencia:** "Esta funcion no es thread-safe."
- **Dependencias de estado:** "Solo funciona si el usuario tiene una sesion activa."

La interfaz informal es peligrosa porque es invisible. No aparece en el autocompletado del IDE. No genera errores de compilacion. Solo se descubre leyendo la documentacion (si existe), leyendo el codigo fuente, o -- en el peor caso -- descubriendo un bug en produccion.

Ousterhout senala que la interfaz informal es una fuente importante de complejidad:

> "Si un desarrollador necesita leer el codigo de un modulo para poder usarlo, no hay abstraccion: toda la complejidad del modulo queda expuesta." [Ousterhout, 2018]

Un modulo bien disenado minimiza su interfaz informal. Idealmente, todo lo que necesitas saber esta en la interfaz formal. Los tipos son informativos. Los nombres son descriptivos. Los defaults son sensatos. Y los pocos aspectos informales que quedan estan documentados explicitamente.

**Ejemplo en DevCourses:** La funcion `cobrar_con_stripe(monto, moneda, usuario)` que Diana creo en el capitulo anterior tiene una interfaz formal clara. Pero tiene una interfaz informal oculta: asume que `usuario` tiene un atributo `stripe_customer_id` valido. Si no lo tiene, la funcion falla con un error criptico de Stripe. Esa dependencia deberia estar en la interfaz formal (quizas como un tipo `UsuarioConMetodoDePago`) o al menos documentada explicitamente.

**Takeaway:** La interfaz de un modulo tiene una parte formal (lo que el compilador verifica) y una parte informal (lo que solo la documentacion o el conocimiento tribal pueden comunicar). Minimizar la parte informal es uno de los objetivos del buen diseno.

---

## La metafora del rectangulo: modulos profundos vs. superficiales

Ousterhout propone una metafora visual que es extraordinariamente util para razonar sobre el diseno de modulos [Ousterhout, 2018]. Imagina cada modulo como un rectangulo:

- **El ancho del rectangulo** representa la complejidad de su interfaz (cuanto necesita saber el usuario del modulo para usarlo).
- **La altura del rectangulo** representa la funcionalidad que el modulo proporciona (cuanto trabajo hace por ti).

```
   Modulo profundo:          Modulo superficial:

   +---------+               +-------------------------+
   | interfaz|               |       interfaz          |
   +---------+               +-------------------------+
   |         |               |                         |
   |         |               +-------------------------+
   |  impl.  |
   |         |
   |         |
   |         |
   +---------+
```

Un **modulo profundo** tiene un rectangulo alto y estrecho: interfaz pequena, mucha funcionalidad. Hace mucho por ti sin pedirte mucho a cambio.

Un **modulo superficial** tiene un rectangulo ancho y bajo: interfaz grande, poca funcionalidad. Te pide mucho y te da poco.

La profundidad no es un numero absoluto. Es una *relacion* -- el ratio entre funcionalidad e interfaz. Un modulo que hace algo genuinamente complejo puede tener una interfaz algo mas grande sin ser superficial, siempre que la relacion sea favorable. La pregunta no es "cuantos parametros tiene?" sino "cuantos parametros tiene *en relacion con lo que resuelve*?"

### El ratio de profundidad

Puedes pensar en esto como una fraccion informal:

```
Profundidad = Funcionalidad oculta / Complejidad de la interfaz
```

Cuanto mayor sea este ratio, mas profundo es el modulo. Cuanto menor, mas superficial.

- `open("archivo.txt", "w")`: Interfaz de 2 parametros. Funcionalidad: manejo de inodos, permisos, descriptores de archivo, buffering, sistemas de archivos multiples. Ratio altisimo. Modulo profundo.

- `BufferedReader(InputStreamReader(FileInputStream("archivo.txt"), "UTF-8"))`: Interfaz de 3 constructores anidados con parametros cada uno. Funcionalidad de cada capa individual: minima (cada una agrega una sola transformacion). Ratio bajo. Modulos superficiales.

- `stripe.Charge.create(amount=1000, currency="usd", source=token)`: Interfaz de 3 parametros. Funcionalidad: validacion del token, comunicacion con la red bancaria, manejo de la transaccion, retries automaticos, manejo de errores, logging, cumplimiento PCI. Ratio alto. Modulo profundo.

**Takeaway:** Piensa en cada modulo como un rectangulo. El objetivo es que sea alto y estrecho: mucha funcionalidad detras de una interfaz simple. Ese es el ideal del diseno modular.

---

## Ejemplos clasicos de modulos profundos

Para que la idea de profundidad se vuelva concreta, examinemos algunos modulos que son ejemplos paradigmaticos de diseno profundo.

### El sistema de archivos Unix

Ya vimos `open()`, pero el sistema de archivos Unix completo es una obra maestra de profundidad. La interfaz completa para trabajar con archivos se reduce a cinco operaciones fundamentales: `open`, `read`, `write`, `close`, y `lseek`. Con estas cinco funciones puedes hacer *cualquier cosa* con archivos: leer, escribir, crear, truncar, posicionar el cursor, obtener metadatos.

Y la filosofia "todo es un archivo" extiende esta interfaz a dispositivos, pipes, sockets, y procesos. Cuando lees de `/dev/urandom`, usas la misma interfaz que cuando lees de un archivo de texto. Cuando escribes a un socket de red, usas la misma interfaz que cuando escribes a un archivo. Cinco funciones para interactuar con practicamente cualquier recurso del sistema operativo.

La implementacion detras de esas cinco funciones incluye: multiples sistemas de archivos (ext4, XFS, NTFS, NFS), caching de paginas en memoria, journaling para consistencia ante fallos, permisos, inodos, bloques, enlaces simbolicos, y docenas de optimizaciones especificas del hardware. Nada de eso lo ves. Nada de eso necesitas saber.

### El garbage collector

Si programas en un lenguaje con garbage collection (Java, Python, Go, JavaScript, C#, Ruby, Elixir), usas uno de los modulos mas profundos que existen. Su interfaz es: nada. Literalmente no tiene interfaz. No lo llamas. No le pasas parametros. No te devuelve nada. Simplemente funciona.

Su implementacion, en cambio, es asombrosamente compleja: algoritmos de mark-and-sweep, recoleccion generacional, compactacion de memoria, barreras de escritura, pausas de stop-the-world con optimizaciones incrementales, heuristicas de cuando correr y cuanto recolectar. En una JVM moderna, el garbage collector es uno de los componentes mas sofisticados del runtime, con decenas de parametros de tuning y anos de investigacion academica detras.

Interfaz: cero. Funcionalidad: enorme. Modulo infinitamente profundo.

### `Array.sort()`

Cuando llamas a `.sort()` en un array, obtienes el array ordenado. Un metodo, cero parametros (o uno opcional para el comparador).

La implementacion tipica en un runtime moderno es mucho mas sofisticada de lo que la mayoria de los programadores asume. V8 (el motor de JavaScript en Chrome y Node.js) usa Timsort -- un algoritmo hibrido que combina merge sort e insertion sort, adaptandose al patron de los datos. Python usa el mismo algoritmo (fue inventado para Python). Java usa una variante de quicksort dual-pivot para primitivos y Timsort para objetos. Go usa un pattern-defeating quicksort.

Cada una de estas implementaciones tiene decenas de optimizaciones para casos especiales: arrays ya ordenados, arrays parcialmente ordenados, arrays pequenos, y patrones repetitivos. Todo eso desaparece detras de `.sort()`.

### La API de Stripe

En el mundo de las APIs HTTP, Stripe es frecuentemente citada como ejemplo de diseno profundo. Para cobrar a un cliente, la interfaz minima es:

```python
stripe.Charge.create(
    amount=2000,
    currency="usd",
    source="tok_visa"
)
```

Tres parametros. Detras de esos tres parametros, Stripe maneja: validacion del token de tarjeta, comunicacion con la red de procesamiento de pagos (Visa, Mastercard, etc.), prevencion de fraude con machine learning, cumplimiento de regulaciones PCI DSS, retries automaticos con backoff exponencial, idempotencia para evitar cobros duplicados, conversion de monedas si aplica, creacion de registros de auditoria, y generacion de webhooks para notificaciones asincronas.

Es un rectangulo altisimo y estrecho. Por eso Stripe se convirtio en el estandar de la industria: oculta una cantidad enorme de complejidad detras de una interfaz que cualquier desarrollador puede usar en cinco minutos.

### El protocolo HTTP

HTTP es otro ejemplo notable. La interfaz basica es un verbo (`GET`, `POST`, `PUT`, `DELETE`), una URL, y opcionalmente un cuerpo y headers. Cuatro conceptos. Con esos cuatro conceptos, puedes interactuar con practicamente cualquier servicio en internet.

La implementacion detras de una solicitud HTTP incluye: resolucion DNS, establecimiento de conexion TCP (three-way handshake), negociacion TLS (si es HTTPS), compresion del cuerpo, chunked transfer encoding, manejo de cookies, redireccionamientos automaticos, caching con ETags y Last-Modified, keep-alive para reutilizar conexiones, y negociacion de contenido (Accept headers). El protocolo ha evolucionado de HTTP/1.0 a HTTP/3 con QUIC, cambiando completamente la capa de transporte, y la interfaz para el desarrollador se mantiene practicamente identica.

Tim Berners-Lee diseno HTTP en 1991 con una interfaz tan simple que un estudiante de primer ano puede hacer una solicitud con `curl` en la terminal. Treinta y cinco anos despues, esa misma interfaz mueve toda la economia digital. Eso es profundidad a escala civilizatoria.

### Que tienen en comun

Si observas los cinco ejemplos -- `open()`, el garbage collector, `.sort()`, Stripe, y HTTP -- notas un patron:

1. **La interfaz se puede explicar en una oracion.** "Abres un archivo con su nombre." "Ordenas un array." "Cobras una cantidad a una tarjeta." No necesitas un tutorial de 30 minutos para empezar a usar el modulo.

2. **La implementacion tardaria horas en explicarse.** Cualquiera de estos modulos tiene suficiente complejidad interna como para llenar un libro entero (y de hecho, los hay).

3. **La interfaz ha sido estable durante anos (o decadas).** `open()` funciona esencialmente igual desde los anos 70. HTTP desde los 90. `.sort()` desde que existe cada lenguaje. La estabilidad de la interfaz es consecuencia directa de su simplicidad: hay menos razones para cambiarla.

4. **La implementacion ha cambiado muchas veces.** Los sistemas de archivos han evolucionado de FAT a ext4 a ZFS. Los garbage collectors pasan por revoluciones cada pocos anos. Stripe reescribe sus internos regularmente. Nada de eso afecta a los usuarios de la interfaz.

Esta es la promesa del modulo profundo: **una interfaz estable que permite que la implementacion evolucione libremente.** Es la separacion entre *que* y *como* llevada a su expresion mas pura.

**Takeaway:** Los mejores modulos de la historia del software comparten una caracteristica: hacen algo inmensamente complejo accesible a traves de una interfaz que cabe en una oracion. La interfaz se mantiene estable durante anos mientras la implementacion evoluciona libremente detras de ella. Esa es la esencia de la profundidad.

---

## El anti-patron: modulos superficiales y classitis

Si los modulos profundos son el ideal, los modulos superficiales son el anti-patron. Un modulo superficial es aquel que tiene una interfaz compleja relativa a la poca funcionalidad que proporciona.

### La cultura del classitis

Ousterhout acuno un termino punzante para describir una patologia comun en ciertos ecosistemas de programacion: **classitis** [Ousterhout, 2018]. Es la tendencia a crear clases excesivamente pequenas que no ocultan nada significativo.

El classitis es especialmente prevalente en el ecosistema Java, donde una interpretacion extrema del principio de responsabilidad unica (SRP) lleva a clases de 10-15 lineas que no hacen casi nada por si solas. El resultado es que para cualquier operacion real, necesitas combinar 5, 10, o 15 clases, cada una con su propia interfaz que debes aprender.

El ejemplo clasico es Java I/O. Para leer un archivo de texto con buffering, necesitas:

```java
BufferedReader reader = new BufferedReader(
    new InputStreamReader(
        new FileInputStream("datos.csv"),
        StandardCharsets.UTF_8
    )
);
```

Tres clases anidadas. Cada una agrega una sola capacidad:

- `FileInputStream`: Lee bytes de un archivo.
- `InputStreamReader`: Convierte bytes a caracteres usando un encoding.
- `BufferedReader`: Agrega buffering y permite leer por lineas.

Cada clase individualmente es "simple". Cada una tiene "una sola responsabilidad". Pero el resultado es una interfaz compleja para una operacion que deberia ser trivial. Comparalo con Python:

```python
with open("datos.csv", "r") as archivo:
    linea = archivo.readline()
```

Python combina las tres responsabilidades en una sola interfaz. El encoding por defecto es UTF-8 (en Python 3). El buffering esta incluido. El manejo de recursos es automatico con `with`. Una linea hace lo que Java requiere cuatro.

Esto no significa que Python sea "mejor" que Java en general. Significa que para este caso particular, el diseno de Python es mas profundo: oculta mas complejidad detras de una interfaz mas simple.

### Por que el classitis es danino

Los modulos superficiales crean problemas acumulativos:

**1. Acumulacion de interfaces.** Cada clase pequena agrega una interfaz mas que los desarrolladores necesitan aprender. Si tienes 200 clases de 15 lineas, tienes 200 interfaces. Si tuvieras 40 clases de 75 lineas (la misma funcionalidad total), tendrias solo 40 interfaces. La superficie de aprendizaje se reduce a la quinta parte.

**2. Dispersion del conocimiento.** Cuando la funcionalidad esta repartida en muchas clases diminutas, entender un flujo completo requiere saltar entre docenas de archivos. La carga cognitiva no disminuye; se transforma de "una funcion compleja" a "muchas funciones simples con conexiones no obvias entre ellas".

**3. Indirection sin beneficio.** Cada capa de envoltorio es un nivel de indirection -- un salto que tu cerebro tiene que hacer para entender que esta pasando. El indirection es valioso cuando oculta complejidad real. Es danino cuando oculta trivialidad. Un getter que solo devuelve un campo privado es indirection sin beneficio.

**4. Falsa sensacion de orden.** El classitis produce codigo que *parece* limpio porque cada clase es pequena y tiene "una responsabilidad". Pero la complejidad no desaparecio; se redistribuyo. Y en muchos casos, la redistribucion la hizo *peor* porque ahora esta dispersa y conectada por dependencias implicitas.

### La diferencia entre profundo y "clase dios"

Hay una objecion natural al argumento de los modulos profundos: "Si hago los modulos grandes, no termino con clases dios?"

La respuesta es no, si entiendes la diferencia. Un modulo profundo tiene una interfaz *simple* y una implementacion *grande*. Una clase dios tiene una interfaz *grande* y una implementacion *grande*. La diferencia esta en la interfaz.

```
   Modulo profundo:          Clase dios:

   +----+                    +-------------------+
   | IF |                    |     interfaz      |
   +----+                    +-------------------+
   |    |                    |                   |
   | I  |                    |  implementacion   |
   | M  |                    |                   |
   | P  |                    |                   |
   | L  |                    +-------------------+
   |    |
   +----+
```

El modulo profundo absorbe complejidad: la esconde de sus usuarios. La clase dios esparce complejidad: la expone a traves de una interfaz enorme con docenas de metodos publicos.

Si tu modulo tiene 500 lineas de implementacion pero solo 3 funciones publicas con parametros claros, es profundo. Si tu modulo tiene 500 lineas de implementacion y 40 funciones publicas, es una clase dios. El tamano de la implementacion es el mismo. La diferencia es la interfaz.

**Takeaway:** El classitis -- la tendencia a crear clases excesivamente pequenas -- no reduce la complejidad. La redistribuye y la fragmenta, creando una red de dependencias que puede ser mas dificil de entender que una sola funcion grande. El objetivo no es tener clases pequenas; es tener interfaces simples.

---

## Proyecto guia: rediseñando el modulo de pagos de DevCourses como modulo profundo

Volvamos a DevCourses. En el capitulo anterior, Diana implemento el soporte para MercadoPago creando dos funciones separadas (`cobrar_con_stripe()` y `cobrar_con_mercadopago()`) con un condicional en la funcion de compra. Y Miguel implemento los bundles con condicionales `if tipo == "bundle"` por toda la funcion de compra. El resultado es una funcion de 120 lineas que sabe demasiado.

Vamos a redisenar el modulo de pagos como un modulo profundo. El objetivo: una interfaz tan simple que el codigo que la use no necesite saber *nada* sobre Stripe, MercadoPago, cupones, monedas, ni metodos de pago.

### Estado actual: el modulo superficial

Asi se ve la logica de compra actualmente (simplificada):

```python
def comprar_curso(usuario_id, curso_id, tipo="curso", metodo_pago="stripe",
                  cupon_codigo=None, moneda="USD"):
    # Validar que existe
    if tipo == "curso":
        producto = obtener_curso(curso_id)
    elif tipo == "bundle":
        producto = obtener_bundle(curso_id)

    # Calcular precio
    precio = producto["precio"]
    if moneda == "MXN":
        precio = convertir_a_mxn(precio)

    # Aplicar cupon
    if cupon_codigo:
        cupon = validar_cupon(cupon_codigo)
        if cupon:
            if cupon["tipo"] == "porcentaje":
                precio = precio * (1 - cupon["valor"] / 100)
            elif cupon["tipo"] == "monto":
                precio = max(0, precio - cupon["valor"])
            marcar_cupon_usado(cupon)

    # Cobrar
    if metodo_pago == "stripe":
        resultado = cobrar_con_stripe(precio, moneda, usuario_id)
    elif metodo_pago == "mercadopago":
        resultado = cobrar_con_mercadopago(precio, moneda, usuario_id)

    # Registrar compra
    registrar_compra(usuario_id, curso_id, tipo, precio, resultado["id"])

    # Dar acceso
    if tipo == "curso":
        dar_acceso_curso(usuario_id, curso_id)
    elif tipo == "bundle":
        for c in obtener_cursos_del_bundle(curso_id):
            dar_acceso_curso(usuario_id, c["id"])

    # Notificar
    enviar_email_compra(usuario_id, producto, precio)
    registrar_evento("compra", {"usuario": usuario_id, "monto": precio})

    return {"exito": True, "monto": precio}
```

Contemos los parametros: 6. Contemos las ramificaciones por tipo: al menos 4 bloques `if tipo ==`. Contemos los conceptos que el codigo que *llama* a esta funcion necesita saber: tipo de producto, metodo de pago, codigo de cupon, moneda.

Hagamos el perfil del rectangulo:

```
+--------------------------------------+
|  interfaz: 6 params, muchos conceptos|
+--------------------------------------+
|                                      |
|   implementacion: muchos detalles    |
|                                      |
+--------------------------------------+
```

Ancho y medianamente alto. Superficial.

### El rediseno: la interfaz profunda

El objetivo es reducir la interfaz al minimo absoluto. Que es lo *unico* que el codigo que llama a esta funcion realmente necesita especificar?

Pensemos desde el punto de vista de un controlador HTTP que recibe una solicitud de compra. El usuario ya esta autenticado (tenemos su ID). El producto ya fue seleccionado (tenemos su ID). El cupon ya fue ingresado (si aplica). El metodo de pago ya fue configurado en el perfil del usuario.

La interfaz minima es:

```python
def comprar(usuario_id: str, producto_id: str,
            cupon_codigo: str = None) -> ResultadoCompra:
    """
    Procesa la compra completa de un producto.

    El modulo resuelve internamente:
    - Que tipo de producto es (curso o bundle)
    - Que metodo de pago usar (segun el perfil del usuario)
    - En que moneda cobrar (segun la region del usuario)
    - Como aplicar el cupon (si es valido)
    - Como otorgar acceso (a un curso o a todos los del bundle)
    - Notificaciones y registro de eventos
    """
    ...
```

De 6 parametros a 3 (y uno es opcional). De "el caller necesita saber que tipo de producto es, que metodo de pago usar, y en que moneda cobrar" a "el caller solo necesita saber *que* quiere comprar *quien*".

Ahora veamos como se ve la implementacion interna:

```python
def comprar(usuario_id: str, producto_id: str,
            cupon_codigo: str = None) -> ResultadoCompra:

    # Obtener producto (el producto sabe su tipo, precio, y contenido)
    producto = catalogo.obtener_producto(producto_id)

    # Calcular precio final (el calculador maneja cupones y monedas)
    precio = precios.calcular_precio_final(
        producto=producto,
        usuario_id=usuario_id,
        cupon_codigo=cupon_codigo
    )

    # Procesar pago (el procesador sabe que metodo usar para este usuario)
    resultado_pago = procesador_pagos.cobrar(
        usuario_id=usuario_id,
        monto=precio.monto,
        moneda=precio.moneda,
        descripcion=producto.nombre
    )

    # Registrar compra
    compra = registro.crear_compra(
        usuario_id=usuario_id,
        producto=producto,
        precio=precio,
        pago=resultado_pago
    )

    # Otorgar acceso (el producto sabe que accesos dar)
    producto.otorgar_acceso(usuario_id)

    # Efectos secundarios (notificaciones, analytics)
    eventos.publicar("compra_completada", compra)

    return ResultadoCompra(
        exito=True,
        compra_id=compra.id,
        monto=precio.monto,
        moneda=precio.moneda
    )
```

Observa que sucedio:

1. **El concepto de "tipo de producto"** desaparecio de la interfaz. `catalogo.obtener_producto()` devuelve un objeto que sabe si es un curso o un bundle. El metodo `otorgar_acceso()` se comporta diferente segun el tipo, pero el codigo de compra no necesita saberlo.

2. **El concepto de "metodo de pago"** desaparecio de la interfaz. `procesador_pagos.cobrar()` consulta internamente que metodo tiene configurado el usuario y usa el procesador correcto (Stripe, MercadoPago, o el que sea).

3. **El concepto de "moneda"** desaparecio de la interfaz. `precios.calcular_precio_final()` determina la moneda basandose en la region del usuario.

4. **La logica de cupones** desaparecio de la interfaz. El modulo de precios la maneja internamente.

5. **Las notificaciones** desaparecieron del flujo principal. Se publican como eventos asincrono que otros modulos pueden escuchar.

Cada uno de estos sub-modulos es, a su vez, profundo. Veamos uno:

```python
# modulo: procesador_pagos.py

def cobrar(usuario_id: str, monto: Decimal, moneda: str,
           descripcion: str) -> ResultadoPago:
    """
    Cobra al usuario usando su metodo de pago configurado.

    Internamente:
    - Determina el procesador correcto (Stripe, MercadoPago, etc.)
    - Maneja reintentos con backoff exponencial
    - Loguea la transaccion para auditoria
    - Convierte moneda si el procesador no la soporta nativamente
    """
    metodo = _obtener_metodo_pago(usuario_id)
    procesador = _obtener_procesador(metodo.tipo)
    return procesador.cobrar(monto, moneda, metodo.token, descripcion)
```

La interfaz tiene 4 parametros, todos significativos y necesarios. La implementacion oculta la seleccion del procesador, los reintentos, el logging, y la conversion de moneda. Modulo profundo.

### El perfil del nuevo diseno

```
     +----------+
     | comprar  |
     | 3 params |
     +----------+
     |          |
     |  resuelve|
     |  tipo    |
     |  pago    |
     |  moneda  |
     |  cupon   |
     |  acceso  |
     |  eventos |
     |          |
     +----------+
```

Estrecho y alto. Profundo.

### Lo que ganamos

1. **Para agregar PayPal como tercer procesador:** Creas una clase `PayPalProcessor` que implementa la interfaz de procesador. La registras en la fabrica. Ningun otro modulo cambia. Cero modificaciones a `comprar()`.

2. **Para agregar un nuevo tipo de producto (suscripcion):** Creas un nuevo tipo de producto que implemente `otorgar_acceso()` a su manera (acceso temporal renovable). La funcion `comprar()` no cambia.

3. **Para agregar una nueva regla de cupones:** Solo modificas `precios.calcular_precio_final()`. Ningun otro modulo se entera.

4. **Para agregar un nuevo canal de notificacion:** Suscribes un nuevo listener al evento `compra_completada`. No tocas la funcion de compra.

Cada cambio es local. Cada modulo absorbe su propia complejidad. Eso es lo que significa disenar modulos profundos.

**Takeaway:** Redisenar un modulo como profundo no es agregar lineas de codigo. Es redistribuir la complejidad: sacarla de la interfaz y esconderla en la implementacion, donde pertenece.

---

## Ejercicio: dibuja el perfil de profundidad de tres modulos de tu proyecto

Este es un ejercicio practico que puedes hacer en 15 minutos con lapiz y papel, o en una pizarra si lo haces con tu equipo.

### Paso 1: Selecciona tres modulos (3 minutos)

Escoge tres modulos de tu proyecto actual. Idealmente:

- Uno que consideres "bien disenado" (te gusta trabajar con el).
- Uno que consideres "problematico" (te cuesta trabajo modificarlo).
- Uno que no hayas escrito tu (una dependencia, una biblioteca).

### Paso 2: Documenta la interfaz (5 minutos)

Para cada modulo, escribe:

- Cuantos metodos/funciones publicos tiene.
- Cuantos parametros tiene cada metodo (incluyendo parametros opcionales).
- Que necesitas saber *ademas* de los parametros para usarlo correctamente (la interfaz informal).
- Cuenta el total: numero de metodos x promedio de parametros + numero de elementos informales. Esa es la "anchura" de tu rectangulo.

### Paso 3: Documenta la funcionalidad (5 minutos)

Para cada modulo, escribe:

- Que operaciones complejas realiza internamente.
- Cuantas dependencias externas maneja (bases de datos, APIs, filesystem).
- Que decisiones de diseno oculta de sus usuarios.
- Cuenta el total: suma de operaciones + dependencias + decisiones ocultas. Esa es la "altura" de tu rectangulo.

### Paso 4: Dibuja y compara (2 minutos)

Dibuja tres rectangulos, uno por modulo. El ancho es proporcional a la interfaz. La altura es proporcional a la funcionalidad. No necesitas numeros exactos -- el ejercicio es visual.

Ahora compara:

- El modulo "bien disenado", es alto y estrecho?
- El modulo "problematico", es ancho y bajo? O ancho y alto (clase dios)?
- El modulo externo (la biblioteca), que perfil tiene?

### Lo que buscar

- **Si el modulo problematico es ancho y bajo:** Es superficial. La solucion es absorber mas funcionalidad -- quizas fusionando dos modulos superficiales en uno profundo, o moviendo logica del caller hacia el modulo.

- **Si el modulo problematico es ancho y alto:** Es una clase dios. La solucion es reducir la interfaz -- quizas dividiendo los metodos publicos en dos o tres interfaces mas enfocadas, cada una con una responsabilidad clara.

- **Si el modulo problematico es estrecho y bajo:** Es un modulo trivial. Preguntate si deberia existir como modulo independiente o si deberia ser parte de otro modulo mas grande.

**Takeaway:** El perfil de profundidad es una herramienta de diagnostico visual. No necesitas numeros exactos. Solo necesitas ver si tu rectangulo es alto y estrecho (profundo, bien), ancho y bajo (superficial, mal), o ancho y alto (dios, peligroso).

---

## Aplica esto el lunes

### 1. Encuentra tu funcion mas superficial

Busca la funcion publica con mas parametros en tu proyecto. Cuenta cuantos tiene. Ahora preguntate: cuantos de esos parametros *realmente* necesita el caller proporcionar? Los demas podria resolverlos el modulo internamente? Si puedes eliminar al menos 2 parametros moviendo la logica hacia adentro del modulo, hazlo. Acabas de hacer tu modulo un poco mas profundo.

### 2. Identifica un caso de classitis

Busca un flujo en tu codigo donde necesites instanciar o llamar a mas de 3 clases/funciones en secuencia para lograr una sola operacion conceptual. Eso es un candidato para un modulo profundo. Diseña en papel como se veria una unica funcion que encapsule toda la secuencia. Cual seria su interfaz minima?

### 3. Haz la prueba del rectangulo con tu equipo

En tu proxima reunion tecnica o code review, dibuja el rectangulo de un modulo que esten discutiendo. Es profundo o superficial? Usen el diagrama como herramienta de discusion. "Queremos que este rectangulo sea mas alto y estrecho. Como lo logramos?" Es una conversacion mas productiva que "deberiamos refactorizar esto", porque tiene un objetivo visual concreto.

---

## Resumen del capitulo

- Un modulo es cualquier construccion que agrupe codigo detras de una interfaz. Funciones, clases, paquetes, servicios -- todos son modulos.
- La interfaz tiene una dimension formal (parametros, tipos, retornos) y una dimension informal (precondiciones, efectos secundarios, convenciones). Minimizar la dimension informal es un objetivo de diseno.
- La metafora del rectangulo de Ousterhout: un modulo profundo es un rectangulo alto y estrecho (mucha funcionalidad, interfaz simple). Un modulo superficial es ancho y bajo (poca funcionalidad, interfaz compleja).
- Ejemplos clasicos de modulos profundos: `open()` de Unix, el garbage collector, `Array.sort()`, la API de Stripe. Todos ocultan complejidad enorme detras de interfaces minimas.
- El classitis -- crear clases excesivamente pequenas -- no reduce la complejidad. La fragmenta y la redistribuye, creando acumulacion de interfaces y dispersion del conocimiento.
- La diferencia entre un modulo profundo y una clase dios esta en la interfaz: el profundo tiene interfaz simple e implementacion grande; la clase dios tiene ambas grandes.
- El modulo de pagos de DevCourses se transformo de una funcion de 6 parametros con multiples condicionales a una funcion de 3 parametros donde cada sub-modulo absorbe su propia complejidad.
- El perfil de profundidad es una herramienta de diagnostico visual: dibuja tus modulos como rectangulos y evalua si son altos y estrechos (bien) o anchos y bajos (problema).

En el siguiente capitulo, vamos a explorar *que* exactamente deben ocultar los modulos. No se trata solo de "meter codigo adentro". Se trata de identificar las *decisiones de diseno* que deben quedar encapsuladas, y de detectar las *fugas de informacion* que rompen el encapsulamiento. Vamos a ver el principio que David Parnas articulo en 1972 y que sigue siendo, medio siglo despues, la idea mas importante del diseno de software.

---

### Referencias

- [Ousterhout, 2018] Ousterhout, J. *A Philosophy of Software Design.* Yaknyam Press, 2018.
- [Parnas, 1972] Parnas, D. L. "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 15(12), 1053-1058, 1972.
