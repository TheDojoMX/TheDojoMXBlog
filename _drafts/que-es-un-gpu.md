---
title: "¿Qué es un GPU?"
date: 2025-10-13
author: Héctor Patricio
tags: gpu hardware paralelismo performance
comments: true
excerpt: "Hablemos de qué es un GPU desde la perspectiva de desarrollo: arquitectura, casos de uso y cuándo aprovecharlo para resolver problemas computacionales complejos."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1760366113/lilian-do-khac-uLyzgGt4MxI-unsplash_ec0low.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1760366113/lilian-do-khac-uLyzgGt4MxI-unsplash_ec0low.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Si has estado atento a las tendencias de desarrollo de software, te habrás dado
cuenta que la computación especializada cada vez está más extendida, sobre todo
por la proliferaciónd de modelos de machine learning que requieren un montón
de cómputo. Uno de los elementos de hardware que brilla en esta industria es
el GPU (Graphics Processing Unit). Hablemos de qué es un GPU desde nuestra
perspectiva como desarrolladores de software.

## GPUs para Desarrolladores

Lo que comenzó como hardware especializado para renderizar gráficos en videojuegos
se ha convertido en el motor computacional detrás de los modelos de inteligencia
artificial más avanzados, simulaciones científicas complejas y procesamiento
masivo de datos.

Como desarrolladores modernos, entender qué es un GPU y cuándo aprovecharlo
es muy importante. Si trabajas (o quieres trabajar) con machine learning,
procesamiento de video, análisis de datos masivos o cualquier problema que
requiera procesar grandes cantidades de información, los GPUs pueden acelerar
tu código de 10x a 100x comparado con implementaciones tradicionales.

Este artículo te explicará qué es un GPU desde la perspectiva de la arquitectura
de computadoras. En otro artúculo veremos cómo identificar problemas que puedan
beneficiarse de una implementación en GPUs en lugar de CPUs tradicionales.

## CPU vs GPU: Filosofías de Diseño Diferentes

Para entender un GPU, primero debemos contrastar su diseño con el de un CPU
(Central Processing Unit). Pongamos un ejemplo sencillo.

### CPU: El Artesano experto

Un CPU tiene **pocos núcleos poderosos** (típicamente 4-64 núcleos en CPUs
modernas). Está optimizado para **para tareas _secuenciales_ complejas** con
muchas dependencias, o con mucho control de flujo (condicionales, branches).
Ejecuta instrucciones individuales muy rápido, algunas de ellas, dependiendo
de la arquitectura, muy compljas. Por ejemplo, una sola instrucción puede
hacer una operación criptográfica como AES (cifrado) o SHA (hashing).

Los CPUs tienen un _control de flujo sofisticado_: pueden predecir
(estadísticamente) por qué camino se irá el código y prerarse para ello.
También tinen cachés "enormes" (L1, L2, L3) para minimizar la latencia de acceso
a memoria. Otra característica es que pueden reordenar las instrucciones
de bajo nivel para aprovechar mejor los recursos, reduciendo la latencia en la
ejecución.

Si quieres tener máximo control y flexibilidad, como en el caso de lógica de
negocio, bases de datos, servidores web, algoritmos complejos, etc., tu programa
debe correr en CPU. Esto es lo que el 99.999% de los desarrolladores hacemos,
a tal punto que ni siquiera nos preguntamos dónde debe vivir nuestro software.

Ahora hablemos del tema que nos concierne: los GPUs.

### GPU: La Línea de Ensamblaje

Un GPU tiene **muchísimos núcleos simples** (miles a decenas de miles en GPUs modernas).
Están pensados para **optimizar paralelismo masivo** con operaciones _independientes_.
Un GPU procesa **grandes cantidades de datos simultáneamente, pero aplicándoles operaciones
relativamente sencillas**.

Su control de flujo es simple, es decir, no puede predecir branches complejos ni
reordenar instrucciones. Digamos que su principal fortaleza es hacer operaciones
matemáticas básicas (suma, multiplicación, etc.) en muchos datos al mismo tiempo.

