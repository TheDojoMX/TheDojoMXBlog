# Capitulo 11: Sistemas en capas -- la arquitectura mas comun y mas malentendida

> "Si tu capa solo pasa datos a la siguiente, no es una capa -- es burocracia."

---

## Las capas estan en todas partes

Casi todo el software que has escrito o usado esta organizado en capas. Los sistemas operativos tienen capas: hardware, drivers, kernel, sistema de archivos, aplicaciones. Las redes de computadoras tienen capas: el modelo OSI define siete, TCP/IP las condensa en cuatro. Tu framework web favorito tiene capas: rutas, controladores, servicios, base de datos. Hasta un simple script de Python que lee un CSV, lo transforma y lo guarda tiene capas implicitas, aunque no las llames asi.

La arquitectura en capas es tan ubicua que parece obvia. Y ese es exactamente el problema. Porque algo tan comun se malinterpreta con la misma frecuencia con la que se usa. La mayoria de los desarrolladores puede dibujar un diagrama de tres capas con los ojos cerrados: presentacion, logica de negocio, datos. Pero preguntale a ese mismo desarrollador *por que* esas tres capas funcionan, o *que criterio* uso para decidir que pertenece a cada una, y la respuesta se vuelve difusa.

En este capitulo vamos a tomar la arquitectura en capas en serio. No como un diagrama bonito para una presentacion, sino como una aplicacion concreta de los principios que hemos explorado en los diez capitulos anteriores: ocultamiento de informacion, abstraccion, cohesion, acoplamiento. Veremos que hace que una capa sea buena, cuando una capa es innecesaria, y como la evolucion de este patron -- desde MVC hasta la arquitectura hexagonal -- refleja un entendimiento cada vez mas profundo de lo que realmente importa en el diseno de software.

**Takeaway:** La arquitectura en capas no es un patron que se "aplica" mecanicamente. Es una consecuencia natural de los principios de buen diseno. Si entiendes por que funciona, sabras cuando usarla, cuando modificarla y cuando descartarla.

---

## La idea central: cada capa, una abstraccion diferente

John Ousterhout articula la regla fundamental de los sistemas en capas con una claridad que vale la pena repetir:

> "Si un sistema contiene niveles adyacentes con abstracciones similares, esto es una senal de alerta que sugiere un problema con la descomposicion de clases." [Ousterhout, 2018]

La clave esta en la palabra *abstraccion*. Cada capa de un sistema bien disenado trabaja con un vocabulario diferente, con conceptos diferentes, con un nivel de detalle diferente. Si dos capas adyacentes hablan el mismo idioma, una de ellas sobra.

Consideremos el ejemplo clasico de un sistema de archivos, que Ousterhout usa magistralmente:

1. **Capa superior (interfaz de usuario):** Trabaja con la abstraccion de *archivos*. Un archivo tiene nombre, extension, tamano, permisos. El usuario dice "abre este documento" o "guarda este archivo".

2. **Capa intermedia (sistema de cache y bloques):** Trabaja con la abstraccion de *bloques de memoria*. No sabe que es un "archivo". Sabe que hay bloques de datos que deben ser leidos, escritos, cacheados y sincronizados.

3. **Capa inferior (disco fisico):** Trabaja con la abstraccion de *sectores y pistas*. No sabe que son bloques logicos. Sabe donde posicionar el cabezal de lectura y cuantos bytes transferir.

Cada capa transforma la abstraccion. La capa superior convierte "abrir archivo" en "leer estos bloques". La capa intermedia convierte "leer estos bloques" en "mover el cabezal a estas coordenadas". La informacion fluye hacia abajo, pero *cambia de forma* en cada transicion. Eso es lo que hace que las capas funcionen.

### Las tres operaciones de una capa legutima

Una capa puede hacer tres cosas con los datos que recibe de la capa superior:

**1. Transformar.** Recibe datos en una abstraccion y los convierte en otra. Esta es la operacion mas valiosa. La capa de servicio de tu aplicacion recibe un `DTO` de la capa de presentacion y lo convierte en una entidad de dominio. La capa de persistencia recibe esa entidad de dominio y la convierte en una sentencia SQL. Cada transicion es una transformacion.

**2. Agregar.** Anade informacion o funcionalidad que la capa superior no tiene ni deberia tener. La capa de servicio agrega validaciones de reglas de negocio que la capa de presentacion desconoce. La capa de infraestructura agrega el manejo de conexiones, reintentos y timeouts que la logica de negocio no deberia ver.

**3. Filtrar.** Reduce la informacion que pasa a la siguiente capa. La capa de presentacion filtra que campos del objeto de dominio se exponen en la respuesta HTTP. La capa de seguridad filtra que peticiones tienen permiso de llegar a la logica de negocio.

