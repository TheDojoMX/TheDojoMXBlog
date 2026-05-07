# Capitulo 3: Programacion tactica vs. estrategica

> "Resolver el ticket de hoy puede arruinar el proyecto de manana."

---

## La tentacion de lo inmediato

Carlos, el lider tecnico de DevCourses, tiene un problema. El equipo de producto acaba de subir la prioridad de tres tickets que necesitan salir esta semana: agregar soporte para cupones con porcentaje variable, permitir pagos en pesos mexicanos ademas de dolares, y mostrar el progreso del estudiante en la pagina de inicio. Son tres cambios que, en teoria, no deberian tomar mas de dos dias cada uno.

Carlos mira el codigo. La funcion `comprar_curso()` que vimos en los capitulos anteriores -- esas 50 lineas que saben todo sobre todo -- es el punto de entrada para los tres cambios. Los cupones con porcentaje variable implican agregar logica condicional a la seccion de cupones. El soporte para pesos mexicanos requiere una conversion de moneda antes de llamar a Stripe. Y el progreso del estudiante necesita una consulta adicional a la tabla de accesos.

Carlos tiene dos opciones. La primera: hacer los tres cambios directamente en `comprar_curso()` y en los archivos donde haga falta, lo mas rapido posible. Agregar un `if` aqui, una consulta alla, un parametro extra por aca. Quizas duplicar algo de logica porque "no hay tiempo para refactorizar". La segunda: invertir medio dia en separar la logica de cupones en su propio modulo, crear una capa de abstraccion para las monedas, y definir una interfaz limpia para el progreso del estudiante antes de implementar los tres cambios.

La primera opcion es rapida. Carlos calcula que puede terminar los tres tickets en dos dias. La segunda opcion es mas lenta al principio -- quizas cuatro dias para los tres tickets -- pero dejaria el sistema en mejor estado para los cambios que vendran.

Carlos elige la primera opcion. Siempre hay presion. Siempre hay prisa. Y los tres tickets salen a tiempo.

Dos meses despues, Diana necesita agregar un cuarto metodo de pago: MercadoPago. La funcion `comprar_curso()` ahora tiene 120 lineas. La logica de cupones esta entrelazada con la logica de monedas. La conversion de pesos a dolares esta hardcodeada en tres lugares diferentes. Y nadie recuerda por que hay un `if moneda == "MXN" and cupon and cupon["tipo"] == "porcentaje"` en la linea 87.

Diana estima una semana. Le toma tres.

Esta historia ilustra las dos filosofias fundamentales que todo desarrollador y todo equipo enfrenta cada dia: la programacion tactica y la programacion estrategica. Son dos formas de pensar, dos actitudes frente al codigo, y dos caminos que divergen mas con cada decision [Ousterhout, 2018].

**Takeaway:** Cada tarea de programacion implica una eleccion: resolver solo el problema inmediato o resolver el problema inmediato *y* mejorar el sistema. Esa eleccion, repetida cientos de veces, define la trayectoria de tu proyecto.

---

## La mentalidad tactica: que funcione y ya

El programador tactico tiene un objetivo claro: que el codigo funcione lo mas rapido posible. No es que sea incompetente ni que no le importe la calidad. Es que su marco mental esta centrado en la tarea inmediata. El ticket. El sprint. La fecha de entrega. La demo del viernes.

Ousterhout describe al programador tactico asi:

> "Para el programador tactico, el objetivo principal es hacer que algo funcione: una nueva funcionalidad, una correccion de bug. A primera vista esto suena razonable. Pero el problema es que la programacion tactica es miope." [Ousterhout, 2018]

Las senales de la mentalidad tactica son reconocibles. Si has trabajado en software el tiempo suficiente, las has visto todas. Probablemente las has practicado:

### Senal 1: El hardcoding rapido

"Solo se usa en un lugar. No tiene caso hacerlo configurable."

Asi empieza. Un URL hardcodeado. Un porcentaje de descuento fijo. Un nombre de tabla directamente en la consulta SQL. Cada instancia es insignificante. Pero cuando tienes 50 valores hardcodeados dispersos en el codigo, cambiar cualquiera de ellos se convierte en una busqueda arqueologica.

En DevCourses, Ernesto hardcodeo la comision de Stripe al 2.9% + 30 centavos en la funcion de compra. Cuando Stripe cambio su estructura de precios para Mexico (3.6% + $3 MXN), el equipo descubrio que la comision estaba escrita literalmente en cuatro archivos diferentes: la funcion de compra, el modulo de reportes financieros, el calculo de ganancias del instructor, y el script de conciliacion mensual.

### Senal 2: La duplicacion defensiva

"La funcion original hace casi lo que necesito, pero no exactamente. Voy a copiarla y modificar la copia."

