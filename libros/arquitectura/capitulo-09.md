# Capitulo 9: Liskov, ISP y DIP -- Los tres principios mas sobrevaluados

> "Si estos principios fueran tan importantes como se ensena, el 80% de los sistemas que funcionan bien en produccion estarian 'mal disenados'. Algo no cuadra."

---

## Tres principios sagrados que nadie necesita (casi)

En el capitulo anterior desmenuzamos SOLID y descubrimos que los cinco principios son aplicaciones particulares de ideas mas profundas: simplicidad, ocultamiento de informacion y buenas abstracciones. Examinamos en detalle SRP y OCP, los dos principios que mas se aplican en la practica cotidiana, y mostramos como sus fundamentos los hacen utiles cuando se interpretan con juicio.

Ahora toca enfrentar a los otros tres: el Principio de Sustitucion de Liskov (LSP), el Principio de Segregacion de Interfaces (ISP), y el Principio de Inversion de Dependencias (DIP). Los tres comparten una caracteristica: se ensenan con reverencia en cursos, libros y entrevistas de trabajo, pero la mayoria de los desarrolladores nunca enfrentan el problema especifico que cada uno resuelve. No porque los principios sean malos, sino porque los problemas que abordan son menos frecuentes de lo que la industria sugiere.

La tesis de este capitulo es directa: LSP, ISP y DIP son utiles en contextos especificos y concretos. Pero aplicarlos como reglas universales produce sobre-ingenieria, interfaces innecesarias y complejidad accidental. Lo que realmente necesitas, el 90% del tiempo, es algo mas viejo y mas simple: bajo acoplamiento y alta cohesion. Eso lo cubriremos en el proximo capitulo.

Aqui haremos algo que rara vez se hace en los libros de diseno de software: seremos honestos sobre cuando estos principios importan y cuando son ruido.

**Takeaway:** LSP, ISP y DIP resuelven problemas reales pero infrecuentes. Ensanarlos como mandamientos universales crea desarrolladores que resuelven problemas que no tienen.

---

## Liskov: util en teoria, rara vez es tu problema real

### La idea original

Barbara Liskov, junto con Jeannette Wing, publico en 1994 el articulo "A Behavioral Notion of Subtyping" [Liskov y Wing, 1994]. La idea central es elegante: si un tipo S es subtipo de un tipo T, entonces los objetos de tipo T pueden ser reemplazados por objetos de tipo S sin alterar las propiedades deseables del programa.

Liskov no hablaba de herencia de clases. Hablaba de *tipos abstractos de datos* (ADTs). Un ADT define una interfaz -- operaciones, precondiciones, postcondiciones, invariantes -- y cualquier implementacion concreta de ese ADT debe respetar esa interfaz. No solo la firma de los metodos, sino su *comportamiento observable*. Si dices que `retirar(monto)` reduce el saldo, toda implementacion de Cuenta debe reducir el saldo cuando se llama `retirar(monto)`. Una implementacion que silenciosamente ignora el retiro viola LSP, aunque compile perfectamente.

La formulacion que Robert C. Martin popularizo es mas simple pero mas estrecha:

> "Las subclases deben ser sustituibles por sus clases base." [Martin, 2000]

Al reducir la idea de Liskov a "subclases" y "clases base", Martin la encadeno a la herencia de clases orientada a objetos. Y eso creo el problema pedagogico que arrastramos hasta hoy: la mayoria de los desarrolladores piensan que LSP solo aplica cuando usas herencia. En realidad, aplica siempre que un componente de software puede ser reemplazado por otro que "se supone" hace lo mismo.

### El rectangulo y el cuadrado: el ejemplo que confunde mas de lo que ensena

Cada libro, cada curso, cada tutorial de SOLID usa el mismo ejemplo para ilustrar LSP: el rectangulo y el cuadrado. Un cuadrado *es* un rectangulo en geometria, asi que parece natural que `Cuadrado` herede de `Rectangulo`. Pero hay un problema:

```python
class Rectangulo:
    def __init__(self, ancho, alto):
        self._ancho = ancho
        self._alto = alto

    def set_ancho(self, ancho):
        self._ancho = ancho

    def set_alto(self, alto):
        self._alto = alto

    def area(self):
        return self._ancho * self._alto


class Cuadrado(Rectangulo):
    def set_ancho(self, ancho):
        self._ancho = ancho
        self._alto = ancho  # Para mantener la invariante del cuadrado

    def set_alto(self, alto):
        self._ancho = alto
        self._alto = alto
```

El codigo que usa rectangulos espera poder cambiar ancho y alto independientemente:

```python
def duplicar_ancho(r: Rectangulo):
    ancho_original = r._ancho
    r.set_ancho(ancho_original * 2)
    assert r.area() == ancho_original * 2 * r._alto  # Falla con Cuadrado
```

Si pasas un `Cuadrado`, la asercion falla porque `set_ancho` tambien cambio el alto. El `Cuadrado` viola LSP: no puede sustituir a un `Rectangulo` sin romper las expectativas del codigo cliente.

