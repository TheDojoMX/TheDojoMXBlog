# Capitulo 6: Modulos de proposito general -- invierte hoy, gana manana

> "Tu modulo resuelve UN problema o UNA CLASE de problemas?"

---

## El cargador de Nokia y el cable USB

En 2005, si querias cargar tu telefono celular, necesitabas un cargador *exacto* para tu modelo. Nokia tenia un conector. Sony Ericsson tenia otro. Motorola tenia otro. Samsung tenia dos diferentes, dependiendo del modelo. Cada cargador resolvia *un* problema: cargar *ese* telefono. Si perdias el cargador, tenias que comprar exactamente el mismo. Si cambiabas de telefono, tu cargador viejo era basura.

En 2025, cargas tu telefono, tus audifonos, tu laptop, tu tablet, tu consola portatil, y tu bateria externa con el mismo cable: USB-C. Un conector resuelve *una clase* de problemas: transferir energia (y datos) entre dispositivos.

La diferencia entre el cargador de Nokia y el cable USB-C no es solo una diferencia tecnica. Es una diferencia de *filosofia de diseno*. El cargador de Nokia fue disenado para resolver el problema inmediato del dispositivo especifico. USB fue disenado para resolver una clase general de problemas de conectividad entre dispositivos.

Los modulos de software enfrentan exactamente la misma disyuntiva. Puedes disenar un modulo que resuelva *tu* problema de *hoy* -- y solo ese. O puedes disenar un modulo que resuelva una clase de problemas similares, de los cuales tu problema de hoy es simplemente una instancia.

Este capitulo argumenta que la segunda opcion es casi siempre la correcta. No porque debas construir frameworks universales antes de resolver tu primer caso de uso. Sino porque los modulos "algo generales" -- ni ultra-especificos ni absurdamente genericos -- producen interfaces mas simples, ocultan mejor la informacion, y son mas faciles de mantener y extender.

**Takeaway:** Un modulo ultra-especifico es como un cargador de Nokia: resuelve un caso y nada mas. Un modulo de proposito algo general es como USB-C: resuelve tu caso de hoy y muchos que vendran. La clave esta en encontrar el nivel correcto de generalidad.

---

## El espectro de generalidad

La generalidad de un modulo no es binaria (especifico o general). Es un espectro continuo que va desde el hardcoding extremo hasta la biblioteca universal.

```
Ultra-especifico                                    Ultra-general
     |                                                    |
     |  Hardcoding  |  Caso unico  |  Algo general  |  Biblioteca  |  Framework  |
     |              |              |                 |              |             |
     v              v              v                 v              v             v
  "Solo sirve     "Solo sirve    "Sirve para      "Sirve para    "Sirve para
   para este       para este      varios casos     cualquier      cualquier
   valor"          caso de uso"   similares"       dominio"       aplicacion"
```

### Ultra-especifico: el hardcoding

El extremo izquierdo es el hardcoding. Un valor fijo en el codigo que solo sirve para una instancia del problema:

```python
def calcular_impuesto(precio):
    return precio * 0.16  # IVA de Mexico, hardcodeado
```

Solo funciona para Mexico. Solo funciona para la tasa actual. Si la tasa cambia o si necesitas calcular impuestos en otro pais, reescribes la funcion.

### Caso unico: el modulo ultra-especifico

Un paso arriba del hardcoding: el modulo que resuelve un solo caso de uso de manera correcta pero que no puede reutilizarse:

```python
def registrar_libro(titulo, autor, isbn, editorial, paginas, fecha_publicacion):
    ...

def registrar_revista(titulo, editor, issn, numero, periodicidad):
    ...

def registrar_panfleto(titulo, autor, paginas, tiraje):
    ...
```

Tres funciones para tres tipos de publicacion. Cada una resuelve *su* caso correctamente. Pero si manana necesitas registrar "podcasts" o "articulos academicos", necesitas crear otra funcion. La interfaz crece linealmente con el numero de tipos de contenido.

### Algo general: el punto optimo

El punto optimo del espectro -- que es donde la mayoria de tus modulos deberian estar:

```python
def registrar_publicacion(titulo: str, tipo: TipoPublicacion,
                          metadata: dict) -> Publicacion:
    ...
```

Una sola funcion para registrar cualquier tipo de publicacion. El `tipo` determina que validaciones se aplican. La `metadata` contiene los campos especificos de cada tipo. Agregar un nuevo tipo de publicacion no requiere una nueva funcion; requiere un nuevo `TipoPublicacion` y su esquema de metadata.

### Ultra-general: la biblioteca

Mas alla del "algo general" estan las bibliotecas y los frameworks, que resuelven problemas en *cualquier* dominio:

```python
# Una biblioteca es extremadamente general
lista = sorted(datos, key=lambda x: x.fecha)
```

`sorted()` no sabe nada sobre tu dominio. Ordena *cualquier cosa* segun *cualquier criterio*. Es un modulo de proposito completamente general.

### Donde deberias estar

La tentacion de muchos desarrolladores es quedarse en el extremo izquierdo (ultra-especifico) porque es lo mas rapido de implementar hoy. La tentacion de otros es irse al extremo derecho (ultra-general) porque se imaginan todos los casos futuros posibles. Ambos extremos son daninos.

El punto optimo para la mayoria de los modulos que escribes en tu dia a dia es el rango *algo general*. Ousterhout lo describe asi:

