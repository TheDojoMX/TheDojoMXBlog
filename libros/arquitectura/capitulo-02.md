# Capitulo 2: La complejidad es el enemigo -- aprende a verla

> "Por que cambiar una linea requiere entender diez archivos?"

---

## El momento en que la complejidad se hace visible

Ana es la desarrolladora senior del equipo de DevCourses. Lleva ocho meses en el proyecto. Una manana, el equipo de producto le pide algo que suena trivial: "Necesitamos que los cursos puedan estar en mas de un idioma."

Ana abre el codigo. Empieza por el modelo de datos. Agrega un campo `idioma` a la tabla `cursos`. Facil. Pero enseguida se da cuenta de que el buscador asume que todos los cursos estan en espanol. Modifica el buscador. Luego nota que la API de listado devuelve cursos sin filtrar por idioma. Modifica la API. Entonces ve que los templates del catalogo tienen textos hardcodeados en espanol ("Comprar curso", "Agregar al carrito"). Modifica los templates. Despues descubre que el sistema de recomendaciones usa una consulta SQL que ordena por popularidad global, sin considerar idioma. Modifica la consulta.

Cuando intenta hacer commit, se da cuenta de que los tests del buscador fallan porque asumian un solo idioma. Modifica los tests. Luego, en el code review, un companero le senala que el modulo de notificaciones envia los emails con plantillas fijas en espanol. Modifica las plantillas.

Al final de la semana, Ana ha tocado 12 archivos, 3 tablas de base de datos, y 2 servicios externos. Todo para agregar un campo que, conceptualmente, es una propiedad simple de un curso.

Esto no es un problema de Ana. Es un problema del sistema.

Muchas mentes brillantes dedicadas al desarrollo de software han llegado a la misma conclusion: **el principal problema al crear y mantener programas es el manejo de la complejidad** [Kernighan & Plauger, 1978; Brooks, 1986; Ousterhout, 2018]. No es el rendimiento, no es la escalabilidad, no es la seguridad. Esos son problemas reales, pero son problemas *derivados*. La raiz de la mayoria de los problemas en software es la complejidad descontrolada.

**Takeaway:** La complejidad no se anuncia. Se revela cuando intentas cambiar algo que deberia ser sencillo y descubres que no lo es.

---

## Que es realmente la complejidad en el software

Antes de combatir la complejidad, necesitamos definirla con precision. La palabra "complejo" se usa de muchas formas en el lenguaje cotidiano, y esa ambiguedad nos confunde.

Etimologicamente, algo complejo es aquello que esta **compuesto por muchas piezas relacionadas entre si**. Un reloj mecanico es complejo. El sistema digestivo es complejo. Pero eso no necesariamente es *malo*. A veces la complejidad es inherente al problema.

Ousterhout ofrece una definicion practica que es la que usaremos en este libro:

> "La complejidad es todo aquello que hace que el software sea dificil de **entender** o **modificar**." [Ousterhout, 2018]

Nota los dos verbos: entender y modificar. No dice "ejecutar" ni "deployar". La complejidad, en el sentido que nos importa, no es sobre lo que la maquina tiene que hacer. Es sobre lo que *tu cerebro* tiene que hacer cuando trabajas con el codigo.

Esta definicion tiene una consecuencia importante que Ousterhout explicita:

> "La complejidad es mas visible para los lectores que para los escritores del codigo. Si escribes una pieza de codigo que parece simple para ti, pero otras personas piensan que es compleja, entonces *es* compleja." [Ousterhout, 2018]

Esto es contraintuitivo. Tendemos a pensar que si nosotros lo entendemos, esta bien. Pero el criterio de complejidad no eres tu. Es el siguiente desarrollador que va a tocar ese codigo. Podrias ser tu mismo en seis meses, cuando ya olvidaste los detalles.

Hay otra distincion fundamental que debemos tener presente. Brooks la articulo en 1986 y sigue siendo vigente:

- **Complejidad esencial:** La inherente al problema. Si tu sistema maneja pagos internacionales, tienes que lidiar con conversiones de moneda, regulaciones tributarias por pais, y zonas horarias. Eso no se puede simplificar sin cambiar el problema.

- **Complejidad accidental:** La que introduces con tus decisiones de implementacion. Que la configuracion de la base de datos este duplicada en tres archivos. Que el formato de fecha sea diferente en el backend y el frontend. Que el modulo de pagos necesite conocer la estructura interna del modulo de usuarios.

La batalla del disenador de software es minimizar la complejidad accidental mientras gestiona la esencial de la manera mas limpia posible.

