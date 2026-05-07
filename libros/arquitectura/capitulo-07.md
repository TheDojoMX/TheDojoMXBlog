# Capitulo 7: Mejor juntos o separados? Cuando dividir el codigo

> "Si cada vez que haces split terminas con mas interfaces que antes, algo anda mal."

---

## La tentacion del bisturi

Todo desarrollador que ha leido un libro de "codigo limpio" conoce la sensacion: ves una funcion de 80 lineas y sientes la urgencia de cortarla. Divide y venceras. Funciones pequenas. Clases con una sola responsabilidad. Modulos minimos. El instinto dice: si algo es grande, partelo.

Pero hay un problema que nadie menciona en los tutoriales. Cada vez que partes un modulo en dos, creas una nueva interfaz entre las partes. Y cada interfaz nueva es un costo: alguien tiene que aprenderla, mantenerla, y entenderla cada vez que necesite seguir el flujo del codigo. Si despues de separar tu codigo tienes mas interfaces que antes, mas conexiones que antes, y mas saltos mentales que antes, no simplificaste nada. Redistribuiste la complejidad y le agregaste un impuesto.

En los capitulos anteriores descubrimos que los modulos profundos ocultan gran funcionalidad detras de interfaces simples, y que el ocultamiento de informacion es el principio mas poderoso del diseno de software. Ahora toca enfrentar la pregunta que completa el panorama: *cuando* es correcto dividir un modulo en varios, y *cuando* es mejor dejarlo junto?

La respuesta no es un numero de lineas. No es una metrica de complejidad ciclomatica. No es una regla de estilo. Es un analisis de informacion, dependencias e interfaces. Y a veces, el resultado de ese analisis es: dejalo junto.

**Takeaway:** La division del codigo no es un acto de higiene; es una decision de diseno. Y como toda decision de diseno, puede mejorar o empeorar el sistema dependiendo de los criterios que uses para tomarla.

---

## Lo que nadie te dice sobre separar codigo

Existe una narrativa dominante en la industria que suena mas o menos asi: "Si tu funcion es larga, separala. Si tu clase hace mas de una cosa, dividela. Si tu modulo es grande, descomponlo." La narrativa es tan ubicua que la mayoria de los desarrolladores la internalizan como verdad autoevidente.

Pero los disenadores de software mas experimentados cuentan una historia diferente. John Ousterhout, en *A Philosophy of Software Design*, dedica un capitulo completo a esta pregunta -- y su conclusion sorprende a muchos: **separar codigo frecuentemente lo empeora** [Ousterhout, 2018].

La razon es matematica. Cuando tienes un modulo M que contiene las funciones A y B, el codigo externo solo necesita conocer la interfaz de M. Cuando separas A y B en dos modulos independientes, el codigo externo ahora necesita conocer *dos* interfaces. Pero eso no es todo: si A y B comparten informacion o dependen mutuamente (como sucede en la mayoria de los casos reales), necesitas ademas una interfaz *entre* A y B. Pasaste de una interfaz a tres.

Esto no significa que separar siempre sea incorrecto. Significa que separar tiene un costo que debes pagar con beneficios concretos. Si no puedes articular que beneficio obtuviste, probablemente pagaste un costo neto.

Parnas lo entendio en 1972: el criterio para dividir un sistema no es el tamano, ni el flujo, ni la convencion. Es el *conocimiento*. Cada modulo debe encapsular una decision de diseno que sea probable que cambie [Parnas, 1972]. Si dos piezas de codigo encapsulan la misma decision de diseno, deberian estar juntas. Si encapsulan decisiones diferentes, deberian estar separadas.

**Takeaway:** Separar codigo crea interfaces nuevas. Cada interfaz nueva es un costo. La separacion solo vale la pena si el beneficio (mejor ocultamiento, menor acoplamiento, interfaces mas simples) supera ese costo.

---

## Cuatro criterios para dejarlo junto

Si la pregunta es "deberia separar este codigo?", la primera opcion que debes considerar es: no. La carga de la prueba esta en la separacion, no en la union. Veamos cuatro criterios concretos que sugieren que el codigo deberia permanecer junto.

### Criterio 1: Acceso a informacion compartida

Si dos piezas de codigo necesitan acceder al mismo conjunto de informacion para funcionar, separarlas fuerza una de dos cosas: o duplicas la informacion, o creas una interfaz para compartirla. Ambas opciones agregan complejidad.

