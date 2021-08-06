---
title: "Principios de Diseño de Software"
date: 2019-03-19
author: Héctor Patricio
tags: solid diseño-de-software dry kiss
comments: true
excerpt: "Aprende qué es un principio de diseño de software y lee acerca de los más importantes."
toc: true
toc_label: Contenido
toc_sticky: true
header:
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_200/v1552951011/evgeni-tcherkasski-974328-unsplash_kqnoni.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1440/v1552951011/evgeni-tcherkasski-974328-unsplash_kqnoni.jpg
---

En este artículo hablaremos primero de la importancia de aprender **principios**: qué son, qué ventajas tienen y cómo aplicarlos.

Hallarás una explicación básica de cada principio y su importancia, pero cada principio tendrá un post extenso explicando sus aplicaciones, forma de implementarlo y ejemplos prácticos, un sólo artículo no es suficiente para explicarlos cuando se podría escribir un libro sobre cada principio.

Ponle atención a los primeros dos 😉. Pero antes hablemos de lo que es un principio en general.

## ¿Qué es un principio?

Un principio se puede entender como una **guía de comportamiento amplia aplicable a muchas situaciones**. En general un principio no te dice que hacer exactamente, sino que te da pistas de cuál es la acción correcta a través de una gran cantidad de situaciones, pero los detalles están a cargo de ti mismo.

En ciencia un principio también se pueden entender como una ley o una verdad que se puede aplicar en una muchas situaciones.

Hablando de **principios de diseño de software**, puedes pensar en ellos como en un faro que te guía a través de la oscuridad de los requerimientos del problema 😛. A diferencia de los [patrones de diseño](/2019/02/23/patrones-de-diseno-que-son-y-cuando-usarlos), no establecen los pasos necesarios para aplicarlos, ni siquiera la situaciones en las que son aplicables, de hecho, se pueden crear varios patrones y reglas basándonos en ellos.

Ahora hablemos de los más relevantes.

## Algunos principios de Diseño de Software

Los siguientes principios de diseño son de los que más escucharás a lo largo de tu carrera. Aquí presentamos una síntesis de lo que tratan pero cada uno tendrá su propio artículo extenso explicando ejemplos de cómo podemos aplicarlos.

### Don't Repeat Yourself (No te repitas)

Este principio (conocido como DRY) se explica por sí mismo: **debes evitar al máximo grado posible la repetición de código**. Partiendo de este principio se han creado un montón de maneras de reutilizar lo que ya hemos programado, piénsalo un poco: funciones, módulos, bibliotecas, clases, prototipos, herencia, composición, macros, saltos (goto).

Estas son sólo algunas maneras de evitar la repetición, claro, cada una de las estrategias anteriores lo logra a su manera y añade otras ventajas y desventajas.

**¿Por qué es importante?** Existen varias razones:

* *Hace el código más mantenible*. Evitar la repetición de código permite que si alguna vez cambia la funcionalidad que estás repitiendo, no lo tengas que hacer en todos los lugares en los que lo repetiste.
* *Reduce el tamaño del código*. Esto lo hace más legible y entendible, porque hay menos código que entender. Los procesos para evitar la repetición implican nombrar el pedazo de código que estás reutilizando para identificarlo, esto hace el código más legible si lo nombraste bien.
* *Ahorra tiempo*. Al tener pedazos de código disponibles para reutilizarlos, en el futuro estás más preparado para lograr lo mismo en menos tiempo.

### KISS

**"Keep it simple[,] stupid"**: hay discrepancias sobre si esta frase significa: "Déjalo simple, estúpido" o "Mantenlo estúpidamente simple". Este principio establece que el código, el diseño, la documentación, todo lo relacionado con el software, debe ser tan simple como sea posible.

Los programadores tendemos a complicar las cosas. Nos piden un formulario sencillo y queremos hacer un generador de formularios que soporte este y todos los formularios en el futuro. No tenemos ni 100 usuarios y ya queremos usar Kubernetes. Necesitamos un simple binding de datos y queremos meter Angular 7, Ionic 3 y 250 bibliotecas más.

Este principio establece que:

* Nuestro software en general debería tener tan pocos componentes (y por lo tanto líneas) como sea posible.
* No deberíamos tener funcionalidades que no se ocupen actualmente *“por si en el futuro se ocupan”*.
* La documentación debe tener la información **estrictamente necesaria**.
* El código debe ser **lo más obvio y sencillo posible**. Se deben evitar esas líneas que sólo sirven para presumir lo inteligente que eres.
* El diseño debe mantener la estructura simple, siempre que se pueda.

**¿Por qué es importante?** Las siguientes son algunas de las razones que justifican la existencia de este principio:

* **Proyectos más mantenibles**. Hay mucho menos que explicar al mantener las cosas simples. El código es más fácil de mantener y actualizar.
* **menos documentación**. Hay menos cosas raras que documentar al hacer el código fácil, sin trucos de listillos que nadie entiende.
* **Debugging más rápido**. Al reducir la complejidad se pueden encontrar los errores más rápidamente.
* **Mayor rendimiento económico**. Los tres efectos anteriores permiten que la inversión económica inicial en el código creado tenga mayores rendimientos.

Este es uno de los principios más difíciles de aplicar, si no es que el *más difícil*. Hacer algo simple para los demás requiere de **pensar las cosas el tiempo suficiente**, de tener la experiencia técnica necesaria para evitar intentar matar una mosca con un cañón (o investigar y tener la capacidad de aprender). A final de cuentas **la simplicidad es la sofisticación más avanzada**.

Los principios que vienen están fundamentados sobre estos dos principios.

### Principios SOLID

Si te dedicas a programar, llegado cierto punto vas a encontrar estos principios mencionados que te sentirás obligado a aprender qué significan.

**SOLID** es un acrónimo que engloba el nombre de 5 principios, originalmente dirigidos a la programación orientada a objetos, pero que son aplicables a muchas otras cosas.

Los 5 principios son:

1. **Single Responsibility** (Responsabilidad Única). Una entidad de software debería tener una sola responsabilidad, esto también se puede interpretar como "tener una y **sólo una** razón para cambiar". En pocas palabras, tu componente/función/clase debería hacer muy bien una sola cosa.

2. **Open/Closed** (Abierto/Cerrado). Una entidad de software (este principio está dirigido a las clases), debería estar abierto a extensión (crecer sus funcionalidades con otras entidades externas) pero cerrado a modificación.

3. **Liskov Substitution** (Sustitución de Liskov). El principio de sustitución de Liskov habla de interfaces: si una entidad de software usa una clase, este debe ser capaz de usar clases derivadas de esta. Esto es muy parecido a la programación por contrato, en el que se establecen las interfaces antes de la implementación.

4. **Interface Segregation** (Segregación de interfaces). Los clientes (las entidades de software) que usan una entidad de software (una clase, originalmente), no deberían estar obligados a depender de métodos que no usan. Para resolver esto, interfaces de gran tamaño se deben *segregar*, es decir, **romper**, en otras más pequeñas.

5. **Dependency Inversion**. El principio de Inversión de Dependencias establece que los módulos de alto nivel, es decir, los más cercanos a las ideas humanas de lo que debe hacer el software, no deben depender de los de bajo nivel (los más cercanos a la implementación de los detalles para la computadora). Ambos deberían depender de las abstracciones del problema (interfaces). Además los detalles de implementación deben depender de las abstracciones también. Se llama así porque en general la gente lo piensa al revés.

Estos principios empiezan sencillos pero se van complicando, así que le dedicaremos más adelante un post entero a cada principio y a su aplicación, extendiéndola más allá del software orientado a objetos.

**¿Por qué son importantes?** Permiten crear software estructurado correctamente que resista el paso del tiempo.

Como podrás ver, estos principios pueden complicar con un poco el código. Sin embargo, dependiendo del fin del software que estés creando, puedes decidir aplicarlos o saltarte alguno de ellos.

## Conclusión

Hay más principios de diseño de software de los que no hablamos en este momento, pero estos son los básicos que todo programador debe de conocer porque facilitan la vida.

Si seguimos estos principios podremos hacer software mantenible, que sea fácil de actualizar, entender, compartir, explicar y que esté preparado para el futuro.

Sigue atento por los siguientes posts que explican cada principio en profundidad, con ejemplos reales.