Rich Hickey, creador de Clojure, hizo otra distincion iluminadora en su famosa charla "Simple Made Easy" de 2011: la diferencia entre *simple* y *facil* [Hickey, 2011]. Lo facil es lo que esta a la mano, lo familiar, lo que no requiere aprendizaje. Lo simple es lo que no esta entrelazado, lo que no tiene dependencias ocultas. Un framework puede ser *facil* de usar (porque ya lo conoces) pero internamente *complejo* (porque entrelaza muchas responsabilidades). Y un enfoque puede ser *simple* (pocas dependencias, pocas interacciones) pero *dificil* de implementar (porque requiere pensar mas).

La trampa habitual es elegir lo facil sobre lo simple. Y cada vez que lo haces, anades una capa de complejidad accidental.

**Takeaway:** La complejidad es lo que hace que el software sea dificil de entender o modificar. No la defines tu; la define quien tiene que leer tu codigo despues de ti.

---

## Los tres sintomas de la complejidad

Ahora que sabemos que es la complejidad, necesitamos aprender a detectarla. Ousterhout identifica tres sintomas que se manifiestan cuando un sistema se ha vuelto mas complejo de lo necesario [Ousterhout, 2018]. Estos sintomas son las *consecuencias observables* de decisiones de diseno que acumularon complejidad accidental.

### Sintoma 1: Amplificacion de cambios

**Definicion:** Un cambio que deberia ser sencillo requiere tocar muchos lugares del codigo.

Este es el sintoma mas facil de notar porque duele inmediatamente. Quieres agregar un campo y necesitas modificar 12 archivos. Quieres cambiar un color y necesitas tocar 8 templates. Quieres agregar un nuevo metodo de pago y necesitas modificar 6 modulos.

La causa tipica es que una decision de diseno -- que deberia estar encapsulada en un solo lugar -- esta dispersa por todo el sistema. Es lo que sucede cuando parametros o valores que podrian estar centralizados se ponen fijos a traves de muchos archivos. O cuando codigo que se podria reutilizar se copia y pega.

**Ejemplo en DevCourses:** Recordemos el caso de Ana. Agregar "idioma" al curso requirio tocar 12 archivos porque el concepto de "curso" no estaba encapsulado en un solo lugar. El buscador conocia la estructura de la tabla. Los templates conocian los textos. Las recomendaciones conocian la consulta SQL. Cada pieza del sistema tenia su propia version de "que es un curso", y para cambiar el concepto habia que actualizar todas las versiones.

Comparemos con un diseno alternativo: si el modulo `catalogo` fuera el unico responsable de saber que es un curso, que campos tiene, y como se busca, agregar "idioma" seria un cambio *dentro* de ese modulo. El buscador le pediria al catalogo "dame cursos en espanol" y el catalogo resolveria el resto.

**La prueba rapida:** Piensa en el ultimo cambio que hiciste. Cuantos archivos tocaste? Si la respuesta es mas de 3 o 4 para un cambio conceptualmente simple, tienes amplificacion de cambios.

**Takeaway:** La amplificacion de cambios es la senal mas visible de la complejidad. Si un cambio sencillo requiere tocar muchos archivos, el conocimiento esta disperso donde no deberia estarlo.

---

### Sintoma 2: Carga cognitiva

**Definicion:** El desarrollador necesita mantener demasiada informacion en la cabeza para poder trabajar con una parte del sistema.

Este sintoma es mas sutil que la amplificacion de cambios. No siempre duele inmediatamente, pero te agota. Es la razon por la que al final del dia sientes que no avanzaste nada aunque estuviste "trabajando" ocho horas.

La carga cognitiva se manifiesta cuando:

- Para modificar el modulo de pagos, necesitas entender como funciona el cache, la base de datos, Y la API de Stripe. Las tres cosas.
- Para usar una funcion, necesitas recordar en que orden pasar los parametros porque los tipos no te ayudan y no hay defaults.
- Para entender un flujo de datos, necesitas saltar entre 7 archivos, construyendo mentalmente el mapa de como se conectan.

La psicologia cognitiva nos dice que la memoria de trabajo humana puede manejar aproximadamente 7 (mas/menos 2) elementos simultaneos [Miller, 1956]. Cuando un modulo de software requiere que mantengas en la cabeza mas de 7 conceptos, datos, o relaciones para poder trabajar con el, estas sobrecargando tu capacidad cognitiva. Y cuando te sobrecargas, cometes errores.

Ousterhout senala algo contraintuitivo: la carga cognitiva no siempre correlaciona con la cantidad de lineas de codigo.