La duplicacion es el refugio del programador con prisa. Es mas rapido copiar 30 lineas y cambiar 3 que entender como generalizar la funcion original para que sirva en ambos casos. Pero ahora tienes dos funciones que hacen casi lo mismo. Y cuando descubras un bug en la logica compartida, tendras que recordar arreglarlo en ambas. (No lo recordaras.)

### Senal 3: El parametro adicional

"Solo necesito agregar un parametro mas a esta funcion."

La funcion empezo con 3 parametros. Despues de seis meses de desarrollo tactico, tiene 11. Tres de ellos son booleanos que nadie recuerda que significan. Uno es un string que puede ser `"normal"`, `"bundle"`, `"suscripcion"`, o `"regalo"`. Y hay un parametro llamado `extra_data` que es un diccionario generico donde se mete todo lo que no cabe en los otros parametros.

### Senal 4: El manejo de errores inexistente

"Si falla, ya veremos."

El try-catch que envuelve todo el bloque. El `except Exception as e: pass`. El error que se loggea pero no se maneja. Cada uno de estos es una bomba de tiempo silenciosa. No explota hoy. Explota a las 3am de un sabado, cuando el desarrollador de guardia tiene que entender por que los pagos no se estan procesando y el unico mensaje en los logs dice "Error procesando compra".

### Senal 5: La abstraccion rota

"Tecnicamente, el modulo de pagos no deberia saber sobre el formato de los emails, pero necesito el titulo del curso para la confirmacion, y la forma mas rapida es importar el modelo directamente."

Cada vez que rompes una frontera entre modulos por conveniencia, creas una dependencia que sera invisible para el siguiente desarrollador. Es como tender un cable electrico por el suelo de una oficina: la primera semana nadie se tropieza. La decima semana, alguien se cae.

### Por que la mentalidad tactica es tan atractiva

La programacion tactica no es un defecto de caracter. Es una respuesta racional a incentivos reales:

- **Presion de negocio.** Los stakeholders quieren resultados ahora, no promesas de que el sistema sera mas facil de cambiar en seis meses.
- **Sistemas de estimacion.** Los sprints de dos semanas penalizan el trabajo que no produce funcionalidades visibles. "Refactorizar el modulo de pagos" no aparece en el roadmap del producto.
- **Retroalimentacion inmediata.** Cuando terminas un ticket, hay una satisfaccion tangible. Cuando inviertes tiempo en disenar una mejor abstraccion, la recompensa es diferida e invisible.
- **Cultura del equipo.** Si todos programan tacticamente, el que intenta hacerlo estrategicamente parece "lento". La presion social refuerza el ciclo.

Ousterhout lo resume con dureza:

> "Casi todos los programadores que he conocido son, en algun grado, tacticos. [...] El enfoque tactico produce un camino rapido al primer release, pero eventualmente las complejidades se acumulan, y la productividad colapsa." [Ousterhout, 2018]

**Takeaway:** La programacion tactica no es maldad ni incompetencia. Es la respuesta natural a incentivos de corto plazo. Pero cada atajo tactico deposita un poco de complejidad accidental en la base de codigo, y esos depositos acumulan intereses.

---

## La mentalidad estrategica: invertir en el futuro del codigo

El programador estrategico tiene un objetivo diferente: si, que el codigo funcione, pero *tambien* que el sistema sea un poco mejor despues de cada cambio. Kent Beck lo capturo en una frase que se ha vuelto casi un mantra:

> "Haz que funcione, haz que sea correcto, haz que sea rapido." [Beck, 2002]

Nota el orden. Primero funciona. Pero no te detienes ahi. Despues de que funciona, lo haces *correcto* -- que significa legible, bien estructurado, con buenas abstracciones, con las dependencias correctas. Y solo entonces, si hace falta, lo optimizas.

La mentalidad estrategica no significa disenar todo por adelantado. No es cascada. No es pasar dos semanas dibujando diagramas UML antes de escribir una linea. Es algo mucho mas practico y cotidiano:

> "El objetivo de la programacion estrategica no es solo hacer que funcione. Lo mas importante es producir un gran diseno, que ademas resulta que funciona. La programacion estrategica requiere una mentalidad de inversion." [Ousterhout, 2018]

### La regla del 10-20%

Ousterhout propone una regla simple y concreta: invierte entre el 10% y el 20% de tu tiempo de desarrollo en mejoras de diseno [Ousterhout, 2018]. No el 50%. No "todo un sprint de refactorizacion". Un 10-20% continuo y sostenido.

En terminos practicos, si un ticket te toma 5 horas, dedica entre 30 minutos y una hora a dejar el codigo mejor de como lo encontraste. Eso puede significar:

- Extraer una funcion que deberia existir pero no existe
- Renombrar una variable cuyo nombre ya no refleja lo que contiene
- Agregar un test para el caso limite que acabas de descubrir
- Documentar una dependencia que no era obvia
- Eliminar codigo muerto que encontraste mientras trabajabas
- Simplificar una condicion compleja que acabas de entender

Ninguna de estas acciones es glamorosa. Ninguna aparece en un changelog. Pero en seis meses, la diferencia entre un equipo que invierte su 10-20% y uno que no lo hace es abismal.

### Como funciona la inversion compuesta

La razon por la que el 10-20% funciona es el mismo principio del interes compuesto en finanzas. Cada pequena mejora facilita la siguiente. Si hoy extraes una funcion limpia para la validacion de cupones, manana cuando necesites modificar la logica de cupones, solo tienes que tocar un archivo en vez de tres. Eso te ahorra 30 minutos. Esos 30 minutos los inviertes en mejorar otra parte del sistema. Y asi sucesivamente.

Ousterhout lo expresa asi:

> "Las inversiones que haces en buen diseno se pagan relativamente rapido. Los modulos que definiste cuidadosamente al principio del proyecto te ahorraran tiempo despues cuando los reutilices una y otra vez." [Ousterhout, 2018]

El equipo de Google que mantiene Abseil (su biblioteca central de C++) es un ejemplo institucional de esta filosofia. Cada cambio que entra al repositorio debe dejar el codigo al menos tan bueno como estaba, y preferiblemente mejor. El resultado es una biblioteca que ha sido usada por miles de proyectos internos durante mas de una decada sin acumular la deuda tecnica que paraliza a otros proyectos de esa edad.

### Practicas concretas del desarrollo estrategico

La mentalidad estrategica se traduce en habitos especificos:

**1. Probar multiples implementaciones antes de elegir.** Antes de comprometerte con una interfaz, escribe dos o tres versiones rapidas. No tienen que estar terminadas -- solo lo suficiente para ver como se sienten desde el lado del usuario. Esto toma 20-30 minutos extra, pero te ahorra semanas de refactorizacion cuando descubres que la interfaz no funciona para el caso de uso numero cuatro.

**2. Limpiar el codigo cada que lo tocas.** Los boy scouts tienen una regla: deja el campamento mas limpio de como lo encontraste. Aplicalo al codigo. Si abres un archivo para hacer un cambio y ves una variable con nombre confuso, renombrala. Si ves codigo muerto, eliminalo. Si ves un comentario desactualizado, actualizalo. Cada limpieza toma segundos. El efecto acumulativo es enorme.

**3. Escribir pruebas como parte del trabajo, no como tarea separada.** Las pruebas no son un "extra" que haces cuando hay tiempo. Son parte de la implementacion. Una funcion sin tests es una funcion que nadie se atrevera a modificar con confianza.

**4. Hacer code review con intencion de diseno.** No solo busques bugs en el review. Pregunta: "Esta solucion deja el sistema en mejor estado? Introduce dependencias nuevas? Se podria simplificar la interfaz?"

**5. Documentar las decisiones, no solo el codigo.** Un comentario que dice `# Calcula el descuento` es inutil. Un comentario que dice `# Usamos porcentaje en vez de monto fijo porque los cupones internacionales necesitan ajustarse por moneda` es invaluable. El primero describe *que* hace el codigo (que ya es obvio). El segundo explica *por que* se tomo esa decision (que no es obvio).

**Takeaway:** La programacion estrategica no es perfeccionismo. Es la disciplina de invertir un 10-20% continuo en mejorar el diseno con cada tarea. Es interes compuesto aplicado al codigo.

---

## La curva de cruce: cuando lo estrategico supera a lo tactico

Si el enfoque tactico es mas rapido al principio y el estrategico es mas lento, la pregunta obvia es: cuando se cruzan?

Ousterhout presenta un modelo mental que es simple pero poderoso. Imaginemos dos equipos que empiezan el mismo proyecto el mismo dia:

- **Equipo Tactico:** Prioriza velocidad. No invierte en diseno. Cada ticket se resuelve de la forma mas directa posible.
- **Equipo Estrategico:** Invierte 10-20% en diseno. Cada ticket tarda un poco mas, pero el sistema se mantiene limpio.

Al principio, el Equipo Tactico va adelante. Entrega mas funciones. El Product Manager esta contento. El CEO muestra la demo a los inversionistas. Todo bien.

Pero la curva de productividad del Equipo Tactico no es lineal. Es una curva que desciende. Cada nueva funcion tarda un poco mas que la anterior porque la complejidad accidental se acumula. El costo de entender el codigo sube. Los bugs se multiplican. Los estimados se inflan.

La curva del Equipo Estrategico empieza mas lenta pero se mantiene estable. El costo de agregar una funcion nueva no crece (o crece muy poco) porque el sistema esta disenado para absorber cambios.

