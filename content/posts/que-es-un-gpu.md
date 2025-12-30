---
title: "¿Qué es un GPU?"
date: 2025-12-29
author: "Héctor Patricio"
tags: ['gpu', 'hardware', 'paralelismo', 'performance']
description: "Hablemos de qué es un GPU desde la perspectiva de desarrollo: arquitectura, casos de uso y cuándo aprovecharlo para resolver problemas computacionales complejos."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1760366113/lilian-do-khac-uLyzgGt4MxI-unsplash_ec0low.jpg"
draft: false
---

Si has estado atento a las tendencias de desarrollo de software, te habrás dado
cuenta que la computación especializada cada vez está más extendida, sobre todo
por la proliferación de modelos de machine learning que requieren un montón
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
Esa mejora llega cuando el trabajo es masivamente paralelo (perfectamente paralelizable)
y el costo de mover datos del host al GPU queda amortizado; en cargas pequeñas
o con mucho branching, un CPU con AVX y varios hilos puede igualar o superar al GPU.

Este artículo te explicará qué es un GPU desde la perspectiva de la arquitectura
de computadoras. En otro artículo veremos cómo identificar problemas que puedan
beneficiarse de una implementación en GPUs en lugar de CPUs tradicionales.

## CPU vs GPU: Filosofías de Diseño Diferentes

Para entender un GPU, primero debemos contrastar su diseño con el de un CPU
(Central Processing Unit). Pongamos un ejemplo sencillo.

### CPU: El Artesano experto

Un CPU tiene **pocos núcleos poderosos** (típicamente 4-64 núcleos en CPUs
modernas). Está optimizado **para tareas _secuenciales_ complejas** con
muchas dependencias, o con mucho control de flujo (condicionales, branches).
Ejecuta instrucciones individuales muy rápido, algunas de ellas, dependiendo
de la arquitectura, muy complejas. Por ejemplo, una sola instrucción puede
hacer una operación criptográfica como AES (cifrado) o SHA (hashing).

Los CPUs tienen un _control de flujo sofisticado_: pueden predecir
(estadísticamente) por qué camino se irá el código y prepararse para ello.
También tienen cachés "enormes" (L1, L2, L3) para minimizar la latencia de acceso
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

La comparación es clara: un GPU es como una línea de ensamblaje que tiene miles de
unidades que pueden hacer trabajo simple al mismo tiempo, mientras que un CPU es
como un conjunto de artesanos expertos haciendo trabajo complejo y _secuencial
principalmente_.

Ahora hablemos de la arquitectura de un GPU para ver cómo hace el paralelismo masivo posible.

## Arquitectura de un GPU

Los GPUs modernos organizan sus recursos computacionales en varias capas. Veamos cuáles y cómo puedes usarlas para tus programas.

### Unidades de Procesamiento

El componente principal es el conjunto de núcleos individuales que hacen el trabajo
real, estos pequeños procesadores tienen diferentes nombres dependiendo del
fabricante:

  - **NVIDIA**: CUDA Cores
  - **AMD**: Stream Processors
  - **Intel**: Execution Units (EUs)

Y así... pero la idea es la misma: muchos núcleos o procesadores encargados
de hacer operaciones matemáticas básicas.

Estos núcleos están agrupados en unidades mayores que llamamos **Streaming Multiprocessors (SMs)**
y tienen una memoria rápida compartida entre ellos. A nivel global, tenemos otro nivel de memoria accesible a todos los SMs.

Desde 2017 (con la arquitectura Volta) y sobre todo pensando en cargas de operaciones matriciales complejas
(como las que se usan en machine learning) se han añadido unidades especializadas: los **Tensor Cores**.
La industria se está adaptando a los nuevos usos del
software.

### Jerarquía de Memoria

Al igual que los _CPUs_, los GPUs tienen un conjunto de diferentes tipos (y velocidades) de memoria.
La jerarquía de memoria típica en un GPU es:

1. **Registros**: Memoria ultra-rápida privada de cada thread para operaciones inmediatas
2. **Memoria compartida**: A nivel de bloque de los SMs, muy rápida, accesible por threads del mismo bloque
3. **Memoria global**: Memoria grande pero con mayor latencia, accesible por todos los threads
4. **Memoria de textura/constantes**: Optimizada para patrones específicos de acceso (solo lectura)
5. **Memoria de host**: La RAM del sistema, accesible a través del bus PCIe (la más lenta)

