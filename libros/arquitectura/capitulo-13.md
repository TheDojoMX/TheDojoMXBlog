# Capitulo 13: Patrones de diseno -- cuando usarlos y cuando son una trampa

> "Los patrones son vocabulario, no objetivos."

---

## La confusion que arruina proyectos

Hay una escena que se repite en equipos de desarrollo de todo el mundo. Un programador recien salido de leer *Design Patterns* llega al proyecto con los ojos brillantes y anuncia: "Voy a refactorizar el modulo de pagos usando el patron Abstract Factory combinado con un Strategy y un Observer." El equipo lo mira con una mezcla de respeto y confusion. Dos semanas despues, el modulo de pagos tiene el triple de archivos, nadie entiende la nueva estructura, y agregar un simple descuento requiere modificar seis clases.

Este escenario no es una caricatura. Es una de las trampas mas comunes del desarrollo profesional de software: confundir el conocimiento de patrones con la obligacion de usarlos. Los patrones de diseno son herramientas poderosas cuando se aplican en el momento correcto. Pero cuando se aplican por inercia, por ego intelectual o por la presion de parecer sofisticado, se convierten en la fuente misma de la complejidad que pretendian resolver.

En este capitulo vamos a tomar los patrones de diseno en serio -- no como recetas que se siguen ciegamente, sino como vocabulario que nos permite comunicar soluciones y como herramientas que se aplican bajo criterios concretos. Veremos de donde vienen, cuales son los que mas te van a servir en la practica, y sobre todo, cuando un patron es sobreingenieria pura.

**Takeaway:** Los patrones de diseno son un lenguaje comun para describir soluciones probadas. Su valor esta en la comunicacion y en resolver problemas reales, no en la acumulacion de capas de abstraccion.

---

## De la arquitectura de edificios a la arquitectura de software

Para entender los patrones de diseno hay que entender su origen, porque el origen explica tanto su poder como sus limitaciones.

En 1977, el arquitecto Christopher Alexander publico *A Pattern Language: Towns, Buildings, Construction*, un libro que identificaba 253 patrones para disenar espacios habitables [Alexander, 1977]. La idea era revolucionaria: Alexander observo que ciertos problemas de diseno aparecian una y otra vez -- como orientar una ventana para aprovechar la luz natural, como crear un espacio comunitario que invite a la interaccion, como conectar una casa con el jardin. Para cada problema recurrente, documento una solucion que habia demostrado funcionar en multiples contextos.

Lo brillante de Alexander no fueron las soluciones individuales, sino la idea de que estas soluciones forman un *lenguaje*. Asi como las palabras de un idioma se combinan para formar oraciones, los patrones se combinan para formar disenos completos. Y asi como conocer el vocabulario de un idioma te permite comunicarte con otros hablantes, conocer los patrones te permite comunicarte con otros disenadores sin tener que explicar cada solucion desde cero.

Diez anos despues de la publicacion de Alexander, Kent Beck y Ward Cunningham presentaron en la conferencia OOPSLA de 1987 los resultados de un experimento: habian aplicado la idea de patrones al diseno de software, y funcionaba [Beck y Cunningham, 1987]. Los problemas recurrentes en el software -- como crear objetos sin acoplarse a clases concretas, como recorrer una coleccion sin exponer su estructura interna, como notificar a multiples componentes de un cambio -- tambien podian capturarse como patrones con nombre, problema, solucion y consecuencias.

La idea germino durante anos. En 1993, Grady Booch y Kent Beck reunieron a varios pioneros de la orientacion a objetos en una cabana en las montanas de Colorado. Uno de los temas centrales fue la fusion de las ideas de Alexander con el trabajo que Erich Gamma venia haciendo sobre patrones para software. De esa reunion surgio el impulso definitivo.

En 1994, Erich Gamma, Richard Helm, Ralph Johnson y John Vlissides -- conocidos como la "Banda de los Cuatro" o Gang of Four (GoF) -- publicaron *Design Patterns: Elements of Reusable Object-Oriented Software* [Gamma et al., 1994]. El libro documenta 23 patrones divididos en tres categorias:

1. **Creacionales:** Como crear objetos (Factory Method, Abstract Factory, Singleton, Builder, Prototype).
2. **Estructurales:** Como componer objetos y clases (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy).
3. **De comportamiento:** Como se comunican y distribuyen responsabilidades entre objetos (Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor).

El libro se convirtio en un clasico inmediato. Treinta anos despues, sigue siendo una referencia fundamental. Pero tambien genero un efecto secundario que Alexander probablemente no habria aprobado: una generacion de programadores que trataron los 23 patrones como mandamientos sagrados en lugar de como vocabulario.

### Lo que Alexander realmente queria

Hay un detalle historico que la mayoria de los desarrolladores desconoce. En 1996, Christopher Alexander fue invitado a dar el discurso inaugural en la conferencia OOPSLA. Ante una audiencia de miles de programadores que habian adoptado su idea de patrones, Alexander expreso una preocupacion: que la comunidad de software habia tomado la forma superficial de su trabajo -- catalogos de soluciones -- sin captar la esencia profunda [Alexander, 1996].