Si una capa no transforma, no agrega y no filtra, entonces solo esta pasando datos. Y una capa que solo pasa datos es, en terminos arquitectonicos, puro desperdicio.

---

## El anti-patron de la capa transparente

Mark Richards, en su libro *Software Architecture Patterns*, identifica el anti-patron mas comun de las arquitecturas en capas: el *architecture sinkhole anti-pattern* [Richards, 2015]. El nombre es descriptivo: los datos caen como en un sumidero, atravesando capas sin que ninguna les haga nada.

Imagina una peticion HTTP para obtener la lista de cursos disponibles en DevCourses:

```python
# Capa 1: Controlador (presentacion)
@app.get("/cursos")
def listar_cursos():
    return servicio_cursos.listar()

# Capa 2: Servicio (logica de negocio)
class ServicioCursos:
    def listar(self):
        return self.repositorio.listar()

# Capa 3: Repositorio (acceso a datos)
class RepositorioCursos:
    def listar(self):
        return db.query("SELECT * FROM cursos")
```

Mira la capa 2. El `ServicioCursos.listar()` no transforma nada, no agrega nada, no filtra nada. Recibe la peticion del controlador y la pasa identica al repositorio. Recibe la respuesta del repositorio y la pasa identica al controlador. Es una funcion de paso -- lo que Ousterhout llama un *pass-through method* [Ousterhout, 2018].

Esta funcion existe porque alguien decidio que "toda aplicacion debe tener tres capas" y creo la capa de servicio por obligacion, no por necesidad. Es burocracia arquitectonica: una firma que no aporta valor pero que todos deben obtener para que el proceso continue.

### La regla 80-20

Richards ofrece una heuristica practica: si mas del 20% de tus peticiones son pass-through puro (los datos atraviesan todas las capas sin transformacion), tu arquitectura tiene un problema. Si el 80% de las peticiones caen en el sinkhole, tus capas no justifican su existencia [Richards, 2015].

Esto no significa que debas eliminar todas las capas. Significa que cada capa debe ganarse su lugar. Una capa existe si y solo si la abstraccion cambia al cruzarla. Si la abstraccion es la misma antes y despues, la capa es transparente -- y lo transparente, en arquitectura, es invisible e inutil.

### Funciones de paso: la senal de alerta

Las funciones de paso no siempre son tan obvias como el ejemplo anterior. A veces se disfrazan de logica legutima:

```python
class ServicioCursos:
    def obtener_curso(self, curso_id: int) -> Curso:
        curso = self.repositorio.obtener(curso_id)
        if curso is None:
            raise CursoNoEncontrado(curso_id)
        return curso
```

Parece que hay logica aqui: el chequeo de `None` y la excepcion. Pero preguntate: esa verificacion, pertenece a esta capa? Es una regla de negocio o es simplemente validacion de existencia que el repositorio podria manejar? Si el repositorio lanzara la excepcion directamente, la capa de servicio desapareceria.

La heuristica es esta: **si puedes eliminar una capa y el sistema sigue funcionando exactamente igual, esa capa no necesita existir.**

### Variables pasadas: la senal gemela

Similar a las funciones de paso, las *variables pasadas* son parametros que una capa recibe y pasa intactos a la siguiente sin usarlos. Son datos que viajan como turistas -- pasan por la capa pero no interactuan con ella.

```python
# La variable 'idioma' viaja a traves de tres capas sin ser usada
# hasta que llega a la capa de presentacion

@app.get("/cursos")
def listar_cursos(idioma: str = "es"):
    return servicio_cursos.listar(idioma=idioma)

class ServicioCursos:
    def listar(self, idioma: str):
        cursos = self.repositorio.listar()
        return self.formateador.formatear(cursos, idioma=idioma)
```

Aqui `idioma` pasa del controlador al servicio, pero el servicio no lo usa -- solo lo reenvia al formateador. El servicio esta acoplado a un concepto que no le pertenece. Esto es una fuga de informacion disfrazada de parametro.

Las soluciones varian segun el paradigma. En algunos frameworks, el contexto de la peticion esta disponible globalmente (como el `request` en Flask o Django). En arquitecturas orientadas a objetos, un objeto de contexto puede viajar con la peticion sin contaminar las firmas de cada capa. Lo importante es reconocer la senal: si un parametro atraviesa dos o mas capas sin ser transformado, algo en la descomposicion esta mal.

---

## Capas abiertas y capas cerradas: la tension de la rigidez

No todas las arquitecturas en capas funcionan de la misma manera. Hay una distincion fundamental que rara vez se ensena pero que tiene consecuencias profundas en la practica: la diferencia entre capas cerradas y capas abiertas.

