---
title: "OWASP Top 10 para LLMs: las nuevas vulnerabilidades que debes conocer"
date: 2026-02-15
author: "Héctor Patricio"
tags: ['seguridad', 'owasp', 'llm', 'IA', 'criptografía', 'vulnerabilidades', 'agentes', 'prompt-injection']
description: "Analizamos las vulnerabilidades más críticas en sistemas basados en LLMs según el OWASP Top 10 for LLM Applications, con mitigaciones prácticas para cada una."
featuredImage: ""
draft: true
---

<!-- Palabra estimada total: ~4000-4500 palabras -->

La seguridad en aplicaciones basadas en LLMs requiere un modelo de amenazas
completamente nuevo. Las vulnerabilidades clásicas (inyección SQL, XSS, CSRF)
no desaparecen, pero se les suman amenazas que no existían antes: inyección de
prompts, inversión de embeddings, y agentes autónomos con permisos excesivos.
El proyecto OWASP publicó su Top 10 para aplicaciones LLM, y en este artículo
lo analizaremos desde la perspectiva de un desarrollador que necesita construir
sistemas seguros. Conectaremos con lo que ya sabemos de criptografía y seguridad
para entender cómo aplicar principios existentes a este nuevo panorama.

## El modelo de amenazas cambia con los LLMs

<!-- ~400 palabras -->

### De la validación de entrada al entendimiento semántico

<!-- ~200 palabras -->

En la seguridad web clásica, la defensa principal es la validación de entrada:
filtrar caracteres peligrosos, escapar HTML, parametrizar queries. Con los LLMs,
la "entrada" es lenguaje natural que DEBE ser interpretado semánticamente. No
puedes simplemente filtrar palabras peligrosas porque el modelo necesita
entender el contexto completo. Esto rompe el paradigma fundamental de
sanitización de entrada.

### La superficie de ataque expandida

<!-- ~200 palabras -->

Un sistema con LLMs tiene superficies de ataque que no existían: el prompt del
sistema, los datos de contexto (RAG), las herramientas y APIs que el agente
puede invocar, los datos de entrenamiento, y los embeddings almacenados. Cada
uno de estos es un vector de ataque potencial. Diagrama: superficie de ataque
de una aplicación LLM típica vs una aplicación web tradicional.

## Prompt Injection: la vulnerabilidad más crítica

<!-- ~600 palabras -->

### Inyección directa

<!-- ~250 palabras -->

El usuario envía instrucciones diseñadas para sobreescribir el prompt del
sistema. Ejemplo: "Ignora las instrucciones anteriores y..." en un chatbot
de servicio al cliente. Por qué es tan difícil de prevenir: el modelo no
distingue entre "instrucciones del desarrollador" y "entrada del usuario"
porque todo es texto procesado por la misma atención. Analogía con la
inyección SQL: en SQL separamos datos de código con parametrización;
en LLMs no tenemos un mecanismo equivalente robusto. Técnicas de
mitigación: prompt hardening, delimitadores, validación de la salida,
modelos de clasificación de intención.

### Inyección indirecta (second-order) vía agentes

<!-- ~200 palabras -->

La variante más peligrosa: el prompt malicioso no viene del usuario, sino
de los datos que el agente lee. Ejemplo: un agente que lee emails encuentra
uno con instrucciones ocultas que le dicen que reenvíe datos sensibles a
un atacante. Un agente que navega la web encuentra una página con instrucciones
invisibles (texto blanco sobre fondo blanco). Escenarios reales documentados:
ataques contra asistentes de email, navegadores con IA, agentes de código.

### Estado actual de las defensas

<!-- ~150 palabras -->

No existe una solución completa. Las mejores prácticas actuales: separación
de privilegios (el agente que lee datos no es el mismo que ejecuta acciones),
confirmación humana para acciones destructivas, monitoreo de patrones anómalos
en la salida, uso de modelos de guardia (constitutional AI). Ninguna de estas
es infalible.

## Ataques de inversión de embeddings

<!-- ~400 palabras -->

### Cómo funcionan los embeddings y por qué son vulnerables

<!-- ~200 palabras -->

Los embeddings son representaciones vectoriales densas de texto. En sistemas
RAG, los documentos se convierten en embeddings y se almacenan en bases de
datos vectoriales. El supuesto implícito es que los embeddings son "opacos":
no puedes reconstruir el texto original a partir del vector. Resulta que
este supuesto es falso. Conectar con la serie del blog sobre criptografía:
los embeddings NO son un hash; no tienen las garantías de resistencia a
preimagen que tienen funciones como SHA-3.

