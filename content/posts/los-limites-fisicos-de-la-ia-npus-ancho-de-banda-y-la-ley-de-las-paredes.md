---
title: "Los límites físicos de la IA: NPUs, ancho de banda de memoria y la ley de las paredes"
date: 2026-02-15
author: "Héctor Patricio"
tags: ['hardware', 'gpu', 'npu', 'inteligencia-artificial', 'performance', 'ciencias-de-la-computación', 'paralelismo']
description: "La IA no solo depende del software: exploramos los límites físicos del hardware que frena la inferencia, por qué domina Mixture of Experts, y qué viene después de la ley de Moore."
featuredImage: ""
draft: true
---

<!-- Palabra estimada total: ~4,750 palabras -->

## Introducción: la IA choca contra la física

<!-- ~400 palabras -->

Contextualizar: mientras la industria se enfoca en modelos más grandes y algoritmos
más sofisticados, los límites físicos del hardware imponen restricciones fundamentales
que no se pueden resolver solo con software. Este artículo explora esas restricciones
y qué significan para el futuro de la IA.

Puntos clave:
- Referencia al artículo del blog sobre GPUs
- La brecha entre lo que el software puede hacer y lo que el hardware puede entregar
- Las tres "paredes" que frenan el progreso: memoria, cómputo y energía

## Contexto histórico: las leyes que nos trajeron aquí

<!-- ~600 palabras -->

Antes de entender los límites actuales, repasemos las leyes y observaciones que
definieron el progreso del hardware durante décadas.

### La ley de Moore: lo que realmente dice (y cuándo dejó de aplicar)

Moore predijo que el número de transistores se duplicaría cada dos años. Esto se
mantuvo durante décadas pero ya no se traduce en mejoras proporcionales de
rendimiento. La ley sigue viva en cantidad de transistores, pero murió en
rendimiento por transistor.

### El escalamiento de Dennard: la pared que nadie vio venir

El escalamiento de Dennard decía que al reducir transistores, el voltaje y
corriente se reducían proporcionalmente, manteniendo la densidad de potencia
constante. Dejó de funcionar alrededor de 2006. Consecuencia: no podemos subir
la frecuencia sin derretir el chip.

### La ley de Amdahl: el límite de la paralelización

No importa cuántos núcleos tengas, la porción secuencial de tu programa limita
la aceleración máxima. Relevancia directa para inferencia de IA, donde algunas
operaciones son inherentemente secuenciales.

## La pared de memoria: el verdadero cuello de botella

<!-- ~800 palabras -->

El límite más crítico para la inferencia de modelos de IA no es el cómputo,
sino la velocidad a la que puedes mover datos de la memoria al procesador.

### Por qué la inferencia está limitada por memoria, no por cómputo

Para generar cada token, un modelo transformer necesita leer TODOS los pesos del
modelo de la memoria. Para un modelo de 70B parámetros en FP16, eso son ~140GB
que deben transferirse. El ancho de banda de HBM3 (~1-2 TB/s) permite solo
~10-14 tokens por segundo, sin importar cuántos TFLOPS tenga tu GPU.

### Arithmetic intensity y el modelo roofline

Explicar el concepto de intensidad aritmética: la proporción entre operaciones
de cómputo y bytes transferidos. La inferencia autoregresiva de transformers
tiene intensidad aritmética muy baja -- está en la zona limitada por memoria
del modelo roofline.

### Batch size como parche, no como solución

Aumentar el batch size mejora la eficiencia porque reutilizas los pesos para
múltiples secuencias. Pero tiene límites: latencia del primer token, memoria
para KV-cache, y no todos los casos de uso permiten batching.

### La diferencia entre entrenamiento e inferencia

El entrenamiento es compute-bound (grandes multiplicaciones de matrices). La
inferencia es memory-bound (lectura secuencial de pesos). Por eso optimizar
entrenamiento e inferencia requiere hardware fundamentalmente diferente.

## NPUs móviles: la promesa subutilizada

<!-- ~500 palabras -->

Las NPUs (Neural Processing Units) en dispositivos móviles tienen capacidades
impresionantes sobre el papel pero enfrentan limitaciones prácticas.

### Qué hay dentro de una NPU moderna