> "Aunque programas mas cortos estan relacionados con baja carga cognitiva, no siempre es el caso. Puede que ese poco codigo que existe sea muy dificil de entender." [Ousterhout, 2018]

Un ejemplo clasico son las funciones de lenguajes de programacion que tienen parametros que, aunque siempre son los mismos, son requeridos porque no tienen un default razonable. O las funciones en las que no recuerdas si mutan sus parametros o devuelven un valor nuevo. Cada una de esas incertidumbres es una pieza de informacion que tu cerebro tiene que cargar.

**Ejemplo en DevCourses:** Mira otra vez la funcion `comprar_curso` del capitulo anterior. Un desarrollador que necesite modificar esa funcion tiene que entender simultaneamente:

1. La estructura de la tabla `cursos`
2. La estructura de la tabla `compras`
3. La logica de validacion de cupones (incluyendo estados, usos maximos, porcentajes)
4. La API de Stripe (como crear cargos, que excepciones puede lanzar)
5. La estructura de la tabla `accesos`
6. La interfaz de envio de emails (que parametros recibe, que templates existen)
7. La interfaz de notificaciones push
8. El sistema de analytics (que eventos existen, que formato tienen)

Son ocho conceptos independientes que necesitas tener en la cabeza simultaneamente. Eso supera la capacidad de la memoria de trabajo. Y es por eso que modificar esa funcion requiere multiples lecturas, mucho scroll, y esa sensacion de "a ver, dejame releer esta parte porque ya se me olvido lo de arriba".

**La prueba rapida:** Escoge el modulo mas complejo de tu sistema. Escribe en una hoja todo lo que alguien nuevo necesita saber para hacer un cambio ahi. Si ocupa mas de media pagina, tienes un problema de carga cognitiva.

**Takeaway:** La carga cognitiva es el impuesto invisible del mal diseno. No se ve en las metricas, pero se siente en la velocidad del equipo y en la cantidad de bugs.

---

### Sintoma 3: Desconocidos desconocidos

**Definicion:** No es que no sepas la respuesta. Es que no sabes que hay una pregunta.

Este es el peor de los tres sintomas. Con la amplificacion de cambios, al menos sabes que hay un problema (porque tocaste muchos archivos). Con la carga cognitiva, al menos sabes que es dificil (porque te sientes agotado). Pero con los desconocidos desconocidos, no sabes que no sabes. Y eso es peligroso.

Un desconocido desconocido es aquella informacion que ni siquiera sabes que existe y que necesitas para hacer un cambio seguro. Es la dependencia oculta que nadie documento. Es el efecto secundario que no es obvio. Es la convencion implicita que todos los desarrolladores originales conocian pero que no esta escrita en ningun lado.

La vieja broma lo dice bien: *"Cuando escribi este codigo solo Dios y yo sabiamos lo que hacia. Ahora solo Dios sabe."*

Donald Rumsfeld popularizo la taxonomia de conocimiento que aplica perfectamente aqui:

- **Conocidos conocidos:** Sabes que el modulo de pagos usa Stripe. Eso esta documentado y es obvio.
- **Conocidos desconocidos:** Sabes que hay una logica de descuentos pero no sabes exactamente como funciona. Al menos sabes que necesitas investigar.
- **Desconocidos desconocidos:** No sabes que cambiar el formato de fecha en la API rompe el reporte de analytics, porque el reporte parsea el campo de fecha de una manera no documentada que depende del formato actual.

Los desconocidos desconocidos son la fuente de los bugs mas costosos. Son los que aparecen en produccion tres semanas despues de un deploy aparentemente inocuo. Son los que el QA no puede atrapar porque nadie sabe que hay que probar ese escenario.

**Ejemplo en DevCourses:** El equipo decide cambiar el timezone del servidor de UTC a America/Mexico_City porque la mayoria de los usuarios estan en Mexico. Parece un cambio de configuracion simple. Lo que no saben es que:

1. El modulo de analytics calcula los reportes diarios sumando eventos entre medianoche y medianoche UTC. Al cambiar la zona horaria, los reportes del dia del cambio van a estar mal.

2. El scheduler de Celery que envia los recordatorios de "continua donde te quedaste" usa la hora del sistema para calcular "hace 24 horas". Al cambiar la zona horaria, algunos usuarios van a recibir recordatorios duplicados y otros no van a recibir ninguno.

3. El campo `fecha_expiracion` de los cupones se compara contra `NOW()` en PostgreSQL, que ahora retorna una hora diferente. Cupones que deberian haber expirado siguen activos. Cupones que deberian estar activos expiraron.