### Capas cerradas: cada peticion baja un escalon a la vez

En una arquitectura con capas cerradas, cada peticion debe pasar por la capa inmediatamente inferior. No se pueden saltar capas. Si la peticion esta en la capa de presentacion y necesita datos, debe pasar por la capa de servicio antes de llegar a la capa de datos, aunque la capa de servicio no haga nada con ella.

La ventaja es el aislamiento. Si cambias la capa de datos, solo afectas a la capa de servicio. La capa de presentacion no se entera. Cada capa es un escudo que protege a las capas superiores de los cambios en las capas inferiores.

La desventaja es la rigidez. Si el 60% de tus peticiones son lecturas simples que no necesitan logica de negocio, estas obligando a esas peticiones a pasar por una capa que no les aporta nada. Es la burocracia que mencionamos al inicio del capitulo.

### Capas abiertas: permitir atajos controlados

En una arquitectura con capas abiertas, una capa puede comunicarse con cualquier capa inferior, no solo la inmediata. El controlador puede llamar directamente al repositorio si no hay logica de negocio que aplicar.

La ventaja es la eficiencia. Las peticiones simples toman el camino mas corto. No hay funciones de paso innecesarias. El codigo es mas directo y facil de seguir.

La desventaja es el riesgo de acoplamiento. Si el controlador llama directamente al repositorio, esta acoplado a la capa de datos. Si la capa de datos cambia su interfaz, el controlador se rompe. Has perdido el escudo de aislamiento.

### La solucion pragmatica: capas selectivamente abiertas

La respuesta no es "siempre cerradas" ni "siempre abiertas". Es tomar la decision capa por capa, basandote en un criterio concreto:

**Una capa deberia ser cerrada si los cambios en la capa inferior son probables y queremos proteger a las capas superiores.** La capa de servicio deberia ser cerrada si la logica de negocio cambia frecuentemente y no queremos que esos cambios afecten a la presentacion.

**Una capa deberia ser abierta si los cambios en la capa inferior son improbables y la capa intermedia no agrega valor.** Si la capa de datos usa un ORM estable y su interfaz rara vez cambia, permitir que el controlador lo use directamente para lecturas simples es pragmatismo, no pecado.

En DevCourses, aplicamos esta distincion asi:

- El modulo de **pagos** tiene capas cerradas. La logica de negocio (calcular precios, aplicar descuentos, validar suscripciones) cambia frecuentemente. El controlador *nunca* accede directamente al repositorio de pagos.
- El modulo de **catalogo** tiene capas abiertas para lecturas. Listar cursos no requiere logica de negocio. El controlador puede consultar directamente el repositorio. Pero las *escrituras* (crear curso, modificar curso) si pasan por un servicio que valida permisos y reglas de publicacion.

Esta flexibilidad no es caos. Es diseno consciente. Cada decision de abrir o cerrar una capa esta documentada y justificada. Y si las circunstancias cambian -- si el catalogo de repente necesita logica de filtrado compleja -- se cierra la capa y se mueve la logica al lugar correcto.

### La "lasana" y el "sinkhole": dos nombres para el mismo error

Vale la pena notar que la industria ha acunado nombres peyorativos para los dos extremos del espectro:

- **Lasagna architecture** (arquitectura lasana): Demasiadas capas cerradas apiladas, creando una estructura donde cada peticion tiene que atravesar multiples capas de burocracia. Capas finas que no aportan valor individual pero que sumadas crean un muro de indirreccion.

- **Architecture sinkhole** (sumidero arquitectonico): Peticiones que caen a traves de las capas sin que ninguna les haga nada, como agua filtrandose por capas de arena.

Ambos nombres describen el mismo error de fondo: **las capas no se ganaron su lugar**. La lasana tiene capas por dogma; el sinkhole tiene capas vacias por inercia. La solucion es la misma: evaluar cada capa con la pregunta "que transforma, agrega o filtra?" y eliminar las que no responden nada.

---

## Diseno en capas como caso especial de ocultamiento de informacion

Si has seguido los capitulos anteriores con atencion, quiza ya notaste la conexion: la arquitectura en capas es una aplicacion directa del principio de ocultamiento de informacion de Parnas [Parnas, 1972].

Cada capa oculta decisiones de diseno a las capas adyacentes:

- **La capa de presentacion** oculta el formato de comunicacion con el exterior (HTTP, GraphQL, gRPC, CLI). La logica de negocio no sabe si esta siendo invocada desde un navegador web, una aplicacion movil o un script automatizado.

- **La capa de servicio** oculta las reglas de negocio y la orquestacion de operaciones. La capa de presentacion no sabe que inscribir a un usuario requiere verificar su suscripcion, validar la disponibilidad del curso y registrar el evento para analytics.