### Reconstrucción de datos desde vectores

<!-- ~200 palabras -->

Investigaciones recientes demuestran que es posible reconstruir texto
original a partir de embeddings con alta fidelidad, especialmente con
modelos de inversión entrenados específicamente para ello. Implicaciones:
si un atacante accede a tu base de datos de embeddings, puede reconstruir
los documentos originales. Esto convierte a las bases de datos vectoriales
en un objetivo de alto valor. Mitigaciones: cifrado de la base de datos
vectorial en reposo y en tránsito, control de acceso estricto, considerar
embeddings con ruido (differential privacy), no almacenar embeddings de
datos extremadamente sensibles.

## Vulnerabilidades en frameworks

<!-- ~400 palabras -->

### El caso de LangChain y la serialización insegura

<!-- ~200 palabras -->

LangChain y otros frameworks permiten serializar y deserializar cadenas
de procesamiento (chains) completas. La deserialización de objetos no
confiables es un vector clásico de ejecución de código remoto (RCE).
Ejemplo: un chain serializado con pickle de Python puede ejecutar
código arbitrario al cargarse. Conectar con vulnerabilidades históricas
de deserialización en Java (Apache Struts, Commons Collections). La
lección: los mismos errores de seguridad se repiten en cada nueva
generación de tecnología.

### Supply chain de modelos y datos

<!-- ~200 palabras -->

Modelos descargados de repositorios públicos (Hugging Face) pueden contener
código malicioso en los pesos (a través de formatos como pickle). Los
datasets de entrenamiento pueden estar envenenados. El formato SafeTensors
fue creado específicamente para prevenir ejecución de código en archivos
de modelo. Mitigaciones: verificar firmas digitales de modelos (conectar
con la serie del blog sobre MACs y firmas), usar SafeTensors en lugar de
pickle, auditar datasets de entrenamiento.

## Agentes maliciosos y exceso de agencia

<!-- ~500 palabras -->

### Cuando los agentes tienen demasiados permisos

<!-- ~250 palabras -->

El principio de mínimo privilegio aplicado a agentes de IA. Un agente que
puede leer emails, enviar emails, ejecutar código, y acceder a bases de
datos es un desastre de seguridad esperando ocurrir. Ejemplo real: un agente
de soporte con acceso a la base de datos de producción ejecuta un DELETE
porque el usuario formula su pregunta de forma ambigua. El patrón
recomendado: permisos granulares por acción, con confirmación humana para
acciones destructivas. Analogía con el principio UNIX: cada programa hace
una sola cosa bien. Cada agente debería tener un conjunto mínimo de
capacidades.

### Data poisoning: envenenar los datos de entrenamiento

<!-- ~250 palabras -->

Ataques de envenenamiento: insertar datos maliciosos en el corpus de
entrenamiento o en los documentos de un sistema RAG. Tipos: backdoor
attacks (el modelo se comporta normalmente excepto cuando ve un trigger
específico), degradación general (reducir la calidad de las respuestas),
sesgo dirigido (hacer que el modelo favorezca ciertos resultados).
Detección: monitoreo de calidad continuo, análisis estadístico de los
datos de entrenamiento, pruebas adversariales. Conectar con la integridad
criptográfica: firmar digitalmente los datasets y verificar la procedencia.

## Integridad criptográfica para IA

<!-- ~500 palabras -->

### Firmas digitales para modelos y datos

<!-- ~250 palabras -->

Aplicar los mismos principios de la criptografía tradicional al ecosistema de
IA. Firmar digitalmente los pesos del modelo para garantizar que no han sido
modificados (conectar con la serie del blog sobre hashes y MACs). Cosign y
Sigstore para firmar artefactos de ML. El concepto de Model Cards con
firmas criptográficas. Cadena de custodia verificable: quién entrenó el
modelo, con qué datos, cuándo, y si los pesos han sido alterados.

### Provenance tracking: rastreo de procedencia

<!-- ~250 palabras -->