En algun punto, las curvas se cruzan. A partir de ese momento, el Equipo Estrategico es mas rapido que el Tactico. Y la brecha crece con el tiempo.

Segun las estimaciones de Ousterhout, el cruce ocurre sorprendentemente pronto -- entre 6 y 12 meses [Ousterhout, 2018]. No anos. Meses.

Es la historia de los tres cochinitos en version software. El primer cochinito construye su casa de paja (enfoque tactico extremo). Terminan rapido, pero el primer viento fuerte -- un cambio de requisitos, un pico de trafico, un nuevo integrante del equipo -- la derrumba. El segundo construye con madera (tactico con algo de cuidado). Aguanta mas, pero eventualmente tambien cede. El tercero construye con ladrillo (enfoque estrategico). Tarda mas al inicio, pero su casa resiste. Y cuando llega el momento de agregar un segundo piso, puede hacerlo sin reconstruir los cimientos.

La analogia falla en un punto importante: en software, siempre puedes reforzar la casa despues de construirla. Puedes pasar de tactico a estrategico. Pero el costo de la transicion es directamente proporcional a cuanta deuda acumulaste.

**Takeaway:** La programacion estrategica supera a la tactica en productividad acumulada entre los 6 y los 12 meses. El momento del cruce depende de la tasa de cambio del proyecto -- cuanto mas rapido cambia, antes se cruzan las curvas.

---

## El costo real de la deuda tecnica (con numeros)

La metafora de la "deuda tecnica" fue acunada por Ward Cunningham en 1992. Como toda metafora financiera, tiene un poder explicativo enorme: la deuda tecnica, como la deuda financiera, genera intereses. Cada dia que pasa sin pagarla, el costo crece.

Pero a diferencia de la deuda financiera, la deuda tecnica no aparece en ningun balance contable. Es invisible para los stakeholders, para los gerentes de proyecto, y a veces hasta para los propios desarrolladores que la estan generando. Asi que pongamosle numeros.

### Los datos globales

Segun un analisis de CAST de 2025 que cubrio 47,000 aplicaciones, el rezago acumulado de deuda tecnica a nivel global alcanzo 61 mil millones de dias-hombre de trabajo [CAST, 2025]. Una investigacion de Sonar en 2025 estimo que las organizaciones gastan en promedio el 30% de sus presupuestos de TI en gestionar deuda tecnica existente [Sonar, 2025]. Un analisis de McKinsey del mismo periodo mostro que los equipos con alta deuda tecnica tardan un 40% mas en entregar funcionalidades comparados con equipos de baja deuda [McKinsey, 2025].

Gartner proyecta que para 2026, el 80% de toda la deuda tecnica sera *arquitectonica* -- no bugs puntuales ni codigo feo, sino decisiones de diseno a nivel de sistema que requieren rediseno estructural para resolverse [Gartner, 2025].

### El costo para un equipo real

Traduzcamos esto a numeros que puedas sentir.

Imagina un equipo de 8 desarrolladores. Salario promedio: $80,000 dolares anuales (incluyendo prestaciones y costos de operacion, el costo real para la empresa es alrededor de $120,000 por persona). Costo total del equipo: $960,000 dolares al ano.

Si el equipo gasta el 33% de su tiempo en deuda tecnica (el promedio de la industria segun CAST), eso equivale a $316,800 dolares anuales. Es como tener casi tres desarrolladores trabajando tiempo completo no en construir valor nuevo, sino en pelear contra decisiones pasadas.

Pero la historia se pone peor. A medida que la deuda crece, el porcentaje sube. En bases de codigo mal mantenidas, la cifra puede llegar al 50-80%. Para nuestro equipo hipotetico de 8 personas, eso significa que entre 4 y 6 personas estan, efectivamente, trabajando para la deuda y no para el producto.

Y hay costos que no aparecen en la hoja de calculo:

- **Costo de onboarding.** Un desarrollador nuevo en un sistema con alta deuda tarda significativamente mas en ser productivo. La investigacion muestra que para un equipo que contrata 10 ingenieros al ano, la diferencia entre onboarding "moderado" y onboarding "pesado" (causado por deuda tecnica) equivale a entre $200,000 y $400,000 dolares en productividad perdida [FlagShark, 2025].
- **Costo de rotacion.** Los buenos desarrolladores se van de proyectos con deuda tecnica severa. El costo de reemplazar un desarrollador senior es de 6-9 meses de su salario.
- **Costo de oportunidad.** Cada hora que el equipo pasa peleando con codigo viejo es una hora que no pasa construyendo la funcion que podria duplicar los ingresos.

### La trampa del "ya lo arreglaremos despues"