- **La capa de infraestructura** oculta los detalles de almacenamiento y comunicacion externa. La logica de negocio no sabe si los datos estan en PostgreSQL, MongoDB, un archivo CSV o una API remota.

La relacion con la cohesion del capitulo anterior tambien es directa. Cada capa tiene alta cohesion porque todos sus elementos trabajan en el mismo nivel de abstraccion. Y el acoplamiento entre capas es bajo porque se comunican a traves de interfaces bien definidas, no accediendo a los detalles internos de la otra.

**Las capas son la materializacion arquitectonica de "pon las cosas relacionadas juntas y oculta los detalles."**

Esta conexion explica por que la arquitectura en capas funciona tan bien cuando se hace correctamente, y por que falla tan estrepitosamente cuando se hace mecanicamente. Si cada capa oculta una decision de diseno genuina, el sistema es robusto. Si las capas existen por obligacion y no ocultan nada, son burocracia.

La prueba definitiva de una buena capa es esta: **si puedes cambiar completamente la implementacion interna de una capa sin que las capas adyacentes se enteren, la capa esta bien disenada.** Si cambiar de PostgreSQL a MongoDB requiere modificar la logica de negocio, tu capa de infraestructura tiene fugas. Si cambiar de HTTP a GraphQL requiere modificar los servicios, tu capa de presentacion tiene fugas.

---

## MVC y sus variantes: la capa hecha patron

No podemos hablar de capas sin hablar de MVC. Es probablemente el patron arquitectonico mas ensenado, mas implementado y mas malinterpretado de la historia del software.

### La idea original de Trygve Reenskaug

MVC fue concebido por Trygve Reenskaug en 1979, en Xerox PARC, como una forma de organizar las interfaces graficas de Smalltalk [Reenskaug, 1979]. La idea era simple pero poderosa:

- **Model (Modelo):** Representa los datos y las reglas del dominio. No sabe nada sobre como se muestra.
- **View (Vista):** Muestra los datos al usuario. No sabe nada sobre reglas de negocio.
- **Controller (Controlador):** Recibe la entrada del usuario, la traduce en operaciones sobre el modelo, y selecciona la vista adecuada.

La genialidad de MVC es que separa tres preocupaciones que cambian por razones diferentes:

1. Las reglas de negocio cambian cuando cambia el dominio.
2. La presentacion cambia cuando cambia la experiencia de usuario.
3. El flujo de interaccion cambia cuando cambia la forma en que el usuario interactua.

Al separarlas, un cambio en una preocupacion no arrastra cambios en las otras. Puedes cambiar como se muestran los cursos sin tocar las reglas de inscripcion. Puedes cambiar las reglas de inscripcion sin tocar la interfaz de usuario. Esto es ocultamiento de informacion en accion.

### Lo que MVC se convirtio

El problema es que MVC muto significativamente desde Smalltalk hasta los frameworks web modernos. En Smalltalk, la View observaba directamente al Model (patron Observer). En Rails, Django, Spring y sus descendientes, MVC se convirtio en algo diferente:

- La "Vista" ya no observa al modelo. Recibe datos preprocesados del controlador.
- El "Controlador" se convirtio en el coordinador de todo: valida entrada, llama a servicios, maneja errores, decide la vista.
- El "Modelo" se redujo a una representacion de tablas de la base de datos (un ORM), perdiendo la nocion de "reglas de dominio".

Django fue honesto con esta evolucion y renombro su arquitectura a MVT (Model-View-Template), donde la "Vista" es realmente un controlador y el "Template" es la vista. Otros frameworks mantuvieron la nomenclatura MVC pero con semantica diferente.

Las variantes son abundantes:

- **MVVM (Model-View-ViewModel):** Usado en frameworks de frontend como Angular y Knockout. El ViewModel es un intermediario que prepara los datos del modelo para la vista.
- **MVP (Model-View-Presenter):** El Presenter maneja toda la logica de presentacion. Popular en aplicaciones de escritorio.
- **MVT (Model-View-Template):** La variante de Django, donde "View" es el controlador y "Template" es la vista real.

Lo que importa no es la variante especifica, sino el principio detras de todas ellas: **separar las preocupaciones que cambian por razones diferentes en capas con abstracciones distintas.** Si entiendes el principio, la variante es un detalle de implementacion.

### El "modelo gordo" y el controlador gordo

Dos anti-patrones clasicos de MVC ilustran lo que sucede cuando las capas pierden su identidad:

**El controlador gordo** acumula logica de negocio, validacion, transformacion de datos, manejo de errores y orquestacion. Es la clase que tiene quinientas lineas y que nadie quiere tocar. El controlador dejo de ser un coordinador y se convirtio en un vertedero de logica. La cohesion es baja porque mezcla preocupaciones de presentacion con reglas de negocio.