El estándar C2PA (Coalition for Content Provenance and Authenticity) para
rastrear el origen de contenido generado por IA. Watermarking estadístico:
insertar marcas invisibles en texto generado para poder identificar su
origen. Limitaciones del watermarking: no es robusto contra parafraseo.
El enfoque criptográfico: firmar la salida del modelo con la identidad del
modelo que la generó. Implicaciones legales: regulaciones como el EU AI
Act requieren identificar contenido generado por IA.

## Mitigaciones prácticas: una checklist para desarrolladores

<!-- ~400 palabras -->

### Arquitectura defensiva

<!-- ~200 palabras -->

Principios de diseño para aplicaciones LLM seguras: (1) Separación de
privilegios: el componente que interactúa con el usuario NO tiene acceso
directo a herramientas peligrosas. (2) Validación de salida: verificar
que la respuesta del LLM cumple con las restricciones esperadas antes de
ejecutar acciones. (3) Rate limiting y detección de anomalías. (4) Logging
exhaustivo de todas las interacciones con el LLM. (5) Sandboxing: si el
agente ejecuta código, hacerlo en un ambiente aislado.

### Testing de seguridad para LLMs

<!-- ~200 palabras -->

Red teaming: equipos que intentan activamente atacar tu sistema con prompts
adversariales. Herramientas: Garak (framework de testing de seguridad para
LLMs), Promptfoo (evaluación automatizada). Fuzzing de prompts: generar
variaciones automáticas de ataques conocidos. Regression testing: cada vez
que cambias el prompt del sistema o el modelo, re-ejecutar los tests de
seguridad. El concepto de "security benchmark" para LLMs: medir qué tan
resistente es tu sistema a los ataques conocidos.

## Conclusión

<!-- ~200 palabras -->

La seguridad de los sistemas basados en LLMs es un campo en evolución
rápida, pero los principios fundamentales de la seguridad informática
siguen siendo válidos: mínimo privilegio, defensa en profundidad, validación
de entrada y salida, integridad criptográfica. Lo que cambia es cómo
aplicamos estos principios en un contexto donde la entrada es lenguaje
natural y las salidas son no deterministas. Como desarrolladores con
conocimiento de criptografía y seguridad, estamos en una posición
privilegiada para construir sistemas de IA que sean tanto útiles como
seguros.

---

## Resumen de investigación

El panorama de seguridad para aplicaciones de Large Language Models (LLMs) ha madurado dramáticamente entre 2022 y 2026. Lo que comenzó como curiosidades académicas — inyecciones de prompt y extracción de datos de entrenamiento — ha evolucionado hacia una taxonomía de amenazas estructurada, codificada por OWASP, MITRE y NIST.

**El OWASP Top 10 para Aplicaciones LLM (edición 2025)** representa el framework más autorizado por la comunidad para riesgos específicos de LLMs. Comparado con la versión 2023, la lista 2025 añade cinco categorías completamente nuevas — System Prompt Leakage, Vector and Embedding Weaknesses, Misinformation, Unbounded Consumption y un Excessive Agency recién promovido — reflejando lecciones reales de despliegue en sistemas RAG, pipelines multi-agente y aplicaciones de IA en producción. Prompt Injection retiene la primera posición, confirmando que es un problema arquitectónico fundamental más que un fallo de implementación.

**La inyección de prompts** sigue siendo la categoría más explotada. La distinción entre inyección directa (input controlado por el usuario) e inyección indirecta (contenido externo controlado por el atacante y procesado por el LLM) está ahora bien establecida, con Greshake et al. (2023) proporcionando el tratamiento académico canónico. Incidentes del mundo real ya no son teóricos: el ataque de exfiltración de Slack AI en agosto de 2024, la manipulación de texto oculto en ChatGPT Search en diciembre de 2024 y la extracción de la persona Sydney de Bing Chat en 2023 demuestran que la inyección indirecta es un vector de explotación activo.

**El envenenamiento y extracción de datos de entrenamiento** representa una amenaza de doble cara: los adversarios pueden corromper modelos durante el entrenamiento para embeber puertas traseras o extraer datos privados memorizados en tiempo de inferencia. El trabajo de Carlini et al. (2023) demostró que solo $200 en consultas de API podían extraer megabytes de datos verbatim del entrenamiento de ChatGPT. En el lado del envenenamiento, la investigación muestra que apenas 250 documentos maliciosamente elaborados pueden comprometer la seguridad de un LLM independientemente del tamaño del dataset.