> "La interfaz de un modulo deberia ser lo suficientemente general como para soportar multiples usos, pero la implementacion puede enfocarse en las necesidades actuales." [Ousterhout, 2018]

Nota la distincion crucial: la *interfaz* es general, pero la *implementacion* puede ser especifica para lo que necesitas hoy. No necesitas implementar todos los casos de uso posibles. Solo necesitas que la interfaz no *impida* esos casos de uso en el futuro.

**Takeaway:** La generalidad es un espectro. El punto optimo esta en "algo general": una interfaz que pueda servir para varios casos similares, con una implementacion enfocada en las necesidades actuales. Ni hardcoding ni framework universal.

---

## Por que los modulos "algo generales" son mejores que los ultra-especificos

La recomendacion de crear modulos de proposito algo general puede parecer contraintuitiva. La sabiduria convencional dice: "No construyas lo que no necesitas" (YAGNI). "Resuelve el problema de hoy, no el de manana." "La generalizacion prematura es la raiz del mal."

Estos consejos no estan equivocados. Pero suelen malinterpretarse como una licencia para crear modulos ultra-especificos. Y los modulos ultra-especificos tienen problemas estructurales que los hacen peores incluso para el caso de uso actual.

### Razon 1: Los modulos algo generales tienen interfaces mas simples

Esto es lo que mas sorprende a los desarrolladores cuando lo ven por primera vez: **generalizar la interfaz frecuentemente la hace mas simple, no mas compleja**.

El ejemplo clasico es el editor de texto que Ousterhout usa en *A Philosophy of Software Design* [Ousterhout, 2018]. Imagina que estas disenando la clase que almacena el texto en memoria y necesitas soportar las operaciones tipicas de un editor: insertar texto, borrar hacia adelante, borrar hacia atras, seleccionar, copiar, pegar, buscar y reemplazar.

**Diseno ultra-especifico:** Una funcion para cada operacion de la interfaz de usuario.

```python
class EditorTexto:
    def insertar_texto(self, posicion, texto): ...
    def borrar_hacia_adelante(self, posicion, cantidad): ...
    def borrar_hacia_atras(self, posicion, cantidad): ...
    def borrar_seleccion(self, inicio, fin): ...
    def copiar_seleccion(self, inicio, fin) -> str: ...
    def pegar(self, posicion, texto): ...
    def reemplazar(self, inicio, fin, texto_nuevo): ...
    def buscar(self, texto) -> int: ...
    def buscar_y_reemplazar(self, texto, reemplazo): ...
```

Nueve funciones. Cada una especifica para una operacion de la interfaz grafica. Si agregas una nueva operacion (por ejemplo, "transponer caracteres"), necesitas una nueva funcion.

**Diseno algo general:** Operaciones fundamentales que componen cualquier edicion.

```python
class EditorTexto:
    def insertar(self, posicion: int, texto: str): ...
    def borrar(self, posicion: int, cantidad: int): ...
    def obtener_texto(self, posicion: int, cantidad: int) -> str: ...
    def longitud(self) -> int: ...
```

Cuatro funciones. Todas las operaciones del diseno anterior se pueden construir con estas cuatro:

- **Borrar hacia adelante:** `borrar(posicion, cantidad)`.
- **Borrar hacia atras:** `borrar(posicion - cantidad, cantidad)`.
- **Borrar seleccion:** `borrar(inicio, fin - inicio)`.
- **Copiar seleccion:** `obtener_texto(inicio, fin - inicio)`.
- **Pegar:** `insertar(posicion, texto)`.
- **Reemplazar:** `borrar(inicio, fin - inicio)` + `insertar(inicio, texto_nuevo)`.
- **Buscar y reemplazar:** Combinacion de `obtener_texto`, `borrar`, e `insertar`.

De nueve funciones a cuatro. La interfaz general es *mas simple* que la especifica. No porque sacrifique funcionalidad, sino porque identifica las operaciones *fundamentales* de las cuales todas las demas son composiciones.

### Razon 2: Los modulos algo generales ocultan mejor la informacion

Cuando una funcion es ultra-especifica, su nombre y sus parametros revelan el contexto de uso. `borrar_seleccion(inicio, fin)` revela que hay un concepto de "seleccion" en el sistema. `enviar_email_bienvenida(usuario_id)` revela que existe un tipo especifico de email. `calcular_precio_curso_con_cupon_porcentual(precio, porcentaje)` revela tres cosas: que hay cursos, que hay cupones, y que los cupones son porcentuales.

Una interfaz algo general oculta el contexto: `borrar(posicion, cantidad)` no sabe nada sobre selecciones. `notificar(usuario_id, evento, datos)` no sabe nada sobre emails de bienvenida. `calcular_descuento(precio, regla)` no sabe si el descuento es para un curso, un bundle, o una suscripcion.

Menos contexto en la interfaz significa menos fugas de informacion. Y menos fugas significa que la implementacion puede evolucionar sin afectar a los consumidores.

### Razon 3: Los modulos algo generales son mas reutilizables

Esto es casi tautologico, pero vale la pena decirlo explicitamente: un modulo que resuelve una clase de problemas se puede usar en mas lugares que un modulo que resuelve un solo problema.

En DevCourses, si tienes `enviar_email_bienvenida()`, `enviar_email_compra()`, `enviar_email_recordatorio()`, y `enviar_email_certificado()`, tienes cuatro funciones que solo sirven para su caso especifico. Si tienes `enviar_notificacion(usuario_id, tipo_evento, datos)`, tienes una funcion que sirve para *cualquier* notificacion, incluidas las que todavia no has imaginado.

