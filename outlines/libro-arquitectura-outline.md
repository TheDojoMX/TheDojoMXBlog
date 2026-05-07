# Pensamiento Arquitectonico: Principios Atemporales para Disenar Software

## Outline Detallado Completo

**Autor:** Hector Patricio
**Estimacion total:** ~75,000-85,000 palabras (~300-340 paginas)
**Proyecto guia:** DevCourses -- Plataforma de cursos en linea

---

## PROYECTO GUIA: DevCourses

Una plataforma de cursos en linea para desarrolladores. Se construye progresivamente a lo largo del libro, empezando como un monolito y evolucionando conforme se aplican los principios.

**Contexto tecnico:**
- Equipo de 6 desarrolladores
- 50k usuarios activos/mes con picos x10 en lanzamientos
- Presupuesto acotado, time-to-market corto
- Stack: Python/FastAPI + PostgreSQL + Redis + S3 para video

**Modulos del sistema:**
1. Catalogo de cursos (listado, busqueda, recomendaciones)
2. Reproduccion de video (streaming, progreso, marcadores)
3. Sistema de pagos y suscripciones
4. Gestion de usuarios y perfiles
5. Comentarios y discusiones
6. Notificaciones
7. Panel de instructor (creacion de contenido, analytics)

**Evolucion a lo largo del libro:**
- Caps 1-3: El sistema nace como script monolitico sin estructura
- Caps 4-6: Se descompone en modulos, se definen interfaces
- Caps 7-9: Se profundizan los modulos, se oculta informacion
- Caps 10-12: Se aplican patrones, se manejan dependencias
- Caps 13-15: Se integran capas, se refina la arquitectura
- Cap 16: El sistema completo, revisado, con lecciones aprendidas

---

## PARTE I: FUNDAMENTOS -- POR QUE IMPORTA EL DISENO

---

### CAPITULO 1: El enemigo invisible: La complejidad

**Hook:** "Tu codigo funciona. Todas las pruebas pasan. El cliente esta contento. Entonces, por que cada nueva funcion tarda el doble que la anterior?"

**Takeaway principal:** La complejidad no es un evento sino una acumulacion. Identificarla es la primera habilidad que necesitas como disenador de software.

#### 1.1 Que es realmente la complejidad en el software
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Post base:** `tres-formas-de-identificar-la-caomplejidad-posd6.md`
- **Contenido nuevo:** Definicion ampliada con analogia de entropia termodinamica. Conexion con la cita de Kernighan y la definicion practica de Ousterhout. Comparacion con complejidad esencial vs accidental (Brooks).

#### 1.2 Tres sintomas de la complejidad
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~2,500
- **Post base:** `tres-formas-de-identificar-la-caomplejidad-posd6.md`
- **Contenido nuevo:** Cada sintoma con ejemplo concreto en DevCourses:
  - **Amplificacion de cambios:** Agregar un campo "idioma" al catalogo requiere tocar 12 archivos porque el formato de curso esta hardcodeado en multiples lugares.
  - **Carga cognitiva:** El modulo de pagos requiere entender el sistema de cache, la base de datos Y la API del procesador de pagos para hacer cualquier cambio.
  - **Desconocidos desconocidos:** Nadie sabe que cambiar el formato de fecha rompe el reporte de analytics porque depende de un parseo implicito.

#### 1.3 La formula de la complejidad: midiendo lo que importa
- **Tipo:** [PRINCIPIO] + [EJERCICIO]
- **Palabras:** ~1,200
- **Post base:** `tres-formas-de-identificar-la-caomplejidad-posd6.md`
- **Contenido nuevo:** Formula de Ousterhout (C = sum(cp * tp)) explicada con ejemplo numerico usando DevCourses. Ejercicio: calcula la complejidad de tu propio proyecto.

#### 1.4 Caso de estudio: DevCourses, el monolito sin estructura
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~1,500
- **Contenido nuevo:** Presentacion del proyecto guia. Codigo inicial: un solo archivo de 2,000 lineas que maneja catalogo, pagos y usuarios. Analisis de los tres sintomas presentes en este codigo.

#### 1.5 Anti-patron: "Si funciona, no lo toques"
- **Tipo:** [ANTI-PATRON]
- **Palabras:** ~800
- **Contenido nuevo:** La falacia de que el codigo que funciona no necesita mejoras. El costo oculto de la deuda tecnica acumulada. Grafica de velocidad de desarrollo vs tiempo.

#### Aplica esto el lunes
1. Identifica en tu proyecto actual un cambio reciente que requirio tocar mas de 3 archivos. Preguntate: era necesario o es un sintoma de amplificacion de cambios?
2. Escoge el modulo mas complejo de tu sistema. Escribe en una hoja todo lo que alguien nuevo necesita saber para hacer un cambio ahi. Si ocupa mas de media pagina, tienes un problema de carga cognitiva.
3. Preguntale a un companero: "Que pasaria si cambio X?" Si la respuesta es "no se", tienes un desconocido desconocido. Documentalo.

**Palabras totales capitulo:** ~7,500

---

### CAPITULO 2: Dos filosofias: Programacion tactica vs estrategica

**Hook:** "Imagina dos equipos que empiezan el mismo proyecto el mismo dia. En seis meses, uno entrega features cada semana. El otro lleva dos meses sin poder deployar. Que hicieron diferente?"

**Takeaway principal:** La programacion estrategica es una inversion que paga rendimientos compuestos. El codigo que funciona no es suficiente.

#### 2.1 El desarrollador tactico: velocidad a toda costa
- **Tipo:** [PRINCIPIO] + [ANTI-PATRON]
- **Palabras:** ~1,500
- **Post base:** `a-philosophy-of-software-design-programacion-tactica-vs-estrategica.md`
- **Contenido nuevo:** Perfil del desarrollador tactico. Presiones organizacionales que lo fomentan. Las cinco senales de alarma: hardcoding, duplicacion, abstracciones rotas, manejo de errores inexistente, codigo ilegible.

#### 2.2 El desarrollador estrategico: inversion en la base de codigo
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Post base:** `a-philosophy-of-software-design-programacion-tactica-vs-estrategica.md`
- **Contenido nuevo:** Practicas concretas del desarrollo estrategico: probar multiples implementaciones, documentar, limpiar codigo al tocarlo, pruebas unitarias, revision de codigo. La regla del 10-20% de inversion.

#### 2.3 La curva de cruce: cuando lo estrategico supera a lo tactico
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,200
- **Post base:** `a-philosophy-of-software-design-programacion-tactica-vs-estrategica.md`
- **Contenido nuevo:** Grafica detallada del cruce. Analogia de los tres cochinitos ampliada. Datos reales de proyectos que pasaron de tactico a estrategico. "Escalar no es cuestion de tecnologia, sino de diseno."

#### 2.4 Caso de estudio: DevCourses -- la deuda del MVP
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~1,500
- **Contenido nuevo:** El equipo lanzo DevCourses en 3 meses con enfoque tactico. Ahora agregar "cursos en paquete" (bundles) requiere 3 semanas. Analisis de que decisiones tacticas causaron esto. Plan de transicion a enfoque estrategico.

#### 2.5 Anti-patron: El perfeccionismo paralizante
- **Tipo:** [ANTI-PATRON]
- **Palabras:** ~800
- **Contenido nuevo:** El extremo opuesto: disenar tanto que nunca se entrega. El balance entre "lo suficientemente bueno" y "deuda tecnica consciente". Cuando SI conviene ser tactico (prototipos desechables, pruebas de concepto).

