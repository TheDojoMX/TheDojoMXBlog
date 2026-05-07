# Capitulo 12: Composicion -- construye combinando, no heredando

> "Nuestra habilidad para descomponer un problema en partes depende directamente de nuestra habilidad para combinar soluciones." -- John Hughes, "Why Functional Programming Matters" [Hughes, 1989]

---

## El arte de combinar

A lo largo de este libro hemos hablado extensamente sobre *descomponer*: separar sistemas en modulos, dividir responsabilidades, aislar preocupaciones. Pero la descomposicion es solo la mitad de la historia. La otra mitad -- igual de importante y menos discutida -- es la *composicion*: el arte de combinar piezas pequenas para construir piezas grandes.

John Hughes, en su influyente paper de 1989, hizo una observacion que deberia estar grabada en la pared de toda oficina de desarrollo: la calidad de nuestras descomposiciones depende enteramente de la calidad de nuestras herramientas para componer. Si no sabes como vas a juntar las piezas, no puedes saber como separarlas. Descomponer sin saber componer es romper un jarrón: terminas con fragmentos que no encajan.

Rich Hickey, creador de Clojure, lo expreso de otra manera en su celebre charla "Simple Made Easy":

> "Componer componentes simples es la clave para construir software robusto. Cuando construyas componentes mas grandes, pasa los subcomponentes como argumentos en vez de cablearlos internamente." [Hickey, 2011]

La composicion no es un concepto exclusivo de la programacion funcional, aunque ahi es donde mas se habla de ella. Componer es la operacion fundamental del software: juntar funciones, objetos, servicios, modulos, sistemas. Todo software no trivial es una composicion de partes mas pequenas. La pregunta no es *si* componer, sino *como* hacerlo bien.

En este capitulo vamos a explorar la composicion en tres niveles: funciones, objetos y servicios. Veremos por que la herencia profunda es una trampa que la industria ha aprendido a evitar, y por que la composicion produce sistemas mas flexibles, mas comprensibles y mas faciles de cambiar. Terminaremos refactorizando DevCourses para reemplazar jerarquias de herencia con composicion.

**Takeaway:** La composicion es la contraparte esencial de la descomposicion. Si sabes como combinar piezas bien, puedes descomponer problemas con confianza. Si no, cada descomposicion es un riesgo.

---

## Composicion de funciones: el validador como ejemplo

Empecemos por el nivel mas basico: componer funciones. La idea es simple: tomar funciones pequenas que resuelven problemas especificos y combinarlas para resolver problemas mas grandes.

### El ejemplo del validador de contrasenas

Necesitamos validar contrasenas en DevCourses. Los requisitos son:

- Longitud minima de 8 caracteres.
- Al menos un numero.
- Al menos un caracter especial.
- No puede contener palabras de una lista prohibida.

La solucion ingenua es una sola funcion con una cascada de condicionales:

```python
def validar_contrasena(contrasena: str) -> list[str]:
    errores = []
    if len(contrasena) < 8:
        errores.append("La contrasena debe tener al menos 8 caracteres")
    if not any(c.isdigit() for c in contrasena):
        errores.append("La contrasena debe contener al menos un numero")
    if not any(c in "!@#$%^&*()_+" for c in contrasena):
        errores.append("La contrasena debe contener un caracter especial")
    palabras_prohibidas = ["password", "123456", "admin"]
    if any(p in contrasena.lower() for p in palabras_prohibidas):
        errores.append("La contrasena contiene palabras prohibidas")
    return errores
```

Funciona. Pero tiene tres problemas: (1) si quieres agregar o quitar una regla, tienes que modificar la funcion; (2) no puedes reutilizar las validaciones individuales en otro contexto; (3) si quieres aplicar diferentes reglas a diferentes tipos de usuario, necesitas condicionales dentro de condicionales.

### Composicion: funciones pequenas combinadas

La alternativa es descomponer en funciones pequeñas y luego componerlas:

```python
from typing import Callable

# Cada validador es una funcion pura: recibe una cadena, devuelve una lista de errores
Validador = Callable[[str], list[str]]

def longitud_minima(minimo: int) -> Validador:
    def validar(contrasena: str) -> list[str]:
        if len(contrasena) < minimo:
            return [f"Debe tener al menos {minimo} caracteres"]
        return []
    return validar

def contiene_numero() -> Validador:
    def validar(contrasena: str) -> list[str]:
        if not any(c.isdigit() for c in contrasena):
            return ["Debe contener al menos un numero"]
        return []
    return validar

def contiene_especial() -> Validador:
    def validar(contrasena: str) -> list[str]:
        if not any(c in "!@#$%^&*()_+" for c in contrasena):
            return ["Debe contener un caracter especial"]
        return []
    return validar

def sin_palabras_prohibidas(palabras: list[str]) -> Validador:
    def validar(contrasena: str) -> list[str]:
        for p in palabras:
            if p in contrasena.lower():
                return [f"No puede contener '{p}'"]
        return []
    return validar
```

Ahora viene la composicion. Necesitamos una funcion que combine multiples validadores en uno solo:

```python
def componer_validadores(*validadores: Validador) -> Validador:
    def validar(contrasena: str) -> list[str]:
        errores = []
        for v in validadores:
            errores.extend(v(contrasena))
        return errores
    return validar
```

Y la usamos asi:

