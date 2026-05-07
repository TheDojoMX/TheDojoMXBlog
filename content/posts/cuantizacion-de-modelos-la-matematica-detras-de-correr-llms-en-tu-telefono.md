---
title: "Cuantización de modelos: la matemática detrás de correr LLMs en tu teléfono"
date: 2026-02-15
author: "Héctor Patricio"
tags: ['llm', 'cuantización', 'matemáticas', 'gpu', 'deep-learning', 'machine-learning', 'hardware', 'performance']
description: "Entiende las matemáticas y técnicas detrás de la cuantización que permite correr modelos de lenguaje de miles de millones de parámetros en dispositivos locales."
featuredImage: ""
draft: true
---

<!-- Palabra estimada total: ~4000-4500 palabras -->

Modelos que originalmente requerían clusters de GPUs con decenas de gigabytes
de memoria ahora corren en tu laptop o incluso en tu teléfono. La cuantización
es la técnica que hace esto posible, reduciendo la precisión numérica de los
pesos del modelo sin destruir (demasiado) su capacidad. En este artículo
exploraremos las matemáticas detrás de esta técnica, entenderemos por qué
funciona y aprenderemos a usarla en la práctica.

## Representación numérica: el problema fundamental

<!-- ~500 palabras -->

### IEEE 754: cómo las computadoras representan números reales

<!-- ~300 palabras -->

Repaso de punto flotante: signo, exponente, mantisa. Los formatos comunes:
FP32 (32 bits, ~7 dígitos de precisión), FP16 (16 bits, ~3.3 dígitos),
BF16 (16 bits con más rango que FP16 pero menos precisión). Por qué los
modelos de deep learning se entrenan típicamente en FP16 o BF16. Cada
parámetro de un modelo ocupa estos bytes en memoria. Conectar con el post
del blog sobre GPUs: la memoria de un GPU es limitada y costosa.

### El costo de la precisión: cuánta memoria necesita un LLM

<!-- ~200 palabras -->

Cálculo directo: Llama 3.1 70B en FP16 = 70 mil millones * 2 bytes = 140 GB.
Ni siquiera cabe en un GPU A100 de 80 GB. Para correrlo necesitas múltiples
GPUs o reducir la precisión. Tabla comparativa: modelos populares y su consumo
de memoria en diferentes precisiones. El problema no es solo el almacenamiento:
la velocidad depende del ancho de banda de memoria.

## Por qué funciona la cuantización: intuición matemática

<!-- ~600 palabras -->

### La distribución de los pesos en redes neuronales

<!-- ~300 palabras -->

Los pesos de un modelo entrenado siguen distribuciones aproximadamente
normales (gaussianas), centradas en cero con colas ligeras. La mayoría
de los pesos están concentrados en un rango pequeño, con pocos outliers.
Esto significa que la mayoría de los valores se pueden representar con pocos
bits sin perder mucha información. Visualización: histograma de pesos de
una capa de transformador mostrando la distribución.

### Cuantización uniforme: la idea básica

<!-- ~300 palabras -->

Mapear un rango continuo de valores de punto flotante a un conjunto discreto
de valores enteros. Fórmula: q = round((x - zero_point) / scale). Donde scale
= (max - min) / (2^bits - 1). Ejemplo numérico paso a paso: cuantizar valores
en el rango [-0.5, 0.5] a INT8 (256 niveles). Error de cuantización: la
diferencia entre el valor original y el valor reconstruido. Por qué INT4
(16 niveles) sigue funcionando sorprendentemente bien: la mayoría de los
pesos están tan cerca que 16 niveles bastan para capturar la estructura.

## Técnicas modernas de cuantización

<!-- ~800 palabras -->

### GPTQ: cuantización post-entrenamiento con mínimo error

<!-- ~200 palabras -->

Basado en OBQ (Optimal Brain Quantization). Cuantiza los pesos de una capa
a la vez, compensando el error de cuantización en los pesos restantes.
Usa una pequeña muestra de datos de calibración para estimar el impacto.
Funciona bien para INT4 y INT3. Proceso: cargar modelo -> calibrar con
~128 ejemplos -> cuantizar capa por capa. Desventaja: proceso lento,
pero solo se hace una vez.

### AWQ: cuantización consciente de la activación

<!-- ~200 palabras -->

Observación clave: no todos los pesos son igualmente importantes. Los pesos
que multiplican activaciones de mayor magnitud tienen más impacto en la salida.
AWQ protege estos pesos "salient" escalándolos antes de cuantizar. Resultado:
mejor calidad que GPTQ con el mismo número de bits. Nombre: Activation-aware
Weight Quantization. Explicar la intuición matemática: al escalar los pesos
importantes, su error relativo de cuantización se reduce.