Así que la comparación es clara: un GPU es como una línea de esamblaje que tiene
miles de unidades que pueden hacer trabajo simple al mismo tiempo, mientras que un
CPU es como un conjunto de artesanos expertos haciendo trabajo complejo y
_secuencial principalmente_.

Ahora hablemos de la arquitectura de un GPU para ver cómo hace el paralelismo masivo posible.

## Arquitectura de un GPU

Los GPUs modernos organizan sus recursos computacionales en varias capas. Veamos cuáles y cómo puedes usarlas para tus programas.

### Unidades de Procesamiento

El componente pricipal es el conjunto de núcleos individuales que hacen el trabajo
real, estos pequeños procesadores tienen diferentes nombres dependiendo del
fabricante:
  - **NVIDIA**: CUDA Cores
  - **AMD**: Stream Processors
  - **Intel**: Execution Units (EUs)

Y así... pero la idea es la misma: muchos núcleos o procesadores encargados
de hacer operacionas matemáticas básicas.

Estos núcleos están agrupados en unidades mayores que llamamos **streaming Multiprocessors (SMs)** y tienen una memoria rápida compartida entre ellos. A nivel global, tenemos otro nivel de memoria accesible a todos los SMs.

Recientemente y sobre todo pensando en cargas de operaciones matriciales complejas
(como las que se usan en machine learning) se han añadido unidades especializadas: los **tensor cores**. La industria se está adaptando  a los nuevos usos del
software.

Pero hablemos un poco de la estructura de memoria.

### Jerarquía de Memoria

Al igual que los CPUs, los GPUs tienen un conjunto de diferentes tipos (y velocidades) de memoria.
La memoria más inmediata para cada uno de los cores son los **registros**: memoria ultra-rápida privada de cada thread que usa para las operaciones más inmediatas.
Ya hablamos de la **memoria compartida** a nivel de bloque de los SMs, que no es tan rápida como los registros pero sigue siendo MUY rápida.

3. **Memoria global**: Memoria grande pero con mayor latencia, accesible por todos
4. **Memoria de textura/constantes**: Optimizada para patrones específicos de acceso
5. **Memoria de host**: La RAM del sistema, accesible a través del bus PCIe (lenta)

### Modelo de Ejecución de un GPU

Veamos cómo corre un programa en un GPU: primero el programa se divide en **kernels**. Un kernel es una función que se ejecuta aprovecha la estructura de procesamiento del GPU: lanza cientos o miles de threads en paralelo. Cada thread ejecuta la misma función pero con datos diferentes. Un **thread** (hilo) es la unidad básica de ejecución en un GPU.

Un Grupo de **32 threads (NVIDIA)** que ejecutan, el bloque de threads: grupo de threads que pueden cooperar y compartir memoria.**Grid**: Colección de bloques que ejecutan el mismo kernel.


### Ancho de Banda vs Latencia

Los GPUs priorizan **throughput** (cantidad de trabajo procesado, basado en datos) sobre **latencia** (tiempo para una operación individual). Esto significa que aunque una operación individual puede tardar más en GPU que en CPU, el GPU puede procesar miles de operaciones simultáneamente, resultando en mayor throughput total.

## Paralelismo de Datos

El modelo de programación de GPUs se basa en **SIMD/SIMT** (Single Instruction, Multiple Data / Single Instruction, Multiple Threads):

- Un mismo conjunto de instrucciones se ejecuta sobre múltiples datos simultáneamente
todos los threads en un warp ejecutan la misma instrucción al mismo tiempo (sobre
diferentees datos), divergencia de control (diferentes branches) causa
serialización y pérdida de performance

### Ejemplo Práctico
**Problema A**: Multiplicar 1 millón de números por una constante
- **Paralelismo perfecto**: Cada operación es independiente
- **GPU gana dramáticamente**: 100x más rápido o más dependiendo del hardware
**Problema B**: Construir un árbol de decisión se lleva mucho mejor con lógica compleja
- **Inherentemente secuencial**: Cada decisión depende de la anterior
- **CPU gana**: Mejor control de flujo y menor overhead