El patrón de acceso es importante: los accesos coalescidos (threads contiguos leyendo direcciones contiguas)
aprovechan el ancho de banda; accesos dispersos o sin alineación
se penalizan con más transacciones y mayor latencia efectiva.

### Modelo de Ejecución de un GPU

Veamos cómo corre un programa en un GPU: primero el programa se divide
en **kernels**. Un kernel es una función que se ejecuta aprovechando
la estructura de procesamiento del GPU: lanza cientos o miles de threads en paralelo.
Cada thread ejecuta la misma función pero con datos diferentes. Un **thread** (hilo)
es la unidad básica de ejecución en un GPU.

La jerarquía de ejecución es:

- **Warp**: Grupo de **32 threads (en NVIDIA)** que ejecutan la misma instrucción simultáneamente en lockstep.
Es la unidad mínima de scheduling. En AMD se llaman wavefronts y suelen ser de 32 o 64 threads.
- **Bloque de threads**: Grupo de threads (múltiples warps) que pueden cooperar y compartir memoria. Un bloque puede tener hasta 1024 threads.
- **Grid**: Colección de bloques que ejecutan el mismo kernel. Puede tener miles de bloques.


### Ancho de Banda vs Latencia

Los GPUs priorizan **throughput** (cantidad de trabajo procesado, basado en datos)
sobre **latencia** (tiempo para una operación individual). Esto significa
que aunque una operación individual puede tardar más en GPU que en CPU, el
GPU puede procesar miles de operaciones simultáneamente, resultando en mayor throughput total.

## Paralelismo de Datos

El modelo de programación de GPUs se basa en **SIMD/SIMT** (Single Instruction, Multiple Data / Single Instruction, Multiple Threads):

- **SIMD** (usado también en CPUs): Una instrucción opera sobre múltiples
datos en registros vectoriales
- **SIMT** (específico de GPUs): Similar, pero cada thread tiene su propio
contador de programa. Todos los threads en un warp ejecutan la misma instrucción
al mismo tiempo sobre diferentes datos

### Ejemplo Práctico

**Problema A**: Multiplicar 1 millón de números por una constante

- **Paralelismo perfecto**: Cada operación es independiente
- **GPU gana dramáticamente**: 100x más rápido o más dependiendo del hardware

**Problema B**: Construir un árbol de decisión con lógica compleja
- **Inherentemente secuencial**: Cada decisión depende de la anterior
- **CPU gana**: Mejor control de flujo y menor overhead

**Benchmark rápido (PyTorch)**: mide multiplicar un vector grande en CPU vs GPU (ideal para Colab con GPU).

```python
import torch, time

device = "cuda" if torch.cuda.is_available() else "cpu"
a = torch.rand(10_000_000, device=device)
b = torch.rand(10_000_000, device=device)

def run(dev):
    x, y = a.to(dev), b.to(dev)
    if dev == "cuda":
        torch.cuda.synchronize()
    t0 = time.time()
    z = x * y + 1.0
    if dev == "cuda":
        torch.cuda.synchronize()
    return time.time() - t0

print("CPU:", run("cpu"))
if torch.cuda.is_available():
    print("GPU:", run("cuda"))
```

La primera llamada en GPU incluye overhead de inicialización; las siguientes suelen ser mucho más rápidas.

### Complejidad de Programación - Desafíos

Programar para GPUs es completamente diferente que programar para CPUs. Aquí
algunos retos:

- **Debugging**: Más difícil que código CPU, porque tenemos herramientas más limitadas
- **Profiling**: Herramientas especializadas necesarias (NVIDIA Nsight, AMD ROCm Profiler)
- **Curva de aprendizaje**: Entender modelo de memoria y ejecución
- **Portabilidad**: CUDA es específico de NVIDIA (alternativas: OpenCL, SYCL, HIP)

### Cuándo NO usar GPU

No todos los problemas se benefician de un GPU. Aquí algunos casos donde un CPU puede ser mejor:

- Lotes pequeños o poca aritmética por dato: el overhead de lanzar kernels y mover datos por PCIe elimina cualquier ganancia.
- Algoritmos con mucha divergencia de branches: los warps/wavefronts se serializan y pierdes throughput. A esto le llamamos _warp divergence_.
- Datos que no caben en VRAM o flujos con mucho ida y vuelta host <-> GPU: el bus se vuelve el cuello de botella.
- Latencias ultrabajas por petición (p.ej., microservicios síncronos): el cold-start y la cola del GPU pueden ser peores que un CPU saturado.

### Consumo Energético

Los GPUs consumen más energía total que los CPUs, aunque en cargas masivas suelen entregar mejor rendimiento por watt.

Para dar contexto:
- **CPU de escritorio típico**: 65-125W
- **GPU de alto rendimiento (RTX 4090)**: 450W
- **GPU de datacenter (H100)**: 700W

Además del consumo, considera:
- Hardware costoso (una H100 cuesta aprox $30,000 USD, una RTX 4090 aprox $1,600 USD)
- Refrigeración y infraestructura adicional necesaria

GPUs integrados (iGPU) comparten memoria con el CPU: menos potencia pero sin viaje por PCIe y útiles para prototipos o edge; los discretos (dGPU) tienen VRAM dedicada y mucho más throughput, a cambio de consumo y costo mayores.

## Librerías que Abstraen el GPU

No siempre necesitas programar en CUDA directamente. Muchas librerías aprovechan
GPUs de forma transparente:

- **Deep Learning**: PyTorch, TensorFlow, JAX
- **Data Science**: cuDF, RAPIDS (equivalentes a Pandas pero en GPU)
- **Computación científica**: CuPy (NumPy en GPU), cuBLAS
- **Procesamiento de imágenes**: OpenCV con CUDA
- **Alternativas AMD/Intel/portables**: ROCm (hip, MIOpen, rocBLAS), oneAPI/SYCL (DPC++), OpenCL para no depender solo de CUDA.

## Futuro y Tendencias

### GPU Programming Más Accesible

Tenemos algunas opciones para programar GPUs sin lidiar directamente con CUDA

- **Compiladores inteligentes**: Generación automática de código GPU
- **Lenguajes de alto nivel**: Triton (Python para kernels), Mojo, SYCL
- **Auto-tuning**: Optimización automática de parámetros

### Hardware Especializado

- **TPUs (Tensor Processing Units)**: Optimizadas para operaciones de ML, desarrolladas por Google
- **NPUs (Neural Processing Units)**: IA en edge devices y dispositivos móviles
- **FPGAs (Field-Programmable Gate Arrays)**: Hardware reconfigurable para cargas específicas, menor consumo pero más difíciles de programar

### GPUs en la Nube

Si no tienes un GPU físico hay varias formas de acceder a GPUs de alto rendimiento,
de forma remota y sin mucha inversión por adelantado:

- **Serverless GPU**: Paga solo por el tiempo de uso (Modal, RunPod, Lambda Labs). Son modelos administrados con cobro por minuto/hora; no siempre hay cold start cero y la disponibilidad varía por región.
- **Spot instances**: GPU computing económico (AWS, GCP, Azure)
- **Kubernetes con GPUs**: Orquestación de cargas GPU
- **Google Colab / Kaggle**: GPUs gratuitas para experimentación

## Conclusión

Los GPUs representan una herramienta fundamental en el arsenal del desarrollador
moderno para resolver problemas que involucran paralelismo masivo de datos.

Entender su arquitectura, fortalezas y limitaciones te permite identificar
oportunidades donde una implementación en GPU puede transformar un problema
intratable en uno solucionable.

La clave está en reconocer el patrón: **¿Estás aplicando la misma operación a muchos datos?** Si la respuesta es sí, probablemente hay una oportunidad de aceleración con GPU.

Si quieres experimentar sin instalar nada, abre Google Colab y prueba PyTorch o TensorFlow con GPU habilitado. Verás la diferencia de velocidad en minutos.

## Referencias y Recursos para Profundizar

La programación de GPUs es un campo amplio y bastante diferente a la programación
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