Hay una frase que todo desarrollador ha dicho o escuchado: "Vamos a sacarlo asi por ahora y despues lo arreglamos." Es el eslogan no oficial de la programacion tactica.

El problema es que "despues" casi nunca llega. Y cuando llega, el costo es mucho mayor que si se hubiera hecho bien desde el principio. La razon es que la deuda tecnica tiene intereses compuestos:

1. **Dia 1:** Hardcodeas la comision de Stripe. Costo de arreglarlo: 15 minutos.
2. **Mes 3:** Alguien copia la logica a otro archivo. Ahora son dos lugares. Costo: 45 minutos (encontrar ambos, asegurar que el cambio es consistente, testear ambos).
3. **Mes 6:** Un tercer archivo usa el valor, y alguien escribio un test que verifica contra el valor hardcodeado. Costo: 2 horas.
4. **Mes 12:** El valor esta en 5 archivos, hay tests que dependen de el, hay un reporte financiero que lo usa para calcular proyecciones, y nadie recuerda todos los lugares. Costo: 1-2 dias.

De 15 minutos a 2 dias. Eso es un crecimiento de 60x en un ano. Y eso es por *un solo* valor hardcodeado. Multiplica por las docenas de decisiones tacticas que un equipo toma cada semana.

**Takeaway:** La deuda tecnica no es gratuita. Equipos promedio gastan un tercio de su tiempo pagando intereses sobre ella. Y como toda deuda con intereses compuestos, cuanto mas tardas en pagarla, mas cara se vuelve.

---

## Por que los startups tambien necesitan pensamiento estrategico

Hay un argumento que escucho con frecuencia, especialmente en el ecosistema de startups latinoamericano: "No podemos darnos el lujo de invertir en diseno. Necesitamos salir al mercado antes de que se acabe el dinero."

Es un argumento comprensible. Una startup con 18 meses de runway tiene una presion existencial que una empresa establecida no tiene. Cada dia que no lanzas es un dia que quemas capital sin generar ingresos. En ese contexto, la programacion tactica parece no solo razonable, sino obligatoria.

Pero el argumento tiene un error fatal: asume que la programacion estrategica es significativamente mas lenta que la tactica. Y la evidencia muestra que no lo es -- al menos, no en la magnitud que la gente asume.

Ousterhout estima que el overhead del enfoque estrategico es de 10-20% [Ousterhout, 2018]. En el peor caso, un 20% adicional. Si tu MVP tactico tomaria 3 meses, el MVP estrategico tomaria 3.6 meses. Esas tres semanas extra no son la diferencia entre sobrevivir y morir para la gran mayoria de los startups.

Pero aqui esta lo que si puede ser la diferencia entre sobrevivir y morir: la velocidad a la que puedes iterar *despues* del lanzamiento. Los startups no ganan con el MVP. Ganan con la iteracion 5, 10, 20 -- cuando han incorporado el feedback de los usuarios y han pivoteado tres veces. Y cada iteracion es mas rapida o mas lenta dependiendo de cuanta deuda tecnica acumulaste en las iteraciones anteriores.

Facebook es un ejemplo que Ousterhout analiza explicitamente. La compania adopto el lema "Move fast and break things" como filosofia de ingenieria durante sus primeros anos -- una declaracion explicita de programacion tactica. Funciono inicialmente: Facebook crecio a una velocidad explosiva. Pero eventualmente la deuda tecnica se acumulo hasta el punto de que "moverse rapido" se volvio imposible. En 2014, Mark Zuckerberg cambio el lema a "Move fast with stable infrastructure" [Ousterhout, 2018]. La compania tuvo que invertir *anos* en pagar la deuda que habia acumulado durante su fase tactica.

Si Facebook -- con recursos practicamente ilimitados -- tuvo que frenar para pagar su deuda tecnica, un startup con 6 desarrolladores y 18 meses de runway no puede darse el lujo de *no* pensar estrategicamente. Porque cuando la deuda tecnica se acumule y necesiten pivotar, no van a tener los miles de ingenieros que Facebook tenia para la limpieza.

### Cuando SI conviene ser tactico

Dicho todo esto, hay escenarios en los que el enfoque tactico es la decision correcta:

- **Prototipos desechables.** Si estas construyendo algo explicitamente para validar una hipotesis y lo vas a tirar despues, no tiene sentido invertir en diseno. La clave es la palabra "explicitamente": si hay la mas minima posibilidad de que el prototipo se convierta en el producto, invierte en diseno.
- **Pruebas de concepto.** Similar a los prototipos, pero orientadas a viabilidad tecnica. "Podemos integrar este servicio?" No necesita diseno impecable.
- **Codigo con fecha de caducidad.** Scripts de migracion de datos, herramientas de una sola vez, hacks para una promocion temporal. Si sabes con certeza que el codigo morira en un mes, el enfoque tactico es sensato.