#### Aplica esto el lunes
1. Revisa tu ultimo commit. Fue tactico o estrategico? Si fue tactico, identifica una mejora que podrias haber hecho en 15 minutos extra.
2. Propone a tu equipo dedicar el 10% del sprint actual a mejorar una parte del codigo que todos temen tocar.
3. Identifica una decision tactica reciente que ya este generando problemas. Estima cuanto tiempo costaría arreglarla ahora vs cuanto costara en 6 meses.

**Palabras totales capitulo:** ~6,500

---

### CAPITULO 3: Principios, patrones y reglas: Una jerarquia para pensar

**Hook:** "Un desarrollador junior memoriza reglas. Un desarrollador mid aplica patrones. Un desarrollador senior entiende principios. Cual es la diferencia y por que importa?"

**Takeaway principal:** Los principios generan patrones, los patrones generan reglas. Entiende la jerarquia para saber cuando romper una regla.

#### 3.1 Que es un principio de diseno de software
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,200
- **Post base:** `principios-de-diseno-de-software.md`
- **Contenido nuevo:** Definicion de principio como "faro" (metafora del post). Diferencia con regla (especifica) y patron (solucion concreta). DRY y KISS como meta-principios.

#### 3.2 Los patrones: soluciones probadas a problemas recurrentes
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,500
- **Post base:** `patrones-de-diseno-que-son-y-cuando-usarlos.md`
- **Contenido nuevo:** Historia desde Christopher Alexander hasta GoF. Las 4 partes de un patron. Por que importa tener un vocabulario comun. Advertencia: los patrones son flaquezas del lenguaje (Peter Norvig).

#### 3.3 SOLID: util, pero no sagrado
- **Tipo:** [PRINCIPIO] + [ANTI-PATRON]
- **Palabras:** ~2,000
- **Post base:** `principios-de-diseno-de-software.md`, todos los posts de SOLID
- **Contenido nuevo:** Vision panoramica de SOLID como se trata en el resto del libro. La tesis central de Hector: los cinco principios se reducen a (1) codigo simple, (2) ocultar informacion, (3) pensar las abstracciones. Anticipacion de la critica de Dan North.

#### 3.4 El principio detras de los principios: Ocultar informacion
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Contenido nuevo:** Argumento de que "Information Hiding" (Parnas/Ousterhout) es el principio unificador detras de SOLID, cohesion/acoplamiento, y la mayoria de los buenos patrones. Esta es la tesis filosofica del libro.

#### 3.5 Ejercicio: Clasifica decisiones en tu proyecto
- **Tipo:** [EJERCICIO]
- **Palabras:** ~800
- **Contenido nuevo:** Ejercicio guiado: toma 5 decisiones de diseno de tu proyecto y clasificalas como principio, patron o regla. Identifica cual principio subyace a cada patron que usas.

#### Aplica esto el lunes
1. Escoge un patron de diseno que uses en tu proyecto. Preguntate: que principio subyace a este patron? Si no puedes responder, investigalo.
2. Identifica una "regla" de tu equipo (por ejemplo, "funciones de maximo 20 lineas"). Preguntate si la regla sirve al principio que intenta proteger, o si se ha convertido en dogma.
3. Lee la descripcion de tu modulo mas importante. Puede un nuevo integrante entender QUE hace sin ver COMO lo hace? Si no, tienes una fuga de informacion.

**Palabras totales capitulo:** ~7,000

---

## PARTE II: LOS MODULOS -- LA UNIDAD FUNDAMENTAL

---

### CAPITULO 4: Que es un modulo y por que descomponer

**Hook:** "Que es mas sencillo: subir 100 escalones de 15cm o dar un salto de 15 metros?"

**Takeaway principal:** Un modulo es cualquier construccion que encapsule una implementacion detras de una interfaz. Descomponer correctamente es la habilidad mas importante del disenador de software.

#### 4.1 Definicion amplia de modulo
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,200
- **Post base:** `a-philosophy-of-software-design-los-modulos-deben-ser-profundos.md`, `descomponiendo-tu-aplicacion-en-modulos.md`
- **Contenido nuevo:** Definicion unificada: funcion, clase, paquete, microservicio, API HTTP. Tabla de equivalencias entre lenguajes (Python: paquete; JS: modulo; Java: clase/paquete; Elixir: aplicacion; C: biblioteca).

#### 4.2 La interfaz: el contrato entre modulos
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,500
- **Post base:** `a-philosophy-of-software-design-los-modulos-deben-ser-profundos.md`
- **Contenido nuevo:** Interfaz formal (firma de funcion, tipos) vs interfaz informal (convenciones, efectos secundarios). Ejemplo: `open("archivo.md", "w")` como interfaz bien disenada. Interfaz como API interna.

#### 4.3 Dos criterios para descomponer: flujo vs especialidad
- **Tipo:** [PRINCIPIO] + [CASO DE ESTUDIO]
- **Palabras:** ~2,500
- **Post base:** `descomponiendo-tu-aplicacion-en-modulos.md`
- **Contenido nuevo:** Los dos criterios de Parnas. Ejemplo completo de la pasarela de pago (del post) como contraste. Analisis de ventajas y desventajas de cada enfoque. Por que "ocultar decisiones de diseno" casi siempre gana.

#### 4.4 Caso de estudio: DevCourses -- primera descomposicion
- **Tipo:** [CASO DE ESTUDIO] + [EJERCICIO]
- **Palabras:** ~2,000
- **Contenido nuevo:** Tomamos el monolito del capitulo 1 y lo descomponemos en 7 modulos. Primera iteracion: por flujo (recibir solicitud -> validar -> procesar pago -> dar acceso -> notificar). Segunda iteracion: por especialidad (catalogo, pagos, usuarios, video, notificaciones, comentarios, instructor). Comparacion de ambas.

#### 4.5 Anti-patron: La fragmentacion excesiva
- **Tipo:** [ANTI-PATRON]
- **Palabras:** ~800
- **Post base:** `cuando-separar-el-codigo.md` (apertura del post)
- **Contenido nuevo:** El mito de "funciones de 5 lineas". Codigo tan fragmentado que trazar la causa de un bug es imposible. El costo oculto de tener demasiadas interfaces.

#### Aplica esto el lunes
1. Dibuja en un papel los modulos de tu sistema actual. Para cada uno, escribe en una oracion que decision de diseno oculta. Si no puedes, ese modulo probablemente esta mal definido.
2. Identifica dos modulos en tu sistema que siempre se cambian juntos. Preguntate si deberian ser uno solo.
3. Toma una funcion de mas de 100 lineas. No la rompas automaticamente. Primero pregunta: las partes resultantes serian realmente independientes?

**Palabras totales capitulo:** ~8,000

---

### CAPITULO 5: Modulos profundos -- el ideal de diseno

**Hook:** "Una television tiene dos botones en el control remoto que te dan acceso a miles de canales. Un formulario de impuestos tiene 200 campos para calcular un solo numero. Cual es el buen diseno?"

**Takeaway principal:** Un modulo profundo oculta gran funcionalidad detras de una interfaz sencilla. Este es el objetivo de todo buen diseno.