### Complejidad de Programación - Desafíos

Programar para GPUs es completamente diferente que programar para CPUs. Aquí
algunos retos:

- **Debugging**: Más difícil que código CPU, porque tenemos herramientas más limitadas
- **Profiling**: Herramientas especializadas necesarias y también hay pocas
- **Curva de aprendizaje**: Entender modelo de memoria y ejecución
- **Portabilidad**: CUDA es específico de NVIDIA

### Consumo Energético

Los GPUs consumen mucha, pero mucha más engergía que los CPU's. Un GPU de alto rendimiento consumen 300-500W
- Hardware costoso (especialmente para ML/AI)
- Refrigeración y infraestructura adicional

## Futuro y Tendencias

### GPU Programming Más Accesible

- **Compiladores inteligentes**: Generación automática de código GPU
- **Domain-specific languages**: Abstracciones de alto nivel: CUDA, OpenCL, SYCL, Triton, Mojo
- **Auto-tuning**: Optimización automática de parámetros
### Hardware Especializado

- **TPUs (Tensor Processing Units)**: Optimizadas para ML
- **NPUs (Neural Processing Units)**: IA en edge devices
- **FPGAs (Field)**
### GPUs en la Nube

Si no tienes un GPU físico hay varias formas de acceder a GPUs de alto rendimiento,
de forma remota y sin mucha inversión por adelantado:

- **Serverless GPU**: Paga solo por el tiempo de uso (Lambda, Functions)
- **Spot instances**: GPU computing económico
- **Kubernetes con GPUs**: Orquestación de cargas GPU

## Conclusión

Los GPUs representan una herramienta fundamental en el arsenal del desarrollador
moderno para resolver problemas que involucran paralelismo masivo de datos.

Entender su arquitectura, fortalezas y limitaciones te permite identificar
oportunidades donde una implementación en GPU puede transformar un problema
intratable en uno solucionable.

La clave está en reconocer el patrón: **¿Estás aplicando la misma operación a muchos datos?** Si la respuesta es sí, probablemente hay una oportunidad de aceleración con GPU.

## Referencias y Recursos para Profundizar

La programación de GPUs es una campo amplio y bastante diferente a la programación
"tradicional". Aquí nos centramos en transformaciones matemáticas, álgebra lineal
e incluso cálculo.


### Libros Fundamentales

**Programming Massively Parallel Processors: A Hands-on Approach** - (David B.
Kirk, Wen-mei W. Hwu, Izzat El Hajj): El LIBRO que tienes que leer para aprender
programación de GPUs. Cubre desde conceptos básicos hasta técnicas avanzadas con
enfoque práctico.