La trampa esta en que mucho codigo que "era temporal" termina siendo permanente. La verificacion es simple: si alguien dice "es solo temporal", pregunta: "Que mecanismo tenemos para asegurar que se elimina?" Si la respuesta es "nos acordaremos", no es temporal.

**Takeaway:** Los startups no se salvan por ser tacticos; se salvan por iterar rapido. Y la velocidad de iteracion depende directamente de la calidad del diseno. Invertir un 10-20% en diseno desde el dia uno no es un lujo; es una estrategia de supervivencia.

---

## Proyecto guia: DevCourses v1.1 -- el primer intento de "arreglar" con parches

Han pasado dos meses desde el diagnostico que hicimos en el capitulo anterior. El equipo de DevCourses sabe que tiene problemas. Los tres sintomas de complejidad estan presentes y empeorando. Pero hay presion de producto: necesitan lanzar tres funcionalidades nuevas antes del fin del trimestre. Bundles de cursos, soporte para MercadoPago, y certificados de finalizacion.

Carlos, el lider tecnico, propone un compromiso: "Vamos a arreglar lo que podamos mientras implementamos las nuevas funciones. Nada de sprints de refactorizacion. Solo mejoras incrementales."

Suena razonable. Es, de hecho, una version del enfoque estrategico. Pero la ejecucion revela lo dificil que es cambiar de mentalidad sin cambiar de habitos.

### El parche de los bundles

Miguel, el desarrollador junior, recibe el ticket de bundles. Un bundle es un paquete de 3-5 cursos que se venden con descuento. La forma mas rapida de implementarlo: agregar un campo `bundle_id` a la tabla de compras y una nueva tabla `bundles` con los cursos incluidos.

Miguel empieza bien. Crea la tabla `bundles`. Define una relacion muchos-a-muchos con cursos. Pero cuando llega a la funcion `comprar_curso()`, se detiene. La funcion asume que siempre se compra un solo curso. El parametro se llama `curso_id`. La logica de cupones calcula el descuento sobre el precio de un solo curso. La logica de accesos otorga acceso a un solo curso.

Miguel tiene tres opciones:

**Opcion A (tactica pura):** Crear una funcion `comprar_bundle()` separada que duplique la mayor parte de la logica de `comprar_curso()`, con las modificaciones necesarias para bundles. Rapido, pero ahora hay dos funciones de 80 lineas que hacen casi lo mismo.

**Opcion B (tactica con disfraz de estrategica):** Agregar un parametro `tipo` a `comprar_curso()` que pueda ser `"curso"` o `"bundle"`, y usar condicionales dentro de la funcion para manejar ambos casos. Parece mas limpio que la Opcion A, pero en realidad solo hace la funcion mas larga y mas dificil de entender.

**Opcion C (estrategica):** Definir una abstraccion -- llamemosla `Producto` -- que puede ser un curso individual o un bundle. La funcion se convierte en `comprar_producto(producto_id)`, donde el producto sabe como calcular su precio, como validar cupones, y como otorgar accesos. Los detalles de "es un curso o un bundle" estan encapsulados dentro del producto.

Miguel, con la presion del deadline, elige la Opcion B. Agrega el parametro `tipo`. La funcion crece a 120 lineas. Hay 8 puntos donde el codigo dice `if tipo == "bundle"`. Funciona. El ticket se cierra.

### El parche de MercadoPago

Diana recibe el ticket de MercadoPago. Abre `comprar_curso()` (ahora `comprar_curso()` con soporte para bundles) y ve que la llamada a Stripe esta directamente en la funcion. No hay abstraccion de "procesador de pagos".

Diana hace algo mejor que Miguel: extrae la logica de Stripe en una funcion separada llamada `cobrar_con_stripe()`. Y crea una funcion `cobrar_con_mercadopago()`. Luego agrega un condicional:

```python
if metodo_pago == "stripe":
    resultado = cobrar_con_stripe(monto, moneda, usuario)
elif metodo_pago == "mercadopago":
    resultado = cobrar_con_mercadopago(monto, moneda, usuario)
```

Es un paso en la direccion correcta -- al menos los detalles de cada procesador estan en su propia funcion. Pero el condicional vive en `comprar_curso()`, y cuando llegue el tercer procesador de pagos (PayPal, inevitablemente), habra que agregar otra rama. Y cuando la logica de reembolsos necesite lo mismo, habra que duplicar el patron.

La solucion estrategica habria sido un patron sencillo: una interfaz `ProcesadorDePago` con un metodo `cobrar(monto, moneda, usuario)` y una fabrica que devuelve el procesador correcto segun la configuracion. Agregar un nuevo procesador seria agregar una clase, no modificar la funcion de compra.

### El parche de los certificados

