---
title: "Computación de alto rendimiento (HPC) con GPU: mapa del terreno"
date: 2025-01-15
author: "Héctor Iván Patricio Moreno"
tags: ['-', 'GPU']
description: "Entiende cuándo conviene usar GPU, qué problemas resuelve mejor y qué aprenderás en esta serie de 22 artículos sobre HPC con CUDA, Triton y PyTorch."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1759763294/jonny-gios-2vVhfhbj5-s-unsplash_eyg5dh.jpg"
draft: true
---

Este es el primer artículo de una serie en la que hablaremos de **computación de alto
rendimiento** (High Perfomance Computing - HPC) usando GPUs, específicamente
para cargas de trabajo relacionadas con machine learning y data science, algo de
lo que más aplicación tiene hoy.

Antes de entrar en materia hablemos de manera más general sobre qué es HPC y por qué
vamos a enfocarnos en la vertiente que usa los GPUs.

## ¿Qué es High Perfomance Computing?

El término **HPC** es un campo amplio que abarca técnicas, hardware y software para hacer
que las computadoras resuelvan problemas complejos de manera eficiente, y casi siempre
tiene que ver con ejecutar grandes cantidades de cálculos. Esto se puede
lograr de muchas formas. Algunas de las más comunes son:

- **Paralelismo y concurrencia**: Dividir el trabajo en partes que se puedan ejecutar al
mismo tiempo en muchísimos núcleos o máquinas. Cuando nos referimos a HPC y paralelismo en
múltiples cores estamos hablando de cientos o miles de núcleos. Además, se requieren
entornos de ejecución especiales como MPI (Message Passing Interface) para coordinar
el trabajo entre nodos. Otra forma de paralelismo es usar GPUs, que tienen miles de núcleos
simples diseñados para ejecutar la misma operación en muchos datos a la vez (SIMT - Single
Instruction Multiple Threads).

- **Optimización de algoritmos**: Este es un campo de estudio enorme que siempre está
buscando la forma de lograr resultados con menos cálculos o usando mejor el hardaware que
soporta esos cálculos.

Pero empecemos desde las mismísimas bases para no obviar nada.

### ¿Qué es un GPU?

Un **GPU** (Graphics Processing Unit) es un procesador especializado, originalmente
diseñado para acelerar el renderizado de elementos gráficos en videojuegos y programas
de diseño (CAD y para diseño industrial). Ahora estamos completamente acostumbrados a su
existencia, pero cuando nacieron las computadoras personales, no era común que las tuvieran.

### ¿Qué hace diferente a una GPU?

- **Miles de núcleos simples** contra decenas de núcleos complejos en CPU. Un núcleo simple puede
ejecutar operaciones matemáticas básicas muy rápido.
- Diseñada para **paralelismo masivo**: misma operación en muchos datos (SIMT: Single Instruction, Multiple Threads)
- **Memoria de alto ancho de banda**: hasta 10× más throughput que RAM de CPU
- **Especialización**: hardware dedicado para operaciones comunes (matmul, convoluciones)

### Algunas reglas qu vale la pena recordar - reglas de platino

Ley de Amdahl: la aceleración está limitada por la parte no paralelizable; perfila antes de invertir.
Intensidad aritmética: si haces muchas operaciones por byte movido, la GPU suele ganar; si mueves más de lo que calculas, optimiza memoria primero.

SIMD (CPU) vs SIMT (GPU): SIMD usa lanes vectoriales en un core; SIMT ejecuta muchos threads en warps con la misma instrucción.

### Candidatos ideales para GPU

**Cómputo denso y regular**

- Multiplicación de matrices grandes
- Convoluciones en imágenes
- Simulaciones físicas con grids uniformes

**Alto paralelismo de datos**
- Procesar millones de píxeles, puntos, embeddings
- Operaciones elementwise en tensores grandes

**Poco branching condicional**
- Flujos de control predecibles
- Sin if/else complejos que divergen entre threads


Por eso el GPU es la columna vertebral del deep learning: las redes neuronales se pueden
programar como una serie de operaciones matemátcas densas sin casi nada de lógica
condicional.

### Cuándo la GPU no ayuda


**Lógica secuencial compleja**
- Algoritmos con dependencias entre pasos
- Mucho código condicional (if/else por cada dato)

❌ **Conjuntos de datos pequeños**
- Overhead de transferencia CPU↔GPU domina
- Latencia de lanzamiento de kernels

❌ **Acceso irregular a memoria**
- Patrones de acceso impredecibles
- Estructuras dispersas sin localidad

---

## Qué cubrirá esta serie (22 artículos)

### Bloque 1: Fundamentos y setup (posts 1-3)
1. **Mapa del terreno** (este post)
2. Setup de entorno: drivers, CUDA Toolkit, PyTorch, Triton
3. Tensores en GPU con PyTorch: transferencias, dtypes, benchmarks

### Bloque 2: Triton — kernels de alto nivel (posts 4-5)
4. Tu primer kernel en Triton: suma de vectores
5. Transformaciones elementwise y broadcasting

### Bloque 3: CUDA C++ — control total (posts 6-9)
6. Tu primer kernel CUDA: compilación, lanzamiento, depuración
7. Hilos, bloques, warps e indexación segura
8. Jerarquía de memoria: global, shared, constant, coalescing
9. Reducciones eficientes con shared memory