```python
# Para usuarios normales
validar_contrasena_usuario = componer_validadores(
    longitud_minima(8),
    contiene_numero(),
    contiene_especial(),
    sin_palabras_prohibidas(["password", "123456", "admin"])
)

# Para instructores (requisitos mas estrictos)
validar_contrasena_instructor = componer_validadores(
    longitud_minima(12),
    contiene_numero(),
    contiene_especial(),
    sin_palabras_prohibidas(["password", "123456", "admin", "instructor"])
)

# Uso
errores = validar_contrasena_usuario("mi_clave")
```

Observa lo que sucedio. `componer_validadores` toma funciones y produce una funcion nueva. Cada validador individual es independiente, reutilizable y testeable por separado. Agregar un nuevo validador no requiere modificar ningun codigo existente -- solo agregarlo a la lista. Y diferentes configuraciones de validacion se crean combinando los mismos bloques de diferentes maneras.

Esto es composicion en su forma mas pura: **combinar piezas simples para construir piezas complejas, donde las piezas no se conocen entre si y la forma de combinarlas es explicita y configurable**.

### Composicion matematica: pipelines de transformacion

Hay una segunda forma de composicion de funciones, mas cercana a la definicion matematica: la salida de una funcion se convierte en la entrada de la siguiente. En matematicas, si tienes `f(x)` y `g(x)`, la composicion `g(f(x))` aplica primero `f` y luego `g`.

En software, esto se manifiesta como pipelines de transformacion. Imagina que DevCourses necesita procesar el titulo de un curso antes de guardarlo:

```python
def normalizar_espacios(texto: str) -> str:
    return " ".join(texto.split())

def capitalizar_titulo(texto: str) -> str:
    preposiciones = {"de", "del", "la", "el", "en", "y", "o", "a"}
    palabras = texto.split()
    return " ".join(
        p if p.lower() in preposiciones and i > 0 else p.capitalize()
        for i, p in enumerate(palabras)
    )

def truncar(maximo: int):
    def _truncar(texto: str) -> str:
        return texto[:maximo] if len(texto) > maximo else texto
    return _truncar

def sanitizar_html(texto: str) -> str:
    import html
    return html.escape(texto)
```

Cuatro funciones simples. Cada una hace una sola cosa. Para combinarlas en un pipeline:

```python
def pipeline(*funciones):
    def ejecutar(dato):
        resultado = dato
        for f in funciones:
            resultado = f(resultado)
        return resultado
    return ejecutar

procesar_titulo = pipeline(
    normalizar_espacios,
    sanitizar_html,
    capitalizar_titulo,
    truncar(200)
)

# Uso
titulo_limpio = procesar_titulo("  <b>introduccion  a   python</b>  ")
# -> "Introduccion a Python"
```

Este patron es tan comun que muchos lenguajes lo tienen incorporado:

- En **Elixir**, el operador pipe `|>` encadena funciones: `texto |> normalizar |> sanitizar |> capitalizar`.
- En **Haskell**, el operador `.` compone funciones: `capitalizar . sanitizar . normalizar`.
- En **JavaScript**, las propuestas de pipeline operator (`|>`) y el metodo `.pipe()` de RxJS hacen lo mismo.
- En **Python**, la funcion `functools.reduce` permite construir pipelines, aunque sin la elegancia sintactica de los lenguajes funcionales.

Lo importante no es la sintaxis sino la idea: **un proceso complejo es una cadena de transformaciones simples**. Cada transformacion es independiente. El orden puede cambiar. Se pueden agregar o quitar pasos. Es facil de probar (cada paso por separado) y facil de entender (lee el pipeline de arriba a abajo).

---

## Composicion de objetos y servicios

La composicion no es exclusiva de las funciones. En el nivel de objetos y servicios, la composicion toma una forma diferente pero igualmente poderosa: un objeto contiene otros objetos como partes, en vez de heredar de ellos.

### "Tiene un" vs "Es un"

La distincion fundamental entre composicion e herencia se captura en dos frases:

- **Herencia:** Un `Instructor` *es un* `Usuario` (relacion "es un").
- **Composicion:** Un `Instructor` *tiene un* `Perfil` y *tiene una* `ConfiguracionPagos` (relacion "tiene un").

Ambas relaciones son validas en distintos contextos. Pero la composicion tiene una ventaja estructural que la herencia no puede igualar: las partes son independientes entre si. Cambiar `ConfiguracionPagos` no afecta a `Perfil`. Reemplazar `Perfil` por un nuevo tipo de perfil no requiere reescribir `Instructor`. Las piezas se pueden recombinar libremente.

Veamos un ejemplo concreto en DevCourses. El sistema tiene diferentes tipos de contenido en los cursos:

```python
# Con herencia (problematico)
class Contenido:
    def __init__(self, titulo, duracion):
        self.titulo = titulo
        self.duracion = duracion

class Video(Contenido):
    def __init__(self, titulo, duracion, url_video, resolucion):
        super().__init__(titulo, duracion)
        self.url_video = url_video
        self.resolucion = resolucion

class Texto(Contenido):
    def __init__(self, titulo, duracion, cuerpo, formato):
        super().__init__(titulo, duracion)
        self.cuerpo = cuerpo
        self.formato = formato

class Quiz(Contenido):
    def __init__(self, titulo, duracion, preguntas, intentos_permitidos):
        super().__init__(titulo, duracion)
        self.preguntas = preguntas
        self.intentos_permitidos = intentos_permitidos
```