Considera el parseo y la validacion de un mensaje HTTP. Para parsear un request, necesitas entender la estructura del protocolo: donde empieza el header, donde empieza el body, como se codifican los caracteres especiales. Para validar ese mismo request, necesitas *exactamente la misma* informacion: la estructura del protocolo. Si separas "parsear" y "validar" en dos modulos, ambos necesitan conocer la estructura de HTTP. Eso es una fuga de informacion -- el conocimiento del formato se duplica en dos lugares.

En DevCourses, el modulo de catalogo tiene una funcion que busca cursos y otra que los ordena por relevancia. Ambas necesitan conocer la estructura interna de un curso: que campos tiene, como se representan las categorias, como se calcula la puntuacion. Separarlas en dos modulos obligaria a exponer la estructura interna del curso a ambos. Es mejor tenerlas juntas, donde la estructura del curso es un detalle privado que nadie mas necesita conocer.

**Regla practica:** Si para separar dos piezas de codigo necesitarias compartir una estructura de datos interna entre ellas, probablemente deberian estar juntas.

### Criterio 2: Cercania semantica

Si dos piezas de codigo se pueden describir bajo la misma idea, probablemente pertenecen al mismo modulo.

Ousterhout usa un ejemplo sencillo: las operaciones sobre cadenas de texto. `uppercase()`, `trim()`, `split()`, `replace()` -- todas estas funciones operan sobre el mismo concepto (una cadena de texto) y comparten la misma categoria mental. Ponerlas en modulos separados (un modulo para transformaciones de caso, otro para eliminacion de espacios, otro para busqueda) seria absurdo. Estan juntas porque *pertenecen* juntas.

En terminos mas formales, la cercania semantica indica alta cohesion. Larry Constantine y Edward Yourdon definieron la cohesion como "la medida en que los elementos de un modulo se relacionan entre si" [Constantine y Yourdon, 1979]. Cuando la relacion semantica es obvia -- cuando un desarrollador nuevo miraria las dos piezas de codigo y diria "estas hacen lo mismo" -- no necesitas mas analisis. Dejalas juntas.

### Criterio 3: Dependencia de uso

Si dos piezas de codigo siempre se usan juntas -- si cada vez que llamas a A, inmediatamente despues llamas a B -- eso es una senal fuerte de que deberian ser un solo modulo.

Piensa en `obtenerHash()` y `verificarHash()`. Si el 95% de las veces que creas un hash es para verificarlo inmediatamente, y el 95% de las veces que verificas un hash es porque lo acabas de crear, estas dos operaciones son un flujo indivisible que deberia tener una sola interfaz: `crearHashVerificado()`.

La dependencia de uso tambien se manifiesta cuando el *orden* de las llamadas importa. Si siempre debes llamar `inicializar()` antes de `ejecutar()`, y `limpiar()` despues de `ejecutar()`, tienes una dependencia temporal que esta fugando informacion. El conocimiento de "primero esto, luego esto, luego esto" esta distribuido en todo el codigo que usa tu modulo. Mejor encapsular el flujo completo en una sola funcion que maneje el ciclo internamente.

### Criterio 4: Eliminacion de duplicacion

Si juntando dos piezas de codigo puedes eliminar logica duplicada, eso es una razon fuerte para juntarlas.

Pero aqui hay un matiz importante que muchos desarrolladores ignoran. No toda duplicacion es mala duplicacion. A veces, dos piezas de codigo se *parecen* pero representan decisiones de diseno *diferentes*. Si los cambios futuros en una no deberian afectar a la otra, la similitud superficial es una coincidencia, no una duplicacion real.

En DevCourses, el modulo de reportes calcula el ingreso promedio por usuario, y el modulo de facturacion calcula el monto promedio por factura. Ambos calculan un promedio dividiendo una suma entre una cantidad. Parecen duplicados. Pero el "promedio" en reportes podria evolucionar para excluir usuarios de prueba, aplicar pesos por tipo de suscripcion, o usar mediana en vez de media. El "promedio" en facturacion es un calculo fiscal regulado que no deberia cambiar caprichosamente. Unificarlos en una sola funcion `calcular_promedio()` acoplaría dos dominios con razones de cambio completamente diferentes.

La pregunta no es "se parecen?" sino "cambiarian por las mismas razones?"