#### 5.1 La metafora del rectangulo: interfaz vs funcionalidad
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Post base:** `a-philosophy-of-software-design-los-modulos-deben-ser-profundos.md`
- **Contenido nuevo:** Explicacion detallada con diagrama. Modulo profundo = base estrecha, altura grande. Modulo superficial = base ancha, poca altura. Cuantificacion: ratio funcionalidad/interfaz.

#### 5.2 Ejemplos de modulos profundos y superficiales
- **Tipo:** [EJEMPLO]
- **Palabras:** ~2,000
- **Post base:** `a-philosophy-of-software-design-los-modulos-deben-ser-profundos.md`
- **Contenido nuevo:**
  - **Profundos:** `open()` en Unix, el garbage collector, un ORM bien disenado, el protocolo HTTP, `Array.sort()`.
  - **Superficiales:** Getters/setters en Java, funciones wrapper que solo delegan, clases con un solo metodo de una linea.
  - Para cada uno: diagrama de rectangulo, analisis del ratio.

#### 5.3 Ventajas concretas de la profundidad
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,200
- **Post base:** `a-philosophy-of-software-design-los-modulos-deben-ser-profundos.md`
- **Contenido nuevo:** Reutilizacion, evitar acumulacion de interfaces, evitar expansion de cambios, ocultar mayor complejidad. Conexion con la carga cognitiva del capitulo 1.

#### 5.4 Caso de estudio: DevCourses -- profundizando el modulo de pagos
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~2,000
- **Contenido nuevo:** El modulo de pagos de DevCourses empieza superficial: `procesar_pago(usuario_id, curso_id, monto, moneda, metodo_pago, token_tarjeta, direccion, codigo_postal, pais, cupon_codigo, es_recurrente, periodo_suscripcion)`. Lo transformamos en profundo: `procesar_pago(usuario_id, curso_id)` donde el modulo internamente resuelve todo lo demas. Codigo antes y despues.

#### 5.5 Modulos de proposito general vs especifico
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~2,000
- **Post base:** `a-philosophy-of-software-design-crea-modulos-de-proposito-general.md`
- **Contenido nuevo:** El continuo de especificidad (Nokia charger vs USB). Ejemplo del editor de texto: `insertar_texto`, `borrar_texto`, `mover_cursor` vs funciones especificas para cada operacion. La regla: "tan general como puedas sin dificultar el uso actual." Ejemplo en DevCourses: `registrar_publicacion()` vs `registrar_curso()`, `registrar_leccion()`, `registrar_quiz()`.

#### 5.6 Anti-patron: La clase dios
- **Tipo:** [ANTI-PATRON]
- **Palabras:** ~800
- **Post base:** `a-philosophy-of-software-design-recomendaciones-disenio-modular.md`
- **Contenido nuevo:** Cuando el modulo profundo se convierte en modulo omnisciente. Senales de alarma. Diferencia entre profundo y dios.

#### Aplica esto el lunes
1. Toma la funcion publica mas usada de tu proyecto. Cuenta sus parametros. Podrias reducirlos a la mitad con defaults inteligentes?
2. Busca un getter o setter en tu codigo que no haga nada mas que devolver un valor. Preguntate: agrega valor esta interfaz?
3. Identifica un modulo superficial (mucha interfaz, poca funcionalidad). Disena en papel como lo harias profundo.

**Palabras totales capitulo:** ~9,500

---

### CAPITULO 6: Ocultar informacion -- la clave de todo

**Hook:** "Cuantas veces has mirado el codigo fuente de `print()` o `console.log()`? Probablemente nunca. Y eso es exactamente lo que hace que funcionen tan bien."

**Takeaway principal:** El trabajo principal de un modulo es ocultar informacion. Si dominas esto, dominas el diseno de software.

#### 6.1 El principio de ocultamiento de informacion (Parnas)
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Post base:** `a-philosophy-of-software-design-ocultar-informacion.md`
- **Contenido nuevo:** Historia de David Parnas y el articulo de 1972. La idea central: "cada modulo debe encapsular decisiones de diseno." Conexion con la tesis del libro.

#### 6.2 Fugas de informacion: cuando la implementacion se escapa
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~2,000
- **Post base:** `a-philosophy-of-software-design-ocultar-informacion.md`
- **Contenido nuevo:** Definicion de fuga de informacion: "una decision de diseno reflejada en multiples modulos". Ejemplo de la API del clima (del post) ampliado. Ejemplo nuevo en DevCourses: el modulo de video expone el formato de almacenamiento de S3 a los controladores, creando acoplamiento.

#### 6.3 Descomposicion temporal: la fuga silenciosa
- **Tipo:** [PRINCIPIO] + [ANTI-PATRON]
- **Palabras:** ~2,000
- **Post base:** `a-philosophy-of-software-design-descomposicion-temporal.md`
- **Contenido nuevo:** Definicion y ejemplos de Ousterhout (protocolo HTTP, lectura/escritura de archivos). Ejemplo en Elixir con composicion funcional mal aplicada (del post). Ejemplo nuevo en DevCourses: separar "validar inscripcion" y "procesar inscripcion" en dos clases cuando ambas necesitan entender las reglas de inscripcion.

#### 6.4 Recomendaciones practicas para ocultar informacion
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~2,000
- **Post base:** `a-philosophy-of-software-design-recomendaciones-disenio-modular.md`
- **Contenido nuevo:**
  - Exponer lo menos posible estructuras de datos internas
  - Defaults utiles (la mejor funcion es la que no sabes que existe)
  - Aislar dentro de las clases y paquetes
  - No ocultar informacion que SI se necesita afuera
  - Ejemplo de mensajeria multi-canal (del post) extendido

#### 6.5 Caso de estudio: DevCourses -- sellando las fugas
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~1,500
- **Contenido nuevo:** Identificamos 4 fugas de informacion en DevCourses:
  1. El controlador sabe que los videos estan en S3
  2. El frontend parsea directamente el formato de fecha de la BD
  3. Dos modulos saben como calcular descuentos
  4. El orden de llamadas entre modulos esta hardcodeado
  - Para cada una: diagnostico y solucion.

#### 6.6 Ejercicio: Auditoria de fugas
- **Tipo:** [EJERCICIO]
- **Palabras:** ~500
- **Contenido nuevo:** Checklist de 10 preguntas para auditar fugas de informacion en cualquier modulo. Template para documentar fugas encontradas.

#### Aplica esto el lunes
1. Escoge un modulo de tu sistema. Preguntate: "Si cambio la implementacion interna completamente, que codigo externo se rompe?" Todo lo que se rompe es una fuga.
2. Revisa las estructuras de datos que tu modulo expone. Alguna revela detalles internos de implementacion? Disenala de nuevo para ser independiente.
3. Busca dos piezas de codigo que siempre se llaman en secuencia. Es descomposicion temporal? Podrian ser un solo modulo?

**Palabras totales capitulo:** ~9,500

---

### CAPITULO 7: Cuando separar y cuando juntar

**Hook:** "Todo el mundo habla de separar codigo, pero nadie habla de cuando juntarlo. Y a veces, juntar es exactamente lo correcto."

**Takeaway principal:** La guia para separar o juntar codigo es simple: escoge la estructura que genere menores dependencias, oculte mejor el conocimiento y cree interfaces mas simples.

#### 7.1 El falso evangelio de lo pequeno
- **Tipo:** [ANTI-PATRON]
- **Palabras:** ~1,200
- **Post base:** `cuando-separar-el-codigo.md`
- **Contenido nuevo:** Critica a la regla de "funciones cortas". Codigo fragmentado = complejidad por cantidad de interfaces. La paradoja: romper para simplificar puede complicar.