Parece limpio. Pero que pasa cuando necesitamos un `VideoConQuiz` -- un video que al final tiene preguntas? No puede heredar de `Video` *y* de `Quiz` (herencia multiple, que la mayoria de los lenguajes prohibe o desaconseja). Que pasa cuando queremos agregar transcripcion a cualquier tipo de contenido? Necesitamos `VideoConTranscripcion`, `TextoConTranscripcion`, y la explosion combinatoria comienza.

```python
# Con composicion (flexible)
class Contenido:
    def __init__(
        self,
        titulo: str,
        duracion: int,
        recurso: Recurso,
        complementos: list[Complemento] = None
    ):
        self.titulo = titulo
        self.duracion = duracion
        self.recurso = recurso
        self.complementos = complementos or []

class RecursoVideo:
    def __init__(self, url: str, resolucion: str):
        self.url = url
        self.resolucion = resolucion

class RecursoTexto:
    def __init__(self, cuerpo: str, formato: str):
        self.cuerpo = cuerpo
        self.formato = formato

class ComplementoQuiz:
    def __init__(self, preguntas: list, intentos: int):
        self.preguntas = preguntas
        self.intentos = intentos

class ComplementoTranscripcion:
    def __init__(self, texto: str, idioma: str):
        self.texto = texto
        self.idioma = idioma
```

Ahora crear un video con quiz y transcripcion es trivial:

```python
leccion = Contenido(
    titulo="Introduccion a FastAPI",
    duracion=1200,
    recurso=RecursoVideo(url="https://cdn.devcourses.com/v/123", resolucion="1080p"),
    complementos=[
        ComplementoQuiz(preguntas=[...], intentos=3),
        ComplementoTranscripcion(texto="...", idioma="es")
    ]
)
```

No hay herencia multiple. No hay explosion combinatoria. Cada componente es independiente: puedes tener un texto con quiz, un video sin complementos, o cualquier combinacion. Y agregar un nuevo tipo de complemento (por ejemplo, `ComplementoEjercicios`) no requiere modificar ninguna clase existente.

### Delegacion: composicion en accion

La composicion funciona a traves de la *delegacion*: en vez de heredar comportamiento, un objeto le pide a otro que haga el trabajo. Es la diferencia entre "soy capaz de hacer X porque lo herede de mi padre" y "soy capaz de hacer X porque tengo un colaborador que sabe hacerlo".

```python
# Con herencia: el conocimiento esta en la jerarquia
class RepositorioConCache(RepositorioPostgres):
    def obtener(self, id):
        cached = self.cache.get(id)
        if cached:
            return cached
        resultado = super().obtener(id)  # Llama al padre
        self.cache.set(id, resultado)
        return resultado

# Con composicion y delegacion: el conocimiento esta en los colaboradores
class RepositorioConCache:
    def __init__(self, repo_real, cache):
        self._repo = repo_real
        self._cache = cache

    def obtener(self, id):
        cached = self._cache.get(id)
        if cached:
            return cached
        resultado = self._repo.obtener(id)
        self._cache.set(id, resultado)
        return resultado
```

La version con composicion tiene dos ventajas cruciales:

1. **El repositorio real es intercambiable.** Puede ser Postgres, MongoDB, un archivo JSON, un mock para pruebas. La version con herencia esta atada a `RepositorioPostgres`.

2. **El cache es intercambiable.** Puede ser Redis, Memcached, un diccionario en memoria. Cada combinacion es posible sin crear nuevas clases.

La composicion convierte una relacion rigida (herencia) en una relacion flexible (colaboracion). Y esa flexibilidad se paga con un costo minimo: una linea extra en el constructor para recibir los colaboradores.

---

## Por que la herencia profunda es una trampa

La herencia no es inherentemente mala. Es una herramienta. Pero como toda herramienta, tiene un dominio de aplicacion estrecho y se vuelve peligrosa cuando se usa fuera de el.

### El problema del acoplamiento vertical

Cuando una clase hereda de otra, se acopla a ella de la forma mas intima posible: acoplamiento de contenido. La subclase tiene acceso a los campos y metodos internos de la clase padre. Conoce su estructura. Depende de ella. Cualquier cambio en la clase padre puede romper la subclase.

Y el problema se amplifica con cada nivel de la jerarquia:

```python
class Entidad:
    # 5 metodos, 3 campos

class EntidadPersistente(Entidad):
    # 4 metodos mas, 2 campos mas. Conoce los 3 campos de Entidad.

class EntidadAuditable(EntidadPersistente):
    # 3 metodos mas. Conoce los 5 campos de los dos niveles superiores.

class Usuario(EntidadAuditable):
    # Finalmente, la logica del usuario.
    # Pero hereda 12 metodos y 5 campos que no pidio.
    # Cambiar cualquiera de las 3 clases padre puede romperla.
```

Cada nivel de herencia es una capa de acoplamiento. Un cambio en `Entidad` puede propagarse a traves de `EntidadPersistente` y `EntidadAuditable` hasta llegar a `Usuario`. Y cuando tienes veinte clases que heredan de `EntidadAuditable`, un cambio en la raiz del arbol puede romper veinte clases.

Este es el *fragile base class problem* (problema de la clase base fragil): las clases base son fragiles porque cualquier modificacion interna puede romper las subclases de formas inesperadas [Mikhajlov y Sekerinski, 1998].