La solucion que los libros proponen es: no hagas que `Cuadrado` herede de `Rectangulo`. Haz que ambos hereden de una interfaz `Forma` con un metodo `area()`. Problema resuelto.

Y aqui es donde debemos hacer una pausa y preguntar: *cuando fue la ultima vez que tuviste este problema en codigo de produccion?*

### Por que casi nunca es tu problema

El ejemplo del rectangulo y el cuadrado ilustra un punto teorico valido: las relaciones de herencia deben respetar contratos de comportamiento, no solo relaciones conceptuales del mundo real. Pero en la practica cotidiana del desarrollo de software, las violaciones de LSP son raras por tres razones:

**Razon 1: La herencia de clases esta en declive.** Los lenguajes y paradigmas modernos favorecen la composicion sobre la herencia. Go no tiene herencia. Rust no tiene herencia. JavaScript la usa poco. Python la usa con moderacion. Los lenguajes funcionales ni la contemplan. Si no usas herencia de clases, la formulacion clasica de LSP simplemente no aplica a tu codigo.

**Razon 2: Los problemas reales de sustitucion se detectan con pruebas.** Si tienes un `CachedRepository` que lanza una excepcion donde el `DatabaseRepository` retorna `null`, la primera prueba de integracion lo detecta. No necesitas invocar a Liskov para saber que algo esta mal. Necesitas pruebas.

**Razon 3: Las violaciones genuinas de LSP son obvias.** Cuando un subtipo se comporta de forma inesperada, el sistema falla visiblemente. No es el tipo de error sutil que necesita un principio formal para detectarse. Es el tipo de error que produce un ticket de soporte en las primeras horas de produccion.

Esto no significa que LSP sea inutil. Significa que su utilidad esta acotada a un escenario especifico: cuando estas disenando jerarquias de tipos que seran extendidas por otros desarrolladores. Si escribes una biblioteca, un framework, o una API publica que otros van a implementar, LSP es crucial. Si escribes una aplicacion de negocio con un equipo de seis personas, probablemente nunca tengas un problema que LSP resuelva.

### Lo que Liskov realmente queria decir

El aporte mas profundo de Barbara Liskov no es el principio de sustitucion. Es la teoria de los *tipos abstractos de datos*. La idea de que puedes definir un tipo por su *comportamiento observable* -- sus operaciones, sus precondiciones, sus postcondiciones, sus invariantes -- sin especificar como se implementa internamente.

Esto es, literalmente, ocultamiento de informacion aplicado a los tipos. Y conecta directamente con la tesis central de este libro: la herramienta mas poderosa del disenador de software es la capacidad de definir *que* hace algo sin revelar *como* lo hace.

Si lees el paper original de Liskov y Wing con atencion, descubres que el principio de sustitucion es un *corolario* de una idea mas amplia: si defines bien las abstracciones, la sustitucion se da naturalmente. Si defines mal las abstracciones, ningun principio te salva.

**Takeaway:** LSP es un caso especifico de un principio mas general: las abstracciones deben tener contratos claros y cualquier implementacion debe respetarlos. Si disenas bien tus interfaces y ocultas informacion correctamente, LSP se cumple sin esfuerzo. Si lo necesitas como regla explicita, probablemente el problema es que tus abstracciones estan mal disenadas.

---

## ISP: cuando la segregacion crea mas problemas de los que resuelve

### El principio en su contexto

El Principio de Segregacion de Interfaces (ISP) dice:

> "Los clientes no deberian ser forzados a depender de interfaces que no usan." [Martin, 2000]

La idea tiene sentido intuitivo. Si tienes una interfaz con diez metodos y un cliente solo usa dos, ese cliente esta acoplado a ocho metodos que no le importan. Si alguien cambia la firma de uno de esos ocho metodos, el cliente podria verse afectado aunque nunca lo use. Eso es acoplamiento innecesario.

Martin ilustra ISP con el ejemplo clasico de la impresora multifuncional: una interfaz `Maquina` que tiene `imprimir()`, `escanear()` y `enviar_fax()`. Si un cliente solo necesita imprimir, no deberia verse obligado a conocer la existencia de `escanear()` y `enviar_fax()`.

La solucion es separar `Maquina` en tres interfaces: `Impresora`, `Escaner` y `Fax`. Cada cliente depende solo de lo que necesita. Limpio. Elegante. Correcto.

Y tambien, frecuentemente, innecesario.

### El formulario que pregunta por tus hijos

Usemos la analogia que propone Hector Patricio: un formulario que te pregunta por los datos de tus hijos, independientemente de si tienes hijos o no [Patricio, 2023]. Te estan forzando a cumplir con una interfaz que no usas. Es incomodo, es confuso, y es una mala experiencia de usuario.

Eso es ISP en su mejor version: una guia para disenar interfaces que no molesten a los consumidores con informacion irrelevante.