#### 7.2 Cuando dejarlo junto: cuatro criterios
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~2,000
- **Post base:** `cuando-separar-el-codigo.md`
- **Contenido nuevo:** Los criterios de Ousterhout ampliados:
  1. **Acceso a la informacion:** Si comparten la misma informacion, juntos.
  2. **Cercania semantica:** Si se categorizan bajo la misma idea, juntos.
  3. **Dependencia:** Si siempre se usan juntos, juntos.
  4. **Eliminacion de duplicacion:** Si juntarlos elimina duplicacion, juntos.
  - Bonus: si juntarlos elimina interfaces, es buena senal.

#### 7.3 Cuando separar: el criterio del nivel de abstraccion
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,500
- **Post base:** `cuando-separar-el-codigo.md`
- **Contenido nuevo:** Codigo general vs especifico no deben convivir. Ejemplo del editor de texto (insercion general vs seleccion visual especifica). Conexion con capas (proximo capitulo).

#### 7.4 Caso de estudio: DevCourses -- el modulo de UNDO/historial
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~2,000
- **Post base:** `cuando-separar-el-codigo.md` (ejemplo de UNDO)
- **Contenido nuevo:** El instructor de DevCourses necesita "deshacer" cambios en el editor de cursos. Diseno 1: historial dentro del editor. Diseno 2: modulo de Historia independiente con acciones autocontenidas. Analisis de por que el segundo es mejor. Codigo completo.

#### 7.5 La regla de oro para decidir
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~800
- **Contenido nuevo:** Diagrama de decision: "Escoge la estructura que (1) genere menores dependencias, (2) oculte mejor el conocimiento, (3) cree interfaces mas simples." Flowchart visual.

#### Aplica esto el lunes
1. Busca dos funciones en tu proyecto que siempre se llaman una despues de la otra. Deberian ser una sola?
2. Busca una funcion larga. Antes de romperla, preguntate: las partes resultantes serian realmente independientes o siempre se usarian juntas?
3. Identifica un caso de duplicacion en tu codigo. Pero antes de extraerlo a una funcion comun, preguntate: las dos copias realmente hacen lo mismo o solo se parecen superficialmente?

**Palabras totales capitulo:** ~7,500

---

## PARTE III: PRINCIPIOS EN ACCION

---

### CAPITULO 8: SOLID desmenuzado -- lo que realmente importa

**Hook:** "Los principios SOLID se tratan como los mandamientos del software. Pero que pasa si te digo que los cinco se reducen a tres ideas?"

**Takeaway principal:** SOLID son aplicaciones particulares de principios mas profundos: simplicidad, ocultamiento de informacion y abstraccion. Entiende los fundamentos y SOLID se vuelve intuitivo.

#### 8.1 Responsabilidad Unica: es sobre informacion, no sobre "hacer una cosa"
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~2,000
- **Post base:** `analisis-de-los-principios-solid-principio-de-responsabilidad-unica.md`
- **Contenido nuevo:** El problema de la ambiguedad de "responsabilidad". La transformacion de Hector: de responsabilidad a informacion. Las 4 preguntas para aplicarlo (del post). Ejemplo en DevCourses: el modulo de inscripcion maneja validacion, pago Y notificacion. Cuales son las "decisiones de diseno" que deberia encapsular?

#### 8.2 Abierto/Cerrado: extension sin miedo
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~2,000
- **Post base:** `el-principio-abierto-cerrado-open-closed.md`
- **Contenido nuevo:** Ejemplo de metodos de pago con polimorfismo (del post). Aplicacion a nivel arquitectonico (del post). Conexion con Variacion Protegida de Cockburn. Ejemplo en DevCourses: agregar un nuevo tipo de contenido (podcast) sin modificar el catalogo existente. La camara con lentes intercambiables.

#### 8.3 Sustitucion de Liskov: tipos, no herencia
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,800
- **Post base:** `el-principio-de-substitucion-de-liskov.md`
- **Contenido nuevo:** Barbara Liskov y tipos abstractos de datos. El ejemplo de la camara (del post). Por que esto NO es solo sobre herencia de clases. Ejemplo en DevCourses: diferentes tipos de suscripcion (mensual, anual, corporativa) como subtipos del ADT Suscripcion.

#### 8.4 Segregacion de Interfaces: interfaces simples, no infinitas
- **Tipo:** [PRINCIPIO] + [ANTI-PATRON]
- **Palabras:** ~1,500
- **Post base:** `el-principio-de-segregacion-de-interfaces.md`
- **Contenido nuevo:** El formulario que pregunta por tus hijos (analogia del post). El peligro de llevarlo al extremo: explosion de interfaces. Los consejos de Ousterhout como equilibrio. Ejemplo en DevCourses: la interfaz de Mensaje para notificaciones multi-canal.

#### 8.5 Inversion de Dependencias: util, pero con cuidado
- **Tipo:** [PRINCIPIO] + [ANTI-PATRON]
- **Palabras:** ~2,000
- **Post base:** `el-principio-de-inversion-de-dependencias.md`
- **Contenido nuevo:** La critica de Dan North: "miles de millones de dolares desperdiciados". "La mayoria de las dependencias no necesitan invertirse." Cuando SI conviene (conexion a multiples APIs) vs cuando NO (la mayoria de los casos). DI, IoC y Service Locator explicados y criticados. Ejemplo en DevCourses: el procesador de pagos SI necesita inversion (Stripe, PayPal, MercadoPago). El modulo de usuarios NO.

#### 8.6 La sintesis: tres principios detras de cinco
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,000
- **Post base:** Conclusion de `el-principio-de-inversion-de-dependencias.md`
- **Contenido nuevo:** Tabla que mapea cada principio SOLID a sus fundamentos: (1) Codigo simple, (2) Ocultar informacion, (3) Buenas abstracciones. La invitacion de Dan North: escribir codigo simple centrado en el uso.

#### Aplica esto el lunes
1. Identifica una clase o modulo con mas de una "razon para cambiar". Pero en vez de dividirla automaticamente, preguntate: que informacion deberia ocultar cada parte?
2. Encuentra un lugar en tu codigo donde necesitaste modificar codigo existente para agregar funcionalidad. Podrias haberlo disenado para extender sin modificar?
3. Busca un caso de inversion de dependencias en tu proyecto. Es realmente necesario o esta sobredisenado?

**Palabras totales capitulo:** ~10,300

---

### CAPITULO 9: Cohesion, acoplamiento y composicion

**Hook:** "Por que cambiar el color de un boton rompio el sistema de pagos? Porque el acoplamiento es un asesino silencioso."

**Takeaway principal:** Alta cohesion y bajo acoplamiento no son metricas abstractas: son la diferencia entre un sistema que evoluciona y uno que se estanca.

#### 9.1 Cohesion: todo lo relacionado junto
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,800
- **Post base:** `entendiendo-la-cohesion-y-el-acoplamiento-en-el-software.md`
- **Contenido nuevo:** Definicion de Constantine (anos 60). Ejemplo del chatbot multi-canal (del post). La formula: agrupar todo lo que tiene que ver con la misma abstraccion o decision. Ejemplo en DevCourses: el modulo de catalogo tiene alta cohesion si contiene busqueda, filtrado, categorias y recomendaciones basicas.