### El problema de la taxonomia prematura

La herencia te obliga a clasificar las cosas en una jerarquia *antes* de saber como las vas a usar. Es como organizar tu biblioteca por color antes de leer los libros. La clasificacion parece ordenada, pero no te ayuda a encontrar lo que necesitas.

En DevCourses, el equipo original clasifico los usuarios asi:

```
Usuario
    ├── Estudiante
    │       ├── EstudianteGratuito
    │       └── EstudiantePremium
    ├── Instructor
    │       ├── InstructorInterno
    │       └── InstructorExterno
    └── Administrador
```

Parece logico. Pero despues llegaron los requisitos:

- Un instructor puede ser tambien estudiante de otros cursos.
- Un administrador puede ser instructor.
- Un estudiante premium puede convertirse en instructor.
- Un instructor externo puede ser contratado como interno.

La jerarquia no puede representar estas combinaciones. Un `InstructorExterno` no puede ser simultaneamente un `EstudiantePremium` porque son ramas diferentes del arbol. La herencia impone una taxonomia exclusiva -- una cosa *es* exactamente un tipo -- pero la realidad del negocio es combinatoria: una persona *tiene* varios roles que pueden cambiar con el tiempo.

Con composicion, el problema desaparece:

```python
class Usuario:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email
        self.roles: list[Rol] = []
        self.suscripcion: Suscripcion = None

class RolEstudiante:
    def __init__(self, cursos_inscritos: list[int]):
        self.cursos_inscritos = cursos_inscritos

class RolInstructor:
    def __init__(self, cursos_creados: list[int], tipo: str):
        self.cursos_creados = cursos_creados
        self.tipo = tipo  # "interno" o "externo"

class RolAdministrador:
    def __init__(self, permisos: list[str]):
        self.permisos = permisos
```

Un usuario puede tener multiples roles. Un instructor externo que tambien es estudiante premium es simplemente un `Usuario` con un `RolInstructor(tipo="externo")` y una `SuscripcionPremium`. No hay jerarquia que romper. No hay taxonomia que se vuelva obsoleta.

### Cuando la herencia si funciona

La herencia tiene un dominio valido y es importante reconocerlo:

**1. Jerarquias genuinamente estables.** Si la relacion "es un" es estable y no va a cambiar, la herencia esta bien. Los widgets de una interfaz grafica son un ejemplo clasico: un `Boton` *es un* `Widget`, y eso no va a cambiar. Los nodos de un AST (arbol de sintaxis abstracta) son otro ejemplo.

**2. Profundidad maxima de 2-3 niveles.** La herencia funciona bien cuando es superficial. Una clase base con implementaciones concretas directas (sin niveles intermedios) es un patron razonable. Es cuando la jerarquia crece a cuatro, cinco, seis niveles que el acoplamiento se vuelve inmanejable.

**3. Frameworks que lo requieren.** Algunos frameworks de trabajo estan disenados alrededor de la herencia: Django Rest Framework con sus `APIView`, FastAPI con ciertos patrones, los componentes de clase de React (antes de los hooks). Cuando el framework lo requiere, usalo. Pero no extiendas la jerarquia mas alla de lo que el framework necesita.

La cita del Gang of Four sigue siendo la mejor guia:

> "Prefiere la composicion de objetos sobre la herencia de clases." [Gamma et al., 1994]

"Prefiere" no significa "prohibe". Significa que la composicion deberia ser tu opcion por defecto, y la herencia, una excepcion justificada.

---

## Patrones de composicion practicos

La composicion se manifiesta en varios patrones que probablemente ya uses, aunque quiza no los llames asi.

### Patron Strategy: comportamiento intercambiable

El patron Strategy encapsula una familia de algoritmos y los hace intercambiables. Es composicion pura: un objeto delega una decision a otro objeto que puede ser reemplazado.

En DevCourses, el calculo de precios varia segun el tipo de suscripcion:

```python
class CalculadorPrecio(ABC):
    @abstractmethod
    def calcular(self, precio_base: Decimal, usuario_id: int) -> Decimal: ...

class PrecioNormal(CalculadorPrecio):
    def calcular(self, precio_base: Decimal, usuario_id: int) -> Decimal:
        return precio_base

class PrecioPremium(CalculadorPrecio):
    def calcular(self, precio_base: Decimal, usuario_id: int) -> Decimal:
        return Decimal("0")  # Incluido en la suscripcion

class PrecioConDescuento(CalculadorPrecio):
    def __init__(self, porcentaje: int):
        self._porcentaje = porcentaje

    def calcular(self, precio_base: Decimal, usuario_id: int) -> Decimal:
        return precio_base * (1 - self._porcentaje / 100)

class ServicioInscripcion:
    def __init__(self, calculador: CalculadorPrecio, repo: RepositorioInscripciones):
        self._calculador = calculador
        self._repo = repo

    def inscribir(self, usuario_id: int, curso_id: int, precio_base: Decimal):
        precio_final = self._calculador.calcular(precio_base, usuario_id)
        inscripcion = Inscripcion(usuario_id, curso_id, precio_final)
        self._repo.guardar(inscripcion)
        return inscripcion
```

El `ServicioInscripcion` no sabe como se calcula el precio. No le importa. Solo sabe que tiene un `CalculadorPrecio` que le da un numero. Puedes agregar nuevas estrategias de precio -- cupones, descuentos por volumen, precios por region -- sin modificar el servicio.