Pero ahora imagina que el formulario, en vez de tener una sola pagina con campos opcionales, te manda a diez paginas diferentes dependiendo de tu situacion: una para solteros sin hijos, otra para solteros con hijos, otra para casados sin hijos, otra para casados con hijos, otra para divorciados... Cada pagina es "pura" -- solo contiene los campos que te aplican. Pero ahora tienes diez paginas que mantener, diez flujos que probar, y diez variantes que documentar. El formulario original, con los campos opcionales claramente marcados, era mas simple para todos.

Eso es ISP llevado al extremo: la segregacion excesiva.

### La explosion de interfaces

Cuando aplicas ISP con celo excesivo, el resultado predecible es una *explosion de interfaces*. Cada interfaz se rompe en interfaces mas pequenas, que a su vez se rompen en interfaces aun mas pequenas. El sistema termina con docenas de interfaces de un solo metodo, y la complejidad de navegacion se dispara.

Consideremos un ejemplo concreto. El modulo de notificaciones de DevCourses empieza con una interfaz razonable:

```python
class Notificador:
    def enviar_email(self, destinatario, asunto, cuerpo): ...
    def enviar_push(self, dispositivo, mensaje): ...
    def enviar_sms(self, telefono, mensaje): ...
    def enviar_in_app(self, usuario_id, mensaje): ...
```

Un desarrollador entusiasta de ISP observa que no todos los clientes necesitan los cuatro metodos. El modulo de inscripcion solo envia emails. El modulo de alertas solo envia push. Asi que segregamos:

```python
class NotificadorEmail:
    def enviar_email(self, destinatario, asunto, cuerpo): ...

class NotificadorPush:
    def enviar_push(self, dispositivo, mensaje): ...

class NotificadorSMS:
    def enviar_sms(self, telefono, mensaje): ...

class NotificadorInApp:
    def enviar_in_app(self, usuario_id, mensaje): ...
```

Cuatro interfaces en vez de una. Cada cliente depende solo de lo que usa. ISP cumplido.

Pero ahora el modulo de recordatorios, que envia emails *y* push dependiendo de las preferencias del usuario, necesita depender de dos interfaces. El modulo de marketing, que usa los cuatro canales, necesita depender de las cuatro. Y el servicio de notificaciones que implementa todo esto necesita implementar cuatro interfaces separadas, con cuatro archivos, cuatro conjuntos de pruebas, y cuatro puntos de inyeccion.

El codigo que *orquesta* las notificaciones se complica:

```python
class ServicioRecordatorios:
    def __init__(self, email: NotificadorEmail, push: NotificadorPush):
        self._email = email
        self._push = push

    def recordar(self, usuario, evento):
        preferencia = usuario.preferencia_notificacion
        if preferencia == "email":
            self._email.enviar_email(usuario.email, evento.asunto, evento.cuerpo)
        elif preferencia == "push":
            self._push.enviar_push(usuario.dispositivo, evento.mensaje)
```

Antes, con una sola interfaz `Notificador`, este codigo era mas directo:

```python
class ServicioRecordatorios:
    def __init__(self, notificador: Notificador):
        self._notificador = notificador

    def recordar(self, usuario, evento):
        self._notificador.enviar(usuario, evento)
```

La version con ISP agresivo tiene *mas* codigo, *mas* dependencias, y *mas* complejidad. La version simple tiene una sola interfaz, y si el cliente no necesita `enviar_sms()`, simplemente no lo llama. La "dependencia" en un metodo que no usas es un costo teorico; la explosion de interfaces es un costo real, cotidiano.

### La regla de Ousterhout que ISP ignora

John Ousterhout ofrece tres consejos sobre interfaces que frecuentemente entran en tension con ISP:

1. **Mientras mas simple la interfaz, mejor.** Menos interfaces significa menos conceptos que mantener en la cabeza. Cuatro interfaces de un metodo cada una son mas dificiles de navegar que una interfaz de cuatro metodos.

2. **Son mejores los modulos de proposito general.** Un modulo que ofrece cuatro operaciones de notificacion es mas general y reutilizable que cuatro modulos hiper-especializados.

3. **Crear las interfaces pensando en el caso mas comun.** Si el 80% de los clientes usan tres de los cuatro metodos, la interfaz combinada es la correcta. El 20% que solo usa uno puede ignorar los otros [Ousterhout, 2018].

ISP prioriza la *pureza* de la dependencia: que cada cliente dependa solo de lo que usa. Ousterhout prioriza la *simplicidad* del sistema: que el sistema completo tenga la menor cantidad de interfaces posible. Cuando ambos criterios entran en conflicto, la simplicidad suele ganar, porque la pureza de dependencia es un costo que se paga una vez (en el diseno), mientras que la cantidad de interfaces se paga todos los dias (en la navegacion, el testing, y el mantenimiento).

### Cuando ISP si importa

ISP es genuinamente util en exactamente dos escenarios:

**Escenario 1: Interfaces publicas de librerias y frameworks.** Si escribes una libreria que otros van a implementar, y tu interfaz tiene quince metodos, los implementadores que solo necesitan tres van a odiar tu libreria. En este caso, segregar es cortesia hacia tus usuarios. Es la razon por la que Java tiene `Iterable`, `Comparable` y `Serializable` como interfaces separadas en vez de una sola `Objeto` con todo.