Para Alexander, los patrones no eran un catalogo para impresionar a colegas ni una lista de verificacion para marcar en revisiones de codigo. Eran una forma de pensar sobre problemas recurrentes, una herramienta para *generar* buenas soluciones, no para *imponer* soluciones predeterminadas. La diferencia es sutil pero crucial: un patron te dice "cuando enfrentes este tipo de problema, esta clase de solucion tiende a funcionar". No te dice "usa esta solucion siempre que puedas".

Esa distincion -- entre patron como generador y patron como receta -- es exactamente la que separa a los desarrolladores que usan patrones con sabiduria de los que caen en la trampa de la sobreingenieria.

---

## Cinco patrones que realmente vas a usar

De los 23 patrones del GoF y los cientos de patrones documentados desde entonces, la realidad practica es que un desarrollador profesional usa regularmente un punado de ellos. No cinco exactos, por supuesto -- depende del dominio, del lenguaje, del tipo de sistema. Pero hay un nucleo de patrones que aparece con tanta frecuencia que vale la pena conocerlos en profundidad.

Los criterios para esta seleccion son tres:

1. **Frecuencia de aparicion:** Se encuentran en la mayoria de las aplicaciones de negocio.
2. **Retorno sobre la inversion:** El beneficio que aportan supera consistentemente el costo de implementarlos.
3. **Independencia del paradigma:** Funcionan tanto en orientacion a objetos como en programacion funcional, aunque cambien de forma.

### 1. Strategy: comportamiento intercambiable

Ya lo vimos en el capitulo 12 cuando refactorizamos el calculo de precios en DevCourses. El patron Strategy encapsula una familia de algoritmos detras de una interfaz comun, permitiendo que el algoritmo cambie sin que el codigo que lo usa se entere.

```python
# La interfaz (el contrato)
class OrdenadorCursos(ABC):
    @abstractmethod
    def ordenar(self, cursos: list[Curso]) -> list[Curso]: ...

# Las estrategias concretas
class OrdenarPorPopularidad(OrdenadorCursos):
    def ordenar(self, cursos: list[Curso]) -> list[Curso]:
        return sorted(cursos, key=lambda c: c.inscripciones, reverse=True)

class OrdenarPorFecha(OrdenadorCursos):
    def ordenar(self, cursos: list[Curso]) -> list[Curso]:
        return sorted(cursos, key=lambda c: c.fecha_publicacion, reverse=True)

class OrdenarPorRelevancia(OrdenadorCursos):
    def __init__(self, perfil_usuario: PerfilUsuario):
        self._perfil = perfil_usuario

    def ordenar(self, cursos: list[Curso]) -> list[Curso]:
        return sorted(cursos, key=lambda c: self._calcular_relevancia(c))

    def _calcular_relevancia(self, curso: Curso) -> float:
        # Logica compleja basada en el perfil del usuario
        ...

# El consumidor no sabe que estrategia se usa
class CatalogoCursos:
    def __init__(self, ordenador: OrdenadorCursos):
        self._ordenador = ordenador

    def listar(self) -> list[Curso]:
        cursos = self._repo.obtener_todos()
        return self._ordenador.ordenar(cursos)
```

**Cuando usarlo:** Cuando tienes multiples formas de hacer lo mismo y la forma de hacerlo puede cambiar en tiempo de ejecucion o entre contextos diferentes.

**Cuando NO usarlo:** Cuando solo hay una forma de hacer algo y no hay evidencia de que vaya a haber otra. En ese caso, Strategy es una capa de indirreccion innecesaria.

**En lenguajes funcionales:** Strategy es simplemente una funcion que se pasa como argumento. No necesitas clases ni interfaces -- una funcion de orden superior hace exactamente lo mismo con menos ceremonia.

### 2. Observer: reaccionar sin acoplarse

El patron Observer permite que un componente notifique a otros de un evento sin conocerlos directamente. Es la base de los sistemas de eventos, las suscripciones y la programacion reactiva.

```python
class EventBus:
    def __init__(self):
        self._suscriptores: dict[str, list[Callable]] = {}

    def suscribir(self, evento: str, callback: Callable):
        if evento not in self._suscriptores:
            self._suscriptores[evento] = []
        self._suscriptores[evento].append(callback)

    def publicar(self, evento: str, datos: dict):
        for callback in self._suscriptores.get(evento, []):
            callback(datos)

# En DevCourses: cuando un usuario se inscribe,
# multiples sistemas reaccionan sin conocerse entre si
bus = EventBus()
bus.suscribir("inscripcion_completada", enviar_email_bienvenida)
bus.suscribir("inscripcion_completada", actualizar_contador_curso)
bus.suscribir("inscripcion_completada", registrar_analytics)
bus.suscribir("inscripcion_completada", notificar_instructor)

# El servicio de inscripcion solo publica el evento
class ServicioInscripcion:
    def __init__(self, repo, bus: EventBus):
        self._repo = repo
        self._bus = bus

    def inscribir(self, usuario_id: int, curso_id: int):
        inscripcion = Inscripcion(usuario_id, curso_id)
        self._repo.guardar(inscripcion)
        self._bus.publicar("inscripcion_completada", {
            "usuario_id": usuario_id,
            "curso_id": curso_id
        })
        return inscripcion
```

