---
title: "Cómo razonan los LLMs: de las máquinas de Turing al inference-time scaling"
date: 2026-02-15
author: "Héctor Patricio"
tags: ['llm', 'IA', 'inteligencia-artificial', 'turing', 'razonamiento', 'deep-learning', 'ciencias-de-la-computación']
description: "¿Realmente razonan los LLMs? Exploramos la conexión entre la teoría de la computación, las máquinas de Turing y las técnicas modernas de razonamiento como chain-of-thought e inference-time scaling."
featuredImage: ""
draft: true
---

<!-- Palabra estimada total: ~3500-4000 palabras -->

Los modelos de lenguaje han evolucionado de simples generadores de texto a sistemas
que parecen "pensar" antes de responder. Modelos como DeepSeek-R1 y o3 de OpenAI
dedican más tiempo de cómputo a razonar durante la inferencia, y los resultados son
sorprendentes. Pero, ¿qué significa "razonar" para una máquina? En este artículo
conectaremos la teoría clásica de la computación con las técnicas modernas de
razonamiento en LLMs, y analizaremos críticamente si esto es verdadero razonamiento
o sofisticado reconocimiento de patrones.

## ¿Qué significa "razonar" computacionalmente?

<!-- ~500 palabras -->

Definición formal de razonamiento desde la perspectiva de la teoría de la computación.
Conectar con las máquinas de Turing: una máquina que sigue reglas para transformar
una entrada en una salida. Distinguir entre computación mecánica (seguir reglas) y
razonamiento genuino (entender, generalizar, crear abstracciones nuevas).

### De las máquinas de Turing a los transformadores

<!-- ~400 palabras -->

Explicar brevemente qué es una máquina de Turing (referenciar los posts anteriores
del blog sobre máquinas de Turing no deterministas y problemas NP). Mostrar cómo
un transformador puede verse como un tipo particular de computador: recibe una
secuencia, aplica transformaciones y produce una salida. Mencionar el resultado
teórico de que los transformadores son Turing-completos bajo ciertas condiciones
(Pérez et al., 2021).

### Problemas NP y los límites del razonamiento automatizado

<!-- ~400 palabras -->

Conectar con la serie del blog sobre problemas NP y complejidad computacional.
Explicar que muchos problemas de "razonamiento" son NP-completos (planificación,
satisfacibilidad lógica). ¿Puede un LLM resolver problemas que una máquina de
Turing determinista no puede resolver eficientemente? La respuesta corta: no,
pero puede encontrar buenas heurísticas.

## Inference-time scaling: pensar más = mejores resultados

<!-- ~600 palabras -->

Explicar el concepto fundamental: en lugar de solo hacer el modelo más grande
(training-time scaling), se le da más cómputo durante la inferencia. El modelo
"piensa" más antes de responder. Presentar la evidencia: DeepSeek-R1, o3 de OpenAI,
y los resultados en benchmarks de matemáticas y programación.

### Chain-of-thought: razonamiento paso a paso

<!-- ~400 palabras -->

Qué es chain-of-thought prompting (Wei et al., 2022). Cómo funciona: el modelo
genera pasos intermedios visibles que guían hacia la respuesta. Analogía con la
heurística de Polya: "¿puedes descomponer el problema en partes más pequeñas?"
(referenciar los posts sobre técnicas de resolución de problemas y la heurística).
Ejemplos concretos con problemas matemáticos.

### Tree-of-thought: explorar múltiples caminos

<!-- ~350 palabras -->

Extensión del chain-of-thought: en lugar de un solo camino de razonamiento, el
modelo explora múltiples ramas y evalúa cuál es más prometedora. Analogía con la
búsqueda en árboles de la IA clásica. Conexión con las máquinas de Turing no
deterministas: explorar múltiples caminos en paralelo.

### Reinforcement learning para razonar

<!-- ~350 palabras -->

Cómo DeepSeek-R1 usa reinforcement learning para aprender a razonar sin
supervisión explícita. El modelo aprende que "pensar más" produce mejores
resultados y es recompensado por ello. Diferencia con el entrenamiento
tradicional supervisado. Explicar GRPO (Group Relative Policy Optimization)
de forma accesible.

## Comparación con el razonamiento humano

<!-- ~500 palabras -->

### Las heurísticas de Polya y los LLMs

<!-- ~300 palabras -->

Conectar con la serie del blog sobre heurística y resolución de problemas.
Las cuatro fases de Polya: entender el problema, concebir un plan, ejecutar
el plan, verificar. ¿Siguen los LLMs algo parecido cuando hacen chain-of-thought?
Comparar las "heurísticas" que un LLM desarrolla con las heurísticas humanas.
Diferencia clave: los humanos entienden *por qué* funcionan sus heurísticas.