#### 9.2 Acoplamiento: lo que necesitas saber de otro para entender este
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~2,000
- **Post base:** `entendiendo-la-cohesion-y-el-acoplamiento-en-el-software.md`
- **Contenido nuevo:** Los 4 factores de acoplamiento de Constantine (tipo de conexion, complejidad de interfaz, tipo de informacion, tiempo). Ejemplo del ecommerce (del post). Ejemplo en DevCourses: el modulo de comentarios esta acoplado al de usuarios porque accede directamente a la tabla de usuarios en vez de usar su interfaz.

#### 9.3 La relacion inversa: mas cohesion, menos acoplamiento
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~800
- **Post base:** `entendiendo-la-cohesion-y-el-acoplamiento-en-el-software.md`
- **Contenido nuevo:** La cita de Constantine y Yourdon. Diagrama visual. "Un modulo autocontenido necesita menos de los demas."

#### 9.4 Composicion: el arte de juntar piezas
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~2,500
- **Post base:** `composicion-en-el-software.md`
- **Contenido nuevo:**
  - **Composicion de funciones:** Validador de contrasenas (del post). Pipeline de transformaciones.
  - **Composicion de objetos:** "Tiene un" vs "Es un". Usuario/Empleado (del post).
  - **Composicion vs herencia:** Por que "tiene un" casi siempre gana.
  - Cita de John Hughes: "Nuestra habilidad para descomponer depende de nuestra habilidad para combinar."
  - Ejemplo en DevCourses: Curso compuesto de Lecciones, que a su vez estan compuestas de Contenidos (video, texto, quiz). Composicion, no herencia.

#### 9.5 Caso de estudio: DevCourses -- midiendo cohesion y acoplamiento
- **Tipo:** [CASO DE ESTUDIO] + [EJERCICIO]
- **Palabras:** ~1,500
- **Contenido nuevo:** Tabla de los 7 modulos de DevCourses. Para cada uno: que tan cohesivo es (1-5), que tan acoplado esta con los demas (1-5). Identificacion de los 3 puntos mas criticos. Plan de mejora.

#### Aplica esto el lunes
1. Dibuja un mapa de dependencias de tus modulos. Donde estan los puntos con mas flechas entrantes y salientes? Esos son tus puntos de mayor acoplamiento.
2. Para un modulo, lista todos sus metodos/funciones publicos. Todos trabajan hacia el mismo objetivo? Si hay "outliers", probablemente tienen baja cohesion.
3. Busca un caso de herencia en tu codigo. Podrias reemplazarlo por composicion? Disenalo en papel.

**Palabras totales capitulo:** ~8,600

---

### CAPITULO 10: Sistemas en capas y arquitecturas por niveles

**Hook:** "Todos usamos MVC, pero cuantos entienden POR QUE funciona?"

**Takeaway principal:** Cada capa debe trabajar con abstracciones diferentes. Si la abstraccion no cambia entre capas, algo esta mal.

#### 10.1 Por que funcionan los sistemas en capas
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Post base:** `a-philosophy-of-software-design-organiza-bien-los-sistemas-en-capas.md`
- **Contenido nuevo:** Desde MVC hasta hexagonal. La idea central: cada componente solo habla con la capa superior e inferior. Ejemplo del sistema de archivos (del post): archivo -> bloques de memoria -> disco.

#### 10.2 Diferente capa, diferente abstraccion
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~2,000
- **Post base:** `a-philosophy-of-software-design-organiza-bien-los-sistemas-en-capas.md`
- **Contenido nuevo:** La regla fundamental de Ousterhout. Ejemplo del editor de texto: interfaz usa "caracteres", implementacion usa "lineas" (del post). Ejemplo en DevCourses: capa API expone "cursos" como JSON, capa de servicio trabaja con objetos de dominio, capa de persistencia trabaja con registros SQL. Tres abstracciones diferentes.

#### 10.3 Funciones de paso y variables pasadas: anti-patrones de capas
- **Tipo:** [ANTI-PATRON]
- **Palabras:** ~1,500
- **Post base:** `a-philosophy-of-software-design-organiza-bien-los-sistemas-en-capas.md`
- **Contenido nuevo:** Funciones que solo delegan. Variables que viajan sin transformarse. Decoradores sobreusados. Cada uno con ejemplo y solucion. En DevCourses: el controlador de cursos solo llama al servicio de cursos que solo llama al repositorio. Solucion: eliminar la capa intermedia vacia.

#### 10.4 Caso de estudio: DevCourses -- diseno en capas
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~2,000
- **Contenido nuevo:** Disenamos la arquitectura en capas de DevCourses:
  - Capa API (FastAPI routes): abstracciones HTTP, request/response
  - Capa de Servicio: logica de negocio, orquestacion
  - Capa de Dominio: entidades y reglas de negocio
  - Capa de Infraestructura: BD, S3, APIs externas
  - Para cada capa: que abstraccion maneja, que oculta. Diagrama completo.

#### 10.5 Mas alla de MVC: hexagonal, vertical slices y bounded contexts
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Post base:** `aplicando-los-grados-de-diseno-de-software-guia-practica.md`
- **Contenido nuevo:** Breve introduccion a arquitectura hexagonal (ports & adapters), vertical slices y bounded contexts de DDD. No como recetas a seguir, sino como aplicaciones del principio de capas. Cuando usar cual. Advertencia de Sasa Juric: "no hagas algo porque un lider de opinion lo dice."

#### Aplica esto el lunes
1. Identifica las capas de tu sistema. Para cada una, escribe en una oracion que abstraccion maneja. Si dos capas manejan la misma abstraccion, algo esta mal.
2. Busca una funcion de paso en tu codigo (una que solo llama a otra). Necesita existir?
3. Busca una variable que se pasa a traves de 3 o mas capas sin ser transformada. Hay una forma de eliminar ese viaje?

**Palabras totales capitulo:** ~8,500

---

## PARTE IV: LA CALIDAD EN LA PRACTICA

---

### CAPITULO 11: Claridad -- el codigo como comunicacion

**Hook:** "Cuando escribi este codigo solo Dios y yo sabiamos lo que hacia. Ahora solo Dios sabe. Esta broma esconde una verdad aterradora sobre tu base de codigo."

**Takeaway principal:** La claridad es mas concreta y util que "codigo limpio". El codigo es una herramienta de comunicacion con otros seres humanos.

#### 11.1 Claridad sobre limpieza: la leccion de Sasa Juric
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Post base:** `claridad-en-el-codigo.md`
- **Contenido nuevo:** Definicion de claridad: "que tan bien una pieza de codigo comunica sus verdaderas intenciones." Por que es mejor que "codigo limpio" (mas concreto, menos dogmatico). La claridad da poder al equipo.

#### 11.2 Nombres que comunican
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,500
- **Post base:** `consistencia-en-el-codigo.md`
- **Contenido nuevo:** Nombrado consistente en estilo y semantica. El ejemplo de `ticket` vs `bill` vs `entrance_ticket` (del post). Variables de un solo caracter: cuando si y cuando no. En DevCourses: vocabulario comun del dominio (Curso, Leccion, Inscripcion, Suscripcion) definido en un glosario.

#### 11.3 Consistencia: el lubricante del entendimiento
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Post base:** `consistencia-en-el-codigo.md`
- **Contenido nuevo:** Consistencia en nombres, interfaces, patrones e invariantes (del post). Herramientas: linters, documentacion, ejemplo personal. El costo de romper la consistencia: cuando vale la pena y cuando no.