### Bloque 4: Algoritmos fundamentales (posts 10-13)
10. Scan (prefix sum): base de muchos algoritmos
11. Matmul I: baseline ingenuo y límites teóricos
12. Roofline model: memoria vs cómputo
13. Matmul II: tiling y shared memory

### Bloque 5: Optimización y depuración (posts 14-17)
14. Warp-level primitives: shuffles y reducciones
15. Depuración GPU: `cuda-gdb`, `compute-sanitizer`, errores típicos
16. Streams y solapamiento: cómputo + I/O asíncrono
17. Perfilado con `Nsight`: métricas clave y cuellos de botella

### Bloque 6: Librerías y ecosistema (posts 18-20)
18. CuBLAS/cuDNN: cuándo usar librerías optimizadas
19. Extensiones CUDA para PyTorch: custom ops con autograd
20. Triton avanzada: matmul con heurísticas

### Bloque 7: Producción (posts 21-22)
21. Mixed precision y Tensor Cores: FP16/BF16 en práctica
22. Caso de estudio end-to-end: training loop optimizado

Caso guía que retomaremos: partimos de un `matmul` y una reducción base, y los optimizamos paso a paso (tiling, shared memory, warp-level) hasta producción.

---

## Práctica guiada: checklist de "síntomas GPU"

Responde estas preguntas sobre tu proyecto actual:

### ¿Es buen candidato para GPU?

Regla práctica: >1e6 elementos o tensores de decenas de MB suelen justificar GPU si hay paralelismo; valida con perfiles.

| Pregunta | Sí | No |
|----------|----|----|
| ¿Operas sobre >1M elementos regularmente? | ⬜ | ⬜ |
| ¿La mayoría de operaciones son numéricas (matmul, convoluciones, activaciones)? | ⬜ | ⬜ |
| ¿El flujo de control es predecible (sin if/else complejos por dato)? | ⬜ | ⬜ |
| ¿El cuello de botella actual es cómputo (no I/O)? | ⬜ | ⬜ |
| ¿Puedes procesar datos en lotes grandes? | ⬜ | ⬜ |

**3+ respuestas "Sí"**: excelente candidato
**1-2 respuestas "Sí"**: evalúa perfiles antes de invertir
**0 respuestas "Sí"**: probablemente la GPU no ayude

### Ejemplos concretos

✅ **Buenos candidatos**:
- Training de redes neuronales (matmul masivo)
- Procesamiento de imágenes en batch (convoluciones, filtros)
- Simulaciones numéricas en grids (física, fluidos)
- Criptominería (hashing masivo y regular)

❌ **Malos candidatos**:
- Parser de JSON con lógica compleja
- Web scraper con decisiones por página
- Algoritmos con mucho branching (árboles de decisión profundos)
- Consultas SQL complejas con joins irregulares

---

## Pitfalls comunes

### 1. "Más rápido en GPU siempre"
No. El overhead de transferencia CPU↔GPU puede dominar en datos pequeños.

**Solución**: benchmark con tamaños realistas antes de migrar.

### 2. "Usar GPU es compilar con `-DGPU`"
Código CPU no se acelera automáticamente. Necesitas reescribir algoritmos para paralelismo masivo.

**Solución**: acepta que HPC con GPU requiere diseñar diferente.

### 3. "Necesito aprender todo CUDA antes de empezar"
Puedes lograr mucho con PyTorch + Triton sin tocar CUDA directamente.

**Solución**: esta serie va de high-level (PyTorch/Triton) a low-level (CUDA) gradualmente.

---

## Entrega: tu checklist aplicada

**Acción**: toma un proyecto o problema actual y completa el checklist de arriba. Escribe en 2-3 líneas:
- ¿Es candidato para GPU?
- ¿Qué operaciones específicas acelerarías?
- ¿Cuál es el riesgo principal (overhead, complejidad, datos pequeños)?

Guarda esta reflexión. Al final de la serie (post 22), revisarás si tu análisis inicial era correcto.

---

## Qué estudiar para escribir este artículo


### Fundamentos necesarios

1. **Arquitectura básica GPU vs CPU**
   - Conceptos: núcleos, SIMT, memoria de alto ancho de banda
   - Recursos: NVIDIA CUDA C Programming Guide (Capítulo 1), "Programming Massively Parallel Processors" (Cap. 1-2)

2. **Modelo de programación paralela**
   - Conceptos: paralelismo de datos, SIMD/SIMT, divergencia de hilos
   - Recursos: artículos introductorios sobre GPU computing, documentación CUDA conceptual

3. **Trade-offs CPU vs GPU**
   - Conceptos: latencia vs throughput, overhead de transferencia, cuándo paralelizar
   - Recursos: benchmarks publicados, casos de estudio de migración a GPU

### Lecturas recomendadas
- **NVIDIA CUDA C Programming Guide**: Introducción y modelo de programación
- **"Programming Massively Parallel Processors"** (Kirk & Hwu): Capítulos 1-3
- **Documentación PyTorch**: sección "CUDA Semantics"
- **Papers**: "Roofline Model" (Williams et al.) para entender límites teóricos

### Práctica previa
- Experiencia básica con PyTorch o NumPy (manejo de arrays/tensores)
- Entender qué es un cuello de botella de rendimiento
- Haber perfilado código al menos una vez (con time, cProfile, o similar)
- Familiaridad con conceptos de paralelismo (threads, procesos)