**CUDA C++ Programming Guide**
- *Fuente*: NVIDIA Official Documentation
- *Descripción*: Documentación completa y oficial del modelo de programación CUDA
- *Link*: [https://docs.nvidia.com/cuda/cuda-c-programming-guide/](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)

**CUDA C++ Best Practices Guide**
- *Descripción*: Técnicas de optimización y patrones idiomáticos para programación CUDA
- *Link*: [https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)

### Cursos

**CS 179: GPU Programming** - Caltech
- De este curso puedes encontrar todas las presentaciones en línea
- Curso académico con 6 tareas y proyecto de 4 semanas
- *Link*: [https://courses.cms.caltech.edu/cs179/](https://courses.cms.caltech.edu/cs179)

**GPU Programming Specialization** - Johns Hopkins (Coursera)
- *Descripción*: Especialización completa en high performance computing con GPUs
- *Link*: [Coursera](https://www.coursera.org/specializations/gpu-programming)

**NVIDIA CUDA Education & Training**
- *Descripción*: Cursos oficiales de NVIDIA, self-paced e instructor-led
- *Incluye*: GPU-accelerated workstations en la nube, certificaciones
- *Link*: [https://developer.nvidia.com/cuda-education-training](https://developer.nvidia.com/cuda-education-training)

### Recursos Técnicos y Tutoriales

**GPU Programming: When, Why and How? (ENCCS)**
- *Descripción*: Guía comprensiva sobre cuándo y cómo usar GPUs
- *Temas*: Conceptos clave, frameworks disponibles, fundamentos prácticos
- *Link*: [https://enccs.github.io/gpu-programming/](https://enccs.github.io/gpu-programming/)

**Cornell Virtual Workshop: Understanding GPU Architecture**
- *Descripción*: Material educativo sobre arquitectura de GPUs
- *Link*: [https://cvw.cac.cornell.edu/gpu-architecture](https://cvw.cac.cornell.edu/gpu-architecture)

**A Case for Learning GPU Programming with a Compute-First Mindset**
- *Autor*: Maister's Graphics Adventures (Octubre 2025)
- *Descripción*: Meta-tutorial moderno sobre aprender programación GPU
- *Link*: [https://themaister.net/blog/2025/10/05/a-case-for-learning-gpu-programming-with-a-compute-first-mindset/](https://themaister.net/blog/2025/10/05/a-case-for-learning-gpu-programming-with-a-compute-first-mindset/)

### Recursos de Arquitectura física

**Demystifying GPU Compute Architectures (The Chip Letter)**
- *Descripción*: Análisis profundo de arquitecturas de cómputo GPU modernas
- *Link*: [https://thechipletter.substack.com/p/demystifying-gpu-compute-architectures](https://thechipletter.substack.com/p/demystifying-gpu-compute-architectures)

**Understanding GPU Architecture (Scale Computing)**
- *Descripción*: Explicación de estructura, capas y componentes de GPUs
- *Link*: [https://www.scalecomputing.com/resources/understanding-gpu-architecture](https://www.scalecomputing.com/resources/understanding-gpu-architecture)

**NASA HECC: Basics on NVIDIA GPU Hardware Architecture**
- *Descripción*: Fundamentos de arquitectura GPU desde perspectiva de cómputo científico
- *Link*: [https://www.nas.nasa.gov/hecc/support/kb/basics-on-nvidia-gpu-hardware-architecture_704.html](https://www.nas.nasa.gov/hecc/support/kb/basics-on-nvidia-gpu-hardware-architecture_704.html)

### Herramientas y SDKs

**CUDA Toolkit**
- *Descripción*: Suite completa de desarrollo para GPU computing
- *Incluye*: Librerías, debugger, profiler, compilador, ejemplos de código
- *Link*: [https://developer.nvidia.com/cuda-toolkit](https://developer.nvidia.com/cuda-toolkit)

**CUDA Zone - Library of Resources**
- *Descripción*: Hub central de recursos CUDA de NVIDIA
- *Link*: [https://developer.nvidia.com/cuda-zone](https://developer.nvidia.com/cuda-zone)

### Artículos y Papers Académicos

**Inside the GPU: A Comprehensive Guide to Modern Graphics Architecture**
- *Fuente*: LearnOpenCV
- *Link*: [https://learnopencv.com/modern-gpu-architecture-explained/](https://learnopencv.com/modern-gpu-architecture-explained/)

**GPU Architecture and Programming — An Introduction (Medium)**
- *Autor*: Najeeb Khan
- *Link*: [https://medium.com/@najeebkan/gpu-architecture-and-programming-an-introduction-561bfcb51f54](https://medium.com/@najeebkan/gpu-architecture-and-programming-an-introduction-561bfcb51f54)