**GPU Gems Series** (Disponibles gratis online)
- *GPU Gems 1* (2004): Técnicas de programación gráfica en tiempo real
- *GPU Gems 2* (2005): 20 capítulos dedicados a GPU programming
- *GPU Gems 3*: Técnicas modernas de GPU programming
- *Link*: [NVIDIA Developer](https://developer.nvidia.com/gpugems)

### Documentación Oficial
**3. CUDA C++ Programming Guide**
- *Fuente*: NVIDIA Official Documentation
- *Descripción*: Documentación completa y oficial del modelo de programación CUDA
- *Link*: [https://docs.nvidia.com/cuda/cuda-c-programming-guide/](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)

**4. CUDA C++ Best Practices Guide**
- *Descripción*: Técnicas de optimización y patrones idiomáticos para programación CUDA
- *Link*: [https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)

### Cursos
De este curso puedes encontrar todas las presentaciones en línea:
**CS 179: GPU Programming** de la universidad de Caltech académico con 6 tareas y proyecto de 4 semanas

[https://courses.cms.caltech.edu/cs179/](https://courses.cms.caltech.edu/cs179)

**6. GPU Programming Specialization (Johns Hopkins - Coursera)**
- *Descripción*: Especialización completa en high performance computing con GPUs
- *Link*: [Coursera](https://www.coursera.org/specializations/gpu-programming)

7. NVIDIA CUDA Education & Training**
- *Descripción*: Cursos oficiales de NVIDIA, self-paced e instructor-led
- *Incluye*: GPU-accelerated workstations en la nube, certificaciones
- *Link*: [https://developer.nvidia.com/cuda-education-training](https://developer.nvidia.com/cuda-education-training)

### Recursos Técnicos y Tutoriales

**8. GPU Programming: When, Why and How? (ENCCS)**
- *Descripción*: Guía comprensiva sobre cuándo y cómo usar GPUs
- *Temas*: Conceptos clave, frameworks disponibles, fundamentos prácticos
- *Link*: [https://enccs.github.io/gpu-programming/](https://enccs.github.io/gpu-programming/)

**9. Cornell Virtual Workshop: Understanding GPU Architecture**
- *Descripción*: Material educativo sobre arquitectura de GPUs
- *Link*: [https://cvw.cac.cornell.edu/gpu-architecture](https://cvw.cac.cornell.edu/gpu-architecture)

**10. A Case for Learning GPU Programming with a Compute-First Mindset**
- *Autor*: Maister's Graphics Adventures (Octubre 2025)
- *Descripción*: Meta-tutorial moderno sobre aprender programación GPU
- *Link*: [https://themaister.net/blog/2025/10/05/a-case-for-learning-gpu-programming-with-a-compute-first-mindset/](https://themaister.net/blog/2025/10/05/a-case-for-learning-gpu-programming-with-a-compute-first-mindset/)

### Recursos de Arquitectura

**11. Demystifying GPU Compute Architectures (The Chip Letter)**
- *Descripción*: Análisis profundo de arquitecturas de cómputo GPU modernas
- *Link*: [https://thechipletter.substack.com/p/demystifying-gpu-compute-architectures](https://thechipletter.substack.com/p/demystifying-gpu-compute-architectures)

**12. Understanding GPU Architecture (Scale Computing)**
- *Descripción*: Explicación de estructura, capas y componentes de GPUs
- *Link*: [https://www.scalecomputing.com/resources/understanding-gpu-architecture](https://www.scalecomputing.com/resources/understanding-gpu-architecture)

**13. NASA HECC: Basics on NVIDIA GPU Hardware Architecture**
- *Descripción*: Fundamentos de arquitectura GPU desde perspectiva de cómputo científico
- *Link*: [https://www.nas.nasa.gov/hecc/support/kb/basics-on-nvidia-gpu-hardware-architecture_704.html](https://www.nas.nasa.gov/hecc/support/kb/basics-on-nvidia-gpu-hardware-architecture_704.html)

### Herramientas y SDKs

**14. CUDA Toolkit**
- *Descripción*: Suite completa de desarrollo para GPU computing
- *Incluye*: Librerías, debugger, profiler, compilador, ejemplos de código
- *Link*: [https://developer.nvidia.com/cuda-toolkit](https://developer.nvidia.com/cuda-toolkit)

**15. CUDA Zone - Library of Resources**
- *Descripción*: Hub central de recursos CUDA de NVIDIA
- *Link*: [https://developer.nvidia.com/cuda-zone](https://developer.nvidia.com/cuda-zone)

### Artículos y Papers Académicos

**16. Inside the GPU: A Comprehensive Guide to Modern Graphics Architecture**
- *Fuente*: LearnOpenCV
- *Link*: [https://learnopencv.com/modern-gpu-architecture-explained/](https://learnopencv.com/modern-gpu-architecture-explained/)

**17. GPU Architecture and Programming — An Introduction (Medium)**
- *Autor*: Najeeb Khan
- *Link*: [https://medium.com/@najeebkan/gpu-architecture-and-programming-an-introduction-561bfcb51f54](https://medium.com/@najeebkan/gpu-architecture-and-programming-an-introduction-561bfcb51f54)