**Cuando usarlo:** Cuando un evento en un componente debe desencadenar acciones en multiples componentes que no deberian conocerse entre si. Es ideal para notificaciones, logging, analytics y cualquier efecto secundario que no sea parte de la logica central.

**Cuando NO usarlo:** Cuando la accion es una consecuencia directa e inmediata que forma parte de la misma operacion logica. Si despues de guardar un pago *siempre* debes generar una factura y *nunca* puede haber pago sin factura, esa relacion es lo suficientemente fuerte como para ser una llamada directa, no un evento.

### 3. Adapter: traducir entre mundos

El patron Adapter traduce la interfaz de un componente para que sea compatible con lo que otro componente espera. Es un traductor entre dos mundos que hablan idiomas diferentes.

```python
# El API externo de Stripe tiene su propia interfaz
class StripeClient:
    def create_charge(self, amount_cents: int, currency: str, source: str):
        ...

# El API externo de MercadoPago tiene otra interfaz diferente
class MercadoPagoClient:
    def crear_preferencia(self, monto: float, moneda: str, metodo: str):
        ...

# Nuestra interfaz interna (lo que DevCourses espera)
class ProcesadorPago(ABC):
    @abstractmethod
    def cobrar(self, monto: Decimal, moneda: str) -> ResultadoPago: ...

# Adaptadores: traducen de nuestra interfaz a la interfaz externa
class AdaptadorStripe(ProcesadorPago):
    def __init__(self, cliente: StripeClient, source: str):
        self._cliente = cliente
        self._source = source

    def cobrar(self, monto: Decimal, moneda: str) -> ResultadoPago:
        centavos = int(monto * 100)
        resultado = self._cliente.create_charge(centavos, moneda, self._source)
        return ResultadoPago(exito=resultado.paid, referencia=resultado.id)

class AdaptadorMercadoPago(ProcesadorPago):
    def __init__(self, cliente: MercadoPagoClient, metodo: str):
        self._cliente = cliente
        self._metodo = metodo

    def cobrar(self, monto: Decimal, moneda: str) -> ResultadoPago:
        resultado = self._cliente.crear_preferencia(float(monto), moneda, self._metodo)
        return ResultadoPago(exito=resultado.status == "approved", referencia=resultado.id)
```

**Cuando usarlo:** Cuando integras un componente externo cuya interfaz no controlas y quieres aislar al resto de tu sistema de esa interfaz ajena. Es el patron por excelencia para integraciones con APIs de terceros, bibliotecas legacy, y sistemas heredados.

**Cuando NO usarlo:** Cuando la interfaz externa es suficientemente simple y estable como para usarla directamente. Adaptar por adaptar anade una capa de indirreccion que no paga su costo.

### 4. Facade: simplicidad sobre complejidad

El patron Facade proporciona una interfaz simple a un subsistema complejo. Es exactamente el concepto de modulo profundo que discutimos en el capitulo 5: mucha funcionalidad detras de poca interfaz.

```python
# El subsistema de inscripcion en DevCourses es complejo internamente
class FachadaInscripcion:
    def __init__(
        self,
        repo_cursos: RepositorioCursos,
        repo_usuarios: RepositorioUsuarios,
        procesador_pago: ProcesadorPago,
        verificador_cupo: VerificadorCupo,
        generador_acceso: GeneradorAcceso,
        notificador: Notificador
    ):
        self._cursos = repo_cursos
        self._usuarios = repo_usuarios
        self._pagos = procesador_pago
        self._cupo = verificador_cupo
        self._acceso = generador_acceso
        self._notificador = notificador

    def inscribir(self, usuario_id: int, curso_id: int) -> Inscripcion:
        """Un solo metodo que orquesta toda la complejidad interna."""
        curso = self._cursos.obtener(curso_id)
        usuario = self._usuarios.obtener(usuario_id)
        self._cupo.verificar(curso)
        pago = self._pagos.cobrar(curso.precio, curso.moneda)
        acceso = self._acceso.crear(usuario, curso)
        self._notificador.enviar(usuario, f"Bienvenido a {curso.titulo}")
        return Inscripcion(usuario_id, curso_id, pago.referencia, acceso.token)
```

El controlador HTTP no necesita saber nada de verificacion de cupo, procesamiento de pago, generacion de acceso ni notificaciones. Solo llama a `fachada.inscribir(usuario_id, curso_id)` y obtiene un resultado.

**Cuando usarlo:** Cuando un proceso involucra multiples pasos y multiples componentes, y los consumidores del proceso no necesitan conocer esos detalles.