Ninguna de estas dependencias estaba documentada. Ninguna era obvia. Y ninguna se hubiera atrapado en un code review normal. Son desconocidos desconocidos.

**La prueba rapida:** Preguntale a un companero: "Que pasaria si cambio X?" Si la respuesta es "no se", tienes un desconocido desconocido. Documentalo inmediatamente.

**Takeaway:** Los desconocidos desconocidos son el sintoma mas peligroso de la complejidad. Son los bugs que no puedes prevenir porque no sabes que existen. El buen diseno los minimiza haciendo las dependencias explicitas.

---

## La formula: C = Sigma(cp x tp)

Hemos hablado de la complejidad en terminos cualitativos. Pero Ousterhout propone algo mas preciso: una formula que, aunque no se use con numeros exactos, ofrece un marco mental poderoso para razonar sobre la complejidad [Ousterhout, 2018].

La complejidad total de un sistema se puede expresar como:

```
C = SUM( cp * tp )
```

Donde:

- **C** es la complejidad total del sistema
- **cp** es la complejidad de la parte *p* del sistema
- **tp** es la fraccion de tiempo que los desarrolladores pasan trabajando en la parte *p*

En palabras:

> La complejidad total de un sistema es la sumatoria de la complejidad de cada una de sus partes, ponderada por el tiempo que los desarrolladores pasan en esa parte del codigo.

Esto tiene implicaciones practicas muy importantes.

### Implicacion 1: Una parte muy compleja que nadie toca no contribuye mucho a la complejidad total

Si tienes un modulo de migracion de datos que es un desastre de 3,000 lineas, pero nadie lo ha tocado en 18 meses y nadie necesita tocarlo, su contribucion a la complejidad total es baja. Su *cp* es alta pero su *tp* es cercano a cero.

Esto va contra la intuicion de muchos desarrolladores que quieren "limpiar todo". La formula te dice: enfocate en lo que duele, no en lo que se ve feo.

### Implicacion 2: Una parte moderadamente compleja que todos tocan constantemente es un problema grave

Si la funcion de compra de cursos tiene complejidad moderada pero todos los desarrolladores la modifican cada semana, su contribucion a la complejidad total es enorme. Su *cp* es media pero su *tp* es muy alto.

### Implicacion 3: La complejidad es relativa al equipo y al momento

Un sistema que era manejable con tres desarrolladores puede volverse insoportable con diez, porque mas personas trabajan en las mismas partes. El *tp* de cada parte cambia con el tamano del equipo.

### Ejemplo numerico con DevCourses

Imaginemos una simplificacion del sistema con cuatro partes:

| Parte | cp (complejidad) | tp (tiempo relativo) | cp * tp |
|-------|------------------|----------------------|---------|
| Compra de cursos | 8 | 0.35 | 2.80 |
| Catalogo y busqueda | 5 | 0.30 | 1.50 |
| Reproduccion de video | 7 | 0.10 | 0.70 |
| Panel de instructor | 4 | 0.25 | 1.00 |
| **Total** | | | **6.00** |

El modulo de compra de cursos es el que mas contribuye a la complejidad total, no porque sea el mas complejo (la reproduccion de video tiene un cp alto), sino porque es donde el equipo pasa mas tiempo. Si pudieras reducir la complejidad de compra de cursos de 8 a 4, la complejidad total bajaria de 6.00 a 4.60 -- una reduccion del 23%.

En cambio, si limpiaras completamente el modulo de reproduccion de video (de cp=7 a cp=1), la complejidad total bajaria de 6.00 a 5.40 -- solo un 10%.

La formula te dice donde invertir tu esfuerzo de refactorizacion. No es donde el codigo es mas feo. Es donde el codigo feo se toca mas.

**Takeaway:** La complejidad se pondera por frecuencia de uso. Enfoca tu esfuerzo en las partes del sistema que son complejas *y* que el equipo toca constantemente.

---

## De donde viene: dependencias y oscuridad

Hemos visto los *sintomas* de la complejidad. Ahora veamos las *causas*. Ousterhout identifica dos causas fundamentales de las que se derivan todos los sintomas [Ousterhout, 2018]:

### Causa 1: Dependencias

Una dependencia existe cuando una pieza de codigo no puede ser entendida o modificada de forma aislada; necesitas considerar otra pieza de codigo para trabajar con ella.

Las dependencias son inevitables. No puedes construir software sin ellas. Si el modulo de pagos necesita saber el precio de un curso, hay una dependencia con el modulo de catalogo. Eso es normal.

El problema no es la existencia de dependencias, sino su *cantidad*, su *tipo*, y sobre todo, si son *visibles o invisibles*.