**Takeaway:** Deja el codigo junto cuando las piezas compartan informacion, cuando pertenezcan semanticamente a la misma idea, cuando siempre se usen juntas, o cuando juntarlas elimine duplicacion *genuina*. El criterio unificador es: juntarlas reduce dependencias y simplifica interfaces.

---

## La senal mas clara: si terminas con menos interfaces

Hay una heuristica que resume los cuatro criterios anteriores en una sola observacion: **si juntar dos piezas de codigo reduce el numero total de interfaces en tu sistema, probablemente deberian estar juntas**.

Interfaces, en este contexto, significa cualquier punto de contacto entre modulos: firmas de funciones publicas, contratos de API, tipos exportados, parametros de configuracion. Cada interfaz es un lugar donde dos modulos necesitan ponerse de acuerdo. Menos interfaces significa menos puntos de acuerdo, menos oportunidades de desacuerdo, y menos carga cognitiva para quien navega el sistema.

Volvamos al ejemplo de `obtenerHash()` y `verificarHash()`. Si las unes en `crearHashVerificado()`, pasas de dos funciones publicas a una. Una interfaz en vez de dos. Y el conocimiento de "como se verifica un hash" queda encapsulado dentro del modulo, en vez de distribuido en cada consumidor que llama a ambas funciones en secuencia.

Lo contrario tambien es cierto: **si separar un modulo incrementa el numero total de interfaces sin reducir la complejidad de cada interfaz individual, la separacion fue un error**.

Esta es la prueba mas rapida que puedes hacer despues de cualquier refactorizacion: cuenta las interfaces antes y despues. Si el numero subio, preguntate si la complejidad total realmente bajo. Si no puedes demostrarlo, considera revertir.

**Takeaway:** La cantidad de interfaces en tu sistema es un proxy util para su complejidad. Si un cambio estructural reduce las interfaces totales, probablemente fue bueno. Si las incrementa sin beneficio claro, probablemente no lo fue.

---

## Cuando separar: el criterio del nivel de abstraccion

Si los criterios anteriores indican cuando *no* separar, este criterio indica cuando *si* hacerlo: **no mezcles codigo general con codigo especifico en el mismo modulo**.

Codigo general es aquel que resuelve un problema de forma independiente del contexto de uso. Codigo especifico es aquel que esta atado a un caso de uso particular, a una interfaz grafica concreta, o a una regla de negocio especifica.

Cuando ambos conviven en el mismo modulo, los cambios en lo especifico contaminan lo general. Y lo general pierde su capacidad de reutilizacion.

### El ejemplo del editor de texto

John Ousterhout ilustra esto con el editor de texto que ya vimos en capitulos anteriores [Ousterhout, 2018]. Las operaciones fundamentales sobre texto -- insertar, borrar, obtener un rango -- son generales. Funcionan independientemente de que el editor tenga interfaz grafica, linea de comandos, o sea una API HTTP. La seleccion visual, en cambio, es especifica: solo tiene sentido en un editor con interfaz grafica.

Si pones la logica de seleccion visual dentro del modulo core de edicion de texto, contaminas un modulo general con logica especifica. El core ahora tiene dos razones para cambiar: si cambia la forma de almacenar texto *y* si cambia la interfaz grafica. Eso viola el principio de ocultamiento de informacion: el modulo ahora necesita conocer detalles de la interfaz visual que no le corresponden.

La separacion correcta es:

- **Modulo core (general):** `insertar(posicion, texto)`, `borrar(posicion, cantidad)`, `obtener_texto(posicion, cantidad)`.
- **Modulo de interfaz (especifico):** Seleccion visual, cursor visible, resaltado de sintaxis. Usa las operaciones del core para implementar sus funcionalidades.

### La regla de capas

Este criterio es el fundamento de las arquitecturas por capas. El patron MVC (Modelo-Vista-Controlador), las arquitecturas hexagonales, y los sistemas operativos con su distincion kernel/userspace siguen todos la misma logica: separar niveles de abstraccion diferentes en modulos diferentes.

En DevCourses:

- La logica de negocio (calcular precios, validar inscripciones, determinar progreso) es general. No depende de si el usuario accede por web, por app movil, o por API.
- La logica de presentacion (renderizar HTML, formatear JSON, manejar sesiones web) es especifica al canal de acceso.
- La logica de persistencia (consultas SQL, conexiones a bases de datos) es especifica a la tecnologia de almacenamiento.