Ana, la senior, recibe los certificados. Necesita detectar cuando un estudiante completa el 100% de las lecciones de un curso y generar un PDF. Ana se da cuenta de que no existe el concepto de "progreso de un curso" en el sistema. La unica forma de saber que lecciones ha visto un estudiante es consultar la tabla `progreso_leccion` y calcular el porcentaje manualmente.

Ana hace algo genuinamente estrategico: crea un modulo `progreso` con una interfaz limpia:

```python
def obtener_progreso(usuario_id, curso_id) -> Progreso:
    """Retorna el progreso del usuario en el curso."""
    ...

def esta_completado(usuario_id, curso_id) -> bool:
    """Retorna True si el usuario completo el 100% del curso."""
    ...
```

Internamente, el modulo consulta las lecciones, calcula porcentajes, y maneja los casos especiales (lecciones opcionales, quizzes con intentos multiples). Nada de eso se expone al exterior. La funcion de certificados solo llama a `esta_completado()` y, si es verdadero, genera el PDF.

Este es un ejemplo de pensamiento estrategico en accion: Ana invirtio medio dia extra en definir una interfaz limpia en vez de meter la consulta SQL directamente en el controlador de certificados. Ese medio dia se pago cuando, dos semanas despues, el equipo de producto pidio "mostrar el porcentaje de progreso en la pagina del curso" -- y la funcion `obtener_progreso()` ya existia.

### El veredicto de v1.1

DevCourses v1.1 funciona. Las tres funcionalidades salieron a tiempo. Pero el codigo es un campo de batalla con parches de diferentes calidades:

- Los bundles estan implementados tacticamente (condicionales dentro de la funcion de compra).
- MercadoPago esta a medio camino (funciones separadas pero sin abstraccion formal).
- Los certificados estan implementados estrategicamente (modulo limpio con interfaz definida).

La inconsistencia es tipica de equipos en transicion. No es un fracaso. Es un paso intermedio. Pero ilustra un punto crucial: **la programacion estrategica no es un switch que prendes o apagas. Es un espectro, y cada decision te mueve hacia un lado o hacia el otro.**

En los capitulos siguientes, vamos a tomar los parches tacticos de v1.1 y transformarlos en diseno estrategico real. Empezaremos por el concepto que Ana aplico intuitivamente con su modulo de progreso: los modulos profundos.

**Takeaway:** La transicion de tactico a estrategico no ocurre de golpe. Ocurre una decision a la vez. Cada tarea es una oportunidad de mover el sistema en la direccion correcta, aunque sea un centimetro.

---

## Como convencer a tu equipo (y a tu jefe) de invertir en diseno

Saber que la programacion estrategica es mejor no sirve de nada si no puedes convencer a quienes toman las decisiones. Y la verdad es que "necesitamos refactorizar" es uno de los argumentos mas dificiles de vender en una organizacion.

Aqui hay cinco estrategias que he visto funcionar:

### 1. Habla en el idioma del negocio, no de la ingenieria

No digas: "Necesitamos refactorizar el modulo de pagos porque tiene alta carga cognitiva y dependencias oscuras."

Di: "Cada nueva funcion de pagos nos esta tomando 3 semanas en vez de 1 semana. Si invertimos 2 semanas en reorganizar ese modulo, las proximas 10 funciones tomaran 1 semana cada una. Es decir, invertimos 2 semanas para ahorrar 20."

Los numeros no tienen que ser exactos. Pero tener numeros -- cualquier numero razonable -- transforma la conversacion de "los ingenieros quieren jugar con el codigo" a "hay un retorno de inversion medible".

### 2. No pidas permiso para invertir el 10-20%

Ousterhout es directo sobre esto:

> "La mejor forma de gestionar la inversion en diseno es haciendola parte del trabajo normal, no como una tarea separada que requiere aprobacion." [Ousterhout, 2018]

Si un ticket toma 5 horas, estimalo en 6. Usa esa hora extra para mejorar el codigo alrededor del cambio. Nadie va a notar la diferencia en la estimacion, pero en 6 meses, todos notaran la diferencia en la velocidad del equipo.

### 3. Usa los datos que ya tienes

Herramientas como `git log` te dan datos poderosos:

```bash
# Los 10 archivos mas modificados en los ultimos 3 meses
git log --since="3 months ago" --pretty=format: --name-only | sort | uniq -c | sort -rn | head -10
```

Si el archivo mas modificado es el mismo que todos en el equipo temen tocar, tienes un argumento basado en datos. "Este archivo se ha modificado 47 veces en 3 meses. Cada modificacion tarda el doble de lo que deberia porque todo esta acoplado. Si lo reorganizamos, reducimos el tiempo de cada una de esas 47 modificaciones."

### 4. Muestra, no cuentes