Apple Neural Engine, Qualcomm Hexagon, Google Tensor TPU móvil. Capacidades de
cómputo en TOPS (Trillions of Operations Per Second) y por qué esos números
son engañosos.

### La fase de decodificación: donde las NPUs se quedan sin trabajo

Durante la generación autoregresiva, cada paso produce un solo token. La NPU,
diseñada para paralelismo masivo, queda subutilizada porque no hay suficiente
trabajo paralelo. Es como tener una fábrica de 1000 trabajadores haciendo una
sola pieza a la vez.

### ExecuTorch 1.0 y la madurez de la inferencia móvil

Meta lanzó ExecuTorch 1.0, un runtime optimizado para inferencia en dispositivos.
Análisis de qué permite hoy: modelos de hasta 3B parámetros con latencia
aceptable, pero con limitaciones significativas.

## Mixture of Experts: la respuesta de la industria a la pared de memoria

<!-- ~600 palabras -->

Por qué el 60%+ de los modelos frontera usan arquitectura MoE.

### Cómo MoE esquiva el cuello de botella de memoria

En un modelo MoE, solo una fracción de los parámetros se activa para cada token
(típicamente 2 de 8 expertos). Esto significa que no necesitas leer TODOS los
pesos, solo los del experto activo. Si tu modelo tiene 671B parámetros pero
solo activa 37B por token, reduces la carga de memoria 18x.

### DeepSeek como caso de estudio

DeepSeek-R1 usa MoE extensivamente. Conectar con el post sobre DeepSeek: parte
de la razón por la que fue tan eficiente es la arquitectura MoE.

### Trade-offs de MoE

Mayor tamaño total del modelo (necesitas más VRAM total), routing impredecible
que dificulta la optimización de hardware, y mayor complejidad en entrenamiento
distribuido.

## La pared de cómputo y la pared de energía

<!-- ~500 palabras -->

Más allá de la memoria, hay dos paredes más.

### La pared de cómputo

Entrenar GPT-4 requirió aproximadamente 2e25 FLOPs. Los modelos más grandes
siguen requiriendo órdenes de magnitud más cómputo. Pero la mejora en FLOPS por
chip crece linealmente, no exponencialmente.

### La pared de energía

Un cluster de entrenamiento de un modelo frontera consume la energía equivalente
a una ciudad pequeña. Los centros de datos de IA ya consumen el 2-3% de la
electricidad global, y está creciendo. ¿Es esto sostenible?

### El problema del enfriamiento

Más potencia = más calor. Las soluciones de enfriamiento líquido y por inmersión
se están convirtiendo en estándar, pero tienen sus propios costos y complejidades.

## Lo que viene: tendencias en hardware para IA

<!-- ~700 palabras -->

Las tecnologías y enfoques que intentan superar estas paredes.

### HBM4 y el futuro del ancho de banda de memoria

La próxima generación de High Bandwidth Memory promete 2-4x más ancho de banda.
Cuánto ayuda esto y si es suficiente.

### Chiplets y diseño heterogéneo

En lugar de un chip monolítico gigante, unir múltiples chips pequeños
especializados (compute chiplet + memory chiplet + I/O chiplet). AMD ya lo
hace con sus CPUs.

### Computación fotónica: procesar con luz

Startups como Lightmatter y Luminous Computing proponen usar fotones en lugar de
electrones para las multiplicaciones de matrices. Ventajas teóricas: velocidad
de la luz, casi cero calor. Estado actual: muy temprano pero prometedor.

### Computación in-memory: eliminar el movimiento de datos

Si no puedes mover los datos más rápido, mueve el cómputo a donde están los
datos. Procesadores en memoria (PIM) y CXL como tecnologías habilitadoras.

### Computación cuántica: ¿relevante para IA?

Breve análisis: la computación cuántica tiene aplicaciones potenciales en
optimización (entrenamiento), pero no en inferencia. No es una solución a
corto plazo para los problemas actuales.

## Implicaciones para los desarrolladores

<!-- ~400 palabras -->

Qué significan estos límites físicos para las decisiones que tomamos como
desarrolladores.

### Cuantización y eficiencia del modelo importan más que nunca