Mezclar estos niveles en el mismo modulo crea modulos que son simultaneamente generales y especificos, lo cual es una contradiccion que siempre causa problemas. Cuando cambias el almacenamiento (de PostgreSQL a DynamoDB), no quieres tener que modificar la logica de negocio. Cuando cambias la interfaz (de web a API movil), no quieres tener que reescribir las reglas de precios.

### Separar para proposito general vs proposito especifico

Hay un caso relacionado pero distinto: cuando un modulo contiene logica que podria servir a otros modulos ademas del actual. Si identificas una pieza de codigo que resuelve un problema *general* -- calcular distancias, parsear formatos, validar estructuras de datos -- y esa pieza esta encerrada dentro de un modulo que resuelve un problema *especifico*, liberarla como un modulo independiente la hace disponible para otros consumidores.

En DevCourses, el modulo de catalogo contiene una funcion que calcula la similitud entre dos textos para sugerir cursos relacionados. Esa funcion de similitud textual no tiene nada que ver con cursos. Podria usarse para busqueda, para detectar duplicados en comentarios, o para sugerir preguntas similares en el foro. Extraerla a un modulo de utilidades de texto la libera de su contexto especifico sin perder nada -- y el catalogo se simplifica al no cargar con logica que no le pertenece conceptualmente.

La distincion clave es que esta separacion *reduce* la complejidad de ambos modulos: el modulo de catalogo pierde logica que no era de su dominio, y el modulo de utilidades gana reutilizacion sin agregar interfaces adicionales al catalogo (simplemente importa la utilidad en vez de implementarla internamente).

**Takeaway:** La razon mas clara para separar codigo es la diferencia de nivel de abstraccion. Lo general y lo especifico no deben convivir en el mismo modulo, porque tienen razones de cambio diferentes y la contaminacion entre ellos destruye la capacidad de reutilizacion y mantenimiento de lo general.

---

## La descomposicion temporal: el error mas comun

Si tuviera que senalar un solo error que los desarrolladores cometen una y otra vez al decidir como dividir su codigo, seria este: la descomposicion temporal.

La descomposicion temporal consiste en separar el codigo segun *cuando* se ejecuta, en vez de segun *que conocimiento* encapsula. Es el error mas natural del mundo, porque la primera vez que analizas un sistema, lo primero que ves es su flujo: primero pasa esto, luego pasa aquello, despues se hace lo otro. Y parece logico que cada paso sea un modulo.

Ya exploramos este concepto en el capitulo anterior, pero aqui lo abordaremos desde el angulo de la decision concreta: como reconocer que estas cayendo en descomposicion temporal y como corregirla.

### El patron clasico

Cuando un equipo diseña un sistema de procesamiento de datos, frecuentemente crea tres modulos:

1. **Lector:** Lee los datos de la fuente.
2. **Procesador:** Transforma los datos.
3. **Escritor:** Guarda los datos en el destino.

Esta division parece impecable. Tres responsabilidades claras. Separacion de preocupaciones. Cada modulo hace "una sola cosa".

Pero considera que sucede si el formato de los datos cambia. El lector necesita entender el nuevo formato para leerlo. El procesador necesita entender el nuevo formato para transformarlo. El escritor necesita entender el nuevo formato para guardarlo. Un cambio en el formato afecta a los tres modulos. El formato es una decision de diseno que *deberia* estar encapsulada en un solo lugar, pero la descomposicion temporal la esparce por todo el sistema.

La alternativa es organizar por conocimiento:

- Un modulo encapsula el conocimiento del formato de datos (lectura y escritura del formato).
- Otro modulo encapsula las reglas de transformacion (la logica de negocio).
- La interfaz entre ambos usa una representacion interna que no depende del formato externo.

Ahora, cambiar el formato solo afecta a un modulo. Las transformaciones pueden evolucionar independientemente. Y la interfaz entre ambos es estable.

### DevCourses: la inscripcion fragmentada

En DevCourses, el equipo original separo el proceso de inscripcion en tres clases:

```python
# Descomposicion temporal: tres clases para un solo flujo

class ValidadorInscripcion:
    def validar(self, usuario_id, curso_id):
        usuario = db.obtener_usuario(usuario_id)
        curso = db.obtener_curso(curso_id)
        if not curso.tiene_cupo():
            raise SinCupo()
        if usuario.ya_inscrito(curso_id):
            raise YaInscrito()
        if curso.requiere_prerequisito():
            if not usuario.completo_curso(curso.prerequisito_id):
                raise FaltaPrerequisito()
        return True

class ProcesadorInscripcion:
    def procesar(self, usuario_id, curso_id):
        db.crear_inscripcion(usuario_id, curso_id)
        db.reducir_cupo(curso_id)
        db.actualizar_historial(usuario_id, curso_id)

class NotificadorInscripcion:
    def notificar(self, usuario_id, curso_id):
        usuario = db.obtener_usuario(usuario_id)
        curso = db.obtener_curso(curso_id)
        email.enviar_confirmacion(usuario.email, curso.nombre)
        analytics.registrar_inscripcion(usuario_id, curso_id)
```

Tres clases, tres "responsabilidades", tres interfaces publicas. Parece un diseno limpio. Pero mira lo que sucede:

1. Las tres clases consultan `db.obtener_usuario()` y `db.obtener_curso()`. La informacion se obtiene tres veces.
2. Las tres clases necesitan saber que significa una inscripcion en DevCourses: que implica cupos, prerequisitos, historial, confirmacion. El *conocimiento* de "que es una inscripcion" esta esparcido en tres lugares.
3. Si agregas una nueva regla de inscripcion (por ejemplo, "los cursos premium requieren suscripcion activa"), necesitas decidir si va en el validador, en el procesador, o en ambos. Y cualquier decision que tomes acopla las tres clases.

El flujo externo que las usa es siempre el mismo:

```python
validador = ValidadorInscripcion()
procesador = ProcesadorInscripcion()
notificador = NotificadorInscripcion()

validador.validar(usuario_id, curso_id)
procesador.procesar(usuario_id, curso_id)
notificador.notificar(usuario_id, curso_id)
```

Siempre las tres. Siempre en ese orden. Siempre con los mismos parametros. Este es el patron clasico de la descomposicion temporal: separar por "primero valido, luego proceso, luego notifico" en vez de por "que conocimiento encapsula cada parte".

La alternativa es un solo modulo profundo:

```python
class ServicioInscripcion:
    """
    Maneja el ciclo completo de inscripcion de un usuario a un curso.
    Encapsula las reglas de validacion, el registro y la notificacion.
    """

    def inscribir(self, usuario_id: str, curso_id: str) -> ResultadoInscripcion:
        usuario = self._obtener_usuario(usuario_id)
        curso = self._obtener_curso(curso_id)

        self._validar_reglas(usuario, curso)
        inscripcion = self._registrar(usuario, curso)
        self._notificar(usuario, curso, inscripcion)

        return ResultadoInscripcion.exitosa(inscripcion)
```

Una clase. Una interfaz publica: `inscribir(usuario_id, curso_id)`. El conocimiento completo de "que significa inscribir a un usuario en un curso" esta en un solo lugar. Los consumidores no necesitan saber que hay validacion, procesamiento y notificacion. Solo necesitan saber que `inscribir()` inscribe.

Los metodos privados `_validar_reglas`, `_registrar` y `_notificar` siguen existiendo, pero son detalles internos del modulo. No son interfaces publicas. No son responsabilidad de nadie mas. Y si manana necesitas agregar una regla, un paso, o cambiar el flujo completo, todo esta en un solo archivo, en un solo contexto.

**Takeaway:** La descomposicion temporal es la trampa de separar el codigo segun "primero esto, luego aquello" en vez de segun "que conocimiento oculta cada parte". Es el error mas comun porque el flujo temporal es lo mas visible. Pero si las partes siempre se usan juntas, siempre en el mismo orden, y comparten la misma informacion, deberian ser un solo modulo.

---

## El arbol de decision

Cuando no estes seguro de si dos piezas de codigo deberian estar juntas o separadas, recorre estas preguntas en orden:

```
  Tengo dos piezas de codigo y no se
  si juntarlas o separarlas.
            |
            v
  1. Comparten informacion?
     (misma estructura de datos, misma regla de negocio,
      mismo conocimiento sobre una decision de diseno)
     |                    |
     SI                   NO
     |                    |
     v                    v
  JUNTAS.              2. Siempre se usan juntas?
  Separarlas              (una siempre llama a la otra,
  duplicaria el           o siempre se usan en secuencia)
  conocimiento.           |                    |
                          SI                   NO
                          |                    |
                          v                    v
                       JUNTAS.              3. Operan en diferentes
                       Separarlas              niveles de abstraccion?
                       crearia una             (una es general, la otra
                       dependencia             es especifica)
                       oculta.                 |                    |
                                               SI                   NO
                                               |                    |
                                               v                    v
                                            SEPARADAS.          4. Juntarlas reduce
                                            Lo general no          el numero total
                                            debe depender          de interfaces?
                                            de lo especifico.      |              |
                                                                   SI             NO
                                                                   |              |
                                                                   v              v
                                                                JUNTAS.       SEPARADAS.
                                                                Menos         Son genuinamente
                                                                interfaces    independientes.
                                                                = menos
                                                                complejidad.
```

Este arbol no es un algoritmo infalible. Es una heuristica. Hay casos ambiguos en los que la respuesta depende de factores de contexto que ningun diagrama puede capturar: el tamano del equipo, la velocidad de cambio del dominio, las limitaciones del lenguaje de programacion. Pero en la gran mayoria de los casos del dia a dia, estas cuatro preguntas te llevan a la decision correcta.

**Takeaway:** Cuando dudes entre juntar o separar, recorre las preguntas en orden: comparten informacion? Se usan juntas? Operan en niveles de abstraccion diferentes? Juntarlas reduce interfaces? La respuesta emerge de los criterios, no de un numero de lineas.

---

## La regla de oro

Todos los criterios que hemos visto convergen en una sola guia. Ousterhout la expresa con la claridad que lo caracteriza:

> "Escoge la estructura que genere menores dependencias, oculte mejor el conocimiento, y cree interfaces mas simples." [Ousterhout, 2018]

Tres preguntas. Tres dimensiones. Una decision.

- **Menores dependencias:** Despues del cambio, hay *menos* conexiones entre modulos, o *mas*? Cada conexion entre modulos es un punto de fragilidad: si un modulo cambia, los modulos conectados podrian necesitar cambiar tambien. Menos conexiones significa un sistema mas resistente al cambio.
- **Mejor ocultamiento:** Despues del cambio, hay *menos* conocimiento esparcido por el sistema, o *mas*? Cada pieza de conocimiento que se repite en multiples modulos es una oportunidad para inconsistencias. Mejor ocultamiento significa que cada decision de diseno vive en un solo lugar.
- **Interfaces mas simples:** Despues del cambio, las interfaces del sistema son *mas faciles* de entender, o *mas dificiles*? Interfaces mas simples significan menor carga cognitiva para quien navega el codigo. Menos parametros, menos funciones publicas, menos conceptos que mantener en la cabeza.

Si las tres respuestas apuntan en la misma direccion, la decision es obvia. Si apuntan en direcciones diferentes, necesitas evaluar cual dimension es mas importante en tu contexto. En la mayoria de los proyectos empresariales, el ocultamiento de informacion gana porque el costo de los cambios propagados domina el costo total de mantenimiento. En sistemas de alto rendimiento, las dependencias dominan porque cada indirección tiene un costo de ejecucion. En equipos grandes con alta rotacion, la simplicidad de interfaces domina porque la carga cognitiva para nuevos integrantes es el cuello de botella.

En la practica, cuando juntas dos piezas de codigo y las tres preguntas mejoran -- menos dependencias, mejor ocultamiento, interfaces mas simples -- puedes estar seguro de que tomaste la decision correcta. Y la senal mas rapida de que las tres mejoraron es la que ya mencionamos: **terminaste con menos interfaces que al principio**.

### La prueba de la explicacion

Hay una prueba complementaria que funciona sorprendentemente bien: la prueba de la explicacion. Despues de hacer un cambio estructural (juntar o separar), intenta explicar la nueva estructura a un companero en una oracion. Si la explicacion es mas simple que antes ("ahora todo lo que tiene que ver con inscripciones esta junto"), el cambio fue bueno. Si la explicacion requiere mas palabras, mas excepciones, y mas "bueno, excepto cuando..." que antes, el cambio introdujo complejidad.

Esta prueba funciona porque refleja la carga cognitiva real. Si no puedes explicar la estructura de forma sencilla, quien la encuentre por primera vez tampoco podra entenderla de forma sencilla.

---

## Proyecto guia: reestructurando el modulo de cursos de DevCourses

DevCourses tiene un problema. El modulo de catalogo, despues de varios meses de desarrollo tactico, se convirtio en una coleccion dispersa de funciones distribuidas en multiples archivos sin un criterio claro de organizacion.