**Escenario 2: Interfaces genuinamente ortogonales.** Si tu interfaz agrupa funcionalidades que son *conceptualmente* independientes -- que nunca se necesitan juntas, que son implementadas por sistemas diferentes, que cambian por razones diferentes -- entonces segregar tiene sentido. `Impresora` y `Fax` son conceptos ortogonales; juntarlos en `Maquina` es un error de diseno independiente de ISP.

Pero si tu interfaz agrupa funcionalidades que son variantes del mismo concepto (enviar notificaciones por diferentes canales), la "segregacion" no mejora nada. Solo multiplica los puntos de contacto.

**Takeaway:** ISP es una guia razonable para interfaces publicas de bibliotecas y para separar funcionalidades genuinamente ortogonales. Pero aplicado como regla universal dentro de una aplicacion de negocio, ISP produce mas interfaces de las necesarias, fragmenta conceptos coherentes, y aumenta la carga cognitiva del sistema.

---

## DIP: cuando la inversion de dependencias es innecesaria

### Lo que dice el principio

El Principio de Inversion de Dependencias (DIP) establece dos reglas:

> A. Los modulos de alto nivel no deberian depender de los modulos de bajo nivel. Ambos deben depender de abstracciones.
>
> B. Las abstracciones no deberian depender de los detalles. Los detalles deben depender de las abstracciones.
>
> [Martin, 2000]

La idea es que tu logica de negocio ("alto nivel") no deberia depender directamente de la base de datos, el sistema de archivos, o la API externa ("bajo nivel"). Ambos deberian depender de una abstraccion intermedia -- una interfaz -- que los desacopla.

El patron tipico se ve asi:

```python
# Sin DIP: dependencia directa
class ServicioCursos:
    def __init__(self):
        self._db = PostgresDatabase()  # Acoplado a Postgres

    def listar_cursos(self):
        return self._db.query("SELECT * FROM cursos")


# Con DIP: dependencia invertida
class RepositorioCursos(ABC):
    @abstractmethod
    def listar(self) -> list[Curso]: ...

class RepositorioCursosPostgres(RepositorioCursos):
    def listar(self):
        return self._db.query("SELECT * FROM cursos")

class ServicioCursos:
    def __init__(self, repo: RepositorioCursos):
        self._repo = repo  # Depende de la abstraccion

    def listar_cursos(self):
        return self._repo.listar()
```

Ahora `ServicioCursos` no sabe ni le importa si los datos vienen de Postgres, MongoDB, un archivo JSON, o una API HTTP. Solo sabe que tiene un `RepositorioCursos` que le da cursos. La dependencia esta "invertida": en vez de que el alto nivel dependa del bajo nivel, ambos dependen de una abstraccion.

Limpio. Correcto. Y en la mayoria de las aplicaciones, completamente innecesario.

### La critica de Dan North: miles de millones desperdiciados

Dan North, creador de Behaviour-Driven Development, no se anda con rodeos:

> "Aunque no hay nada fundamentalmente malo con DIP, no creo que sea una exageracion decir que nuestra obsesion con la inversion de dependencias ha causado por si sola miles de millones de dolares en costos irrecuperables durante las ultimas dos decadas." [North, 2021]

La critica de North es precisa y vale la pena examinarla en detalle. Su argumento central es:

> "La mayoria de las dependencias no necesitan invertirse, porque la mayoria de las dependencias no son opciones. Son simplemente la forma en que lo haremos esta vez. Asi que mi sugerencia es escribir codigo simple, centrandose en el uso en lugar de en la reutilizacion." [North, 2021]

Pensemos en esto. En DevCourses, el sistema usa PostgreSQL. Cuantas veces en la vida del proyecto van a cambiar de Postgres a otro motor de base de datos? Probablemente nunca. Y si lo hacen, cuantas veces van a hacerlo? Una. Y cuando lo hagan, cuanto les costara introducir la abstraccion *en ese momento*? Un par de dias, como mucho.

Pero el costo de tener la abstraccion *desde el dia uno* se paga todos los dias:

- Un archivo extra por cada repositorio (la interfaz abstracta).
- Indirreccion al navegar el codigo: `ServicioCursos` -> `RepositorioCursos` (interfaz) -> `RepositorioCursosPostgres` (implementacion). Tres saltos en vez de uno.
- Configuracion de inyeccion de dependencias: alguien tiene que decidir que implementacion se usa y cablearla.
- Pruebas mas complicadas: ahora necesitas mocks para la interfaz, pero los mocks no prueban el comportamiento real de Postgres.

Todo eso para protegerte de un cambio que probablemente nunca suceda.

### El ecosistema de complejidad que DIP genera

DIP no viaja solo. Siempre llega acompanado de un ecosistema de tecnicas y herramientas:

**Inyeccion de Dependencias (DI).** Si tus modulos dependen de abstracciones, alguien tiene que proporcionarles las implementaciones concretas. Eso es la inyeccion de dependencias: pasar las dependencias como parametros al constructor, en vez de crearlas internamente. En principio es simple. En la practica, genera constructores con cinco, diez, quince parametros, y requiere un punto central de "cableado" donde todo se conecta.

**Contenedores de Inversion de Control (IoC).** Cuando el cableado manual se vuelve inmanejable, entran los contenedores de IoC: frameworks que automaticamente resuelven las dependencias. Spring en Java, el contenedor de servicios en .NET, injector en Python. Ahora tienes un framework completo que necesitas aprender, configurar y depurar, solo para conectar clases entre si.

**Service Locator.** Otra variante: en vez de inyectar dependencias, le "pides" a un registro central que te de lo que necesitas. Patron comodo pero que oculta las dependencias, haciendo exactamente lo opuesto de lo que DIP pretendia (hacer las dependencias explicitas).

Lo que empezo como "no dependas directamente de Postgres" se convirtio en un ecosistema de interfaces abstractas, contenedores, configuraciones XML, anotaciones magicas y depuracion de cableado de dependencias. La cura resulto mas costosa que la enfermedad.

### El costo oculto: la perdida de navegabilidad

Uno de los costos mas insidiosos de DIP aplicado universalmente es la perdida de navegabilidad del codigo. Cuando cada clase depende de una interfaz abstracta, y la implementacion concreta se decide en tiempo de ejecucion o en un archivo de configuracion, ya no puedes hacer "Ctrl+Click" y llegar al codigo real. Llegas a la interfaz. Y desde ahi tienes que buscar manualmente que implementacion se esta usando en este contexto.

En un sistema con cincuenta interfaces abstractas, cada una con una sola implementacion, la navegacion del codigo es un ejercicio de frustracion. Sabes que hay una clase `RepositorioCursosPostgres` en algun lugar, pero el IDE te lleva a `RepositorioCursos` (la interfaz vacia) y de ahi tienes que adivinar.

Esto conecta directamente con la definicion de complejidad que establecimos en el capitulo 1: **la complejidad se manifiesta cuando entender o modificar el sistema requiere mas esfuerzo del necesario** [Ousterhout, 2018]. Si navegar tu codigo es mas dificil *con* DIP que *sin* DIP, y la unica ventaja es protegerte de un cambio hipotetico, estas pagando complejidad real por un beneficio imaginario.

### Cuando DIP si importa

Como con los otros principios, DIP tiene un lugar valido. Y ese lugar es mas especifico de lo que la dogma sugiere:

**Escenario 1: Multiples implementaciones concretas.** Si tu sistema realmente se conecta a multiples proveedores del mismo servicio, DIP es la solucion natural. DevCourses acepta pagos con Stripe, MercadoPago y PayPal. Tres proveedores. Tres implementaciones. Una interfaz `ProcesadorPagos` con tres implementaciones concretas. Aqui DIP no es especulativo; es una generalizacion de variaciones reales.

```python
class ProcesadorPagos(ABC):
    @abstractmethod
    def cobrar(self, monto, moneda, token) -> ResultadoPago: ...

class ProcesadorStripe(ProcesadorPagos): ...
class ProcesadorMercadoPago(ProcesadorPagos): ...
class ProcesadorPayPal(ProcesadorPagos): ...
```

**Escenario 2: Limites del sistema.** Cuando tu modulo se conecta a un sistema externo que genuinamente podria cambiar -- una API de terceros que tiene alternativas, un servicio de mensajeria que podria ser reemplazado -- la abstraccion tiene sentido. El limite entre tu sistema y el mundo exterior es el lugar natural para una interfaz.

**Escenario 3: Testing requiere aislamiento real.** Si necesitas probar tu logica de negocio aislada de la base de datos y las pruebas de integracion no son suficientes (por velocidad o por complejidad del setup), una interfaz te permite inyectar un repositorio en memoria. Pero incluso aqui, la tendencia moderna es preferir pruebas de integracion con bases de datos reales (usando containers) sobre mocks de interfaces abstractas.

**Escenario 4: Bibliotecas y frameworks.** Si escribes codigo que otros van a extender, DIP te permite definir puntos de extension claros. Es por eso que los frameworks de aplicaciones usan DIP extensivamente: necesitan que los usuarios provean implementaciones concretas de interfaces predefinidas.

### La heuristica honesta

La regla practica es esta:

- **Tienes dos o mas implementaciones concretas del mismo comportamiento?** Usa DIP. La abstraccion no es especulativa; es una generalizacion de la realidad.
- **Solo tienes una implementacion y no hay evidencia concreta de que habra otra?** No uses DIP. Usa la implementacion directamente. Si algun dia necesitas la abstraccion, introducirla tomara horas, no semanas.
- **No estas seguro?** No uses DIP. Es mas facil agregar una abstraccion cuando la necesitas que remover una que nunca necesitaste.