**El modelo gordo** surge como reaccion: "muevan toda la logica al modelo". Pero entonces el modelo -- que originalmente era una representacion del dominio -- se llena de metodos de formateo, notificaciones, interaccion con servicios externos, y cualquier cosa que "no sea del controlador". La cohesion es igualmente baja, solo que la basura cambio de lugar.

La solucion no es hacer un controlador gordo o un modelo gordo. Es reconocer que MVC de tres capas es insuficiente para la mayoria de las aplicaciones no triviales. Necesitas capas intermedias: servicios para la logica de negocio, repositorios para el acceso a datos, objetos de transferencia para la comunicacion entre capas. Y cada capa extra debe ganarse su lugar transformando, agregando o filtrando -- nunca simplemente pasando datos.

---

## Hexagonal: cuando las capas dejan de ser horizontales

En el ano 2005, Alistair Cockburn propuso una alternativa radical a la vision tradicional de capas horizontales: la arquitectura hexagonal, tambien conocida como "ports and adapters" [Cockburn, 2005]. La idea surgio de una frustracion concreta: en la arquitectura en capas clasica, la logica de negocio esta en el medio, atrapada entre la capa de presentacion (arriba) y la capa de datos (abajo). Pero esa relacion de "arriba" y "abajo" es enganiosa. La logica de negocio no depende *mas* de la base de datos que de la interfaz de usuario. Ambas son *externas* al dominio.

### La metafora del hexagono

Cockburn propuso imaginar la aplicacion como un hexagono. Adentro esta el dominio: la logica de negocio pura, las reglas, las entidades. Afuera estan todos los elementos externos: bases de datos, APIs, interfaces de usuario, colas de mensajes, servicios de terceros.

La comunicacion entre el interior y el exterior se da a traves de dos conceptos:

- **Puertos (ports):** Interfaces que el dominio define para comunicarse con el mundo exterior. Un puerto de entrada dice "asi es como puedes pedirme cosas". Un puerto de salida dice "esto es lo que necesito del exterior".

- **Adaptadores (adapters):** Implementaciones concretas que conectan los puertos con la tecnologia especifica. Un adaptador HTTP conecta el puerto de entrada con las peticiones web. Un adaptador PostgreSQL conecta el puerto de salida con la base de datos.

```python
# Puerto de entrada (definido por el dominio)
class PuertoInscripcion(ABC):
    @abstractmethod
    def inscribir(self, usuario_id: int, curso_id: int) -> Inscripcion: ...

# Puerto de salida (definido por el dominio)
class PuertoRepositorioCursos(ABC):
    @abstractmethod
    def obtener(self, curso_id: int) -> Curso: ...

# Dominio (no sabe nada del exterior)
class ServicioInscripcion(PuertoInscripcion):
    def __init__(self, repo: PuertoRepositorioCursos):
        self._repo = repo

    def inscribir(self, usuario_id: int, curso_id: int) -> Inscripcion:
        curso = self._repo.obtener(curso_id)
        if not curso.tiene_cupo():
            raise SinCupo(curso_id)
        return Inscripcion(usuario_id=usuario_id, curso_id=curso_id)

# Adaptador de entrada (conecta HTTP con el dominio)
@app.post("/inscripciones")
def crear_inscripcion(request: InscripcionRequest):
    servicio = obtener_servicio_inscripcion()
    inscripcion = servicio.inscribir(request.usuario_id, request.curso_id)
    return InscripcionResponse.from_domain(inscripcion)

# Adaptador de salida (conecta el dominio con PostgreSQL)
class RepositorioCursosPostgres(PuertoRepositorioCursos):
    def obtener(self, curso_id: int) -> Curso:
        row = db.query("SELECT * FROM cursos WHERE id = %s", curso_id)
        return Curso.from_row(row)
```

### La inversion que importa

La diferencia fundamental con la arquitectura en capas clasica no es estetica -- es la *direccion de las dependencias*. En capas clasicas, la logica de negocio depende de la capa de datos: el servicio importa el repositorio concreto. En hexagonal, la capa de datos depende de la logica de negocio: el repositorio implementa una interfaz que el dominio definio.

Esta inversion no es gratuita. Como discutimos en el capitulo 9, invertir dependencias tiene un costo: indirreccion, navegabilidad reducida, configuracion de cableado. Pero en el caso especifico de los limites del sistema -- donde tu aplicacion se conecta con bases de datos, APIs externas, interfaces de usuario -- la inversion se justifica porque esos limites son genuinamente volatiles. Puedes cambiar de framework web, de base de datos, de proveedor de servicios. El dominio deberia sobrevivir a todos esos cambios.