Si la memoria es el cuello de botella, reducir el tamaño del modelo (4-bit,
2-bit cuantización) tiene un impacto directo en velocidad. GGUF, GPTQ, AWQ
como herramientas prácticas.

### Elegir el hardware correcto para tu caso de uso

No todo necesita un H100. Para inferencia de modelos pequeños, un Apple M4 con
UMA puede ser más eficiente en costo/rendimiento que una GPU discreta.

### Diseñar para las limitaciones del hardware

Entender las limitaciones físicas te permite diseñar sistemas que las respeten
en lugar de luchar contra ellas. Batching, caching de KV, speculative decoding
como técnicas que nacen de entender el hardware.

## Conclusión: la física como maestra de humildad

<!-- ~250 palabras -->

Resumen: el software de IA avanza rápido, pero la física impone límites duros.
Entender estos límites no es solo conocimiento teórico -- informa directamente
las decisiones de arquitectura, la selección de hardware y las expectativas
realistas sobre qué es posible.

---

## Resumen de investigación

Tres "paredes" interconectadas — memoria, cómputo y energía — convergen para restringir el escalamiento de la IA de maneras que las mejoras puramente algorítmicas o de software no pueden resolver completamente.

**El fin del escalamiento gratuito.** El escalamiento de Dennard se rompió ~2005-2007 (corrientes de fuga dejaron de escalar), terminando la era del escalamiento de frecuencia. Desde ~2010, el progreso de semiconductores se desaceleró por debajo del ritmo de Moore. La respuesta: especialización extrema y heterogeneidad arquitectónica (Shalf, 2020).

**La pared de memoria: el cuello de botella dominante.** Los FLOPS de chips de IA crecen ~3x cada 2 años, pero el ancho de banda DRAM crece solo 1.6x y el de interconexión solo 1.4x (Gholami et al., 2024). La decodificación autoregresiva de LLMs requiere leer todos los pesos del modelo para cada token generado. El modelo Roofline confirma que virtualmente todas las operaciones de decode son memory-bound. HBM evoluciona hacia HBM4 (~2.8 TB/s por stack) pero la demanda supera la oferta.

**Hardware especializado.** TPU v7 "Ironwood" de Google (4,614 TFLOP/s por chip), Apple Neural Engine (35 TOPS en A19 Pro), Qualcomm Hexagon (45+ TOPS en Snapdragon X Elite). Cerebras WSE-3 (4 billones de transistores, 125 petaflops) ataca la pared de memoria integrando SRAM on-chip masiva, eliminando la latencia DRAM.

**MoE como arquitectura hardware-aware.** DeepSeek-V3 activa solo ~37B de 671B parámetros por paso de inferencia, reduciendo requisitos de ancho de banda de memoria y logrando throughput de inferencia hasta 5.76x mayor que modelos densos equivalentes.

**Energía: la tercera pared.** Inferencia ya domina el consumo total de energía de IA (60-70% en 2025). Data centers de IA en EE.UU. consumieron 53-76 TWh en 2024, con proyecciones de 165-326 TWh para 2028. Google reporta que la mediana de prompt de Gemini usa 0.24 Wh, pero lograron reducción de 33x en energía por prompt en 12 meses.

**Hardware emergente.** Computación fotónica (Lightmatter, valuación $4.4B): luz en lugar de electrones para operaciones matriciales. Computación neuromórfica (Intel Hala Point: 1.15 mil millones de neuronas, 2,600W). Compute-in-memory (CIM): operaciones MAC analógicas directamente en arrays de memoria, eliminando el cuello de botella de von Neumann.

---

### Referencias y recursos

#### Escalamiento y leyes fundamentales