### Razon 4: Los modulos algo generales reducen el acoplamiento

Un modulo ultra-especifico acopla a sus consumidores al caso de uso actual. Si la interfaz cambia porque el caso de uso evoluciona, todos los consumidores deben adaptarse. Un modulo algo general acopla a sus consumidores a una abstraccion estable que sobrevive la evolucion del caso de uso.

**Takeaway:** Los modulos algo generales son mejores que los ultra-especificos por cuatro razones concretas: interfaces mas simples, mejor ocultamiento de informacion, mayor reutilizacion, y menor acoplamiento. Generalizar la interfaz no es agregar complejidad; frecuentemente es *reducirla*.

---

## La regla de los 3 usos: cuando generalizar y cuando no

Si los modulos algo generales son mejores, surge una pregunta practica: cuando generalizo? Lo hago desde la primera vez que escribo el codigo, o espero a que se repita?

La respuesta la da una heuristica conocida como la "Regla de Tres" (Rule of Three), que Jeff Atwood popularizo en el contexto de software [Atwood, 2007]:

> "La primera vez que haces algo, simplemente hazlo. La segunda vez que haces algo similar, notas la duplicacion pero la toleras. La tercera vez que haces algo similar, refactoriza."

La Regla de Tres es una defensa contra la generalizacion prematura. Cuando solo tienes un caso de uso, no puedes saber que es lo general y que es lo especifico. Cuando tienes dos, puedes sospechar pero no confirmar. Cuando tienes tres, los patrones reales se hacen visibles y puedes generalizar con confianza.

### Aplicacion practica

**Primera vez:** Escribe la solucion especifica. No te preocupes por reutilizacion. Enfocate en resolver el problema.

```python
# Primera notificacion: email de bienvenida
def enviar_email_bienvenida(usuario_id):
    usuario = obtener_usuario(usuario_id)
    asunto = f"Bienvenido a DevCourses, {usuario.nombre}"
    cuerpo = renderizar_template("bienvenida.html", usuario=usuario)
    enviar_email(usuario.email, asunto, cuerpo)
```

**Segunda vez:** Notas la similitud con el primer caso. Resiste la tentacion de generalizar inmediatamente.

```python
# Segunda notificacion: email de compra
def enviar_email_compra(usuario_id, curso_id):
    usuario = obtener_usuario(usuario_id)
    curso = obtener_curso(curso_id)
    asunto = f"Confirmacion de compra: {curso.titulo}"
    cuerpo = renderizar_template("compra.html", usuario=usuario, curso=curso)
    enviar_email(usuario.email, asunto, cuerpo)
```

Las dos funciones son casi identicas. La unica diferencia es el template y los datos. Pero con solo dos casos, no sabes si todos los futuros casos seguiran el mismo patron.

**Tercera vez:** Ahora puedes ver el patron con claridad.

```python
# Tercera notificacion: email de certificado
def enviar_email_certificado(usuario_id, curso_id, certificado_id):
    usuario = obtener_usuario(usuario_id)
    curso = obtener_curso(curso_id)
    certificado = obtener_certificado(certificado_id)
    asunto = f"Tu certificado de {curso.titulo}"
    cuerpo = renderizar_template("certificado.html",
                                  usuario=usuario,
                                  curso=curso,
                                  certificado=certificado)
    enviar_email(usuario.email, asunto, cuerpo)
```

Tres casos. El patron es evidente: obtener datos, renderizar un template, enviar un email. Ahora si, refactoriza:

```python
def notificar_email(usuario_id: str, tipo_evento: str,
                    datos: dict) -> None:
    """Envia una notificacion por email basada en el tipo de evento."""
    usuario = obtener_usuario(usuario_id)
    config = obtener_config_notificacion(tipo_evento)
    cuerpo = renderizar_template(config.template, usuario=usuario, **datos)
    enviar_email(usuario.email, config.asunto_template.format(**datos), cuerpo)
```

Una funcion que reemplaza tres (y las que vendran). La generalizacion esta justificada porque viste el patron real en tres instancias concretas.

### Cuando romper la regla y generalizar antes

La Regla de Tres es una heuristica, no una ley. Hay situaciones donde es correcto generalizar desde la primera vez:

1. **El patron es obvio y bien conocido.** Si estas implementando un CRUD, no necesitas esperar tres entidades para crear un modulo generico de persistencia. El patron esta probado por decadas.

2. **La generalidad simplifica la interfaz.** Si la version general tiene *menos* parametros que la version especifica (como en el ejemplo del editor de texto), generaliza inmediatamente. Estas haciendo el codigo mas simple, no mas complejo.

3. **El costo de no generalizar es alto.** Si sabes que agregar cada nuevo caso especifico requiere tocar diez archivos, la generalizacion temprana tiene un retorno claro.

4. **Estas disenando una API publica.** Si tu modulo sera usado por otros equipos o por terceros, la interfaz deberia ser lo mas general posible desde el inicio, porque cambiarla despues es costoso o imposible.

### Cuando esperar mas de tres

A veces, tres instancias no son suficientes para ver el patron real:

1. **Los tres casos son "accidentalmente" similares.** Se parecen hoy, pero representan conceptos de negocio diferentes que evolucionaran de formas distintas. Generalizar crearia un acoplamiento artificial.

2. **La generalizacion requiere una abstraccion no trivial.** Si para unificar tres casos necesitas crear una jerarquia de clases con herencia multiple y un visitor pattern, quizas es mejor mantenerlos separados.