**Cuando NO usarlo:** Cuando la fachada se convierte en una clase dios que hace demasiado. Si tu fachada tiene quince dependencias y diez metodos publicos, probablemente necesites descomponerla en fachadas mas pequenas.

### 5. Factory: crear sin acoplarse

Los patrones de creacion (Factory Method, Abstract Factory) encapsulan la logica de creacion de objetos, permitiendo que el codigo que usa los objetos no sepa como se construyen.

```python
class NotificadorFactory:
    @staticmethod
    def crear(tipo: str, config: dict) -> Notificador:
        canales = {
            "email": lambda: CanalEmail(SMTPClient(config["smtp_host"])),
            "push": lambda: CanalPush(FirebaseClient(config["firebase_key"])),
            "sms": lambda: CanalSMS(TwilioClient(config["twilio_sid"])),
        }

        formateadores = {
            "plano": lambda: FormateadorPlano(),
            "template": lambda: FormateadorTemplate(config.get("template", "")),
        }

        canal = canales.get(tipo)
        if not canal:
            raise ValueError(f"Tipo de notificacion desconocido: {tipo}")

        formateador = formateadores.get(config.get("formato", "plano"))
        return Notificador(canal(), formateador())

# Uso: el consumidor no sabe como se construye
notificador = NotificadorFactory.crear("email", {
    "smtp_host": "smtp.devcourses.com",
    "formato": "template",
    "template": "Hola {nombre}, bienvenido a {curso}."
})
```

**Cuando usarlo:** Cuando la creacion de un objeto requiere logica compleja, multiples pasos, o la decision de que tipo concreto crear depende de configuracion o contexto.

**Cuando NO usarlo:** Cuando la creacion es simple y directa. Si crear un objeto es `MiObjeto(parametro)`, una factory es burocracia innecesaria.

---

## Cuando un patron es sobreingenieria

Aqui llegamos al corazon del capitulo. Porque si los patrones son herramientas tan utiles, por que tantos proyectos sufren por su uso excesivo?

La respuesta esta en una confusion fundamental: **los patrones son vocabulario, no objetivos**. Aprender los 23 patrones del GoF no significa que tu codigo deba contener los 23. Asi como conocer la palabra "antidisestablecimientarianismo" no te obliga a usarla en cada conversacion.

### Las tres senales de la sobreingenieria por patrones

**1. El patron resuelve un problema que no tienes.**

Esta es la senal mas comun. Introduces un Abstract Factory porque "quiza en el futuro necesitemos crear familias de objetos". Introduces un Observer porque "quiza algun dia necesitemos desacoplar este evento". Introduces un Strategy porque "quiza la logica de calculo cambie".

La palabra clave es "quiza". Los patrones deben resolver problemas presentes, no problemas hipoteticos. Cuando introduces un patron para un problema futuro que no esta respaldado por evidencia concreta, estas pagando un costo real de complejidad hoy para resolver un beneficio especulativo manana.

John Ousterhout es directo al respecto: "Disenar para el caso general desde el principio puede funcionar si las extensiones futuras son predecibles, pero tambien puede llevar a sobreingenieria si esas extensiones nunca se materializan" [Ousterhout, 2018].

**2. El patron anade mas complejidad de la que resuelve.**

Un patron debe *reducir* la complejidad neta del sistema. Si despues de aplicarlo tienes mas archivos, mas interfaces, mas niveles de indirreccion, y la unica ventaja es que "ahora sigue el patron Strategy", algo anda mal.

La prueba es simple: toma a un nuevo miembro del equipo. Muestrale el codigo con el patron y el codigo sin el. Si el codigo sin el patron es mas facil de entender y modificar, el patron no se justifica.

Peter Norvig hizo una observacion demoledora al respecto: en su presentacion de 1996, demostro que 16 de los 23 patrones del GoF se vuelven "invisibles o mas simples" en lenguajes con funciones de primera clase, closures y metaprogramacion [Norvig, 1996]. Los patrones que eran necesarios en C++ como workarounds por las limitaciones del lenguaje resultaban innecesarios en Lisp, Dylan, y por extension, en Python, Ruby o JavaScript.

Esto no significa que los patrones sean inutiles en lenguajes dinamicos. Significa que a veces la solucion mas simple -- una funcion que se pasa como argumento, un closure, un diccionario -- es mejor que la solucion ceremoniosa de clases, interfaces y fabricas.

**3. El patron existe para satisfacer una regla, no una necesidad.**

"Todo acceso a datos debe pasar por un repositorio." "Toda logica de negocio debe estar en un servicio." "Toda creacion de objetos debe usar una factory." Estas reglas suenan razonables en abstracto, pero cuando se aplican sin discriminacion, producen exactamente las capas transparentes que criticamos en el capitulo 11.

Si tu repositorio solo ejecuta `db.query("SELECT * FROM cursos")` y tu servicio solo llama a `self.repo.listar()`, no tienes un patron bien aplicado. Tienes burocracia arquitectonica.