**Takeaway:** DIP es valioso cuando tienes multiples implementaciones concretas de un mismo comportamiento. Es perjudicial cuando lo aplicas especulativamente a dependencias que nunca van a cambiar. La heuristica de Dan North es la mas productiva: "la mayoria de las dependencias no son opciones. Son simplemente la forma en que lo haremos esta vez."

---

## Lo que realmente necesitas: bajo acoplamiento y alta cohesion

Si los tres principios que acabamos de examinar son sobrevaluados, que es lo que realmente importa para el diseno del dia a dia?

La respuesta no es nueva. Larry Constantine y Edward Yourdon la articularon en 1974, antes de que existieran Java, Python, o incluso C++:

> "A mayor cohesion de los modulos individuales en el sistema, menor sera el acoplamiento." [Constantine y Yourdon, 1979]

Esta frase contiene mas sabiduria practica sobre diseno de software que los cinco principios SOLID combinados. Y la razón es que no es una heuristica ambigua: es un criterio medible. Puedes contar las dependencias entre modulos (acoplamiento). Puedes evaluar si los elementos de un modulo trabajan hacia el mismo objetivo (cohesion). Son propiedades observables, no juicios subjetivos.

Consideremos como los tres principios que analizamos se reducen a cohesion y acoplamiento:

- **LSP** dice: los subtipos deben respetar el contrato del tipo padre. *Traduccion en terminos de acoplamiento:* si los consumidores estan acoplados a un contrato, no rompas ese contrato. Es una regla de estabilidad de interfaces, que es simplemente otra forma de decir "minimiza el acoplamiento".

- **ISP** dice: los clientes no deberian depender de lo que no usan. *Traduccion en terminos de acoplamiento:* reduce el acoplamiento innecesario. Pero ISP no te da el criterio para decidir *cuanto* segregar. Cohesion si: si los metodos de una interfaz operan sobre el mismo concepto y se usan juntos frecuentemente, mantenerlos juntos es alta cohesion.

- **DIP** dice: depende de abstracciones, no de implementaciones. *Traduccion en terminos de acoplamiento:* reduce el acoplamiento entre modulos de diferentes niveles de abstraccion. Pero DIP no te dice *cuando* ese acoplamiento es un problema real. Acoplamiento y cohesion si: si cambiar la implementacion concreta no afecta a ningun otro modulo (porque la interfaz es estable), el acoplamiento ya es bajo. No necesitas una capa de abstraccion adicional.

Los tres principios son casos particulares de una idea mas general. Y la idea general -- bajo acoplamiento, alta cohesion -- es mas facil de aplicar porque no requiere juzgar "responsabilidades" ambiguas o decidir si una dependencia es "de alto nivel" o "de bajo nivel". Solo requiere dos preguntas:

1. **Las cosas que estan juntas, pertenecen juntas?** (Cohesion)
2. **Las cosas que estan separadas, dependen lo menos posible entre si?** (Acoplamiento)

Si la respuesta a ambas es si, tu diseno es bueno. Independientemente de cuantos principios SOLID "viole".

En el proximo capitulo profundizaremos en cohesion y acoplamiento como los verdaderos pilares del diseno de software. Pero quiero dejar clara la conexion: no estamos abandonando SOLID. Estamos reconociendo que SOLID es una expresion incompleta de principios mas fundamentales, y que esos principios fundamentales son mas utiles en la practica diaria.

**Takeaway:** LSP, ISP y DIP son casos particulares de "bajo acoplamiento y alta cohesion". Si dominas los fundamentos, los tres principios se vuelven intuitivos. Si solo memorizas los principios sin entender los fundamentos, aplicas reglas sin criterio.

---

## Cuando SI usar cada principio: la guia honesta

Terminemos con algo que rara vez aparece en los libros: una guia honesta de cuando cada principio vale la pena y cuando no.

### LSP: guia de uso

| Situacion | Usa LSP? | Por que |
|---|---|---|
| Escribes una libreria o framework que otros van a extender | Si | Los usuarios necesitan poder implementar tus interfaces sin sorpresas |
| Disenas una jerarquia de tipos que sera heredada | Si | Los subtipos deben respetar los invariantes del tipo padre |
| Escribes una aplicacion de negocio sin herencia | No | LSP no aplica cuando no hay subtipos |
| Usas composicion en vez de herencia | Rara vez | La composicion elimina la mayoria de los problemas que LSP resuelve |
| Tu lenguaje no tiene tipos o herencia (Python duck typing) | Indirectamente | El principio se reduce a "respeta los contratos implicitos" |

### ISP: guia de uso

| Situacion | Usa ISP? | Por que |
|---|---|---|
| Una interfaz agrupa funcionalidades genuinamente ortogonales | Si | Segregar reduce acoplamiento real |
| Escribes una interfaz publica para una libreria | Si | Los implementadores no deberian verse forzados a implementar metodos irrelevantes |
| Los metodos de tu interfaz operan sobre el mismo concepto | No | Segregar un concepto coherente es fragmentacion, no mejora |
| Solo tienes un par de clientes y ambos usan casi toda la interfaz | No | El costo de la segregacion supera el beneficio |
| Te preocupa que un cliente "dependa" de un metodo que no llama | No | Esa dependencia es teorica; la explosion de interfaces es practica |