### Estado actual: fragmentacion por conveniencia

```
catalogo/
    modelos.py           # Curso, Leccion, Categoria
    repositorio.py       # Consultas a la base de datos
    buscador.py          # Logica de busqueda por texto
    filtros.py           # Filtrado por categoria, precio, nivel
    ordenamiento.py      # Ordenar por relevancia, fecha, popularidad
    recomendador.py      # Sugerencias de cursos relacionados
    serializador.py      # Conversion a JSON para la API
    validador.py         # Validacion de datos al crear/editar cursos
    caché.py             # Cache de resultados frecuentes
```

Nueve archivos. Nueve modulos con interfaces entre ellos. Parece organizado. Pero veamos que pasa cuando un desarrollador necesita agregar un campo nuevo al modelo de curso -- digamos, `idioma`.

1. Modifica `modelos.py` para agregar el campo.
2. Modifica `repositorio.py` para incluirlo en las consultas.
3. Modifica `buscador.py` para que se pueda buscar por idioma.
4. Modifica `filtros.py` para que se pueda filtrar por idioma.
5. Modifica `serializador.py` para incluirlo en la respuesta JSON.
6. Modifica `validador.py` para validar el campo.
7. Modifica `caché.py` para invalidar las entradas afectadas.

Siete archivos modificados para agregar un campo. Esto es amplificacion de cambios -- el primer sintoma de complejidad que identificamos en el capitulo 1. Y la causa es clara: el conocimiento de "que es un curso" esta esparcido en nueve lugares.

### Analisis con los criterios

Apliquemos el arbol de decision a los modulos existentes:

**Buscador, filtros y ordenamiento:** Los tres acceden a la misma informacion (la estructura del curso y sus campos). Los tres se usan frecuentemente juntos (una busqueda casi siempre incluye filtros y ordenamiento). Operan en el mismo nivel de abstraccion (logica de consulta). *Criterio: juntos.*

**Repositorio, modelos y validador:** Los tres comparten conocimiento sobre la estructura del curso. El repositorio necesita saber que campos tiene un curso para consultarlos. El validador necesita saber que campos tiene un curso para validarlos. Los modelos *son* la definicion de esa estructura. *Criterio: juntos.*

**Serializador:** Depende de los modelos, pero opera en un nivel de abstraccion diferente. La serializacion a JSON es logica de *presentacion*, no logica de *dominio*. Un cambio en como se presenta la informacion al exterior no deberia forzar cambios en la logica de negocio. *Criterio: separado.*

**Recomendador:** Usa los datos de los cursos, pero encapsula un conocimiento distinto: los algoritmos de recomendacion. Este conocimiento podria evolucionar independientemente (de recomendaciones basadas en categorias a recomendaciones basadas en ML). *Criterio: separado.*

**Cache:** Es un mecanismo transversal que no pertenece a la logica de dominio. Deberia ser invisible para los consumidores del catalogo, un detalle de implementacion interno. *Criterio: interno al modulo principal, no un modulo independiente.*

### Estructura propuesta

```
catalogo/
    __init__.py          # Interfaz publica del modulo
    _dominio.py          # Curso, Leccion, Categoria + validacion
    _consultas.py        # Busqueda, filtrado, ordenamiento, repositorio
    _cache.py            # Detalle de implementacion interna
    serializador.py      # Conversion a JSON (nivel de abstraccion diferente)
    recomendador.py      # Conocimiento independiente: algoritmos de sugerencia
```

De nueve archivos con interfaces publicas entre ellos, pasamos a dos modulos publicos (`serializador`, `recomendador`), un modulo principal (`catalogo`) con sus internos, y una interfaz publica limpia en `__init__.py`:

```python
# catalogo/__init__.py
from ._dominio import Curso, Leccion, Categoria, CrearCurso
from ._consultas import (
    buscar_cursos,
    obtener_curso,
    listar_por_categoria,
)

__all__ = [
    "Curso", "Leccion", "Categoria", "CrearCurso",
    "buscar_cursos", "obtener_curso", "listar_por_categoria",
]
```

El resultado:

- **Menos interfaces:** De nueve modulos con interfaces entre ellos a cinco archivos con dos interfaces publicas principales.
- **Mejor ocultamiento:** El cache es un detalle privado. La busqueda, el filtrado y el ordenamiento son detalles internos de las consultas. La validacion vive junto a los modelos que valida.
- **Menores dependencias:** Agregar un campo a `Curso` ahora requiere modificar `_dominio.py` (el modelo y su validacion) y `_consultas.py` (si el campo es buscable). Dos archivos en vez de siete.

### Verificacion: el campo "idioma" con la nueva estructura

Con la estructura reorganizada, agregar el campo `idioma` requiere:

1. Agregar el campo a `Curso` en `_dominio.py` (modelo + validacion juntos).
2. Agregar el filtro en `_consultas.py` (busqueda + filtrado juntos).
3. Agregar el campo en `serializador.py` (presentacion separada).

Tres archivos. Tres cambios coherentes. Cada cambio toca un *concepto* diferente (dominio, consultas, presentacion), no un *paso* diferente del mismo concepto.

**Takeaway:** La reestructuracion del catalogo de DevCourses demuestra que los criterios no son abstractos. Aplicar el arbol de decision -- comparten informacion? Se usan juntos? Diferentes niveles de abstraccion? -- produce una estructura concreta con menos interfaces, mejor ocultamiento y menores dependencias.

---

## Tres anti-patrones que producen separaciones daninas

Antes de cerrar el capitulo, vale la pena identificar tres patrones de separacion que se presentan como buenas practicas pero que frecuentemente producen el efecto opuesto.

### Anti-patron 1: Un archivo por "tipo de operacion"

```
usuario/
    crear_usuario.py
    leer_usuario.py
    actualizar_usuario.py
    eliminar_usuario.py
```

Cuatro archivos que comparten toda la informacion (la estructura del usuario), siempre se necesitan en conjunto (un servicio de usuarios necesita las cuatro operaciones), y operan en el mismo nivel de abstraccion. La separacion no oculta nada; solo esparce el conocimiento.

### Anti-patron 2: La interfaz prematura

```python
class RepositorioCursosInterface(ABC):
    @abstractmethod
    def obtener(self, curso_id): ...
    @abstractmethod
    def guardar(self, curso): ...

class RepositorioCursosPostgres(RepositorioCursosInterface):
    def obtener(self, curso_id):
        return db.query("SELECT * FROM cursos WHERE id = %s", curso_id)
    def guardar(self, curso):
        db.execute("INSERT INTO cursos ...", curso)
```

Una interfaz abstracta con *una sola implementacion*. Esto es codigo que anticipa un cambio que probablemente nunca llegara. Si mañana necesitas una segunda implementacion, puedes crear la interfaz en ese momento. Mientras tanto, la interfaz abstracta es una capa extra de indirección que dificulta la navegacion del codigo sin agregar valor.

### Anti-patron 3: Micromodulos de utilidad

```
utils/
    formatear_fecha.py
    formatear_moneda.py
    formatear_nombre.py
    validar_email.py
    validar_telefono.py
    generar_id.py
```

Cada funcion en su propio archivo. Seis interfaces para seis funciones que podrian ser un solo modulo `formatos.py` y `validaciones.py`. La fragmentacion no oculta nada -- cada funcion de tres lineas no tiene complejidad que ocultar. Solo multiplica los archivos que debes navegar.

**Takeaway:** Los anti-patrones de separacion comparten una causa comun: aplicar reglas mecanicas ("un archivo por operacion", "siempre usa interfaces abstractas", "una funcion por archivo") sin evaluar si la separacion cumple los criterios de ocultamiento y reduccion de interfaces.

---

## Aplica esto el lunes

1. Busca dos funciones en tu proyecto que *siempre* se llaman una despues de la otra, con los mismos parametros. Preguntate: el codigo externo necesita saber que son dos pasos, o deberian ser una sola operacion? Si la respuesta es una sola operacion, unelas y observa cuantas interfaces eliminaste.

2. Busca una funcion larga en tu codigo. Antes de separarla automaticamente, hazte las cuatro preguntas del arbol de decision. Las partes resultantes compartiran informacion? Se usaran siempre juntas? Operan en el mismo nivel de abstraccion? Si las respuestas son si, si y si, dejala como esta y usa comentarios para marcar las secciones.

3. Toma tu modulo mas fragmentado -- el directorio con mas archivos. Para cada par de archivos, preguntate: comparten informacion? Se usan juntos? Si la respuesta a ambas preguntas es si, experimenta con juntarlos. Cuenta las interfaces antes y despues.