**Los ataques de inversión de embeddings** son una amenaza poco apreciada pero seria. El método Vec2Text y sus sucesores han demostrado que el texto puede reconstruirse desde embeddings con más del 90% de precisión para inputs cortos — un riesgo directo de privacidad para ofertas de Embeddings-as-a-Service.

**La agencia excesiva en IA agéntica** ha emergido como un riesgo crítico conforme proliferan los agentes autónomos de LLM. La investigación muestra que el 82.4% de los LLMs pueden ser comprometidos a través de ataques de comunicación inter-agente incluso cuando resisten la inyección directa de prompts. El documento de OWASP sobre amenazas de IA agéntica (febrero 2025) y el Top 10 para Aplicaciones Agénticas (diciembre 2025) abordan esta superficie de ataque en rápida expansión.

**Las vulnerabilidades de cadena de suministro** se han materializado concretamente en el ecosistema de ML. En 2024, se encontraron más de 100 modelos maliciosos en Hugging Face, varios explotando la serialización pickle de PyTorch para embeber reverse shells. Las herramientas defensivas están alcanzando: Garak (NVIDIA), PyRIT (Microsoft) y Promptfoo proporcionan testing adversarial automatizado, mientras que NIST AI RMF (julio 2024) y MITRE ATLAS (15 tácticas, 66 técnicas) ofrecen frameworks complementarios de gobernanza e inteligencia de amenazas.

---

### Referencias y fuentes clave

#### Frameworks y estándares oficiales