### SmoothQuant: suavizar las activaciones

<!-- ~200 palabras -->

El problema: las activaciones (no los pesos) tienen outliers enormes que
dificultan la cuantización. SmoothQuant migra la dificultad de cuantización
de las activaciones a los pesos aplicando un factor de escala por canal.
Matemáticamente: Y = (X * diag(s)^-1) * (diag(s) * W). Esto "suaviza" las
activaciones y "rugosiza" los pesos, pero los pesos son más fáciles de
cuantizar porque tienen distribuciones más uniformes.

### SpinQuant: rotaciones para eliminar outliers

<!-- ~200 palabras -->

Técnica más reciente que aplica rotaciones ortogonales a los pesos y
activaciones para hacer sus distribuciones más uniformes antes de cuantizar.
Las rotaciones no cambian la computación (son invertibles), pero hacen que
la cuantización sea más efectiva. Resultados: calidad competitiva con INT4
en modelos grandes.

## De 16 bits a 4 bits: qué se pierde y qué se conserva

<!-- ~500 palabras -->

### Métricas de calidad: perplexidad y benchmarks

<!-- ~250 palabras -->

Perplexidad: la métrica estándar para evaluar modelos de lenguaje. Cómo cambia
la perplexidad al cuantizar: FP16 -> INT8 (casi sin pérdida) -> INT4 (1-3%
de degradación) -> INT3 (5-10% de degradación, inaceptable para muchos usos).
Benchmarks de razonamiento (MMLU, HumanEval) muestran patrones similares.
La regla empírica: un modelo grande cuantizado a 4 bits generalmente supera
a un modelo pequeño en 16 bits con la misma huella de memoria.

### El verdadero cuello de botella: ancho de banda de memoria, no cómputo

<!-- ~250 palabras -->

Conectar con el post sobre GPUs. La inferencia de LLMs está limitada por la
velocidad a la que puedes leer los pesos de memoria (memory bandwidth bound),
no por la velocidad de cálculo (compute bound). Cada token generado requiere
leer TODOS los pesos del modelo. Si cuantizas de FP16 a INT4, reduces 4x
la cantidad de datos a leer, acelerando la inferencia ~3-4x. Por eso la
cuantización no solo ahorra memoria, sino que acelera la generación. Números:
un GPU con 2 TB/s de ancho de banda puede generar X tokens/s con FP16 vs
4X tokens/s con INT4.

## Guía práctica: corriendo modelos localmente

<!-- ~600 palabras -->

### llama.cpp y el formato GGUF

<!-- ~200 palabras -->

llama.cpp: la biblioteca que democratizó la inferencia local de LLMs. Escrita
en C/C++ puro, corre en CPU, GPU Apple Silicon, NVIDIA, AMD. El formato GGUF:
cómo empaqueta pesos cuantizados con metadatos. Los niveles de cuantización
en GGUF: Q4_K_M, Q5_K_M, Q6_K, Q8_0. Cómo elegir el nivel correcto para
tu hardware.

### Ollama: la experiencia simplificada

<!-- ~150 palabras -->

Ollama como interfaz de alto nivel sobre llama.cpp. Instalación y uso básico.
El catálogo de modelos pre-cuantizados. API compatible con OpenAI para
integración con aplicaciones existentes. Limitación: menos control que
llama.cpp directo.

### Modelos que funcionan bien cuantizados

<!-- ~250 palabras -->

Llama 3.2 1B y 3B: diseñados para dispositivos móviles, excelentes en Q4.
Gemma 3 (Google): buen rendimiento en tareas de código y razonamiento en Q4.
Phi-4 mini (Microsoft): sorprendente rendimiento para su tamaño. SmolLM2
(Hugging Face): modelos ultra-compactos. Qwen 2.5: fuerte en multilingüe.
Tabla: modelo, tamaño original, tamaño cuantizado Q4, RAM necesaria,
rendimiento en benchmarks. Recomendaciones por tipo de hardware: MacBook
con 8 GB, laptop con 16 GB, PC con GPU discreta.

## Más allá de la cuantización: el futuro

<!-- ~300 palabras -->

### Modelos nativamente eficientes

<!-- ~150 palabras -->

BitNet y modelos de 1 bit: entrenados desde cero con pesos ternarios (-1, 0, 1).
No necesitan cuantización posterior porque son eficientes por diseño. El paper
"The Era of 1-bit LLMs" de Microsoft. Implicaciones: hardware especializado
para inferencia de modelos de 1 bit podría ser transformador.

### Speculative decoding y otros trucos de inferencia

<!-- ~150 palabras -->

Técnicas complementarias a la cuantización: speculative decoding (un modelo
pequeño propone tokens, el grande los verifica en batch), KV-cache quantization,
pruning. Estas técnicas se combinan con cuantización para maximizar la eficiencia.