### Patron Decorator funcional: enriquecer sin heredar

En el capitulo 11 hablamos de los decoradores con precaucion. Pero hay una forma de decorador que es composicion pura y no sufre los problemas de la herencia: el decorador funcional.

```python
def con_logging(func):
    def wrapper(*args, **kwargs):
        print(f"Llamando a {func.__name__} con {args}, {kwargs}")
        resultado = func(*args, **kwargs)
        print(f"{func.__name__} retorno {resultado}")
        return resultado
    return wrapper

def con_reintentos(max_intentos: int):
    def decorar(func):
        def wrapper(*args, **kwargs):
            for intento in range(max_intentos):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if intento == max_intentos - 1:
                        raise
        return wrapper
    return decorar

def con_cache(cache: dict):
    def decorar(func):
        def wrapper(*args):
            if args in cache:
                return cache[args]
            resultado = func(*args)
            cache[args] = resultado
            return resultado
        return wrapper
    return decorar
```

Estos decoradores son funciones que toman funciones y devuelven funciones. Son composicion de funciones en estado puro. Y se pueden combinar:

```python
@con_logging
@con_reintentos(3)
@con_cache({})
def obtener_curso(curso_id: int) -> Curso:
    return db.query("SELECT * FROM cursos WHERE id = %s", curso_id)
```

La funcion `obtener_curso` ahora tiene logging, reintentos y cache, sin que ninguna de esas preocupaciones este en su codigo. Y cada decorador es independiente de los otros -- puedes quitar el logging sin afectar los reintentos, o agregar un decorador de metricas sin tocar nada existente.

### Patron Builder: composicion paso a paso

Cuando construir un objeto requiere muchos pasos opcionales, el patron Builder permite componer el resultado incrementalmente:

```python
class CursoBuilder:
    def __init__(self, titulo: str, instructor_id: int):
        self._titulo = titulo
        self._instructor_id = instructor_id
        self._lecciones = []
        self._precio = None
        self._idioma = "es"
        self._nivel = "principiante"
        self._certificado = False

    def con_leccion(self, leccion: Leccion) -> "CursoBuilder":
        self._lecciones.append(leccion)
        return self

    def con_precio(self, precio: Decimal) -> "CursoBuilder":
        self._precio = precio
        return self

    def con_idioma(self, idioma: str) -> "CursoBuilder":
        self._idioma = idioma
        return self

    def con_certificado(self) -> "CursoBuilder":
        self._certificado = True
        return self

    def construir(self) -> Curso:
        if not self._lecciones:
            raise ValueError("Un curso necesita al menos una leccion")
        return Curso(
            titulo=self._titulo,
            instructor_id=self._instructor_id,
            lecciones=self._lecciones,
            precio=self._precio,
            idioma=self._idioma,
            nivel=self._nivel,
            certificado=self._certificado
        )

# Uso
curso = (CursoBuilder("FastAPI Avanzado", instructor_id=42)
    .con_leccion(Leccion("Middleware", 600))
    .con_leccion(Leccion("WebSockets", 900))
    .con_precio(Decimal("49.99"))
    .con_certificado()
    .construir())
```

Cada metodo del Builder agrega una pieza al resultado final. El orden no importa (excepto para restricciones logicas). Puedes omitir pasos opcionales. Y el metodo `construir()` valida que el resultado sea coherente antes de crearlo.

### Composicion de servicios: el middleware pipeline

A nivel de servicios, la composicion se manifiesta como cadenas de middleware -- funciones que procesan una peticion en secuencia, cada una agregando o transformando algo:

```python
class Middleware(ABC):
    @abstractmethod
    def procesar(self, request, siguiente):
        ...

class MiddlewareAutenticacion(Middleware):
    def procesar(self, request, siguiente):
        token = request.headers.get("Authorization")
        if not token:
            raise NoAutorizado()
        request.usuario = verificar_token(token)
        return siguiente(request)

class MiddlewareRateLimit(Middleware):
    def __init__(self, limite_por_minuto: int):
        self._limite = limite_por_minuto

    def procesar(self, request, siguiente):
        if self._excede_limite(request.usuario):
            raise LimiteExcedido()
        return siguiente(request)

class MiddlewareLogging(Middleware):
    def procesar(self, request, siguiente):
        inicio = time.time()
        respuesta = siguiente(request)
        duracion = time.time() - inicio
        log.info(f"{request.method} {request.path} -> {respuesta.status} ({duracion:.2f}s)")
        return respuesta

# Composicion del pipeline
def crear_pipeline(middlewares: list[Middleware], handler_final):
    def ejecutar(request):
        cadena = handler_final
        for mw in reversed(middlewares):
            cadena_anterior = cadena
            cadena = lambda req, mw=mw, sig=cadena_anterior: mw.procesar(req, sig)
        return cadena(request)
    return ejecutar

pipeline = crear_pipeline(
    [MiddlewareLogging(), MiddlewareAutenticacion(), MiddlewareRateLimit(100)],
    handler_final=procesar_peticion
)
```

Cada middleware es independiente. El orden de composicion determina el comportamiento. Puedes agregar o quitar middleware sin modificar los existentes. Es el mismo principio del pipeline de funciones, pero a nivel de servicios.

---