Erik Bernhardsson lo resumio bien: "La primera vez que resuelves algo, no sabes nada. La segunda vez, empiezas a ver similitudes. La tercera vez, puedes ver el patron general" [Bernhardsson, 2017]. Pero ver el patron no significa que debas automaticamente construir la abstraccion. Evalua si la abstraccion simplifica o complica.

**Takeaway:** La Regla de Tres dice: primera vez, hazlo; segunda vez, nota la duplicacion; tercera vez, refactoriza. Es una defensa contra la generalizacion prematura. Pero no es absoluta: si la generalidad simplifica la interfaz o si el patron es bien conocido, generaliza antes.

---

## La interfaz general, la implementacion especifica

Hay una idea clave de Ousterhout que merece su propia seccion porque es contraintuitiva y extraordinariamente util:

> "La interfaz de un modulo deberia ser lo suficientemente general como para soportar multiples usos. Sin embargo, la implementacion no necesita ser general: puede enfocarse unicamente en lo que necesitas hoy." [Ousterhout, 2018]

Esto resuelve la tension entre YAGNI ("no construyas lo que no necesitas") y la generalidad ("diseña para el futuro"). La respuesta es: **diseña la interfaz para el futuro, implementa para el presente**.

### Ejemplo concreto

En DevCourses, necesitas un modulo para almacenar el progreso del estudiante en un curso. Hoy, el progreso es simple: el porcentaje de lecciones vistas.

**Diseno ultra-especifico (interfaz y implementacion especificas):**

```python
def registrar_leccion_vista(usuario_id: str, curso_id: str,
                            leccion_id: str) -> None:
    """Marca una leccion como vista y recalcula el porcentaje."""
    db.execute("""
        INSERT INTO lecciones_vistas (usuario_id, leccion_id)
        VALUES (%s, %s)
    """, usuario_id, leccion_id)

    total = db.execute("""
        SELECT COUNT(*) FROM lecciones WHERE curso_id = %s
    """, curso_id)

    vistas = db.execute("""
        SELECT COUNT(*) FROM lecciones_vistas
        WHERE usuario_id = %s AND leccion_id IN
            (SELECT id FROM lecciones WHERE curso_id = %s)
    """, usuario_id, curso_id)

    porcentaje = (vistas / total) * 100
    db.execute("""
        UPDATE progreso SET porcentaje = %s
        WHERE usuario_id = %s AND curso_id = %s
    """, porcentaje, usuario_id, curso_id)
```

Funciona. Pero la interfaz esta atada al concepto de "leccion vista" y "porcentaje". Si manana el progreso incluye quizzes, ejercicios de codigo, o tiempo de estudio, necesitas una interfaz completamente diferente.

**Diseno "algo general" (interfaz general, implementacion especifica):**

```python
def registrar_progreso(usuario_id: str, curso_id: str,
                       actividad: Actividad) -> ProgresoActualizado:
    """
    Registra que un usuario completo una actividad en un curso.
    Recalcula el progreso total.

    Tipos de actividad soportados actualmente: LECCION_VISTA.
    La interfaz soporta extensiones futuras sin cambios.
    """
    # Implementacion actual: solo maneja lecciones vistas
    if actividad.tipo != TipoActividad.LECCION_VISTA:
        raise NoSoportado(f"Tipo de actividad no soportado: {actividad.tipo}")

    _marcar_leccion_vista(usuario_id, actividad.recurso_id)
    porcentaje = _calcular_porcentaje_lecciones(usuario_id, curso_id)

    return ProgresoActualizado(
        porcentaje_total=porcentaje,
        actividades_completadas=1
    )
```

La interfaz es general: acepta cualquier `Actividad` y devuelve un `ProgresoActualizado`. La implementacion es especifica: solo maneja `LECCION_VISTA` y lanza una excepcion para cualquier otro tipo. No implementamos lo que no necesitamos (YAGNI). Pero cuando necesitemos agregar quizzes, la interfaz no cambia. Solo la implementacion se extiende.

Este patron -- interfaz general, implementacion especifica -- es la clave para reconciliar la generalidad con el pragmatismo.

**Takeaway:** No necesitas implementar todos los casos de uso futuros. Solo necesitas que la interfaz no los *impida*. Diseña la interfaz para la clase de problemas. Implementa para el caso de hoy. Extiende manana sin romper.

---

## Cuando separar y cuando juntar: el arbol de decision

Hasta aqui hemos hablado de que tan generales deben ser los modulos. Pero hay una pregunta complementaria que surge constantemente en la practica: *este codigo deberia estar junto en un modulo o separado en dos?*

Es una pregunta que genera debates acalorados. Los seguidores de Robert C. Martin tienden a separar: funciones pequenas, clases de una responsabilidad, muchos archivos. Los seguidores de Ousterhout tienden a juntar: modulos profundos, menos interfaces, codigo mas concentrado.

La respuesta no es siempre la misma. A veces separar es correcto. A veces juntar es correcto. La clave es tener criterios claros para decidir.

### Criterios para dejarlo junto

Hay cuatro situaciones donde juntar codigo es la decision correcta:

**1. Comparten la misma informacion.** Si dos piezas de codigo necesitan conocer la misma estructura de datos, la misma regla de negocio, o el mismo formato, deberias considerar juntarlas. Separarlas significa duplicar ese conocimiento, lo cual es una fuga de informacion.