Tipos de dependencias en orden de peligrosidad:

1. **Dependencias explicitas en la interfaz:** La funcion `procesar_pago(usuario_id, curso_id)` declara explicitamente que depende de un usuario y un curso. Esto es una dependencia saludable: es visible, tipada, y obvia.

2. **Dependencias implicitas en la interfaz:** La funcion funciona correctamente solo si la llamas *despues* de `validar_sesion()`. Eso no esta declarado en la firma. Es una dependencia, pero esta escondida.

3. **Dependencias por datos compartidos:** Dos modulos leen y escriben la misma tabla de base de datos. Ninguno "llama" al otro, pero estan acoplados a traves de la estructura de la tabla. Si cambias la tabla, ambos se rompen.

4. **Dependencias temporales:** El modulo A debe ejecutarse antes que el modulo B porque B asume que A ya dejo cierto estado en la base de datos. Esto no esta documentado en ningun contrato; es una convencion que vive en la cabeza de los desarrolladores.

5. **Dependencias de formato:** El frontend asume que las fechas vienen en formato "YYYY-MM-DD" porque el backend las serializa asi. No hay un contrato formal. Si el backend cambia el formato, el frontend se rompe sin aviso.

Las dependencias mas peligrosas son las que no puedes ver. Y eso nos lleva a la segunda causa.

### Causa 2: Oscuridad

La oscuridad es cuando informacion importante no es obvia. Puede ser un conocimiento no documentado, una convencion implicita, una dependencia no declarada, o un efecto secundario que no se puede inferir de la interfaz.

David Parnas, en su articulo fundacional de 1972, argumento que la clave para disenar bien un sistema es decidir que informacion *ocultar* dentro de cada modulo [Parnas, 1972]. Pero hay una diferencia crucial entre **ocultar informacion intencionalmente** (que es bueno) y **tener informacion oculta accidentalmente** (que es oscuridad).

Cuando ocultas intencionalmente los detalles de Stripe dentro del modulo de pagos, estas reduciendo la complejidad para todos los demas. Cuando la dependencia entre el formato de fecha y el reporte de analytics esta oculta accidentalmente, estas creando una bomba de tiempo.

Ejemplos de oscuridad en DevCourses:

- **Convencion no documentada:** Los IDs de Stripe siempre empiezan con "ch_" para cargos y "sub_" para suscripciones. El codigo de reportes usa un `startswith()` para distinguirlos, pero esto no esta documentado. Si alguien agrega otro procesador de pagos cuyos IDs no sigan esta convencion, los reportes se rompen.

- **Efecto secundario oculto:** La funcion `registrar_evento()` de analytics no solo registra el evento, sino que tambien actualiza un contador en Redis. Si el contador de Redis no esta disponible, la funcion lanza una excepcion que no esta declarada. Cualquier codigo que llame a `registrar_evento()` puede fallar por una razon que no tiene nada que ver con analytics.

- **Dependencia de orden:** Para que un usuario pueda ver un curso, necesita tener un registro en la tabla `accesos`. Pero ese registro se crea en la funcion `comprar_curso()` *despues* de cobrar pero *antes* de enviar la notificacion. Si otro modulo intenta crear accesos directamente (por ejemplo, para un periodo de prueba gratuito), no sabe que tambien deberia registrar un evento de analytics.

La relacion entre dependencias y oscuridad con los tres sintomas es directa:

| Causa | Produce |
|-------|---------|
| Muchas dependencias | Amplificacion de cambios |
| Dependencias complicadas | Carga cognitiva |
| Dependencias oscuras | Desconocidos desconocidos |

**Takeaway:** Toda complejidad proviene de dos fuentes: demasiadas dependencias y dependencias que no son obvias. El buen diseno minimiza las primeras y hace visibles las segundas.

---

## La complejidad es incremental

Aqui viene la razon por la que la complejidad es tan dificil de combatir: **no aparece de golpe.** No hay un commit que diga "aqui fue donde el proyecto se volvio inmanejable". No hay un momento dramatico. La complejidad se acumula gota a gota.

Cada decision individual parece razonable en su momento:

- "Voy a hardcodear este valor porque solo se usa aqui." (Un minuto ahorrado hoy, un archivo mas que tocar manana.)
- "Voy a copiar esta funcion en vez de extraerla, porque tiene una diferencia pequena." (Cinco minutos ahorrados hoy, dos funciones que mantener sincronizadas de aqui en adelante.)
- "No voy a documentar este comportamiento porque es obvio." (Treinta segundos ahorrados hoy, un desconocido desconocido para el siguiente desarrollador.)
- "Voy a agregar este parametro a la funcion en vez de crear una nueva." (Tres minutos ahorrados hoy, una firma de funcion que nadie entiende la proxima semana.)