## Conclusión

<!-- ~200 palabras -->

La cuantización es el puente entre los modelos masivos de la nube y tu
dispositivo local. Las matemáticas son elegantes: aprovechamos las propiedades
estadísticas de los pesos para reducir la precisión sin perder la esencia.
Como desarrolladores, entender estas técnicas nos permite tomar decisiones
informadas sobre qué modelo usar, con qué precisión, y en qué hardware. La
tendencia es clara: los modelos del futuro serán más eficientes por diseño,
y la cuantización es solo el primer paso.

---

## Resumen de investigación

La cuantización reduce la precisión numérica de los pesos de una red neuronal de formatos de punto flotante de alta precisión a representaciones de menor número de bits. Es la técnica principal que permite correr LLMs de miles de millones de parámetros en hardware de consumo.

**Fundamentos de punto flotante.** Los LLMs se entrenan tradicionalmente en FP32 (IEEE 754). BF16 (Brain Float 16) resolvió elegantemente los problemas de FP16 al mantener los 8 bits de exponente de FP32 pero truncar la mantisa a 7 bits, preservando el rango dinámico. La frontera actual es FP8, soportado nativamente en GPUs H100 de NVIDIA, habilitando ~2x speedup de entrenamiento y 50-75% ahorro de memoria.

**Por qué funciona.** Los pesos de redes neuronales entrenadas no están distribuidos uniformemente; siguen distribuciones aproximadamente gaussianas centradas en cero. La cuantización uniforme con enteros mapea bien sobre esta distribución. En la práctica, aproximaciones de 4 bits o incluso 3 bits capturan la información esencial con pérdida mínima de perplejidad. El mayor desafío son las activaciones, que pueden tener outliers sistemáticos de hasta 100x el valor típico.

**El verdadero cuello de botella: ancho de banda de memoria.** La inferencia de LLMs, particularmente la fase de decodificación autoregresiva, está casi universalmente limitada por ancho de banda de memoria, no por cómputo. Para cada token generado, el modelo completo debe ser leído de DRAM a las unidades de cómputo. La cuantización ataca directamente este cuello de botella: reducir la precisión a la mitad duplica el ancho de banda efectivo y aproximadamente duplica el throughput.

**La frontera de 1 bit.** BitNet b1.58 lleva la cuantización al extremo: cada peso es un valor ternario en {-1, 0, +1}, requiriendo solo 1.58 bits por parámetro. La multiplicación se reemplaza por suma y resta, habilitando speedups dramáticos en CPUs ARM y x86 (2-6x) con 55-82% de reducción de energía.

---

### Referencias y fuentes clave

#### Surveys y fundamentos