### Inducción, deducción y abducción en los LLMs

<!-- ~200 palabras -->

Referenciar el post sobre inducción y deducción según Polya. Los LLMs hacen
principalmente inducción (generalizan a partir de patrones en los datos de
entrenamiento). Su "deducción" es simulada. Discutir si pueden hacer abducción
(inferir la mejor explicación).

## Análisis crítico: ¿razonan o reconocen patrones?

<!-- ~600 palabras -->

### El argumento a favor: comportamiento emergente

<!-- ~300 palabras -->

Los LLMs muestran capacidades que no fueron explícitamente entrenadas. Resuelven
problemas nuevos que no estaban en los datos de entrenamiento. El inference-time
scaling produce mejoras consistentes en tareas de razonamiento. Resultados en
competencias de matemáticas (AIME, Olympiad).

### El argumento en contra: la habitación china escalada

<!-- ~300 palabras -->

El argumento de John Searle aplicado a los LLMs: manipulan símbolos sin
comprensión. Los LLMs fallan en problemas triviales que requieren comprensión
genuina (el "reversal curse", problemas de conteo). La diferencia entre
correlación estadística y causalidad. Los modelos no tienen un modelo del mundo,
solo un modelo del lenguaje sobre el mundo.

## Implicaciones para los desarrolladores

<!-- ~300 palabras -->

Qué significa todo esto en la práctica. Los LLMs como herramientas de
razonamiento asistido, no como razonadores autónomos. Cuándo confiar en el
razonamiento de un LLM y cuándo no. El futuro: ¿modelos que realmente razonan
o mejores imitadores de razonamiento?

## Conclusión

<!-- ~200 palabras -->

Síntesis de la discusión. La pregunta "¿razonan los LLMs?" probablemente está
mal formulada. Lo que importa es: ¿son útiles para resolver problemas reales?
Y la respuesta es sí, con matices importantes. El verdadero razonamiento sigue
siendo un problema abierto en IA.

---

## Resumen de investigación

La pregunta de si los LLMs pueden genuinamente "razonar" se encuentra en la intersección de la ciencia de la computación teórica, la ciencia cognitiva y la investigación empírica en IA. Pérez et al. (2021) establecieron que los transformadores con precisión arbitraria son Turing-completos, pero los transformadores de precisión fija (es decir, todo modelo real) no lo son. Investigación posterior en complejidad de circuitos (Strobl, Merrill et al., 2024) muestra que transformadores de profundidad constante solo reconocen lenguajes en AC⁰/TC⁰, muy por debajo de lo necesario para muchas tareas de razonamiento.

La conexión clave entre inference-time compute y capacidad es que los tokens de chain-of-thought efectivamente aumentan la profundidad computacional del transformador. Li et al. (2024, ICLR) demostraron formalmente que con T pasos de CoT, incluso transformadores de profundidad constante pueden resolver problemas solubles por circuitos booleanos de tamaño T, elevándolos de AC⁰ a PTIME en el límite.

El paradigma de inference-time scaling fue formalizado por Snell et al. (2024), quienes demostraron que más cómputo en inferencia puede superar a modelos 14x más grandes. OpenAI o1 y DeepSeek-R1 operacionalizaron esto: DeepSeek-R1 demostró que RL puro, sin trazas de razonamiento supervisadas, puede producir modelos que desarrollan espontáneamente auto-reflexión y verificación.

Sin embargo, críticos como Apple Research (GSM-Symbolic, 2024) muestran que los LLMs sufren caídas significativas cuando solo cambian los valores numéricos en problemas. "The Illusion of Thinking" (Apple, 2025) muestra que los modelos de razonamiento colapsan completamente más allá de cierto umbral de complejidad. Kambhampati (2024) argumenta que los LLMs hacen "recuperación aproximada" más que razonamiento deliberativo.

---

### Referencias y fuentes clave

#### Fundamentos teóricos