La proxima vez que implementes algo con enfoque estrategico y quede bien, muestra la diferencia en el siguiente standup o code review. "Miren: agregar los certificados tomo 3 dias, pero ahora cuando nos pidan mostrar progreso en la pagina del curso, es una linea de codigo. Eso es lo que pasa cuando invertimos en la interfaz."

Los ejemplos concretos son mas persuasivos que los argumentos abstractos.

### 5. Empieza por lo que mas duele

No propongas "refactorizar todo el sistema". Propone refactorizar *el modulo que mas problemas causa*. El que genera mas bugs. El que mas tiempo consume. El que todos temen. Ese es facil de vender porque todos ya saben que es un problema. Y cuando la refactorizacion funcione y el equipo vea la mejora, tendras credibilidad para proponer la siguiente.

**Takeaway:** No necesitas convencer a nadie de que la programacion estrategica es mejor en teoria. Necesitas demostrar que es mejor en la practica, con numeros, con ejemplos, y empezando por donde mas duele.

---

## Aplica esto el lunes

### 1. Audita tu ultimo commit

Abre tu commit mas reciente. Leelo con ojos criticos. Fue tactico o estrategico? Identifica una mejora concreta que podrias haber hecho con 15 minutos extra de trabajo. No la hagas retroactivamente (eso no tiene sentido). Solo registra el patron. Hazlo con tus proximos cinco commits. Si mas de tres de cinco son puramente tacticos, tienes una tendencia que puedes corregir.

### 2. Propone la regla del 10%

En tu proxima reunion de equipo o retrospectiva, propone dedicar explicitamente el 10% del tiempo del sprint a mejoras de diseno. No como un "sprint de refactorizacion" (esos se cancelan). Como parte de cada ticket. "Cada ticket incluye hasta 2 horas de mejoras al codigo circundante." Medlo durante tres sprints y compara la velocidad del equipo.

### 3. Calcula el costo de tu deuda

Toma el modulo mas problematico de tu sistema. Estima cuantas horas semanales le cuesta al equipo su estado actual (bugs, cambios lentos, onboarding dificil). Multiplica por el costo por hora del equipo. Multiplica por 52 semanas. Ese es el costo anual de *ese solo modulo*. Ahora estima cuanto costaria arreglarlo. Dividelo por el costo anual. Ese es el periodo de recuperacion de la inversion. Si es menor a un ano, tienes un caso de negocio irrefutable.

---

## Resumen del capitulo

- La programacion tactica prioriza la velocidad inmediata: que funcione ahora. La programacion estrategica prioriza la velocidad sostenida: que funcione ahora *y* que sea facil de cambiar manana.
- La mentalidad tactica se manifiesta en hardcoding, duplicacion, parametros acumulados, manejo de errores negligente, y abstracciones rotas.
- La regla del 10-20% de Ousterhout propone invertir una fraccion constante del tiempo en mejoras de diseno. Es interes compuesto aplicado al codigo.
- Las curvas de productividad se cruzan entre los 6 y los 12 meses. A partir de ese punto, el equipo estrategico es permanentemente mas rapido.
- La deuda tecnica tiene costos medibles: los equipos promedio gastan un tercio de su tiempo en ella. Para 2026, el 80% sera arquitectonica.
- Los startups no son la excepcion. El 10-20% de inversion en diseno no es un lujo, es una estrategia de supervivencia, porque la ventaja competitiva esta en la velocidad de iteracion, no en la velocidad del primer release.
- DevCourses v1.1 muestra la realidad de la transicion: parches tacticos conviviendo con mejoras estrategicas. La consistencia se logra con practica, no con decretos.
- Convencer a los stakeholders requiere hablar en su idioma: retorno de inversion, no jargon de ingenieria.

En el siguiente capitulo, vamos a profundizar en el principio que Ana descubrio intuitivamente cuando creo su modulo de progreso: la idea de que los mejores modulos ocultan mucho mas de lo que muestran. Vamos a aprender a disenar modulos profundos.

---

### Referencias

- [Beck, 2002] Beck, K. *Test-Driven Development: By Example.* Addison-Wesley, 2002.
- [CAST, 2025] CAST Software. "Coding in the Red: The State of Global Technical Debt, 2025."
- [FlagShark, 2025] FlagShark. "The Developer Experience Cost of Technical Debt." 2025.
- [Gartner, 2025] Gartner. "Technical Debt and IT Budgets." Market Analysis, 2025.
- [McKinsey, 2025] McKinsey & Company. "Engineering Productivity and Technical Debt." 2025.
- [Ousterhout, 2018] Ousterhout, J. *A Philosophy of Software Design.* Yaknyam Press, 2018.
- [Sonar, 2025] Sonar. "New Research on the Cost of Technical Debt." 2025.