1. **Gholami, A., Kim, S., Dong, Z., et al. (2021).** "A Survey of Quantization Methods for Efficient Neural Network Inference." [https://arxiv.org/abs/2103.13630](https://arxiv.org/abs/2103.13630) — Survey fundacional del campo de cuantización completo: uniforme vs no-uniforme, PTQ vs QAT, métodos data-free y consideraciones de hardware.

2. **Kalamkar, D., et al. (2019).** "A Study of BFLOAT16 for Deep Learning Training." [https://arxiv.org/pdf/1905.12322](https://arxiv.org/pdf/1905.12322) — Paper autoritativo que establece BF16 como formato práctico de entrenamiento, igualando la precisión de FP32 en visión, habla, lenguaje y recomendación.

3. **Grootendorst, M. (2024).** "A Visual Guide to Quantization." [https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization) — Guía visual con 50+ ilustraciones que cubre todos los conceptos clave de cuantización de forma intuitiva.

#### Métodos de cuantización post-entrenamiento (PTQ)

4. **Frantar, E., Ashkboos, S., Hoefler, T., & Alistarh, D. (2023).** "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers." *ICLR 2023*. [https://arxiv.org/abs/2210.17323](https://arxiv.org/abs/2210.17323) — PTQ capa por capa guiada por Hessiano, comprime OPT-175B a 3-4 bits en ~4 horas GPU. Primer método ampliamente adoptado para cuantizar LLMs de 100B+.

5. **Lin, J., Tang, J., et al. (2024).** "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration." *MLSys 2024 Best Paper*. [https://arxiv.org/abs/2306.00978](https://arxiv.org/abs/2306.00978) — Identifica que solo ~1% de canales de pesos son "salientes" y los protege durante cuantización. Ideal para despliegue en edge.

6. **Xiao, G., Lin, J., et al. (2023).** "SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models." *ICML 2023*. [https://arxiv.org/abs/2211.10438](https://arxiv.org/abs/2211.10438) — Migra dificultad de cuantización de activaciones a pesos mediante escalado por canal, habilitando INT8 sin pérdida con 1.56x speedup.

7. **Tseng, A., Chee, J., et al. (2024).** "QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks." *ICML 2024*. [https://arxiv.org/abs/2402.04396](https://arxiv.org/abs/2402.04396) — Primer método PTQ que demuestra que modelos de 3 bits pueden escalar mejor que los de 4 bits, usando transformadas Hadamard y codebooks E8.

8. **Kim, S., Hooper, C., et al. (2023).** "SqueezeLLM: Dense-and-Sparse Quantization." *ICML 2024*. [https://arxiv.org/abs/2306.07629](https://arxiv.org/abs/2306.07629) — Descomposición dense-and-sparse: mayoría de pesos a 3-4 bits, outliers en precisión completa en matriz sparse.

#### Cuantización durante entrenamiento (QAT)

9. **Liu, J., et al. (2024).** "LLM-QAT: Data-Free Quantization Aware Training for Large Language Models." *Findings of ACL 2024*. [https://arxiv.org/abs/2305.17888](https://arxiv.org/abs/2305.17888) — Extiende QAT a LLMs usando generaciones del propio modelo como datos de calibración, recuperando precisión a 2-4 bits.

10. **Sheng, Z., et al. (2024).** "EfficientQAT: Efficient Quantization-Aware Training for Large Language Models." [https://arxiv.org/abs/2407.11062](https://arxiv.org/abs/2407.11062) — Hace QAT factible a escala 7B-70B. Llama-2-70B a 2 bits en un solo A100-80GB en 41 horas con <3 puntos de degradación.

#### Inferencia y ancho de banda

11. **Dettmers, T., Lewis, M., et al. (2022).** "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale." [https://arxiv.org/abs/2208.07339](https://arxiv.org/abs/2208.07339) — Pionero en descomposición mixed-precision: INT8 para la mayoría, FP16 para outliers. Implementado en la biblioteca `bitsandbytes`.

12. **Yuan, Z., Shang, Y., et al. (2024).** "LLM Inference Unveiled: Survey and Roofline Model Insights." [https://arxiv.org/abs/2402.16363](https://arxiv.org/abs/2402.16363) — Aplica el modelo Roofline para demostrar rigurosamente que la decodificación de LLMs está limitada por ancho de banda de memoria, no por cómputo.

13. **Peng, H., Wu, K., et al. (2023).** "FP8-LM: Training FP8 Large Language Models." [https://arxiv.org/abs/2310.18313](https://arxiv.org/abs/2310.18313) — Entrenamiento end-to-end en FP8 de LLMs escala GPT-175B: 39% reducción de memoria y 75% speedup sobre BF16 en H100.

#### Modelos de 1 bit y hardware

14. **Ma, S., Wang, H., et al. (2024).** "The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits." [https://arxiv.org/abs/2402.17764](https://arxiv.org/abs/2402.17764) — BitNet b1.58: pesos ternarios {-1, 0, +1} entrenados desde cero, igualan la perplejidad de modelos FP16 del mismo tamaño reemplazando multiplicaciones por sumas.

15. **Microsoft Research. (2025).** "BitNet b1.58 2B4T Technical Report." [https://arxiv.org/html/2504.12285v1](https://arxiv.org/html/2504.12285v1) — Primer LLM nativo de 1 bit con pesos abiertos a escala 2B, entrenado en 4T tokens. Cabe en 400MB con 2-6x speedup en CPU y 55-82% reducción de energía.

#### Herramientas prácticas

16. **Gerganov, G. et al. (2023).** "llama.cpp: LLM Inference in C/C++." [https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) — Proyecto que democratizó la inferencia local de LLMs. Formato GGUF con esquemas Q4_K, Q5_K, Q6_K. Soporta Llama, Mistral, Phi, DeepSeek, Qwen.

17. **Xu, D., et al. (2025).** "Fast On-device LLM Inference with NPUs." *ASPLOS 2025*. [https://arxiv.org/html/2407.05858v2](https://arxiv.org/html/2407.05858v2) — Inferencia en NPUs móviles con "shadow outlier execution": hasta 100x speedup vs CPU y 10x vs GPU en dispositivos móviles.

- **Liu et al. (2024).** "SpinQuant: LLM quantization with learned rotations" — Rotaciones ortogonales para hacer distribuciones más uniformes antes de cuantizar.
- **Ollama:** [https://ollama.com](https://ollama.com) — Interfaz de alto nivel sobre llama.cpp con catálogo de modelos pre-cuantizados.
- **IEEE 754** Standard for Floating-Point Arithmetic
- Posts del blog: "¿Qué es un GPU?", "Las matemáticas que debes saber para programar", "Intro a Machine Learning: entendiendo el perceptrón"