### El costo real de la sobreingenieria

La sobreingenieria por patrones tiene costos concretos que a menudo se subestiman:

- **Carga cognitiva multiplicada.** Cada capa de indirreccion es una capa mas que el desarrollador debe recorrer mentalmente. Cada interfaz abstracta es un nivel mas de "salto" al leer el codigo. Como discutimos en el capitulo 1, la carga cognitiva es el sintoma mas pernicioso de la complejidad.

- **Tiempo de navegacion aumentado.** En un proyecto sobredisenado, encontrar donde realmente se ejecuta la logica puede requerir seguir una cadena de delegaciones que pasa por una interfaz, una factory, un adaptador, un servicio y finalmente llega al codigo que hace algo util. Ese tiempo de navegacion se paga cada vez que alguien necesita modificar o depurar el sistema.

- **Rigidez paradojica.** La ironia suprema: los patrones que se introdujeron para hacer el sistema mas flexible pueden hacerlo mas rigido. Si para agregar un nuevo tipo de descuento necesitas crear una nueva clase que implemente una interfaz, registrarla en una factory, configurarla en el contenedor de inyeccion de dependencias y escribir tests para cada capa, tienes un sistema que es teoricamente extensible pero practicamente inflexible.

- **Onboarding mas lento.** Un desarrollador nuevo que llega a un proyecto con patrones bien aplicados puede aprender el vocabulario y orientarse rapidamente. Un desarrollador nuevo que llega a un proyecto *sobredisenado* se ahoga en capas de abstraccion antes de entender que hace realmente el sistema.

---

## Anti-patron: Pattern-itis

Existe un anti-patron tan comun que merece su propio nombre: la *Pattern-itis*. Es la enfermedad del desarrollador que, habiendo aprendido patrones de diseno, los ve en todas partes y siente la compulsion de aplicarlos en cada oportunidad.

La Pattern-itis tiene una progresion tipica:

**Fase 1: El descubrimiento.** El desarrollador lee el libro del GoF o un tutorial de patrones. Siente una revelacion. De repente, el codigo que escribia antes le parece primitivo e indigno. Ahora *entiende* como deberia ser el diseno de software.

**Fase 2: La euforia.** Todo problema es un clavo y el martillo es un patron. El formulario de registro necesita un Builder. El sistema de permisos necesita un Chain of Responsibility. El logger necesita un Singleton. La lista de cursos necesita un Iterator personalizado (a pesar de que el lenguaje ya tiene uno integrado).

**Fase 3: La complejidad.** El proyecto empieza a acumular capas. Las revisiones de codigo se convierten en debates sobre que patron usar. Los tiempos de implementacion se alargan. Los bugs se vuelven mas dificiles de rastrear porque la logica esta dispersa en multiples capas de indirreccion.

**Fase 4: La reflexion (o no).** El mejor escenario es que el desarrollador reconoce que se excedio y empieza a simplificar. El peor escenario es que culpa al equipo de "no entender los patrones" y anade mas capas para "resolver" los problemas que las capas anteriores causaron.

### Como se ve la Pattern-itis en el codigo

Un ejemplo real. Supongamos que DevCourses necesita una funcion para verificar si un usuario puede ver un curso. Con Pattern-itis, el codigo podria verse asi:

```python
# Interfaz del verificador
class VerificadorAcceso(ABC):
    @abstractmethod
    def verificar(self, context: ContextoVerificacion) -> ResultadoVerificacion: ...

# Contexto (DTO)
@dataclass
class ContextoVerificacion:
    usuario_id: int
    curso_id: int
    timestamp: datetime

# Resultado (DTO)
@dataclass
class ResultadoVerificacion:
    permitido: bool
    razon: str = ""

# Implementacion concreta
class VerificadorAccesoInscripcion(VerificadorAcceso):
    def __init__(self, repo: RepositorioInscripciones):
        self._repo = repo

    def verificar(self, context: ContextoVerificacion) -> ResultadoVerificacion:
        inscripcion = self._repo.buscar(context.usuario_id, context.curso_id)
        if inscripcion and inscripcion.activa:
            return ResultadoVerificacion(permitido=True)
        return ResultadoVerificacion(permitido=False, razon="No inscrito")

# Factory para crear verificadores
class VerificadorAccesoFactory:
    @staticmethod
    def crear(tipo: str, repo: RepositorioInscripciones) -> VerificadorAcceso:
        if tipo == "inscripcion":
            return VerificadorAccesoInscripcion(repo)
        raise ValueError(f"Tipo desconocido: {tipo}")

# Uso
verificador = VerificadorAccesoFactory.crear("inscripcion", repo)
resultado = verificador.verificar(ContextoVerificacion(
    usuario_id=42,
    curso_id=101,
    timestamp=datetime.now()
))
if resultado.permitido:
    mostrar_curso()
```

Seis clases, un factory, dos DTOs, una interfaz abstracta. Y todo para responder una pregunta simple: esta inscrito este usuario en este curso?