Ninguna de estas decisiones, por si sola, arruina un proyecto. Pero despues de seis meses de tomar docenas de estas decisiones al dia, la base de codigo ha acumulado cientos de capas de complejidad accidental.

Es como la analogia del agua caliente con la rana: si metes una rana en agua hirviendo, salta. Pero si la metes en agua tibia y la calientas gradualmente, no nota el cambio hasta que es demasiado tarde. Con el software pasa lo mismo. Nunca hay un dia en que digas "hoy el proyecto paso de manejable a inmanejable". Simplemente un dia te das cuenta de que los estimados son el doble de lo que eran, que los bugs son mas frecuentes, y que nadie quiere tocar ciertos archivos.

Ousterhout lo dice de manera directa:

> "La complejidad no es causada por una sola decision catastrofica. Se acumula en porciones pequenas a lo largo de muchos cambios." [Ousterhout, 2018]

Esto significa que la batalla contra la complejidad tambien es incremental. No vas a "arreglar" tu base de codigo en un sprint de refactorizacion epico. Vas a mejorarla gradualmente, con cada commit, con cada code review, con cada decision consciente de invertir cinco minutos extra en hacer las cosas un poco mejor.

El kernel de Linux es quizas el mejor ejemplo de como se puede manejar la complejidad incremental a gran escala. Con mas de 40 millones de lineas de codigo en enero de 2025 y mas de 5,000 contribuidores por ciclo de desarrollo, el kernel crece en aproximadamente 400,000 lineas cada dos meses. Y sin embargo, sigue siendo un sistema funcional y evolutivo [Linux Foundation, 2025]. La razon es que tiene reglas estrictas de modularizacion: los drivers (que representan el 60% del codigo) estan aislados del kernel central. Puedes agregar un driver nuevo sin entender el subsistema de memoria. Esa es la disciplina del diseno incremental.

Ousterhout llama a esto *programacion estrategica*: la actitud de invertir un poco mas en cada tarea para dejar el sistema mejor de como lo encontraste. En contraste con la *programacion tactica*, donde el unico objetivo es que funcione lo mas rapido posible [Ousterhout, 2018]. Exploraremos esta distincion en profundidad en el siguiente capitulo.

**Takeaway:** La complejidad es incremental. Se acumula con cientos de decisiones pequenas, no con una sola decision mala. Y se combate de la misma forma: con cientos de decisiones pequenas y conscientes.

---

## Proyecto guia: diagnosticando DevCourses v1

Vamos a aplicar todo lo que hemos aprendido al estado actual de DevCourses. Recordemos: tenemos un monolito de cuatro archivos principales (`app.py`, `models.py`, `utils.py`, y los templates) que funciona pero que esta empezando a doler.

### Diagnostico de amplificacion de cambios

Escenario: el equipo necesita agregar "paquetes de cursos" (bundles), donde puedes comprar 3 cursos juntos con descuento.

Archivos que habria que tocar:

1. `models.py` -- Nuevo modelo `Bundle` y tabla de relacion bundle-cursos
2. `app.py` (ruta `/catalogo`) -- Mostrar bundles en el listado
3. `app.py` (ruta `/comprar-curso`) -- Ahora tambien debe poder comprar bundles, no solo cursos individuales
4. `app.py` (ruta `/mis-cursos`) -- Mostrar cursos adquiridos via bundle
5. `utils.py` (funcion de calculo de precios) -- La logica de descuento debe considerar bundles
6. `utils.py` (funcion de cupones) -- Los cupones aplican diferente para bundles?
7. Templates del catalogo -- Renderizar tarjetas de bundle
8. Templates de checkout -- El flujo de compra es diferente para bundles
9. Templates de "mis cursos" -- Agrupar cursos por bundle
10. `app.py` (analytics) -- Nuevo tipo de evento "compra_bundle"
11. `app.py` (notificaciones) -- Nuevo template de email para bundles

Son 11 puntos de cambio para una funcionalidad que, conceptualmente, es "un producto que contiene varios cursos". La amplificacion es severa.

**Causa raiz:** El concepto de "que es algo comprable" esta disperso por todo el sistema. No hay una abstraccion que unifique "curso individual" y "bundle" como variantes de un mismo concepto.

### Diagnostico de carga cognitiva

Tomemos al desarrollador junior del equipo, Miguel. Se le asigna corregir un bug: "Cuando un usuario compra un curso con cupon de 100% de descuento, Stripe lanza un error porque se intenta cobrar $0."