En DevCourses, si la validacion de cupones y la aplicacion de cupones necesitan conocer las mismas reglas (porcentaje maximo, cupones acumulables o no, fecha de vigencia), ambas operaciones deberian estar en el mismo modulo.

**2. Tienen cercania semantica.** Si puedes describir dos piezas de codigo con la misma frase general, probablemente pertenecen al mismo modulo. "Operaciones sobre el texto" es una categoria semantica. "Cosas que pasan el martes" no lo es.

**3. Siempre se usan juntas.** Si cada vez que llamas a la funcion A tambien llamas a la funcion B, y nunca llamas a una sin la otra, probablemente deberian ser una sola funcion. Ousterhout pone un ejemplo claro: si siempre creas un hash y luego lo verificas, quizas la funcion deberia ser `crear_hash_verificado()`.

**4. Juntarlas elimina interfaces.** Este es un indicador particularmente fuerte. Si al fusionar dos funciones terminas con *menos* interfaces totales en el sistema (menos funciones publicas, menos parametros, menos conceptos que los consumidores deben aprender), la fusion es casi seguramente correcta.

### Criterios para separar

Hay dos situaciones principales donde separar es la decision correcta:

**1. Operan en diferentes niveles de abstraccion.** Si una pieza de codigo es general (aplica a muchos casos) y otra es especifica (aplica a un solo caso de uso), deberias separarlas. La pieza general deberia estar en un modulo que pueda reutilizarse; la pieza especifica deberia estar en un modulo que la compose.

En el ejemplo del editor de texto: las operaciones fundamentales de texto (`insertar`, `borrar`, `obtener_texto`) son generales. La seleccion visual (que depende de la interfaz grafica) es especifica. Deben estar en modulos separados, con el modulo especifico usando al general.

**2. Son independientes y no comparten informacion.** Si dos piezas de codigo no comparten datos, no comparten reglas de negocio, y no se llaman mutuamente, no tienen razon para estar juntas. Juntarlas solo crearia un modulo grande sin cohesion.

### El arbol de decision

Cuando no estes seguro, recorre estas preguntas en orden:

```
1. Las dos piezas de codigo comparten informacion
   (misma estructura de datos, misma regla de negocio)?
   |
   SI -> Probablemente juntas.
   |
   NO -> Siguiente pregunta.

2. Siempre se usan juntas (una siempre llama a la otra)?
   |
   SI -> Probablemente juntas.
   |
   NO -> Siguiente pregunta.

3. Operan en diferentes niveles de abstraccion
   (una es general, la otra es especifica)?
   |
   SI -> Probablemente separadas.
   |
   NO -> Siguiente pregunta.

4. Juntarlas reduce el numero total de interfaces?
   |
   SI -> Juntas.
   |
   NO -> Separadas.
```

La regla de oro que resume todo:

> "Escoge la estructura que genere menores dependencias, oculte mejor el conocimiento, y cree interfaces mas simples." [Ousterhout, 2018]

Si juntar reduce dependencias, oculta mejor y simplifica interfaces, junta. Si separar lo hace, separa. No hay dogma. Hay criterios.

**Takeaway:** La decision de juntar o separar codigo no tiene una respuesta universal. Junta cuando compartan informacion, cuando siempre se usen juntas, o cuando juntarlas elimine interfaces. Separa cuando operen en diferentes niveles de abstraccion o cuando sean genuinamente independientes. El criterio siempre es: menos dependencias, mejor ocultamiento, interfaces mas simples.

---

## El falso evangelio de lo pequeno

Antes de pasar al proyecto guia, necesitamos abordar un mito que causa mucho dano: la idea de que las funciones y las clases deben ser lo mas pequenas posible.

Robert C. Martin, en *Clean Code*, propone que las funciones deben tener idealmente entre 1 y 4 lineas, y que "la primera regla de las funciones es que deben ser pequenas. La segunda regla es que deben ser aun mas pequenas" [Martin, 2008]. Esta recomendacion, tomada como dogma, lleva a lo que Ousterhout llama "classitis": la proliferacion de modulos diminutos que individualmente son triviales pero colectivamente crean un sistema fragmentado e incomprensible.

Consideremos que pasa cuando aplicas la regla de "funciones pequenas" a la funcion `comprar()` de DevCourses:

```python
def comprar(usuario_id, producto_id, cupon_codigo=None):
    producto = _obtener_y_validar_producto(producto_id)
    _verificar_no_comprado(usuario_id, producto_id)
    precio = _calcular_precio(producto, usuario_id, cupon_codigo)
    pago = _procesar_pago(usuario_id, precio)
    _registrar_compra(usuario_id, producto, precio, pago)
    _otorgar_acceso(usuario_id, producto)
    _publicar_evento(usuario_id, producto, precio)
```

Esto parece limpio. Pero ahora tienes *siete* funciones privadas que necesitas saltar a leer para entender el flujo. Si cada funcion privada a su vez llama a otras funciones auxiliares, puedes terminar con una cadena de 20 funciones de 3 lineas cada una. Para entender el flujo de una compra, necesitas mantener en tu cabeza un arbol de llamadas de cuatro niveles de profundidad.

Ousterhout argumenta que la complejidad no desaparece cuando fragmentas una funcion. Se redistribuye:

> "Si cortas un metodo en pedazos, estos necesitaran ser leidos juntos de cualquier forma. Si el metodo original era un flujo logico y coherente, separarlo puede hacer que la complejidad sea mayor, no menor, porque ahora necesitas reconstruir mentalmente el flujo que antes estaba explicito." [Ousterhout, 2018]