1. **Shalf, J. (2020).** "The future of computing beyond Moore's Law." *Philosophical Transactions of the Royal Society A*, 378(2166). [https://royalsocietypublishing.org/rsta/article/378/2166/20190061](https://royalsocietypublishing.org/rsta/article/378/2166/20190061) — Tratamiento completo de por qué el escalamiento clásico de transistores termina ~2025, argumentando especialización y heterogeneidad extrema como respuesta.

2. **Wulf, W. A. & McKee, S. A. (1995).** "Hitting the Memory Wall: Implications of the Obvious." *ACM SIGARCH*, 23(1). [https://dl.acm.org/doi/10.1145/216585.216588](https://dl.acm.org/doi/10.1145/216585.216588) — Paper que acuñó el término "memory wall". Su tesis central es aún más aguda en la era de IA.

3. **Hoffmann, J., et al. (2022).** "Training Compute-Optimal Large Language Models." *NeurIPS 2022*. [https://arxiv.org/abs/2203.15556](https://arxiv.org/abs/2203.15556) — "Chinchilla": modelos y tokens de entrenamiento deben escalar igualmente, reconfigurando estrategias de hardware.

#### La pared de memoria

4. **Gholami, A., et al. (2024).** "AI and Memory Wall." *arXiv:2403.14123* (también IEEE Micro). [https://arxiv.org/abs/2403.14123](https://arxiv.org/abs/2403.14123) — Análisis definitivo moderno: compute 3x/2yr, DRAM bandwidth 1.6x/2yr. Decodificación autoregresiva fundamentalmente memory-bound.

5. **Yuan, Z., et al. (2024).** "LLM Inference Unveiled: Survey and Roofline Model Insights." [https://arxiv.org/abs/2402.16363](https://arxiv.org/abs/2402.16363) — Modelo Roofline aplicado a inferencia de LLMs: la fase de decode es casi enteramente memory-bound.

6. **"Mind the Memory Gap." (2025).** arXiv:2503.08311. [https://arxiv.org/abs/2503.08311](https://arxiv.org/abs/2503.08311) — Incluso inferencia large-batch sigue principalmente memory-bound con GPUs actuales.

7. **"Amdahl Limits On AI." (2024).** *Semiconductor Engineering*. [https://semiengineering.com/amdahl-limits-on-ai/](https://semiengineering.com/amdahl-limits-on-ai/) — Ley de Amdahl aplicada a inferencia de redes neuronales: cuellos de botella secuenciales limitan speedup de cualquier optimización individual.

8. **TrendForce. (2024).** "Memory Wall Bottleneck: AI Compute Sparks Memory Supercycle." [https://www.trendforce.com/insights/memory-wall](https://www.trendforce.com/insights/memory-wall) — Compute de chips IA creció 80x en una década; bandwidth de memoria solo 17x. HBM4 con precios +30%.

#### Hardware especializado: TPUs, NPUs

9. **Jouppi, N. P., et al. (2023).** "TPU v4: An Optically Reconfigurable Supercomputer for Machine Learning." *ISCA 2023*. [https://arxiv.org/abs/2304.01433](https://arxiv.org/abs/2304.01433) — Arquitectura domain-specific con arrays sistólicos e interconexión óptica reconfigurable. ~60% eficiencia de peak FLOPS.

10. **Google Cloud Blog. (2025).** "Ironwood: The first Google TPU for the age of inference." [https://blog.google/products/google-cloud/ironwood-tpu-age-of-inference/](https://blog.google/products/google-cloud/ironwood-tpu-age-of-inference/) — TPU v7 explícitamente diseñado para inferencia. 4,614 TFLOP/s por chip, configs hasta 9,216 chips.

11. **The Chip Letter. (2024).** "Qualcomm's Hexagon AI Accelerators." [https://thechipletter.substack.com/p/qualcomms-hexagon-ai-accelerators](https://thechipletter.substack.com/p/qualcomms-hexagon-ai-accelerators) — Evolución de Hexagon DSP a cores tensoriales dedicados. Snapdragon X Elite: 45+ TOPS on-device.

#### Mixture of Experts

12. **DeepSeek-AI. (2024).** "DeepSeek-V3 Technical Report." [https://arxiv.org/abs/2412.19437](https://arxiv.org/abs/2412.19437) — 671B MoE activando solo 37B por forward pass: 42.5% menos costo de entrenamiento, 5.76x mayor throughput de inferencia, 93.3% reducción de KV cache.

13. **Tsinghua Science and Technology. (2025).** "A Survey on Accelerated Technologies for MoE Model Training Systems." [https://www.sciopen.com/article/10.26599/TST.2025.9010169](https://www.sciopen.com/article/10.26599/TST.2025.9010169) — Optimizaciones a nivel de hardware para MoE: paralelismo híbrido, gestión de memoria, scheduling de comunicación.

#### Energía

14. **Strubell, E., Ganesh, A., & McCallum, A. (2019).** "Energy and Policy Considerations for Deep Learning in NLP." *ACL 2019*. [https://arxiv.org/abs/1906.02243](https://arxiv.org/abs/1906.02243) — Paper que inició el movimiento "Green AI", cuantificando huella de carbono de entrenar modelos grandes.

15. **MIT Technology Review. (2025).** "We did the math on AI's energy footprint." [https://www.technologyreview.com/2025/05/20/1116327/ai-energy-usage-climate-footprint-big-tech/](https://www.technologyreview.com/2025/05/20/1116327/ai-energy-usage-climate-footprint-big-tech/) — Inferencia = 60-70% del consumo total. Data centers IA en EE.UU.: 53-76 TWh en 2024, proyección 165-326 TWh para 2028.

16. **Google. (2025).** "Measuring the environmental impact of delivering AI at Google Scale." [https://arxiv.org/pdf/2508.15734](https://arxiv.org/pdf/2508.15734) — Mediana de prompt Gemini: 0.24 Wh, 0.03 gCO2e. Reducción de 33x en energía/prompt en 12 meses, pero demanda crece más rápido.

17. **Introl Blog. (2025).** "Inference-Time Scaling." [https://introl.com/blog/inference-time-scaling-research-reasoning-models-december-2025](https://introl.com/blog/inference-time-scaling-research-reasoning-models-december-2025) — Modelos de razonamiento pueden demandar 100x más cómputo por query. Demanda de inferencia excederá training 118x para 2026.

#### Hardware emergente

18. **Cerebras Systems. (2024).** "WSE-3: World's Fastest AI Chip." [https://www.cerebras.ai/press-release/cerebras-announces-third-generation-wafer-scale-engine](https://www.cerebras.ai/press-release/cerebras-announces-third-generation-wafer-scale-engine) — 4 billones de transistores, 900K cores, 125 petaflops, 21 PB/s bandwidth on-chip. Elimina DRAM para modelos que caben on-chip.

19. **Lightmatter. (2024).** "Lightmatter Raises $400M Series D; Valuation $4.4B." [https://lightmatter.co/press-release/lightmatter-raises-400m-series-d-quadruples-valuation-to-4-4b-as-photonics-leader-for-next-gen-ai-data-centers/](https://lightmatter.co/press-release/lightmatter-raises-400m-series-d-quadruples-valuation-to-4-4b-as-photonics-leader-for-next-gen-ai-data-centers/) — Computación fotónica transitando de investigación a despliegue comercial.

20. **"Photonics for Neuromorphic Computing." (2024).** *Advanced Materials*. [https://arxiv.org/html/2311.09767v2](https://arxiv.org/html/2311.09767v2) — Survey de arquitecturas fotónicas neuromórficas: 97.7% precisión MNIST con 30% menos potencia.

21. **Intel Newsroom. (2024).** "Intel Builds World's Largest Neuromorphic System." [https://newsroom.intel.com/artificial-intelligence/intel-builds-worlds-largest-neuromorphic-system-to-enable-more-sustainable-ai](https://newsroom.intel.com/artificial-intelligence/intel-builds-worlds-largest-neuromorphic-system-to-enable-more-sustainable-ai) — Hala Point: 1,152 chips Loihi 2, 1.15B neuronas, solo 2,600W.

22. **"Memory Is All You Need." (2024).** arXiv:2406.08413. [https://arxiv.org/abs/2406.08413](https://arxiv.org/abs/2406.08413) — Survey de CIM para inferencia de LLMs: operaciones MAC analógicas directamente en arrays de memoria.

23. **"Breaking the memory wall: next-generation AI hardware." (2025).** *Frontiers in Science*. [https://www.frontiersin.org/journals/science/articles/10.3389/fsci.2025.1611658/full](https://www.frontiersin.org/journals/science/articles/10.3389/fsci.2025.1611658/full) — Síntesis del estado del arte de soluciones a la pared de memoria.

- **"Computer Architecture: A Quantitative Approach"** - Hennessy & Patterson
- **"The Bitter Lesson"** - Rich Sutton
- Post del blog: "¿Qué es un GPU?"
- ExecuTorch documentación: [pytorch.org/executorch](https://pytorch.org/executorch)