## Composicion en la practica: lecciones del mundo real

La composicion suena elegante en la teoria. Pero en la practica, trae consigo sus propios desafios. Ignorarlos seria deshonesto.

### El problema de la configuracion

Cuando usas herencia, el ensamblaje es implicito: la subclase automaticamente "tiene" todo lo del padre. Cuando usas composicion, el ensamblaje es explicito: *tu* decides que piezas combinar y como cablearlas.

Esto significa que necesitas un lugar donde se tomen las decisiones de composicion. En sistemas pequenos, ese lugar es el punto de entrada de la aplicacion (el `main()`, la configuracion de rutas, el modulo de inicializacion). En sistemas grandes, puede ser un contenedor de inyeccion de dependencias.

```python
# El "composition root": donde se ensamblan las piezas
def crear_aplicacion():
    # Infraestructura
    db = PostgresDatabase(config.DATABASE_URL)
    cache = RedisCache(config.REDIS_URL)
    smtp = SMTPClient(config.SMTP_HOST)

    # Repositorios
    repo_cursos = RepositorioCursosPostgres(db)
    repo_inscripciones = RepositorioInscripcionesPostgres(db)

    # Servicios (composicion explicita)
    notificador = Notificador(CanalEmail(smtp), FormateadorTemplate(templates))
    calculador_precio = CalculadorPrecioConDescuentos(repo_descuentos)
    servicio_inscripcion = ServicioInscripcion(
        repo=repo_inscripciones,
        precios=calculador_precio,
        eventos=EventBus()
    )

    return App(servicio_inscripcion, notificador, ...)
```

Este "composition root" es el precio de la composicion. Es codigo de configuracion que no existiria con herencia. Pero es codigo *honesto*: muestra explicitamente como estan conectadas las piezas del sistema. Con herencia, esas conexiones existen pero estan ocultas en la jerarquia de clases.

### El problema de la navegabilidad

Cuando usas herencia y quieres saber que hace `usuario.autenticar()`, haces Ctrl+Click y llegas a la clase padre. La cadena es lineal y facil de seguir.

Cuando usas composicion, `usuario.autenticar()` delega a `self._autenticador.autenticar()`. Llegas a una interfaz abstracta. Tienes que buscar la implementacion concreta, que se decidio en el composition root. Son mas saltos, mas archivos, mas busquedas.

Esta es la misma critica que le hicimos a DIP en el capitulo 9: la indirreccion tiene un costo cognitivo real. La diferencia es que con composicion, la indirreccion compra algo tangible: flexibilidad para cambiar, facilidad para probar, independencia de los componentes.

El trade-off se resuelve caso por caso. Para componentes que nunca van a cambiar y que solo tienen una implementacion, la composicion a traves de interfaces abstractas es sobreingenieria. Para componentes que tienen multiples variantes o que necesitan ser probados en aislamiento, la composicion vale cada salto extra de navegacion.

### La regla de las tres implementaciones

Una heuristica util: no introduzcas una interfaz abstracta hasta que tengas dos implementaciones concretas, o evidencia clara de que habra una segunda. Hasta entonces, usa la implementacion directa. Si mas adelante necesitas la abstraccion, refactorizar para agregarla es un cambio local y controlado.

Esta heuristica es aplicable tanto a la composicion como a DIP. No anticipes variaciones que no existen. Compone cuando la composicion resuelve un problema real, no cuando resuelve un problema hipotetico.

---

## La simplicidad de lo compuesto

Rich Hickey hace una distincion crucial que aplica directamente a la composicion: la diferencia entre *simple* y *facil* [Hickey, 2011].

**Simple** significa "sin entrelazamiento". Un componente simple hace una cosa, no tiene dependencias ocultas, y su comportamiento es predecible. Un validador que solo checa la longitud de una cadena es simple.

**Facil** significa "familiar" o "comodo". Una clase base que hereda catorce comportamientos es facil de *usar* -- llamas a `super().__init__()` y todo funciona. Pero no es simple: tiene dependencias ocultas, comportamiento heredado que quiza no entiendes, y cambios en la clase padre pueden romperla de formas inesperadas.

La composicion privilegia lo simple sobre lo facil:

- Cada pieza compuesta es simple: hace una cosa.
- La forma de combinarlas es explicita: ves que piezas se usan y en que orden.
- No hay magia oculta: no hay `super()` que invoque codigo que no ves.
- El costo es que requiere un poco mas de codigo: tienes que ensamblar las piezas explicitamente.

Es un trade-off que casi siempre vale la pena. El codigo compuesto es mas largo que el codigo heredado, pero es mas facil de entender, de modificar y de depurar. Y esas tres propiedades son las que determinan la productividad a largo plazo.

---

## Proyecto guia: refactorizando DevCourses de herencia a composicion

Volvamos a DevCourses. El sistema tiene tres areas donde la herencia esta causando problemas. Vamos a refactorizarlas usando composicion.

### Refactorizacion 1: Sistema de notificaciones

**Antes (herencia):**