Sin Pattern-itis:

```python
def puede_ver_curso(usuario_id: int, curso_id: int, repo) -> bool:
    inscripcion = repo.buscar_inscripcion(usuario_id, curso_id)
    return inscripcion is not None and inscripcion.activa
```

Una funcion. Tres lineas. Hace exactamente lo mismo. Es mas facil de leer, de probar, de modificar y de explicar a un nuevo miembro del equipo.

La pregunta obvia es: cuando se justificaria la version con patrones? Cuando *realmente* existan multiples formas de verificar el acceso -- por inscripcion, por suscripcion premium, por invitacion de instructor, por periodo de prueba -- y esas formas se combinen o cambien en tiempo de ejecucion. En ese caso, el patron Strategy para los verificadores tiene sentido. Pero hasta que ese escenario sea *real* y no hipotetico, la funcion simple gana.

---

## El arbol de decision: necesito un patron aqui?

La siguiente secuencia de preguntas te ayudara a decidir si un patron se justifica en una situacion concreta. No es una formula exacta -- el diseno de software nunca lo es --, pero es una heuristica util para evitar tanto la sobreingenieria como el subdisenio.

### Pregunta 1: Tengo un problema concreto que el patron resuelve?

No "podria tener en el futuro". No "seria elegante si". Tengo un problema *ahora* -- hoy, en este sprint, en este modulo -- que el patron aborda directamente?

Si la respuesta es no, detente. No apliques el patron.

### Pregunta 2: El problema se repite o va a repetirse?

Un patron vale la pena cuando el problema aparece multiples veces en tu codigo o cuando hay evidencia razonable de que aparecera de nuevo. Si el problema es unico y aislado, una solucion ad hoc puede ser mas apropiada que la maquinaria completa de un patron.

### Pregunta 3: El patron reduce la complejidad neta del sistema?

Cuenta. Despues de aplicar el patron, tienes menos carga cognitiva total o mas? Hay menos archivos que revisar para entender el flujo o mas? Las interfaces son mas simples o mas complejas?

Si la complejidad neta aumenta, el patron no se justifica. No importa lo elegante que sea.

### Pregunta 4: Hay una solucion mas simple que logre lo mismo?

Antes de aplicar un Strategy, preguntate: puedo resolver esto con un `if` o con una funcion que se pasa como parametro? Antes de aplicar un Observer, preguntate: puedo resolver esto con una llamada directa? Antes de aplicar un Factory, preguntate: puedo simplemente instanciar el objeto directamente?

La solucion mas simple que resuelve el problema es casi siempre la correcta. Los patrones son para cuando la solucion simple ya no alcanza.

### Pregunta 5: Mi equipo va a entender esto?

Un patron que solo tu entiendes no es una solucion -- es una deuda de conocimiento. Si aplicar el patron requiere que todo el equipo lea un capitulo del GoF para entender el codigo, el costo de adopcion puede superar el beneficio.

Esto no significa que debas evitar patrones que tu equipo no conoce. Significa que debes considerar el costo de educacion como parte del costo total del patron.

### La regla de las tres apariciones

Una heuristica complementaria, similar a la "regla de tres" para refactoring: no introduzcas un patron hasta que el problema que resuelve haya aparecido al menos tres veces en tu codigo. Las primeras dos veces, resuelve el problema de la forma mas simple posible. Si aparece una tercera vez, ahora tienes evidencia suficiente de que el problema es recurrente y la solucion merece formalizarse como patron.

Esta regla no es absoluta -- hay situaciones donde el patron es claramente correcto desde la primera aparicion, como un Adapter para una API externa. Pero como heuristica general, te protege de la Pattern-itis.

---

## Los patrones que ya no necesitas (porque tu lenguaje los resolvio)

La observacion de Peter Norvig merece atencion especial. En 1996, Norvig demostro que muchos de los patrones del GoF eran soluciones a limitaciones de C++, no a problemas universales del software [Norvig, 1996]. A medida que los lenguajes evolucionaron, incorporaron muchas de estas soluciones como caracteristicas nativas.

### Iterator

El GoF dedica paginas a explicar como crear un iterador personalizado con una interfaz `hasNext()` y `next()`. En Python, `for curso in cursos` ya *es* el patron Iterator. El lenguaje lo tiene integrado a traves del protocolo `__iter__` y `__next__`. Crear un iterador personalizado con clases es casi siempre innecesario cuando tienes generadores:

```python
# No necesitas una clase IteradorCursosFiltrados
def cursos_publicados(cursos):
    for curso in cursos:
        if curso.publicado:
            yield curso

# Uso
for curso in cursos_publicados(todos_los_cursos):
    print(curso.titulo)
```

### Command

El patron Command encapsula una operacion como un objeto. En lenguajes con funciones de primera clase, una funcion *es* un comando:

```python
# No necesitas una clase ComandoInscribir
# con metodo ejecutar()
def inscribir(usuario_id, curso_id):
    ...

# Las funciones se pueden almacenar, pasar, encolar
cola_de_comandos = [
    lambda: inscribir(42, 101),
    lambda: enviar_notificacion(42, "Bienvenido"),
]

for comando in cola_de_comandos:
    comando()
```

### Singleton

El Singleton es quiza el patron mas controvertido del GoF. Su intencion -- garantizar una sola instancia de una clase -- se resuelve en Python con un simple modulo. Un modulo de Python *es* un singleton: se importa una vez y todas las importaciones comparten el mismo estado.

```python
# config.py -- ya es un singleton
DATABASE_URL = "postgresql://localhost/devcourses"
REDIS_URL = "redis://localhost:6379"

# En cualquier parte del codigo
from config import DATABASE_URL  # Siempre la misma instancia
```

No necesitas una clase con `__new__` sobreescrito ni un metaclass. Un modulo es suficiente.

### Template Method

El Template Method define el esqueleto de un algoritmo en una clase base y permite que las subclases redefinan ciertos pasos. En lenguajes funcionales, esto es simplemente una funcion de orden superior:

```python
# En vez de una clase base abstracta con metodos hook
def procesar_pago(monto, moneda, validar, cobrar, confirmar):
    validar(monto, moneda)
    resultado = cobrar(monto, moneda)
    confirmar(resultado)
    return resultado

# Uso: los "pasos" se pasan como funciones
procesar_pago(
    monto=49.99,
    moneda="MXN",
    validar=validar_monto_positivo,
    cobrar=cobrar_con_stripe,
    confirmar=enviar_recibo
)
```

Esto no invalida la version con clases. En algunos contextos -- cuando los pasos son muchos, cuando necesitas estado compartido entre pasos, cuando el framework lo requiere -- la clase base con Template Method sigue siendo apropiada. Pero es importante reconocer que no es la *unica* forma de resolver el problema.

---

## Patrones en la era de la inteligencia artificial

Un desarrollo reciente merece mencion. Con el auge de los asistentes de codigo basados en IA, los patrones de diseno adquieren un rol nuevo e inesperado: sirven como *vocabulario de comunicacion con la maquina*.

Cuando le dices a un asistente de codigo "aplica el patron Strategy para la logica de precios", el asistente sabe exactamente que estructura generar. Los patrones funcionan como instrucciones precisas porque son soluciones estandarizadas con nombres universales. Esto refuerza la idea central del capitulo: el valor principal de los patrones es la comunicacion, no la estructura en si.

Pero la misma advertencia aplica. Que un asistente de IA pueda generar un Abstract Factory en treinta segundos no significa que tu proyecto lo necesite. La facilidad de generacion puede agravar la Pattern-itis si no se acompana de criterio.

---

## Proyecto guia: patrones en DevCourses

Revisemos DevCourses con un ojo critico. Despues de doce capitulos de desarrollo, el sistema tiene varios modulos con diferentes niveles de complejidad. Donde se justifican los patrones y donde serian sobreingenieria?

### Modulo de pagos: Strategy + Adapter (justificado)

DevCourses acepta pagos con Stripe, PayPal y MercadoPago. Cada procesador tiene su propia API, su propio formato de respuesta, su propia logica de reintentos. Ademas, las reglas de precios varian: hay precios normales, precios premium (incluidos en suscripcion), descuentos por cupon y precios por region.

Aqui el patron Strategy para el calculo de precios y el patron Adapter para los procesadores de pago son *necesarios*. Sin ellos, el codigo estaria lleno de condicionales (`if procesador == "stripe": ... elif procesador == "paypal": ...`) que se multiplicarian con cada nuevo procesador o regla de precio.

La prueba de justificacion: hay tres implementaciones concretas de procesador de pago y cuatro estrategias de precio. El patron paga su costo desde la segunda implementacion.

### Modulo de notificaciones: Observer + Strategy (justificado parcialmente)

Ya vimos en el capitulo 12 que el sistema de notificaciones usa composicion con canales (email, push, SMS) y formateadores (plano, template). El patron Observer para los eventos de inscripcion tambien se justifica: hay cuatro suscriptores diferentes que reaccionan a una inscripcion completada.

Pero el Event Bus no debe convertirse en la forma *predeterminada* de comunicacion. Si el modulo de catalogo necesita consultar el precio de un curso, una llamada directa al modulo de precios es mas clara y mas simple que publicar un evento "solicitud_precio" y esperar una respuesta. No todo necesita ser un evento.

### Modulo de catalogo: sin patrones especiales (la simplicidad gana)

El catalogo de cursos es fundamentalmente un CRUD con busqueda. Listar cursos, filtrar por categoria, obtener detalle de un curso. No hay multiples implementaciones de nada. No hay logica compleja que varie en tiempo de ejecucion. No hay integraciones con APIs externas.

Introducir patrones aqui -- un Repository abstracto, un Service Layer, un DTO separado del modelo -- seria sobreingenieria pura. Un modulo con funciones directas que consultan la base de datos y devuelven resultados es mas que suficiente:

```python
# catalogo/queries.py -- simple, directo, suficiente
def listar_cursos(db, filtros: dict = None) -> list[Curso]:
    query = "SELECT * FROM cursos WHERE publicado = true"
    if filtros and filtros.get("categoria"):
        query += " AND categoria = %(categoria)s"
    return db.query(query, filtros or {})

def obtener_curso(db, curso_id: int) -> Curso | None:
    return db.query_one("SELECT * FROM cursos WHERE id = %(id)s", {"id": curso_id})
```

Si en el futuro el catalogo necesita multiples fuentes de datos (por ejemplo, busqueda full-text con Elasticsearch ademas de PostgreSQL), entonces un Adapter o un Facade se justificara. Pero hasta que ese momento llegue, la simplicidad es la mejor arquitectura.

### Modulo de autenticacion: Facade (justificado)

El proceso de autenticacion involucra multiples pasos: validar credenciales, verificar que la cuenta no este bloqueada, generar un token JWT, registrar el inicio de sesion en analytics, y opcionalmente enviar una notificacion de seguridad. Cada uno de estos pasos es simple, pero la orquestacion es compleja.

Un Facade que exponga `autenticador.iniciar_sesion(email, contrasena)` y oculte toda la complejidad interna es exactamente lo que el modulo necesita. El controlador HTTP no deberia conocer los pasos internos de autenticacion.

### La leccion

Observa el patron: los patrones se justifican en los modulos con mas variabilidad, mas integraciones externas y mas complejidad de orquestacion. En los modulos simples, la ausencia de patrones *es* el buen diseno. No hay verguenza en tener un modulo sin un solo patron del GoF. La verguenza esta en tener patrones que no resuelven nada.

---

## Mas alla del GoF: patrones modernos

El catalogo del GoF no es el unico que existe ni el mas relevante para todos los contextos. Con la evolucion del software hacia sistemas distribuidos, arquitecturas event-driven y aplicaciones cloud-native, han surgido patrones nuevos que vale la pena conocer:

- **Circuit Breaker:** Detecta fallos en un servicio externo y deja de enviarle peticiones temporalmente para evitar cascadas de errores. Esencial en arquitecturas de microservicios.

- **Saga:** Coordina transacciones distribuidas entre multiples servicios, con mecanismos de compensacion si alguno falla. Necesario cuando una operacion de negocio abarca varios sistemas.

- **CQRS (Command Query Responsibility Segregation):** Separa los modelos de lectura y escritura, permitiendo optimizar cada uno independientemente. Util cuando los patrones de lectura y escritura son radicalmente diferentes.

- **Event Sourcing:** En vez de guardar el estado actual, guarda la secuencia de eventos que produjeron ese estado. Permite reconstruir cualquier estado pasado y auditar completamente el sistema.

Estos patrones son herramientas para problemas especificos de sistemas distribuidos. La misma advertencia aplica: no los uses porque suenan sofisticados. Usalos cuando el problema que resuelven sea tu problema.

---

## Aplica esto el lunes

1. **Auditoria de patrones.** Identifica los patrones de diseno presentes en tu proyecto actual. Para cada uno, preguntate: este patron resuelve un problema real que tenemos hoy? Si no puedes articular el problema concreto, el patron probablemente sobra. Eliminar una capa de abstraccion innecesaria es una de las refactorizaciones mas valiosas que puedes hacer.

2. **La prueba de la alternativa simple.** Escoge el patron mas complejo de tu codigo. Imagina la version mas simple posible que resuelva el mismo problema -- quiza una funcion, quiza un `if`, quiza un diccionario. Compara ambas versiones. Si la version simple es igualmente mantenible y extensible *para tus necesidades actuales*, considera simplificar.

3. **Vocabulario compartido.** En tu proxima sesion de diseno con el equipo, describe una solucion usando el nombre de un patron en vez de explicar la estructura completa. Si tu equipo entiende inmediatamente, el patron esta cumpliendo su funcion como vocabulario. Si no, invierte 15 minutos en compartir el conocimiento -- esa inversion pagara dividendos en toda comunicacion futura.

4. **Resistir la tentacion.** La proxima vez que sientas el impulso de aplicar un patron, espera. Implementa la solucion mas simple primero. Si en dos semanas el problema se repite o la solucion simple no escala, entonces introduce el patron. Esa espera deliberada te protege de la Pattern-itis.

---

## Referencias del capitulo

- Alexander, C. (1977). *A Pattern Language: Towns, Buildings, Construction*. Oxford University Press.
- Alexander, C. (1996). Keynote Speech, OOPSLA 1996.
- Beck, K. y Cunningham, W. (1987). "Using Pattern Languages for Object-Oriented Programs." OOPSLA '87 Workshop.
- Gamma, E., Helm, R., Johnson, R. y Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
- Norvig, P. (1996). "Design Patterns in Dynamic Languages." Presentacion, Object World, 1996.
- Ousterhout, J. (2018). *A Philosophy of Software Design*. Yaknyam Press.