### Capas vs hexagonal: no es una competencia

Es tentador presentar la arquitectura hexagonal como "mejor" que la arquitectura en capas. Pero eso seria caer en el mismo error que criticamos con SOLID: tratar las herramientas como dogma.

La arquitectura en capas y la hexagonal no son mutuamente excluyentes. Son perspectivas complementarias:

- **Las capas** te dicen como organizar el codigo *verticalmente*: presentacion arriba, dominio en medio, infraestructura abajo. Son utiles para entender el flujo de una peticion.

- **El hexagono** te dice como organizar las *dependencias*: el dominio al centro, todo lo externo en la periferia. Es util para entender que depende de que.

Puedes tener ambas. De hecho, la mayoria de las aplicaciones bien disenadas las tienen. Las capas organizan la estructura del directorio; el hexagono organiza la direccion de las dependencias.

La pregunta no es "capas o hexagonal?" sino "mis capas ocultan las decisiones correctas y mis dependencias apuntan en la direccion correcta?"

### Cuando hexagonal es excesivo

La arquitectura hexagonal no es gratuita. Requiere interfaces para cada puerto, implementaciones concretas para cada adaptador, y un mecanismo para cablear adaptadores con puertos. En una aplicacion CRUD simple -- donde la logica de negocio es minima y la base de datos probablemente nunca va a cambiar -- toda esa maquinaria es desperdicio.

AWS Prescriptive Guidance es honesto al respecto: "El codigo adicional de adaptadores que hace la arquitectura pluggable solo se justifica si el componente de la aplicacion requiere varias fuentes de entrada y destinos de salida, o cuando las entradas y los almacenes de datos deben cambiar con el tiempo" [AWS, 2024].

La heuristica es la misma que usamos para DIP en el capitulo 9: si tienes multiples implementaciones concretas o evidencia real de que la implementacion va a cambiar, el costo del hexagono se justifica. Si solo tienes una implementacion y no hay evidencia de cambio, una capa directa es mas simple y mas honesta.

---

## Vertical slices: la alternativa a las capas horizontales

Una critica recurrente a las capas horizontales es que fragmentan los features. Para implementar "inscribir a un usuario en un curso", tienes que tocar la capa de presentacion (crear la ruta), la capa de servicio (crear el metodo), la capa de repositorio (crear la query), y posiblemente la capa de dominio (crear o modificar la entidad). Cuatro archivos en cuatro directorios diferentes para una sola funcionalidad.

Jimmy Bogard popularizo la idea de *vertical slices*: en vez de organizar el codigo por capa tecnica, organizarlo por funcionalidad de negocio [Bogard, 2018]. Cada "slice" contiene todo lo necesario para una operacion: la ruta, la validacion, la logica, el acceso a datos.

```
# En vez de:
controllers/
    cursos_controller.py
    inscripciones_controller.py
services/
    servicio_cursos.py
    servicio_inscripciones.py
repositories/
    repo_cursos.py
    repo_inscripciones.py

# Organizar asi:
features/
    listar_cursos/
        handler.py
        query.py
    inscribir_usuario/
        handler.py
        command.py
        validator.py
```

La ventaja es que la cohesion es altisima: todo lo relacionado con "inscribir usuario" esta en un solo lugar. El acoplamiento entre slices es bajo porque cada uno es autocontenido.

La desventaja es que el codigo compartido (utilidades de base de datos, validaciones comunes, logica de autorizacion) necesita un lugar donde vivir. Y si no se gestiona bien, terminas con duplicacion entre slices.

Vertical slices no reemplazan las capas -- las complementan. Dentro de cada slice, sigue habiendo capas implicitas (validacion, logica, persistencia). La diferencia es que la unidad de organizacion primaria es la funcionalidad, no la capa tecnica. Es un cambio de prioridad: primero cohesion por feature, luego separacion por abstraccion.

---

## Proyecto guia: rediseniando las capas de DevCourses

Vamos a aplicar todo lo que hemos discutido para redisenar la arquitectura en capas de DevCourses. El sistema, despues de las mejoras de los capitulos anteriores, tiene siete modulos con buena cohesion y acoplamiento razonable. Ahora necesitamos decidir como se organizan las capas *dentro* de cada modulo.

### Estado actual: el problema

El equipo de DevCourses implemento una arquitectura de tres capas clasica al principio del proyecto:

```
app/
    controllers/     # Capa 1: Presentacion
        cursos.py
        inscripciones.py
        pagos.py
        usuarios.py
        video.py
        comentarios.py
        notificaciones.py
    services/        # Capa 2: Logica de negocio
        servicio_cursos.py
        servicio_inscripciones.py
        servicio_pagos.py
        servicio_usuarios.py
        servicio_video.py
        servicio_comentarios.py
        servicio_notificaciones.py
    repositories/    # Capa 3: Acceso a datos
        repo_cursos.py
        repo_inscripciones.py
        repo_pagos.py
        repo_usuarios.py
        repo_video.py
        repo_comentarios.py
        repo_notificaciones.py
```

A primera vista, parece limpio. Tres capas, siete modulos, veintiun archivos. Pero al examinar el codigo, encontramos problemas:

**Problema 1: Capas transparentes.** Cuatro de los siete servicios son funciones de paso. `ServicioCursos.listar()` llama a `repo_cursos.listar()` sin agregar nada. `ServicioComentarios.obtener(id)` llama a `repo_comentarios.obtener(id)` sin agregar nada. El 57% de las operaciones del sistema son sinkhole puro.

**Problema 2: Cohesion por capa, no por dominio.** Todos los controladores estan juntos, todos los servicios estan juntos, todos los repositorios estan juntos. Si quiero entender como funciona el sistema de inscripciones, tengo que navegar tres directorios diferentes. La cohesion es logica ("todos los controladores"), no funcional ("todo sobre inscripciones").

**Problema 3: Acoplamiento oculto.** Los servicios se llaman entre si libremente. `ServicioInscripciones` llama a `ServicioPagos`, que llama a `ServicioNotificaciones`. Las capas son horizontales, pero las dependencias son diagonales. El diagrama de tres capas es una mentira; en realidad, el grafo de dependencias es un laberinto.

### El rediseno: capas con proposito

Aplicamos tres cambios:

**Cambio 1: Eliminar capas transparentes.** Para los modulos cuyo servicio es pura burocracia (catalogo, comentarios, video), eliminamos la capa de servicio. El controlador llama directamente al repositorio. Esto reduce la indirreccion sin sacrificar nada, porque la capa de servicio no estaba aportando valor.

```python
# Antes: tres capas, la del medio es transparente
@app.get("/cursos")
def listar_cursos():
    return servicio_cursos.listar()  # Solo pasa datos al repo

# Despues: dos capas, cada una transforma
@app.get("/cursos")
def listar_cursos(filtros: FiltrosCursos = Depends()):
    cursos = repo_cursos.listar(filtros.to_query())
    return [CursoResponse.from_domain(c) for c in cursos]
```

Ahora el controlador transforma: convierte los parametros HTTP en una query, y convierte los objetos de dominio en respuestas HTTP. Dos transformaciones reales en vez de tres funciones de paso.

**Cambio 2: Reorganizar por dominio, no por capa.** Los modulos que tienen logica real (inscripciones, pagos, usuarios/autenticacion) conservan tres capas, pero organizadas por dominio:

```
app/
    catalogo/             # Modulo simple: 2 capas
        routes.py
        repository.py
        models.py
    inscripciones/        # Modulo complejo: 3 capas
        routes.py
        service.py
        repository.py
        models.py
    pagos/                # Modulo complejo: 3 capas
        routes.py
        service.py
        repository.py
        models.py
        processors/       # Adaptadores para Stripe, MercadoPago, PayPal
            stripe.py
            mercadopago.py
            paypal.py
    perfiles/             # Modulo simple: 2 capas
        routes.py
        repository.py
        models.py
    autenticacion/        # Modulo con logica de seguridad: 3 capas
        routes.py
        service.py
        repository.py
        models.py
    video/                # Modulo simple: 2 capas
        routes.py
        repository.py
        models.py
    comentarios/          # Modulo simple: 2 capas
        routes.py
        repository.py
        models.py
    notificaciones/       # Modulo con logica de canales: 3 capas
        routes.py
        service.py
        channels/
            email.py
            push.py
            sms.py
```

Ahora la cohesion es funcional: todo lo de inscripciones esta en `inscripciones/`. Y la cantidad de capas no es uniforme -- cada modulo tiene las capas que necesita, ni mas ni menos.

**Cambio 3: Limites claros entre modulos.** Los servicios ya no se llaman entre si directamente. Definimos interfaces publicas explicitas para cada modulo y usamos eventos para la comunicacion asincrona:

```python
# inscripciones/service.py
class ServicioInscripciones:
    def __init__(
        self,
        repo: RepositorioInscripciones,
        precios: PuertoPrecios,         # Interfaz, no ServicioPagos
        eventos: PuertoEventos           # Interfaz para emitir eventos
    ):
        self._repo = repo
        self._precios = precios
        self._eventos = eventos

    def inscribir(self, usuario_id: int, curso_id: int) -> Inscripcion:
        precio = self._precios.obtener_precio(curso_id)
        inscripcion = Inscripcion.crear(usuario_id, curso_id, precio)
        self._repo.guardar(inscripcion)
        self._eventos.emitir("inscripcion_completada", inscripcion.to_evento())
        return inscripcion
```