```python
class Notificacion:
    def __init__(self, destinatario, mensaje):
        self.destinatario = destinatario
        self.mensaje = mensaje

    def enviar(self):
        raise NotImplementedError

class NotificacionEmail(Notificacion):
    def enviar(self):
        smtp.enviar(self.destinatario.email, self.mensaje)

class NotificacionPush(Notificacion):
    def enviar(self):
        firebase.enviar(self.destinatario.dispositivo, self.mensaje)

class NotificacionEmailConTemplate(NotificacionEmail):
    def __init__(self, destinatario, mensaje, template):
        super().__init__(destinatario, mensaje)
        self.template = template

    def enviar(self):
        cuerpo = self.template.renderizar(self.mensaje)
        smtp.enviar(self.destinatario.email, cuerpo)
```

Ya hay tres niveles de herencia y el sistema todavia es basico. Agregar SMS requiere otra rama. Agregar templates a Push requiere otra rama paralela. La jerarquia crece exponencialmente.

**Despues (composicion):**

```python
class Canal(ABC):
    @abstractmethod
    def enviar(self, destino: str, contenido: str) -> None: ...

class CanalEmail(Canal):
    def enviar(self, destino: str, contenido: str):
        smtp.enviar(destino, contenido)

class CanalPush(Canal):
    def enviar(self, destino: str, contenido: str):
        firebase.enviar(destino, contenido)

class CanalSMS(Canal):
    def enviar(self, destino: str, contenido: str):
        twilio.enviar(destino, contenido)

class Formateador(ABC):
    @abstractmethod
    def formatear(self, mensaje: str, contexto: dict) -> str: ...

class FormateadorPlano(Formateador):
    def formatear(self, mensaje: str, contexto: dict) -> str:
        return mensaje

class FormateadorTemplate(Formateador):
    def __init__(self, template: str):
        self._template = template

    def formatear(self, mensaje: str, contexto: dict) -> str:
        return self._template.format(mensaje=mensaje, **contexto)

class Notificador:
    def __init__(self, canal: Canal, formateador: Formateador):
        self._canal = canal
        self._formateador = formateador

    def enviar(self, destino: str, mensaje: str, contexto: dict = None):
        contenido = self._formateador.formatear(mensaje, contexto or {})
        self._canal.enviar(destino, contenido)
```

Ahora cualquier combinacion es posible:

```python
# Email con template
notificador_email = Notificador(CanalEmail(), FormateadorTemplate(template_bienvenida))

# Push con texto plano
notificador_push = Notificador(CanalPush(), FormateadorPlano())

# SMS con template
notificador_sms = Notificador(CanalSMS(), FormateadorTemplate(template_sms))
```

Tres canales y dos formateadores producen seis combinaciones sin crear seis clases. Y agregar un nuevo canal o un nuevo formateador no afecta a ninguno existente.

### Refactorizacion 2: Sistema de descuentos

**Antes (herencia):**

```python
class Descuento:
    def aplicar(self, precio: Decimal) -> Decimal:
        return precio

class DescuentoPorcentaje(Descuento):
    def __init__(self, porcentaje: int):
        self._porcentaje = porcentaje

    def aplicar(self, precio: Decimal) -> Decimal:
        return precio * (1 - self._porcentaje / 100)

class DescuentoFijo(Descuento):
    def __init__(self, monto: Decimal):
        self._monto = monto

    def aplicar(self, precio: Decimal) -> Decimal:
        return max(precio - self._monto, Decimal("0"))

# Que pasa cuando necesitas combinar descuentos?
# DescuentoPorcentajeYFijo? DescuentoDoble?
```

**Despues (composicion):**

```python
class Descuento(ABC):
    @abstractmethod
    def aplicar(self, precio: Decimal) -> Decimal: ...

class DescuentoPorcentaje(Descuento):
    def __init__(self, porcentaje: int):
        self._porcentaje = porcentaje

    def aplicar(self, precio: Decimal) -> Decimal:
        return precio * (1 - self._porcentaje / 100)

class DescuentoFijo(Descuento):
    def __init__(self, monto: Decimal):
        self._monto = monto

    def aplicar(self, precio: Decimal) -> Decimal:
        return max(precio - self._monto, Decimal("0"))

class DescuentoCompuesto(Descuento):
    """Aplica multiples descuentos en secuencia."""
    def __init__(self, *descuentos: Descuento):
        self._descuentos = descuentos

    def aplicar(self, precio: Decimal) -> Decimal:
        resultado = precio
        for d in self._descuentos:
            resultado = d.aplicar(resultado)
        return resultado

class DescuentoCondicional(Descuento):
    """Aplica un descuento solo si se cumple una condicion."""
    def __init__(self, condicion: Callable[[], bool], descuento: Descuento):
        self._condicion = condicion
        self._descuento = descuento

    def aplicar(self, precio: Decimal) -> Decimal:
        if self._condicion():
            return self._descuento.aplicar(precio)
        return precio
```

Ahora puedes crear reglas de descuento arbitrariamente complejas combinando piezas simples:

```python
# 20% de descuento + 5 dolares fijos en Black Friday
descuento_black_friday = DescuentoCompuesto(
    DescuentoPorcentaje(20),
    DescuentoFijo(Decimal("5"))
)

# 30% si es primera compra, si no 10%
descuento_nuevo_usuario = DescuentoCondicional(
    condicion=lambda: usuario.es_primera_compra(),
    descuento=DescuentoPorcentaje(30)
)

# Todo junto
descuento_final = DescuentoCompuesto(
    descuento_black_friday,
    descuento_nuevo_usuario
)

precio_final = descuento_final.aplicar(precio_base)
```