Para arreglar este bug, Miguel necesita entender:

1. El flujo completo de la funcion `comprar_curso()` (la vimos en el capitulo anterior: 50+ lineas con 8 conceptos diferentes).
2. La logica de validacion de cupones (activo, usos maximos, porcentaje).
3. El comportamiento de `stripe.Charge.create()` cuando el amount es 0.
4. Si debe crear la compra sin llamar a Stripe, o si debe llamar a Stripe con amount=0 de alguna forma especial.
5. Si el modulo de accesos necesita saber que fue una compra gratuita.
6. Si analytics debe registrar el evento diferente (monto=0 vs. monto>0).

Miguel estima que el fix tomara 2 horas. Le toma un dia y medio, porque cada vez que resuelve una parte, descubre que hay otra parte que no habia considerado.

**Causa raiz:** Toda la logica vive en una sola funcion que mezcla niveles de abstraccion. No hay separacion entre "que significa comprar" y "como se cobra".

### Diagnostico de desconocidos desconocidos

El equipo decide migrar de Stripe como unico procesador de pagos a soportar tambien MercadoPago para el mercado latinoamericano.

Desconocidos desconocidos que descubren durante la implementacion:

1. La funcion de reportes financieros asume que todos los IDs de transaccion tienen el prefijo "ch_" de Stripe. Nadie lo sabia hasta que los reportes empezaron a excluir las transacciones de MercadoPago.

2. El template de email de "compra exitosa" incluye un link directo al dashboard de Stripe para que el usuario vea su recibo. Ese link no tiene equivalente en MercadoPago.

3. La funcion de reembolsos (que nadie habia tocado en meses) tiene hardcodeado `stripe.Refund.create()`. No hay forma de hacer un reembolso para compras hechas con MercadoPago sin reescribir esa funcion.

4. El sistema de webhooks esta configurado solo para Stripe. MercadoPago usa un formato de webhook completamente diferente.

Cada uno de estos descubrimientos agrego dias al proyecto. Y cada uno era invisible antes de empezar.

**Causa raiz:** Los detalles de Stripe estan dispersos por todo el sistema en vez de estar encapsulados en un modulo de pagos con una interfaz generica.

### El veredicto

DevCourses v1 tiene los tres sintomas de complejidad en estado avanzado. Y no es porque el equipo sea malo. Es porque el sistema fue construido con un enfoque tactico -- prioridad a la velocidad, sin inversion en diseno -- y seis meses de decisiones incrementales produjeron un sistema donde todo esta conectado con todo.

**Takeaway:** Diagnosticar tu sistema contra los tres sintomas es el primer paso para saber donde duele y donde invertir esfuerzo de diseno.

---

## Checklist: tu codigo tiene este problema si...

Usa esta checklist como herramienta de diagnostico. Cada afirmacion describe un sintoma de complejidad excesiva. Cuenta cuantas aplican a tu proyecto.

### Amplificacion de cambios

- [ ] Agregar un campo a una entidad principal requiere tocar mas de 5 archivos.
- [ ] Cambiar un texto visible al usuario requiere modificar tanto el backend como el frontend.
- [ ] Agregar un nuevo tipo de [entidad principal] requiere copiar y adaptar logica que ya existe para otro tipo.
- [ ] Las migraciones de base de datos frecuentemente van acompanadas de cambios en multiples modulos de aplicacion.
- [ ] Hay codigo duplicado que "se parece pero no es igual" en multiples archivos.

### Carga cognitiva

- [ ] Hay funciones que reciben mas de 5 parametros sin defaults razonables.
- [ ] Para hacer un cambio en un modulo, necesitas entender al menos otros dos modulos.
- [ ] Los desarrolladores nuevos tardan mas de una semana en poder hacer su primer commit productivo.
- [ ] Hay archivos de mas de 500 lineas que mezclan multiples responsabilidades.
- [ ] Los code reviews toman mas de una hora porque el revisor necesita entender mucho contexto.

### Desconocidos desconocidos

- [ ] En el ultimo mes, un deploy causo un bug inesperado en una parte del sistema aparentemente no relacionada.
- [ ] Hay partes del codigo donde nadie en el equipo actual sabe exactamente que hacen.
- [ ] No existe documentacion de las dependencias entre modulos.
- [ ] Hay "reglas" que todo el equipo conoce pero que no estan escritas en ningun lado (e.g., "siempre hay que correr X antes de Y").
- [ ] Un desarrollador que se fue del equipo era la unica persona que entendia un componente critico.