La pregunta no es "cuantas lineas tiene esta funcion?" La pregunta es: "las partes resultantes de separar esta funcion serian *genuinamente independientes* y *reutilizables*, o son fragmentos que solo tienen sentido juntos?"

Si una funcion de 60 lineas cuenta una historia coherente de principio a fin, y cada "subfuncion" solo se usaria en ese contexto, mantenerla como una sola funcion es la decision correcta. Puedes usar comentarios para marcar las secciones:

```python
def comprar(usuario_id, producto_id, cupon_codigo=None):
    # --- Validacion ---
    producto = catalogo.obtener_producto(producto_id)
    if not producto:
        raise ProductoNoEncontrado(producto_id)
    if registro.ya_comprado(usuario_id, producto_id):
        raise ComprasDuplicada(usuario_id, producto_id)

    # --- Calculo de precio ---
    precio = precios.calcular_precio_final(
        producto=producto,
        usuario_id=usuario_id,
        cupon_codigo=cupon_codigo
    )

    # --- Procesamiento de pago ---
    resultado_pago = procesador_pagos.cobrar(
        usuario_id=usuario_id,
        monto=precio.monto,
        moneda=precio.moneda,
        descripcion=producto.nombre
    )

    # --- Registro y acceso ---
    compra = registro.crear_compra(usuario_id, producto, precio, resultado_pago)
    producto.otorgar_acceso(usuario_id)

    # --- Notificacion ---
    eventos.publicar("compra_completada", compra)

    return ResultadoCompra.exitosa(compra)
```

Esta funcion tiene unas 25 lineas. Es mas larga que la version ultra-fragmentada. Pero es mas facil de entender porque el flujo completo esta visible de un vistazo. Cada seccion llama a otros modulos profundos que ocultan su propia complejidad. Y no necesitas saltar a siete funciones auxiliares para reconstruir la narrativa.

**Takeaway:** El tamano de una funcion no es un indicador confiable de calidad. Una funcion larga y coherente puede ser mas clara que diez funciones cortas con conexiones implicitas. El criterio correcto no es "cuantas lineas tiene?" sino "las partes son genuinamente independientes o solo tienen sentido juntas?"

---

## Proyecto guia: generalizando el sistema de notificaciones de DevCourses

Volvamos a DevCourses para aplicar todo lo que hemos discutido. El sistema de notificaciones es un candidato perfecto para la generalizacion: empezo ultra-especifico, crecio por acumulacion de casos, y ahora es un desastre.

### Estado actual: el modulo ultra-especifico

El equipo de DevCourses fue agregando notificaciones de manera tactica. El resultado:

```python
# notificaciones.py -- estado actual

def enviar_email_bienvenida(usuario_id):
    usuario = db.obtener_usuario(usuario_id)
    asunto = f"Bienvenido a DevCourses, {usuario['nombre']}"
    cuerpo = render_template("emails/bienvenida.html", usuario=usuario)
    ses_client.send_email(
        Source="hola@devcourses.com",
        Destination={"ToAddresses": [usuario["email"]]},
        Message={"Subject": {"Data": asunto}, "Body": {"Html": {"Data": cuerpo}}}
    )

def enviar_email_compra(usuario_id, curso_id, monto):
    usuario = db.obtener_usuario(usuario_id)
    curso = db.obtener_curso(curso_id)
    asunto = f"Confirmacion de compra: {curso['titulo']}"
    cuerpo = render_template("emails/compra.html",
                              usuario=usuario, curso=curso, monto=monto)
    ses_client.send_email(
        Source="pagos@devcourses.com",
        Destination={"ToAddresses": [usuario["email"]]},
        Message={"Subject": {"Data": asunto}, "Body": {"Html": {"Data": cuerpo}}}
    )

def enviar_push_nuevo_curso(usuario_id, curso_id):
    usuario = db.obtener_usuario(usuario_id)
    curso = db.obtener_curso(curso_id)
    token = db.obtener_token_push(usuario_id)
    if token:
        firebase.send(token, {
            "title": "Nuevo curso disponible",
            "body": f"{curso['titulo']} ya esta disponible",
            "data": {"curso_id": curso_id}
        })

def enviar_email_certificado(usuario_id, curso_id, certificado_url):
    # ... Otro bloque de 15 lineas casi identico a los anteriores ...
    ...

def enviar_push_recordatorio(usuario_id, curso_id):
    # ... Otro bloque similar ...
    ...

# ... 8 funciones mas, cada una para un caso especifico ...
```

### Los problemas

1. **Explosion de funciones.** Hay 13 funciones, una por cada tipo de notificacion. Cada nueva funcionalidad del producto requiere agregar una o dos funciones mas.

2. **Duplicacion masiva.** Todas las funciones de email repiten el patron: obtener usuario, renderizar template, llamar a SES. Todas las funciones de push repiten: obtener usuario, obtener token, llamar a Firebase.

3. **Fugas de informacion.** Los nombres `ses_client` y `firebase` revelan los proveedores. Si migras a SendGrid o a OneSignal, tocas las 13 funciones.

4. **No hay un lugar para politicas transversales.** Si quieres agregar "no enviar notificaciones a usuarios que las desactivaron" o "limitar a 5 notificaciones push por dia", necesitas agregar la logica a cada funcion individual.

### El rediseno: interfaz general, implementacion extensible