`DescuentoCompuesto` es el patron Composite: un descuento que contiene otros descuentos. `DescuentoCondicional` es el patron Decorator: un descuento que envuelve a otro y agrega una condicion. Ambos son composicion pura.

### Refactorizacion 3: Tipos de contenido (ya visto)

La tercera refactorizacion es la que mostramos antes: reemplazar la jerarquia de `Video`, `Texto`, `Quiz` por una composicion de `Contenido` + `Recurso` + `Complemento`. El resultado es un sistema donde los tipos de contenido se definen combinando partes, no heredando de una taxonomia rigida.

### Resultado de las tres refactorizaciones

| Aspecto | Antes (herencia) | Despues (composicion) |
|---|---|---|
| Clases totales | 11 clases en 3 jerarquias | 14 clases independientes |
| Combinaciones posibles | Limitadas por la jerarquia | Ilimitadas |
| Agregar nuevo tipo | Crear nueva subclase, posible herencia multiple | Crear nuevo componente, componer |
| Nivel maximo de herencia | 3 | 1 (interfaz -> implementacion) |
| Acoplamiento | Alto (cada subclase acoplada al padre) | Bajo (solo a la interfaz) |
| Facilidad de prueba | Media (necesitas setup del padre) | Alta (cada componente se prueba solo) |

Hay mas clases con composicion, pero cada una es mas simple, mas independiente y mas facil de entender. El aumento en cantidad es un trade-off que se paga con creces en flexibilidad y mantenibilidad.

---

## Composicion y los principios del libro

La composicion conecta con cada principio que hemos explorado:

**Ocultamiento de informacion (capitulo 6).** Cada componente compuesto oculta su implementacion detras de una interfaz. El `Notificador` no sabe como funciona el `CanalEmail` internamente. Solo sabe que tiene un metodo `enviar`. Eso es ocultamiento de informacion aplicado a la colaboracion entre objetos.

**Modulos profundos (capitulo 5).** Los componentes compuestos son modulos profundos: su interfaz es simple (un metodo, dos parametros) y su funcionalidad es rica (enviar por SMTP, formatear con templates, manejar errores). La composicion permite crear profundidad combinando modulos simples.

**Cohesion (capitulo 10).** Cada componente compuesto tiene cohesion funcional: `CanalEmail` solo se encarga de enviar emails. `FormateadorTemplate` solo se encarga de formatear. No hay mezcla de preocupaciones.

**Bajo acoplamiento (capitulo 10).** Los componentes se conectan a traves de interfaces abstractas, no de implementaciones concretas. El acoplamiento es de datos (bajo), no de contenido (alto). Cambiar una implementacion no afecta a los otros componentes.

**Capas (capitulo 11).** La composicion permite construir capas con diferentes niveles de abstraccion. El `Notificador` es una capa de orquestacion. El `Canal` es una capa de infraestructura. El `Formateador` es una capa de presentacion. Cada una trabaja con abstracciones diferentes.

La composicion no es un principio separado. Es la manifestacion practica de todos los principios operando juntos. Cuando ocultas informacion, creas componentes que se pueden componer. Cuando mantienes alta cohesion, los componentes son piezas independientes listas para combinar. Cuando minimizas el acoplamiento, las combinaciones posibles se multiplican.

---

## Aplica esto el lunes

1. **Busca una jerarquia de herencia de mas de dos niveles en tu proyecto.** Preguntate: las subclases estan acopladas a los detalles internos de la clase padre? Podrian ser objetos independientes que colaboran a traves de una interfaz? Si la respuesta a ambas es si, es un candidato para refactorizar hacia composicion.

2. **Identifica una funcion larga con multiples condicionales.** Puede descomponerse en funciones pequenas que se combinen con un pipeline o una lista de validadores? Intenta la refactorizacion y compara: el codigo compuesto es mas facil de extender?

3. **La proxima vez que necesites agregar funcionalidad a una clase, preguntate: herencia o composicion?** Si la funcionalidad nueva es un "comportamiento intercambiable" (diferentes formas de hacer lo mismo), usa Strategy. Si es funcionalidad adicional que se puede encender o apagar, usa un decorador funcional. Solo usa herencia si la relacion "es un" es genuina, estable y superficial.

4. **Refactoriza un caso de herencia hacia composicion.** Escoge el mas sencillo de tu proyecto. Reemplaza la relacion "es un" por "tiene un". Observa como cambia la testabilidad del codigo: cada componente deberia poder probarse de forma independiente, sin necesitar el setup de una jerarquia.

5. **Piensa en los objetos de tu sistema como Legos, no como muniequas rusas.** Las muniequas rusas (herencia) solo encajan de una manera: cada una dentro de la otra, en orden. Los Legos (composicion) encajan de infinitas maneras: cualquier pieza con cualquier otra. Cual de las dos metaforas describe mejor como deberia evolucionar tu sistema?

---

## Referencias del capitulo

- Gamma, E., Helm, R., Johnson, R. y Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
- Hickey, R. (2011). "Simple Made Easy." Strange Loop Conference.
- Hughes, J. (1989). "Why Functional Programming Matters." *The Computer Journal*, 32(2).
- Mikhajlov, L. y Sekerinski, E. (1998). "A Study of the Fragile Base Class Problem." *ECOOP 1998*. Lecture Notes in Computer Science, vol. 1445.
- Ousterhout, J. (2018). *A Philosophy of Software Design*. Yaknyam Press.