#### 11.4 Comentarios como herramienta de diseno
- **Tipo:** [PRINCIPIO] + [ANTI-PATRON]
- **Palabras:** ~2,500
- **Post base:** `deberias-comentar-tu-codigo.md`
- **Contenido nuevo:**
  - Por que el lenguaje no es suficiente para expresar todo
  - Escribe los comentarios primero (como herramienta de diseno, a la TDD)
  - Comenta la interfaz, no la implementacion
  - Anti-patron: comentarios que repiten lo que el codigo dice
  - La regla: si no puedes escribir un comentario conciso, redisena
  - En DevCourses: documentacion de la API del modulo de pagos, con docstrings que guiaron el diseno.

#### 11.5 Revision de codigo como practica de claridad
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,000
- **Post base:** `claridad-en-el-codigo.md`
- **Contenido nuevo:** El foco del code review debe ser la claridad. Reglas para el autor (PRs pequenos, commits pequenos) y para el revisor (senalar donde no entiende, sugerir mejoras). Sesiones de pair programming para desbloquear.

#### 11.6 Caso de estudio: DevCourses -- guia de estilo y claridad
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~1,000
- **Contenido nuevo:** El equipo de DevCourses crea: (1) Glosario de dominio, (2) Guia de nombrado, (3) Template de docstrings para interfaces, (4) Checklist de code review centrada en claridad. Ejemplo de una PR antes y despues de aplicar estas practicas.

#### Aplica esto el lunes
1. Lee una funcion que escribiste hace mas de 3 meses. La entiendes en menos de 2 minutos? Si no, reescribela para que sea clara.
2. En tu proxima PR, antes de escribir codigo, escribe los comentarios de interfaz primero. Te ayudo a pensar mejor en el diseno?
3. En tu proximo code review, enfocate exclusivamente en claridad. Senala cada punto donde te costo entender que pasa.

**Palabras totales capitulo:** ~9,000

---

### CAPITULO 12: Testing como herramienta de diseno

**Hook:** "Si tu test necesita 15 mocks para funcionar, el problema no es el test. Es tu diseno."

**Takeaway principal:** Los tests deben probar comportamiento, no implementacion. Un test dificil de escribir es una senal de mal diseno.

#### 12.1 Tests como detector de complejidad
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Contenido nuevo:** Si un modulo es dificil de testear, probablemente esta mal disenado. Los tests como "primer usuario" de tu interfaz. Conexion con modulos profundos: un modulo profundo es facil de testear.

#### 12.2 Prueba el comportamiento, no la implementacion
- **Tipo:** [PRINCIPIO] + [ANTI-PATRON]
- **Palabras:** ~1,500
- **Post base:** `claridad-en-el-codigo.md` (seccion de testing de Sasa Juric)
- **Contenido nuevo:** Las unidades son de comportamiento, no de codigo. Mocks agresivos como anti-patron. Tests fragiles que se rompen con refactoring. En DevCourses: test del modulo de inscripcion que verifica "el usuario puede ver el curso despues de inscribirse" vs test que verifica "se llamo al metodo X con parametro Y".

#### 12.3 Tests como documentacion viva
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,200
- **Contenido nuevo:** Un buen test es una especificacion ejecutable. Nombrado de tests como oraciones legibles. En DevCourses: `test_usuario_con_suscripcion_activa_puede_acceder_a_cualquier_curso()`.

#### 12.4 Estrategia de testing para DevCourses
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~2,000
- **Contenido nuevo:** Piramide de tests para DevCourses: unitarias por invariantes de dominio, de integracion por contratos entre modulos, E2E para flujos criticos (inscripcion, pago, reproduccion). Ejemplo de cada tipo. Por que NO testeamos cada metodo individual.

#### 12.5 Anti-patron: el test que testea el framework
- **Tipo:** [ANTI-PATRON]
- **Palabras:** ~800
- **Contenido nuevo:** Tests que verifican que Django guarde en la BD, que FastAPI parsee JSON, etc. Cuando un test no agrega valor. La regla: testea TU logica, no la del framework.

#### Aplica esto el lunes
1. Busca el test con mas mocks en tu proyecto. Cuantos mocks tiene? Si son mas de 3, preguntate si el codigo bajo test esta bien disenado.
2. Lee los nombres de tus tests. Un nuevo integrante del equipo podria entender que hace el sistema solo leyendolos?
3. Identifica un test que se rompe cada vez que refactorizas. Es un test de implementacion, no de comportamiento. Reescribelo.

**Palabras totales capitulo:** ~7,000

---

### CAPITULO 13: Estandares y calidad del codigo en equipo

**Hook:** "Un equipo sin estandares es como una orquesta sin partitura: cada quien toca su propio tema y el resultado es ruido."

**Takeaway principal:** Los estandares no son restricciones: son acuerdos que multiplican la capacidad del equipo.

#### 13.1 Por que los estandares importan
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,200
- **Post base:** `estandares-de-calidad-en-el-software.md`
- **Contenido nuevo:** Deteccion temprana de fallas, reduccion de complejidad, codigo legible, onboarding rapido. Datos reales: reduccion del 40-60% en incidencias.

#### 13.2 Como implementar estandares sin paralizar al equipo
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,500
- **Post base:** `estandares-de-calidad-en-el-software.md`
- **Contenido nuevo:** "Roma no fue construida en un dia." Migracion progresiva. Automatizacion con linters y hooks. Documentacion como acuerdo vivo. En DevCourses: setup de pre-commit hooks, ruff para Python, guia de estilo inicial.

#### 13.3 Metricas que importan y metricas que distraen
- **Tipo:** [PRINCIPIO] + [ANTI-PATRON]
- **Palabras:** ~1,500
- **Contenido nuevo:** Metricas utiles: complejidad ciclomatica, acoplamiento entre modulos, cobertura de tests como guia (no como objetivo). Metricas daninas: lineas de codigo, numero de commits, "code coverage" como KPI. En DevCourses: dashboard de calidad con las metricas correctas.

#### 13.4 Caso de estudio: DevCourses -- el pacto de calidad del equipo
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~1,500
- **Contenido nuevo:** El equipo de DevCourses crea su "pacto de calidad": (1) guia de estilo automatizada, (2) reglas de code review, (3) ADRs para decisiones importantes, (4) retrospectiva trimestral de arquitectura. Plantilla de ADR incluida.

#### Aplica esto el lunes
1. Identifica una regla de estilo que tu equipo sigue informalmente pero no esta documentada. Documentala y automatizala.
2. Revisa tus metricas de calidad. Alguna es un "vanity metric" que no refleja calidad real? Eliminala.
3. Propone a tu equipo una sesion de 30 minutos para definir 5 estandares basicos que todos acuerden seguir.

**Palabras totales capitulo:** ~5,700

---

## PARTE V: ARQUITECTURA Y VISION GLOBAL

---

### CAPITULO 14: Los cuatro niveles de diseno

**Hook:** "Disenar software no es una sola actividad. Son cuatro actividades diferentes en cuatro niveles distintos, y confundirlas es la causa del 80% de los problemas arquitectonicos."

**Takeaway principal:** Distingue entre arquitectura de soluciones, arquitectura de software, diseno de sistemas y diseno de codigo. Cada nivel tiene sus propias herramientas y artefactos.