1. **Pérez, J., Marinković, J., & Barceló, P. (2021).** "Attention is Turing-Complete." *Journal of Machine Learning Research*, 22, 1–35. [https://jmlr.org/papers/v22/20-302.html](https://jmlr.org/papers/v22/20-302.html) — Prueba fundacional de que los transformadores con encodings posicionales y precisión arbitraria pueden simular cualquier máquina de Turing.

2. **Strobl, L., Merrill, W., Weiss, G., Chiang, D., & Angluin, D. (2024).** "What Formal Languages Can Transformers Express? A Survey." *Transactions of the ACL*, 12, 543–561. [https://arxiv.org/abs/2311.00208](https://arxiv.org/abs/2311.00208) — Survey que unifica resultados sobre expresividad de transformadores usando teoría de lenguajes formales y complejidad de circuitos.

3. **"Barriers to Discrete Reasoning with Transformers: A Survey Across Depth, Exactness, and Bandwidth." (2025).** [https://arxiv.org/abs/2602.11175](https://arxiv.org/abs/2602.11175) — Síntesis de febrero 2025 sobre tres barreras estructurales: profundidad insuficiente, precisión finita y ancho de banda limitado entre cabezas de atención.

#### Chain-of-Thought e Inference-Time Scaling

4. **Wei, J., Wang, X., Schuurmans, D., et al. (2022).** "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*. [https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903) — Paper seminal que muestra que los pasos intermedios de razonamiento mejoran dramáticamente el rendimiento en tareas aritméticas y de sentido común.

5. **Li, Z., Liu, H., Zhou, D., & Ma, T. (2024).** "Chain of Thought Empowers Transformers to Solve Inherently Serial Problems." *ICLR 2024*. [https://arxiv.org/abs/2402.12875](https://arxiv.org/abs/2402.12875) — Explicación formal de por qué CoT funciona: cada token intermedio agrega una capa de computación, elevando transformadores de AC⁰ a PTIME.

6. **Wang, X., Wei, J., et al. (2022).** "Self-Consistency Improves Chain of Thought Reasoning in Language Models." *ICLR 2023*. [https://arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171) — Muestrear múltiples cadenas de razonamiento y votar por la respuesta más común mejora hasta +17.9% en GSM8K.

7. **Yao, S., Yu, D., et al. (2023).** "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." *NeurIPS 2023*. [https://arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601) — Generaliza CoT a búsqueda en árbol con backtracking. Eleva GPT-4 de 4% a 74% en Game of 24.

8. **Snell, C., Lee, J., Xu, K., & Kumar, A. (2024).** "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters." [https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314) — Demuestra que la asignación óptima de cómputo en inferencia permite que un modelo pequeño supere a uno 14x más grande.

9. **"Lower Bounds for Chain-of-Thought Reasoning in Hard-Attention Transformers." ICML 2025.** [https://arxiv.org/abs/2502.02393](https://arxiv.org/abs/2502.02393) — Establece cotas inferiores ajustadas para el número de pasos CoT necesarios para problemas algorítmicos específicos.

#### Modelos de razonamiento

10. **OpenAI. (2024).** "Learning to Reason with LLMs." [https://openai.com/index/learning-to-reason-with-llms/](https://openai.com/index/learning-to-reason-with-llms/) — Primer modelo comercial que hace de inference-time scaling su mecanismo principal. 83.3% en AIME 2024 vs ~13% de GPT-4o.

11. **DeepSeek-AI, Guo, D., et al. (2025).** "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." [https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948) — RL puro produce modelos con auto-reflexión emergente, igualando a o1 a 70% menos costo.

#### Crítica y debate

12. **Mirzadeh, I., Alizadeh, K., et al. (2024).** "GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models." *ICLR 2025*. [https://arxiv.org/abs/2410.05229](https://arxiv.org/abs/2410.05229) — Los LLMs sufren caídas significativas al cambiar solo valores numéricos en problemas matemáticos, sugiriendo pattern matching sobre plantillas.

13. **Apple Machine Learning Research. (2025).** "The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity." [https://machinelearning.apple.com/research/illusion-of-thinking](https://machinelearning.apple.com/research/illusion-of-thinking) — Los modelos de razonamiento colapsan completamente más allá de cierto umbral de complejidad y paradójicamente generan menos tokens en problemas difíciles.

14. **Kambhampati, S. (2024).** "Can Large Language Models Reason and Plan?" *Annals of the New York Academy of Sciences*, 1534(1), 15–18. [https://arxiv.org/abs/2403.04121](https://arxiv.org/abs/2403.04121) — Los LLMs hacen "recuperación aproximada" más que razonamiento deliberativo. Propone el framework "LLM-Modulo" donde LLMs generan candidatos verificados por sistemas simbólicos.

#### Clásicos y contexto

15. **Polya, G. (1945).** *How to Solve It*. Princeton University Press — Las cuatro fases de resolución de problemas como marco para comparar con el razonamiento de LLMs.

16. **Searle, J. (1980).** "Minds, Brains, and Programs." — El argumento de la habitación china como marco filosófico para evaluar si la manipulación de símbolos constituye comprensión.

17. **Berglund et al. (2023).** "The Reversal Curse: LLMs trained on 'A is B' fail to learn 'B is A'" — Evidencia empírica de que los LLMs no generalizan relaciones simétricas, sugiriendo limitaciones fundamentales.

- Posts del blog: "Máquinas de Turing no deterministas y problemas NP", "El arte de resolver problemas: la heurística", "Técnicas para resolver problemas", "Inducción y deducción según Polya"