Aplicamos los principios de este capitulo: interfaz general, implementacion enfocada en los casos actuales.

**La interfaz publica (lo que ven los otros modulos):**

```python
# notificaciones.py -- interfaz publica

def notificar(usuario_id: str, evento: str,
              datos: dict = None) -> ResultadoNotificacion:
    """
    Envia una notificacion al usuario basada en el tipo de evento.

    El modulo decide internamente:
    - Por que canales enviar (email, push, in-app)
    - Que template usar
    - Que datos incluir
    - Si el usuario tiene ese canal habilitado
    - Si se exceden limites de frecuencia

    Args:
        usuario_id: Identificador del usuario destinatario.
        evento: Tipo de evento (ej: "bienvenida", "compra_completada",
                "nuevo_curso", "certificado_emitido").
        datos: Datos adicionales del evento (ej: {"curso_id": "xyz"}).

    Returns:
        ResultadoNotificacion con los canales por los que se envio.
    """
    ...
```

Una funcion. Tres parametros (uno opcional). En vez de 13 funciones con interfaces diferentes, una sola funcion que acepta cualquier tipo de evento.

Los otros modulos la usan asi:

```python
# En el modulo de compras
eventos.publicar("compra_completada", {
    "usuario_id": usuario_id,
    "curso_id": curso_id,
    "monto": precio.monto
})

# El listener de notificaciones escucha el evento y llama:
notificaciones.notificar(
    usuario_id=evento.datos["usuario_id"],
    evento="compra_completada",
    datos=evento.datos
)
```

**La implementacion interna:**

```python
# notificaciones.py -- implementacion interna

# Registro de configuraciones por evento
_CONFIGURACIONES = {
    "bienvenida": ConfigNotificacion(
        canales=[Canal.EMAIL],
        template_email="emails/bienvenida.html",
        asunto_template="Bienvenido a DevCourses, {nombre}",
        remitente="hola@devcourses.com",
    ),
    "compra_completada": ConfigNotificacion(
        canales=[Canal.EMAIL, Canal.PUSH],
        template_email="emails/compra.html",
        asunto_template="Confirmacion de compra: {curso_titulo}",
        remitente="pagos@devcourses.com",
        template_push="Ya tienes acceso a {curso_titulo}",
    ),
    "nuevo_curso": ConfigNotificacion(
        canales=[Canal.PUSH],
        template_push="{curso_titulo} ya esta disponible",
    ),
    "certificado_emitido": ConfigNotificacion(
        canales=[Canal.EMAIL],
        template_email="emails/certificado.html",
        asunto_template="Tu certificado de {curso_titulo}",
        remitente="certificados@devcourses.com",
    ),
}


def notificar(usuario_id: str, evento: str,
              datos: dict = None) -> ResultadoNotificacion:
    datos = datos or {}
    config = _CONFIGURACIONES.get(evento)
    if not config:
        raise EventoNoConfigurado(evento)

    usuario = _obtener_usuario_con_preferencias(usuario_id)
    datos_enriquecidos = _enriquecer_datos(datos, usuario)
    resultados = []

    for canal in config.canales:
        if not _canal_habilitado(usuario, canal):
            continue
        if _excede_limite_frecuencia(usuario_id, canal):
            continue

        resultado = _enviar_por_canal(canal, usuario, config, datos_enriquecidos)
        resultados.append(resultado)

    return ResultadoNotificacion(canales_enviados=resultados)


def _enviar_por_canal(canal, usuario, config, datos):
    """Despacha al canal correcto. Oculta los proveedores."""
    if canal == Canal.EMAIL:
        return _enviar_email(usuario, config, datos)
    elif canal == Canal.PUSH:
        return _enviar_push(usuario, config, datos)
    elif canal == Canal.IN_APP:
        return _crear_notificacion_in_app(usuario, config, datos)


def _enviar_email(usuario, config, datos):
    """Envia un email. Oculta que usamos SES (o cualquier proveedor)."""
    asunto = config.asunto_template.format(**datos)
    cuerpo = renderizar_template(config.template_email, **datos)
    return _proveedor_email.enviar(
        destinatario=usuario.email,
        remitente=config.remitente,
        asunto=asunto,
        cuerpo_html=cuerpo
    )


def _enviar_push(usuario, config, datos):
    """Envia push notification. Oculta que usamos Firebase."""
    token = _obtener_token_push(usuario.id)
    if not token:
        return ResultadoCanal(canal=Canal.PUSH, enviado=False, razon="sin_token")
    mensaje = config.template_push.format(**datos)
    return _proveedor_push.enviar(token=token, titulo=mensaje, datos=datos)
```

### Lo que ganamos

1. **Agregar un nuevo tipo de notificacion** es agregar una entrada a `_CONFIGURACIONES`. Cero codigo nuevo. Cero funciones nuevas.

```python
# Agregar notificacion de "quiz_completado"
_CONFIGURACIONES["quiz_completado"] = ConfigNotificacion(
    canales=[Canal.PUSH, Canal.IN_APP],
    template_push="Completaste el quiz de {leccion_titulo}!",
)
```

2. **Agregar un nuevo canal** (por ejemplo, SMS) es agregar un caso a `_enviar_por_canal` y un nuevo `_proveedor_sms`. Los otros modulos no se enteran. La interfaz `notificar()` no cambia.

3. **Cambiar de proveedor** (de SES a SendGrid, de Firebase a OneSignal) es cambiar `_proveedor_email` o `_proveedor_push`. Una linea de configuracion. Cero cambios en los 13 tipos de notificacion.