#### 14.1 Mapa de los cuatro niveles
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Post base:** `aplicando-los-grados-de-diseno-de-software-guia-practica.md`
- **Contenido nuevo:** Los 4 niveles:
  1. Arquitectura de soluciones: que construir y por que
  2. Arquitectura de software: atributos de calidad y decisiones estructurales
  3. Diseno de sistemas: topologia, datos, contratos, escala
  4. Diseno de codigo: modulos, APIs, patrones, pruebas
  - Entregables tipicos de cada nivel. Diagrama visual.

#### 14.2 Nivel 1: Arquitectura de soluciones
- **Tipo:** [PRINCIPIO] + [CASO DE ESTUDIO]
- **Palabras:** ~2,000
- **Post base:** `aplicando-los-grados-de-diseno-de-software-guia-practica.md`
- **Contenido nuevo:** Entradas, decisiones, artefactos, validacion. Anti-patron: decidir por moda tecnologica. En DevCourses: objetivos de negocio (activacion, retencion, conversion), mapa de stakeholders, decision build vs buy para video y pagos.

#### 14.3 Nivel 2: Arquitectura de software
- **Tipo:** [PRINCIPIO] + [CASO DE ESTUDIO]
- **Palabras:** ~2,000
- **Post base:** `aplicando-los-grados-de-diseno-de-software-guia-practica.md`
- **Contenido nuevo:** NFRs como escenarios medibles. ADRs. Diagramas C4 nivel 2. Trade-offs. En DevCourses: ADR "monolito modular en vez de microservicios", escenarios de latencia y disponibilidad, diagrama C4 completo.

#### 14.4 Nivel 3: Diseno de sistemas
- **Tipo:** [PRINCIPIO] + [CASO DE ESTUDIO]
- **Palabras:** ~2,000
- **Post base:** `aplicando-los-grados-de-diseno-de-software-guia-practica.md`
- **Contenido nuevo:** Contratos API, modelo de datos, diagramas de secuencia, estrategias de escala. En DevCourses: diagrama de secuencia para "compra + acceso a curso", definicion de 3 contratos API.

#### 14.5 Nivel 4: Diseno de codigo (lo que cubre este libro)
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,000
- **Post base:** `aplicando-los-grados-de-diseno-de-software-guia-practica.md`
- **Contenido nuevo:** Conexion con todo lo visto en el libro. Organizacion por dominio, APIs y errores como parte del contrato, pruebas por invariantes. El diseno de codigo es donde los principios atemporales se aplican diariamente.

#### 14.6 Integracion entre niveles
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,000
- **Contenido nuevo:** Los niveles no son independientes. Cambios en NFRs deben reflejarse en ADRs, C4 y codigo. Documentacion viva. Revisiones trimestrales.

#### Aplica esto el lunes
1. Identifica en que nivel opera la mayor parte de tu trabajo diario. Es donde mas impacto puedes tener? Si no, sube o baja un nivel.
2. Escribe un ADR para la decision arquitectonica mas reciente de tu equipo. Incluye: contexto, decision, alternativas consideradas, consecuencias.
3. Dibuja un diagrama C4 nivel 2 de tu sistema actual. Donde estan los limites mas difusos? Esos son tus proximos puntos de mejora.

**Palabras totales capitulo:** ~9,500

---

### CAPITULO 15: Diseno evolutivo -- el software que crece bien

**Hook:** "El unico software que no cambia es el software muerto. Si tu sistema esta vivo, necesitas disenarlo para el cambio."

**Takeaway principal:** El buen diseno no es estatico. Es la capacidad de evolucionar sin acumular complejidad descontrolada.

#### 15.1 El diseno no se hace una vez
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,200
- **Contenido nuevo:** El mito del Big Design Up Front. Diseno emergente vs diseno inexistente. El equilibrio: decidir lo suficiente para empezar, refinar continuamente. Conexion con desarrollo estrategico (cap 2).

#### 15.2 Decisiones reversibles e irreversibles
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,500
- **Contenido nuevo:** Las puertas de una via y dos vias (Jeff Bezos). Decisiones irreversibles (base de datos, lenguaje, arquitectura distribuida) merecen mas analisis. Decisiones reversibles (nombre de variable, patron especifico) se toman rapido. En DevCourses: la decision de usar PostgreSQL es irreversible; la estructura interna de un modulo es reversible.

#### 15.3 Refactoring como practica de diseno
- **Tipo:** [PRINCIPIO] + [EJEMPLO]
- **Palabras:** ~1,500
- **Contenido nuevo:** Refactoring no es "limpiar codigo los viernes". Es mejorar el diseno continuamente. La regla de los boy scouts. Cuando refactorizar (cada vez que tocas el codigo) vs cuando reescribir (casi nunca). En DevCourses: refactoring del modulo de catalogo cuando se agrega busqueda full-text.

#### 15.4 Manejo del cambio: proteger los puntos de extension
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,200
- **Contenido nuevo:** Conexion con Open/Closed. Identificar los puntos del sistema que mas probablemente cambiaran. Disenarlos con interfaces extensibles. En DevCourses: el sistema de contenido disenado para agregar nuevos tipos (video, texto, quiz, podcast) sin tocar el core.

#### 15.5 Caso de estudio: DevCourses -- de MVP a plataforma madura
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~2,500
- **Contenido nuevo:** La evolucion completa de DevCourses desde el monolito del capitulo 1 hasta la arquitectura del capitulo 14. Timeline de decisiones, refactorings clave y lecciones aprendidas. Que hariamos diferente sabiendo lo que sabemos ahora. Diagrama final de la arquitectura.

#### 15.6 Anti-patron: El segundo sistema
- **Tipo:** [ANTI-PATRON]
- **Palabras:** ~800
- **Contenido nuevo:** El "efecto del segundo sistema" de Brooks: la tentacion de sobredisenar la version 2.0. "Es mas facil hacerlo de nuevo" casi siempre es falso. La alternativa: evolucionar incrementalmente.

#### Aplica esto el lunes
1. Identifica la decision arquitectonica mas irreversible de tu proyecto. Esta documentada? Entiendes por que se tomo? Si no, documentala ahora.
2. La proxima vez que toques un archivo, mejora una cosa pequena: un nombre, un comentario, una estructura. Practica la regla del boy scout.
3. Identifica los 3 puntos de tu sistema que mas probablemente cambiaran en los proximos 6 meses. Estan disenados para acomodar ese cambio?

**Palabras totales capitulo:** ~8,700

---

## PARTE VI: CIERRE Y REFERENCIA

---

### CAPITULO 16: El pensamiento arquitectonico -- juntando todo

**Hook:** "Despues de 15 capitulos de principios, patrones y ejemplos, cual es el minimo que necesitas recordar el lunes por la manana?"

**Takeaway principal:** El pensamiento arquitectonico no es un conjunto de reglas. Es una forma de ver el codigo: como un sistema de modulos que ocultan informacion detras de interfaces simples.

#### 16.1 Los 7 principios atemporales (resumen)
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~2,000
- **Contenido nuevo:** Destilacion de todo el libro en 7 principios:
  1. La complejidad es el enemigo. Identifica sus sintomas.
  2. Invierte en el diseno (programacion estrategica).
  3. Descompone por especialidad, no por flujo.
  4. Crea modulos profundos: mucha funcionalidad, interfaz simple.
  5. Oculta informacion: el trabajo de todo modulo.
  6. Diferente capa, diferente abstraccion.
  7. Escribe codigo claro que comunique sus intenciones.