El modulo de inscripciones no sabe que las notificaciones se envian por email. No sabe que los pagos se procesan con Stripe. Solo sabe que hay un puerto de precios y un puerto de eventos. Los adaptadores concretos se cablea en el punto de entrada de la aplicacion.

### El resultado

| Aspecto | Antes | Despues |
|---|---|---|
| Capas transparentes | 4 de 7 (57%) | 0 |
| Organizacion | Por capa tecnica | Por dominio |
| Archivos para entender inscripciones | 3 (en 3 directorios) | 4 (en 1 directorio) |
| Dependencias entre servicios | Llamadas directas | Interfaces + eventos |
| Capas por modulo | 3 (uniforme) | 2-3 (segun necesidad) |

El sistema tiene menos capas en total, pero cada capa que existe transforma, agrega o filtra. No hay burocracia. Y la cohesion por dominio facilita que un desarrollador nuevo entienda un modulo completo sin navegar todo el proyecto.

---

## Las capas y los principios del libro

Las buenas capas son la manifestacion arquitectonica de todo lo que hemos cubierto:

**Ocultamiento de informacion (capitulo 6).** Cada capa oculta decisiones de diseno. La capa de infraestructura oculta que usamos PostgreSQL. La capa de presentacion oculta que usamos HTTP. Si puedes cambiar una decision sin afectar otras capas, el ocultamiento funciona.

**Modulos profundos (capitulo 5).** Una buena capa es un modulo profundo: ofrece una interfaz simple a la capa superior y oculta gran complejidad internamente. Una mala capa es un modulo superficial: ofrece una interfaz que es practicamente igual a lo que oculta.

**Cohesion y acoplamiento (capitulo 10).** Cada capa tiene alta cohesion interna (todos sus elementos trabajan en el mismo nivel de abstraccion) y bajo acoplamiento con las capas adyacentes (se comunican a traves de interfaces definidas, no accediendo a detalles internos).

**Separar o juntar (capitulo 7).** Las capas se justifican cuando los niveles de abstraccion son diferentes. Se eliminan cuando no hay diferencia real entre lo que entra y lo que sale.

No es casualidad. Los buenos principios de diseno producen buenas capas de forma natural. Si ocultas informacion correctamente, las capas emergen. Si mantienes la cohesion alta, cada capa tiene un proposito claro. Si minimizas el acoplamiento, las capas se comunican limpiamente.

Las capas no son un patron que se impone desde arriba. Son una consecuencia de disenar bien desde abajo.

---

## Aplica esto el lunes

1. **Identifica las capas de tu sistema.** Para cada una, escribe en una oracion que abstraccion maneja. Si dos capas adyacentes manejan la misma abstraccion, una de ellas probablemente sobra. Preguntate: que transformacion ocurre al cruzar de una capa a otra?

2. **Busca funciones de paso en tu codigo.** Funciones que solo llaman a otra funcion de la capa inferior sin transformar, agregar ni filtrar nada. Cada una es un candidato para eliminacion. Usa la regla 80-20 de Richards: si mas del 20% de tus operaciones son pass-through, tienes un problema.

3. **Busca variables que viajan sin ser usadas.** Parametros que una capa recibe y pasa intactos a la siguiente. Cada uno es una fuga de informacion que acopla capas que no deberian conocerse.

4. **Evalua si tu organizacion es por capa tecnica o por dominio.** Si para entender un feature necesitas abrir archivos en tres directorios diferentes, considera reorganizar por dominio. La cohesion por feature casi siempre gana a la cohesion por capa tecnica.

5. **Antes de agregar una capa nueva, preguntate: que decision de diseno va a ocultar esta capa?** Si la respuesta es "ninguna, pero asi es como se hace en nuestra arquitectura", no la agregues. Las capas se ganan su lugar; no se imponen por dogma.

---

## Referencias del capitulo

- AWS Prescriptive Guidance. (2024). "Hexagonal Architecture Pattern." Amazon Web Services.
- Bogard, J. (2018). "Vertical Slice Architecture." Blog post.
- Cockburn, A. (2005). "Hexagonal Architecture." alistair.cockburn.us.
- Ousterhout, J. (2018). *A Philosophy of Software Design*. Yaknyam Press.
- Parnas, D. (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 15(12).
- Reenskaug, T. (1979). "Models-Views-Controllers." Technical note, Xerox PARC.
- Richards, M. (2015). *Software Architecture Patterns*. O'Reilly Media.