### Interpretacion

- **0-3 marcados:** Tu sistema esta razonablemente bien disenado. Sigue invirtiendo en mantenerlo asi.
- **4-7 marcados:** Hay areas de mejora claras. Prioriza la que mas duele y aplica las tecnicas de los siguientes capitulos.
- **8-11 marcados:** El sistema tiene problemas serios de diseno. Necesitas una estrategia de refactorizacion incremental. No intentes arreglar todo de golpe.
- **12-15 marcados:** Estas en territorio de "es mas facil hacerlo de nuevo". Pero antes de reescribir, lee el resto de este libro -- probablemente puedes salvarlo con diseno incremental.

**Takeaway:** Una checklist concreta te permite pasar de la intuicion ("siento que el codigo es dificil") a un diagnostico estructurado.

---

## Aplica esto el lunes

### 1. Haz un "mapa de calor" de complejidad

Abre el historial de commits de los ultimos 3 meses. Identifica los 5 archivos que mas se han modificado. Para cada uno, estima su complejidad del 1 al 10. Multiplica. Los que tengan el puntaje mas alto son tus candidatos prioritarios para refactorizacion. No refactorices lo que se ve mal; refactoriza lo que duele mas segun la formula C = SUM(cp * tp).

Para obtener los archivos mas modificados, puedes usar:

```bash
git log --since="3 months ago" --pretty=format: --name-only | sort | uniq -c | sort -rn | head -10
```

### 2. Documenta un desconocido desconocido

Piensa en el ultimo bug que aparecio en produccion y que nadie anticipaba. Rastrealo hasta su causa raiz. Luego preguntate: que deberia haber sido diferente en el diseno para que este bug fuera *imposible* o al menos *obvio*? Escribe un parrafo con tu analisis y compartelo con tu equipo. Un desconocido desconocido documentado deja de ser desconocido.

### 3. Mide la carga cognitiva de tu modulo mas critico

Escoge el modulo que tu equipo modifica mas frecuentemente. Escribe una lista de todo lo que un desarrollador necesita saber para hacer un cambio seguro en ese modulo. Cuenta los items. Si son mas de 7, piensa en como podrias reducir esa lista. Las tecnicas de los capitulos 4, 5, y 6 te daran herramientas concretas para hacerlo.

---

## Resumen del capitulo

- La complejidad es todo aquello que hace que el software sea dificil de entender o modificar. No la defines tu; la define quien lee tu codigo.
- Se manifiesta en tres sintomas: amplificacion de cambios (un cambio sencillo toca muchos archivos), carga cognitiva (necesitas tener demasiada informacion en la cabeza), y desconocidos desconocidos (no sabes que hay una dependencia hasta que algo se rompe).
- La formula C = SUM(cp * tp) te dice donde invertir: en las partes del codigo que son complejas *y* que se tocan con frecuencia.
- Toda complejidad proviene de dos causas: demasiadas dependencias y dependencias que no son obvias (oscuridad).
- La complejidad es incremental. No hay un momento dramatico. Se acumula gota a gota con cientos de decisiones pequenas.
- DevCourses v1 presenta los tres sintomas en estado avanzado. No es porque el equipo sea malo, sino porque el enfoque fue tactico.
- La checklist de 15 preguntas te permite hacer un diagnostico estructurado de tu propio proyecto.

En el siguiente capitulo, vamos a explorar las dos filosofias fundamentales de desarrollo: la tactica ("que funcione rapido") y la estrategica ("que funcione bien"). Veremos cuando cada una tiene sentido, y por que la curva de productividad siempre favorece al enfoque estrategico en el mediano plazo.

---

### Referencias

- [Brooks, 1986] Brooks, F. "No Silver Bullet -- Essence and Accident in Software Engineering." *Proceedings of the IFIP Tenth World Computing Conference*, 1986.
- [Hickey, 2011] Hickey, R. "Simple Made Easy." *Strange Loop Conference*, 2011.
- [Kernighan & Plauger, 1978] Kernighan, B. W. y Plauger, P. J. *The Elements of Programming Style.* McGraw-Hill, 1978.
- [Linux Foundation, 2025] The Linux Foundation. "2025 Annual Report on Linux Kernel Development."
- [Miller, 1956] Miller, G. A. "The Magical Number Seven, Plus or Minus Two." *Psychological Review*, 63(2), 81-97, 1956.
- [Ousterhout, 2018] Ousterhout, J. *A Philosophy of Software Design.* Yaknyam Press, 2018.
- [Parnas, 1972] Parnas, D. L. "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 15(12), 1053-1058, 1972.