#### 16.2 DevCourses: el sistema completo
- **Tipo:** [CASO DE ESTUDIO]
- **Palabras:** ~2,000
- **Contenido nuevo:** Diagrama final completo de DevCourses. Tour por los 7 modulos mostrando como cada principio se aplico. Metricas de antes vs despues: tiempo para agregar features, bugs por sprint, onboarding de nuevos devs.

#### 16.3 Quick Reference Card
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,500
- **Contenido nuevo:** Tarjeta de referencia rapida de doble cara con:
  - Los 7 principios con definicion de una linea
  - Checklist de diseno de modulos (5 preguntas)
  - Checklist de deteccion de complejidad (5 preguntas)
  - Senales de alarma (5 anti-patrones)
  - Decision tree: separar o juntar?
  - Decision tree: profundo o superficial?

#### 16.4 Mapa de lecturas recomendadas
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~1,000
- **Contenido nuevo:** Ruta de lectura organizada por nivel:
  - **Esencial:** A Philosophy of Software Design (Ousterhout), Clean Code (Martin)
  - **Intermedio:** Design Patterns (GoF), Structured Design (Constantine & Yourdon)
  - **Avanzado:** Release It!, Team Topologies, Accelerate
  - **Papers:** Parnas 1972, Liskov & Wing 1994
  - Para cada recurso: que aporta y cuando leerlo.

#### 16.5 Carta al lector: el diseno es una practica
- **Tipo:** [PRINCIPIO]
- **Palabras:** ~800
- **Contenido nuevo:** El diseno de software se aprende con practica, practica y mas practica (Constantine & Yourdon). No existe el diseno perfecto. Siempre podras mejorar. La invitacion: aplica un principio el lunes, reflexiona el viernes, repite.

#### Aplica esto el lunes (final)
1. Imprime o guarda la Quick Reference Card. Consúltala antes de cada decision de diseno esta semana.
2. Escoge UN principio del libro que no apliques actualmente. Comprometete a aplicarlo en tu proximo feature.
3. Agenda una sesion de 30 minutos con tu equipo para discutir: "Cual es el modulo mas complejo de nuestro sistema y que podemos hacer al respecto?"

**Palabras totales capitulo:** ~7,300

---

## APENDICES

### Apendice A: Glosario de terminos
- **Palabras:** ~1,500
- Definiciones concisas de: modulo, interfaz, abstraccion, cohesion, acoplamiento, complejidad, fuga de informacion, descomposicion temporal, modulo profundo/superficial, ADR, NFR, etc.

### Apendice B: Quick Reference Card (version imprimible)
- **Palabras:** ~500
- Formato de una pagina, lista para imprimir y pegar junto al monitor.

### Apendice C: Plantillas
- **Palabras:** ~1,000
- Plantilla de ADR
- Plantilla de escenario de calidad
- Checklist de auditoria de fugas de informacion
- Template de code review centrado en claridad

### Apendice D: DevCourses -- codigo fuente completo de referencia
- **Palabras:** ~1,000
- Enlace a repositorio con la implementacion de referencia. Estructura de directorios. Guia de navegacion del codigo por capitulo.

---

## RESUMEN DE METRICAS

| Parte | Capitulos | Palabras estimadas |
|-------|-----------|-------------------|
| I: Fundamentos | 1-3 | ~21,000 |
| II: Los modulos | 4-7 | ~34,500 |
| III: Principios en accion | 8-10 | ~27,400 |
| IV: Calidad en la practica | 11-13 | ~21,700 |
| V: Arquitectura y vision global | 14-15 | ~18,200 |
| VI: Cierre y referencia | 16 | ~7,300 |
| Apendices | A-D | ~4,000 |
| **Total** | **16 + apendices** | **~80,100** |

---

## MAPA DE POSTS DEL BLOG -> CAPITULOS

| Post del blog | Capitulo(s) donde se usa |
|---------------|------------------------|
| `tres-formas-de-identificar-la-caomplejidad-posd6.md` | 1 |
| `a-philosophy-of-software-design-programacion-tactica-vs-estrategica.md` | 2 |
| `principios-de-diseno-de-software.md` | 3 |
| `patrones-de-diseno-que-son-y-cuando-usarlos.md` | 3 |
| `a-philosophy-of-software-design-los-modulos-deben-ser-profundos.md` | 4, 5 |
| `descomponiendo-tu-aplicacion-en-modulos.md` | 4 |
| `a-philosophy-of-software-design-crea-modulos-de-proposito-general.md` | 5 |
| `a-philosophy-of-software-design-ocultar-informacion.md` | 6 |
| `a-philosophy-of-software-design-descomposicion-temporal.md` | 6 |
| `a-philosophy-of-software-design-recomendaciones-disenio-modular.md` | 5, 6 |
| `cuando-separar-el-codigo.md` | 7 |
| `analisis-de-los-principios-solid-principio-de-responsabilidad-unica.md` | 8 |
| `el-principio-abierto-cerrado-open-closed.md` | 8 |
| `el-principio-de-substitucion-de-liskov.md` | 8 |
| `el-principio-de-segregacion-de-interfaces.md` | 8 |
| `el-principio-de-inversion-de-dependencias.md` | 8 |
| `entendiendo-la-cohesion-y-el-acoplamiento-en-el-software.md` | 9 |
| `composicion-en-el-software.md` | 9 |
| `a-philosophy-of-software-design-organiza-bien-los-sistemas-en-capas.md` | 10 |
| `claridad-en-el-codigo.md` | 11, 12 |
| `consistencia-en-el-codigo.md` | 11 |
| `deberias-comentar-tu-codigo.md` | 11 |
| `estandares-de-calidad-en-el-software.md` | 13 |
| `aplicando-los-grados-de-diseno-de-software-guia-practica.md` | 14 |

---

## CONTENIDO NUEVO REQUERIDO (no cubierto por posts existentes)

1. **Proyecto guia completo (DevCourses):** Todos los casos de estudio, codigo de ejemplo y evoluciones progresivas. Estimacion: ~15,000 palabras de contenido nuevo.

2. **Testing como herramienta de diseno (Cap 12):** Capitulo completamente nuevo. No hay posts de blog sobre testing. Estimacion: ~7,000 palabras.

3. **Diseno evolutivo (Cap 15):** Capitulo mayormente nuevo. Solo hay fragmentos en el post de programacion tactica/estrategica. Estimacion: ~6,000 palabras.

4. **Los cuatro niveles de diseno (Cap 14):** Basado en un post draft no publicado. Necesita expansion significativa. Estimacion: ~5,000 palabras nuevas.

5. **Quick Reference Card y apendices:** Todo nuevo. Estimacion: ~4,000 palabras.

6. **Anti-patrones y ejercicios:** Distribuidos por todo el libro. Mayormente nuevos. Estimacion: ~8,000 palabras.

7. **Secciones "Aplica esto el lunes":** Todas nuevas. 16 secciones x ~150 palabras = ~2,400 palabras.

8. **Hooks y takeaways:** Todos nuevos. 16 capitulos x ~100 palabras = ~1,600 palabras.

**Total contenido nuevo estimado:** ~49,000 palabras (~61% del libro)
**Total contenido basado en posts:** ~31,000 palabras (~39% del libro, expandido y reescrito)