4. **Politicas transversales** (limites de frecuencia, preferencias de usuario, horarios de silencio) se implementan *una vez* en `notificar()` y aplican a *todos* los tipos de notificacion automaticamente.

5. **La interfaz publica es radicalmente simple.** Tres parametros. Un concepto. Los otros modulos del sistema no necesitan saber cuantos canales existen, que proveedores se usan, ni como se formatean los mensajes.

### El perfil de profundidad: antes y despues

```
ANTES:                          DESPUES:

+------------------------+      +----------+
| 13 funciones publicas  |      | notificar|
| cada una con 2-4 params|      | 3 params |
+------------------------+      +----------+
|                        |      |          |
| implementacion         |      | config   |
| duplicada              |      | canales  |
|                        |      | proveed. |
+------------------------+      | limites  |
                                | prefs.   |
                                | templates|
                                |          |
                                +----------+

Superficial                     Profundo
```

De 13 interfaces publicas a 1. De parametros especificos de cada caso a 3 parametros genericos. De duplicacion masiva a implementacion compartida. De fugas de proveedor a ocultamiento completo.

**Takeaway:** La generalizacion del sistema de notificaciones no fue un ejercicio teorico. Redujo la superficie de la interfaz de 13 funciones a 1, elimino la duplicacion, oculto los proveedores, y creo un punto unico donde agregar politicas transversales. Todo con menos codigo total que la version original.

---

## Aplica esto el lunes

### 1. Busca el patron de tres

Revisa tu codigo buscando funciones que se parecen: `procesar_X`, `procesar_Y`, `procesar_Z`. Si encuentras tres o mas funciones con la misma estructura pero diferentes datos, tienes un candidato para generalizacion. Diseña en papel como se veria una version unificada. Cuantos parametros tendria? La interfaz general es mas simple o mas compleja que las tres especificas?

### 2. Separa la interfaz de la implementacion

Escoge un modulo de tu proyecto. Escribe en un papel su interfaz *ideal* -- la mas general y simple que puedas imaginar, asumiendo que la implementacion es magica. Ahora compara con la interfaz real. La interfaz real es mas compleja porque la implementacion actual se lo exige? Si es asi, tienes una oportunidad de rediseno: la interfaz deberia ser general aunque la implementacion sea especifica.

### 3. Aplica el arbol de decision a un caso real

Identifica dos funciones en tu codigo que estes dudando si deberian estar juntas o separadas. Recorre el arbol de decision de este capitulo:
- Comparten informacion? Si: juntas.
- Siempre se usan juntas? Si: juntas.
- Operan en diferentes niveles de abstraccion? Si: separadas.
- Juntarlas reduce interfaces? Si: juntas.

Haz el cambio si el resultado es claro. Si no es claro, dejalo como esta. La claridad llegara con el tiempo y con mas contexto.

---

## Resumen del capitulo

- La generalidad de un modulo es un espectro: desde el hardcoding ultra-especifico hasta el framework universal. El punto optimo para la mayoria de los modulos es "algo general": una interfaz que sirva para varios casos similares, con una implementacion enfocada en las necesidades actuales.
- Los modulos algo generales son mejores que los ultra-especificos por cuatro razones: interfaces mas simples, mejor ocultamiento de informacion, mayor reutilizacion, y menor acoplamiento. Generalizar la interfaz frecuentemente la *simplifica*.
- La Regla de Tres es una heuristica para decidir cuando generalizar: primera vez hazlo especifico, segunda vez nota la duplicacion, tercera vez refactoriza. Pero si la generalidad simplifica la interfaz, generaliza desde la primera vez.
- Diseña la interfaz para la clase de problemas; implementa para el caso de hoy. La interfaz general y la implementacion especifica no son contradictorias; son complementarias.
- Para decidir si juntar o separar codigo, usa estos criterios: junta cuando compartan informacion, cuando siempre se usen juntas, o cuando juntarlas elimine interfaces. Separa cuando operen en diferentes niveles de abstraccion o cuando sean genuinamente independientes.
- El tamano de una funcion no es un indicador confiable de calidad. El criterio correcto es: las partes resultantes de separar son genuinamente independientes, o solo tienen sentido juntas?
- El sistema de notificaciones de DevCourses se transformo de 13 funciones especificas a 1 funcion general, reduciendo la superficie de la interfaz, eliminando duplicacion, y creando un punto unico para politicas transversales.

En el siguiente capitulo, vamos a profundizar en dos conceptos que estan intimamente ligados con todo lo que hemos discutido: cohesion y acoplamiento. Veremos como medir la calidad de nuestros modulos con estos dos criterios complementarios, y como usarlos para tomar decisiones de diseno en los casos ambiguos donde los criterios de este capitulo no dan una respuesta clara.

---

### Referencias

- [Parnas, 1972] Parnas, D. L. "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 15(12), 1053-1058, 1972.
- [Ousterhout, 2018] Ousterhout, J. *A Philosophy of Software Design.* Yaknyam Press, 2018.
- [Martin, 2008] Martin, R. C. *Clean Code: A Handbook of Agile Software Craftsmanship.* Prentice Hall, 2008.
- [Atwood, 2007] Atwood, J. "Rule of Three." *Coding Horror*, 2007. codinghorror.com.
- [Bernhardsson, 2017] Bernhardsson, E. "The software engineering rule of 3." erikbern.com, 2017.