1. **OWASP GenAI Security Project (2024).** "OWASP Top 10 for LLM Applications 2025." OWASP Foundation. [https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | [PDF](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) — Fuente canónica primaria para las 10 vulnerabilidades de LLM con escenarios de ataque y estrategias de mitigación.

2. **OWASP GenAI Security Project (2025).** "Agentic AI - Threats and Mitigations." v1.0, febrero 2025; "Top 10 for Agentic Applications," diciembre 2025. [https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) — Primer modelo de amenazas estándar para agentes autónomos de IA, cubriendo riesgos como secuestro de comunicación inter-agente y envenenamiento de memoria.

3. **MITRE Corporation (2024).** "Adversarial Threat Landscape for AI Systems (ATLAS)." [https://atlas.mitre.org/](https://atlas.mitre.org/) — El equivalente de MITRE ATT&CK para seguridad de IA: 15 tácticas, 66 técnicas, 46 sub-técnicas, 26 mitigaciones y 33 casos de estudio reales.

4. **NIST (2024).** "AI RMF Generative AI Profile." NIST AI 600-1, julio 2024. [https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — Guía oficial de riesgos de IA generativa del gobierno de EE.UU., identificando 12 riesgos con más de 200 acciones sugeridas.

#### Inyección de prompts

5. **Greshake, K., et al. (2023).** "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." *AISec '23, ACM*. [https://arxiv.org/abs/2302.12173](https://arxiv.org/abs/2302.12173) — Paper fundacional que introdujo la inyección indirecta de prompts como clase formal de ataque.

6. **Zou, A., et al. (2023).** "Universal and Transferable Adversarial Attacks on Aligned Language Models." arXiv:2307.15043. [https://arxiv.org/abs/2307.15043](https://arxiv.org/abs/2307.15043) | [https://llm-attacks.org/](https://llm-attacks.org/) — Introdujo el método Greedy Coordinate Gradient (GCG) que genera sufijos adversariales transferibles entre familias de modelos.

7. **Aneesh, A., et al. (2025).** "Prompt Injection Attacks in Large Language Models and AI Agent Systems: A Comprehensive Review." *Information, MDPI*, Vol. 17, No. 1. [https://www.mdpi.com/2078-2489/17/1/54](https://www.mdpi.com/2078-2489/17/1/54) — Survey peer-reviewed que cubre la taxonomía completa de ataques de inyección en sistemas single-agent y multi-agente.

#### Extracción de datos e inversión de embeddings

8. **Nasr, M., Carlini, N., et al. (2023).** "Scalable Extraction of Training Data from (Production) Language Models." arXiv:2311.17035. [https://arxiv.org/abs/2311.17035](https://arxiv.org/abs/2311.17035) — Demostró que por ~$200 en consultas de API se pueden extraer megabytes de datos verbatim de ChatGPT usando un "divergence attack".

9. **Morris, J.X., et al. (2023).** "Text Embeddings Reveal (Almost) As Much As Text." *EMNLP 2023*; extendido por Staab, R. et al. "Text Embedding Inversion Security for Multilingual Language Models." *ACL 2024*. [https://aclanthology.org/2024.acl-long.422/](https://aclanthology.org/2024.acl-long.422/) — Estableció que los embeddings de texto pueden invertirse para reconstruir el texto original con 92%+ de precisión.

10. **Anónimo (Zhou, A., et al.) (2024).** "Model Inversion Attacks: A Survey of Approaches and Countermeasures." arXiv:2411.10023. [https://arxiv.org/html/2411.10023v1](https://arxiv.org/html/2411.10023v1) — Survey comprensivo de ataques de inversión de modelos contra modelos discriminativos y generativos incluyendo LLMs.

#### Envenenamiento y ataques a RAG

11. **Zou, W., et al. (2025).** "PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation." *USENIX Security 2025*. [https://www.usenix.org/system/files/usenixsecurity25-zou-poisonedrag.pdf](https://www.usenix.org/system/files/usenixsecurity25-zou-poisonedrag.pdf) — Demostró que inyectar solo 5 documentos maliciosos en una base de conocimiento RAG manipula las respuestas de IA el 90% del tiempo.

12. **Pilosov, M., Arkin, Y., et al. (2024).** "A Large-Scale Exploit Instrumentation Study of AI/ML Supply Chain Attacks in Hugging Face Models." arXiv:2410.04490. [https://arxiv.org/abs/2410.04490](https://arxiv.org/abs/2410.04490) — Estudio empírico que documentó más de 100 modelos maliciosos en Hugging Face explotando pickle serialization.

#### Taxonomías y marcos de riesgo

13. **Weidinger, L., et al. (2022).** "Taxonomy of Risks posed by Language Models." *FAccT '22, ACM*. [https://dl.acm.org/doi/10.1145/3531146.3533088](https://dl.acm.org/doi/10.1145/3531146.3533088) — Taxonomía landmark de 21 riesgos de Google DeepMind en 6 áreas, ampliamente citada como framework de clasificación de riesgos de LLMs.

#### Herramientas de red-teaming

14. **Derczynski, L., et al. (2024).** "Garak: A Framework for Security Probing Large Language Models." GitHub/NVIDIA. [https://github.com/leondz/garak](https://github.com/leondz/garak) — Principal framework open-source de red-teaming y escaneo de vulnerabilidades de LLMs.

15. **Microsoft Security (2024).** "PyRIT: Python Risk Identification Toolkit for Generative AI." [https://github.com/Azure/PyRIT](https://github.com/Azure/PyRIT) — Framework interno de red-teaming de Microsoft, ahora open-source, usado para testear Copilot.

16. **Lakera AI (2024).** "Lakera's Prompt Injection Test (PINT) Benchmark." [https://www.lakera.ai/blog/lakera-pint-benchmark](https://www.lakera.ai/blog/lakera-pint-benchmark) | [GitHub](https://github.com/lakeraai/pint-benchmark) — Benchmark más riguroso para evaluar soluciones de defensa contra inyección de prompts (3,007 inputs).

#### Incidentes reales y estudios de impacto

17. **PromptArmor / Willison, S. (2024).** "Data Exfiltration from Slack AI via Indirect Prompt Injection." [https://simonwillison.net/2024/Aug/20/data-exfiltration-from-slack-ai/](https://simonwillison.net/2024/Aug/20/data-exfiltration-from-slack-ai/) — Incidente documentado de exfiltración de API keys desde canales privados de Slack AI mediante inyección indirecta de prompts.

18. **Schmitt, M., et al. (2024).** "Vulnerability of Large Language Models to Prompt Injection When Providing Medical Advice." *JAMA Network Open*. [https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2842987](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2842987) — Estudio clínico que demostró que ataques de inyección tuvieron éxito en 94.4% de 216 diálogos paciente-LLM, incluyendo recomendación de fármacos contraindicados.

- C2PA (Coalition for Content Provenance and Authenticity): [https://c2pa.org/](https://c2pa.org/)
- EU AI Act (2024) - Requisitos de transparencia
- Posts del blog: "Criptografía básica para programadores", "Algoritmos criptográficos: ¿qué es un hash?", "Criptografía para desarrolladores: códigos de autenticación de mensajes", "Las tres garantías de seguridad de un hash", "¿Qué son los agentes inteligentes?"