### DIP: guia de uso

| Situacion | Usa DIP? | Por que |
|---|---|---|
| Tienes dos o mas implementaciones concretas | Si | La abstraccion generaliza variaciones reales |
| Tu modulo se conecta a APIs externas que podrian cambiar | Si | El limite del sistema es el lugar natural para interfaces |
| Escribes una libreria o framework | Si | Los usuarios necesitan puntos de extension |
| Solo tienes una implementacion y no hay evidencia de otra | No | La abstraccion es especulativa |
| Quieres "facilitar el testing" pero podrias usar pruebas de integracion | Probablemente no | Las pruebas de integracion con datos reales son mas confiables que mocks |
| "Por si acaso necesitamos cambiar la base de datos" | No | YAGNI (You Aren't Gonna Need It) |

### La regla unificadora

Si tuviera que condensar la guia en una sola oracion, seria esta:

**Aplica estos principios cuando tengas evidencia concreta del problema que resuelven. No los apliques como proteccion contra problemas hipoteticos.**

La evidencia concreta es: ya tienes dos implementaciones (DIP). Ya tienes clientes que solo usan la mitad de tu interfaz (ISP). Ya tienes subtipos que rompen invariantes (LSP). Sin evidencia, la aplicacion preventiva de estos principios es como tomar antibioticos por si acaso te enfermas: el costo de los efectos secundarios supera el beneficio de la prevencion.

**Takeaway:** Los tres principios tienen un lugar valido. Ese lugar es mas estrecho de lo que la industria sugiere. La guia honesta es: aplica cuando veas el problema. No apliques para prevenirlo.

---

## Proyecto guia: evaluando DevCourses con los tres principios

DevCourses ha crecido a lo largo de los ultimos capitulos. Tenemos siete modulos definidos, un sistema de inscripcion bien disenado, y una estructura de catalogo reorganizada. Evaluemos el sistema actual bajo la lente de LSP, ISP y DIP, con honestidad.

### Evaluacion de LSP

Recorremos los puntos donde DevCourses tiene jerarquias de tipos:

**Tipos de contenido:** DevCourses tiene `CursoVideo`, `CursoTexto` y `CursoInteractivo`. Los tres implementan la interfaz `Contenido` con metodos `obtener_metadata()`, `iniciar()` y `marcar_completado()`. Un `CursoInteractivo` marca como completado solo cuando el usuario pasa el quiz final. Los otros dos marcan como completado cuando el usuario llega al final del contenido.

Pregunta: viola esto LSP? No. La interfaz `Contenido` no especifica *cuando* se marca como completado. Solo dice que `marcar_completado()` cambia el estado del contenido a completado. Las condiciones para llamar a `marcar_completado()` son responsabilidad del modulo de progreso, no del tipo de contenido. El contrato se respeta.

**Tipos de suscripcion:** DevCourses tiene `SuscripcionMensual`, `SuscripcionAnual` y `SuscripcionCorporativa`. Las tres implementan `Suscripcion` con `es_activa()`, `renovar()` y `cancelar()`. La `SuscripcionCorporativa` no puede ser cancelada por el usuario individual; solo por el administrador de la cuenta. Si un modulo intenta `suscripcion.cancelar()` en una suscripcion corporativa, lanza una excepcion.

Pregunta: viola esto LSP? Si. El codigo que usa `Suscripcion` espera poder llamar `cancelar()` sin excepciones. La suscripcion corporativa rompe esa expectativa.

Solucion: la interfaz deberia tener `puede_cancelar() -> bool`, y `cancelar()` deberia tener como precondicion que `puede_cancelar()` sea verdadero. O mejor aun: `cancelar()` deberia retornar un `ResultadoCancelacion` que indique exito o fallo con razon. Asi el contrato es claro y ningun subtipo lo viola.

```python
class Suscripcion(ABC):
    @abstractmethod
    def cancelar(self) -> ResultadoCancelacion:
        """Intenta cancelar. Retorna exito o fallo con razon."""
        ...
```

Este es un caso legitimo donde LSP senala un problema real. Nota que solo lo encontramos porque buscamos activamente: en el dia a dia, este bug habria aparecido en la primera prueba de integracion.

### Evaluacion de ISP

La interfaz del `Notificador` en DevCourses tiene cuatro metodos: `enviar_email`, `enviar_push`, `enviar_sms`, `enviar_in_app`. Deberiamos segregarla?

Analicemos los clientes:
- `ServicioInscripcion`: usa `enviar_email`.
- `ServicioAlertas`: usa `enviar_push` y `enviar_in_app`.
- `ServicioMarketing`: usa los cuatro.
- `ServicioRecordatorios`: usa `enviar_email` y `enviar_push`.

Tres de cuatro clientes usan mas de un metodo. El unico que usa solo uno es `ServicioInscripcion`, y eso podria cambiar (enviar push de confirmacion ademas de email).

Decision: no segregar. La interfaz es cohesiva -- todos los metodos son variantes de "enviar notificacion" -- y la mayoria de los clientes usan multiples metodos. La "dependencia" de `ServicioInscripcion` en los metodos de push y SMS es una dependencia que existe en la firma pero no en el codigo. El costo de mantener cuatro interfaces separadas supera el beneficio de eliminar esa dependencia nominal.

Una mejor solucion, si queremos limpiar la interfaz, es hacerla mas general:

```python
class Notificador:
    def enviar(self, destinatario: Destinatario,
               mensaje: Mensaje,
               canal: Canal = Canal.DEFAULT) -> ResultadoEnvio:
        ...
```

Un metodo. Un concepto. Menos interfaz. Modulo mas profundo. Esto no es ISP; es simplicidad.

### Evaluacion de DIP

DevCourses tiene las siguientes dependencias concretas:

| Modulo | Dependencia | Hay alternativa real? |
|---|---|---|
| Catalogo | PostgreSQL | No |
| Video | Amazon S3 | No (contrato de 3 anos) |
| Pagos | Stripe, MercadoPago, PayPal | Si, tres implementaciones |
| Notificaciones | SendGrid (email), Firebase (push) | Posiblemente |
| Usuarios | PostgreSQL | No |
| Comentarios | PostgreSQL | No |
| Instructor | PostgreSQL | No |

Solo el modulo de pagos tiene multiples implementaciones reales. Ahi DIP esta justificado y ya lo implementamos.

Para notificaciones, hay una posibilidad razonable de cambiar de proveedor (de SendGrid a Mailgun, de Firebase a OneSignal). Una interfaz aqui tiene sentido, pero no por DIP como dogma, sino porque estamos en el limite del sistema: la conexion con un servicio externo que concretamente tiene alternativas.

Para el catalogo, video, usuarios, comentarios e instructor, todos usan PostgreSQL. Crear interfaces abstractas `RepositorioCatalogo`, `RepositorioUsuarios`, `RepositorioComentarios` con una sola implementacion cada una seria puro teatro. DevCourses no va a migrar de Postgres a MongoDB modulo por modulo. Si cambian de base de datos (cosa improbable), sera una migracion de todo el sistema, y la abstraccion del repositorio no les ahorrara trabajo: tendran que reescribir todas las consultas de todas formas.

Decision: DIP solo en pagos y notificaciones. El resto usa PostgreSQL directamente. Si algun dia necesitamos una abstraccion, la introducimos en ese momento.

**Takeaway:** Evaluar DevCourses con los tres principios produce resultados honestos: LSP revelo un bug genuino en las suscripciones (lo cual es valioso), ISP no aporta nada que la simplicidad no logre mejor, y DIP se justifica solo en los limites del sistema donde hay proveedores alternativos reales.

---

## Aplica esto el lunes

1. Busca en tu proyecto una interfaz abstracta que tenga una sola implementacion. Preguntate: hay evidencia concreta de que habra una segunda implementacion en los proximos seis meses? Si la respuesta es no, considera eliminar la interfaz y usar la implementacion directamente. Puedes reintroducir la abstraccion cuando la necesites.

2. Cuenta las interfaces en tu modulo mas complejo. Si hay mas interfaces que implementaciones, tienes un caso de sobre-segregacion. Identifica que interfaces podrias unir sin perder claridad. Recuerda: menos interfaces significa menos complejidad de navegacion.

3. Revisa un caso de inversion de dependencias en tu proyecto. Responde honestamente: cuantas implementaciones tiene esa abstraccion? Si la respuesta es "una", calcula cuanto tiempo se tarda en introducir la abstraccion *cuando* se necesite una segunda implementacion. Si la respuesta es "un par de horas", la abstraccion es prematura.

4. Para tu siguiente diseno, en vez de preguntar "es SOLID?", pregunta: "los modulos son cohesivos?" (lo que esta junto, pertenece junto) y "el acoplamiento es bajo?" (los modulos dependen lo menos posible entre si). Esas dos preguntas te van a dar mejor orientacion que los cinco principios SOLID.

---

## Referencias del capitulo

- Constantine, L. y Yourdon, E. (1979). *Structured Design*. Prentice-Hall.
- Liskov, B. y Wing, J. (1994). "A Behavioral Notion of Subtyping." *ACM Transactions on Programming Languages and Systems*, 16(6), pp. 1811-1841.
- Martin, R. C. (2000). "Design Principles and Design Patterns."
- North, D. (2021). "CUPID -- the back story." *dannorth.net*.
- North, D. (2022). "CUPID -- for joyful coding." *dannorth.net*.
- Ousterhout, J. (2018). *A Philosophy of Software Design*. Yaknyam Press.
- Patricio, H. (2023). "El principio de segregacion de interfaces." *The Dojo MX Blog*.
- Patricio, H. (2023). "El principio de inversion de dependencias." *The Dojo MX Blog*.
