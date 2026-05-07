# Apendice C: Recursos y Lecturas Adicionales

Seleccion curada de los recursos mas relevantes organizados por tema. Incluye papers academicos, documentacion oficial, articulos tecnicos y libros. Fecha de compilacion: marzo 2026.

---

## Fundamentos de agentes (Capitulos 1-3)

### Papers

- Yao, S. et al. "ReAct: Synergizing Reasoning and Acting in Language Models." *ICLR*, 2023. https://arxiv.org/abs/2210.03629 -- Fundamento del patron ReAct y del loop agentico.
- Wei, J. et al. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS*, 2022. https://arxiv.org/abs/2201.11903 -- Base del razonamiento paso a paso en LLMs.
- Yao, S. et al. "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." *NeurIPS*, 2023. https://arxiv.org/abs/2305.10601 -- Exploracion de multiples caminos de razonamiento con backtracking.
- Shinn, N. et al. "Reflexion: Language Agents with Verbal Reinforcement Learning." *NeurIPS*, 2023. https://arxiv.org/abs/2303.11366 -- Aprendizaje por retroalimentacion verbal sin actualizar pesos.
- Zhou, A. et al. "Language Agent Tree Search Unifies Reasoning, Acting, and Planning." *ICML*, 2024. https://arxiv.org/abs/2310.04406 -- Monte Carlo Tree Search aplicado a agentes.
- Rao, A. y Georgeff, M. "BDI Agents: From Theory to Practice." *ICMAS*, 1995. https://cdn.aaai.org/ICMAS/1995/ICMAS95-042.pdf -- Paper fundacional de la arquitectura BDI.
- Snell, C. et al. "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters." 2024. https://arxiv.org/abs/2408.03314 -- Inference-time scaling como alternativa a modelos mas grandes.

### Libros

- Russell, S. y Norvig, P. *Artificial Intelligence: A Modern Approach*. 4ta edicion, Pearson, 2020. Capitulo 2: Intelligent Agents. https://aima.cs.berkeley.edu/ -- Definicion canonica de PEAS y taxonomia de agentes.

### Articulos

- Weng, L. "LLM Powered Autonomous Agents." OpenAI Blog, junio 2023. https://lilianweng.github.io/posts/2023-06-23-agent/ -- El articulo de referencia sobre agentes LLM.
- Anthropic. "Building Effective Agents." diciembre 2024. https://www.anthropic.com/research/building-effective-agents -- Cinco patrones de workflows y agentes.

---

## Arquitectura e infraestructura (Capitulos 4-7)

### Papers

- Packer, C. et al. "MemGPT: Towards LLMs as Operating Systems." 2023. https://arxiv.org/abs/2310.08560 -- Memoria jerarquica inspirada en sistemas operativos.
- Xu, L. et al. "A-MEM: Agentic Memory for LLM Agents." 2025. https://arxiv.org/abs/2502.12110 -- Sistema de memoria basado en Zettelkasten.
- Liu, N. et al. "Lost in the Middle: How Language Models Use Long Contexts." Stanford, 2023. -- Los LLMs pierden acceso a informacion en la parte media de la ventana de contexto.

### Articulos

- Chase, H. "Context Engineering for Agents." blog.langchain.com, 2025. https://blog.langchain.com/context-engineering-for-agents/ -- Write, select, compress, isolate como estrategias de contexto.
- Anthropic. "Effective Context Engineering for AI Agents." 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents -- Guia practica de context engineering.
- Huyen, C. "Building a Generative AI Platform." julio 2024. https://huyenchip.com/2024/07/25/genai-platform.html -- Arquitectura completa de plataforma GenAI incluyendo RAG.

---

## Seguridad, harness y controles (Capitulos 8-10)

### Papers y estandares

- OWASP. "Top 10 for LLM Applications 2025." noviembre 2024. https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/ -- Las diez vulnerabilidades principales en aplicaciones LLM.
- Zou, A. et al. "Improving Alignment and Robustness with Circuit Breakers." Gray Swan AI, 2024. https://github.com/GraySwanAI/circuit-breakers -- Circuit breakers via Representation Rerouting.
- AGrail. "A Lifelong Agent Guardrail." *ACL*, 2025. https://aclanthology.org/2025.acl-long.399.pdf -- Framework de guardrails para agentes.
- NIST. "AI Risk Management Framework (AI RMF 1.0)." enero 2023. https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf -- Framework para gestion de riesgos de IA.
- Saltzer, J. y Schroeder, M. "The Protection of Information in Computer Systems." *Proceedings of the IEEE*, 63(9), 1975. -- Principio de minimo privilegio.

### Articulos

- Bockeler, B. "Harness Engineering." martinfowler.com, 2026. https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html -- Context engineering + restricciones arquitectonicas + gestion de entropia.
- OpenAI. "Harness Engineering: Leveraging Codex in an Agent-First World." febrero 2026. https://openai.com/index/harness-engineering/ -- Caso practico con Codex.
- Willison, S. "The Lethal Trifecta for AI Agents." 2025. https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents -- Datos privados + contenido no confiable + comunicacion externa.
- Anthropic. "Writing Tools for Agents." 2025. https://www.anthropic.com/engineering/writing-tools-for-agents -- Diseno de herramientas efectivas para agentes.

---

## Testing y verificacion (Capitulo 11)

### Papers

- Hou, Z. et al. "Position: Trustworthy AI Agents Require the Integration of LLMs and Formal Methods." 2025. https://openreview.net/forum?id=wkisIZbntD -- LLMs + metodos formales para agentes confiables.
- AgentGuard. "Runtime Verification of AI Agents." 2025. https://arxiv.org/html/2509.23864v1 -- Verificacion en tiempo de ejecucion.
- Anthropic. "Sabotage Evaluations for Frontier Models." 2024. https://www.anthropic.com/research/sabotage-evaluations -- Framework para evaluar capacidades de sabotaje.

### Benchmarks

- SWE-bench. "Can Language Models Resolve Real-World GitHub Issues?" https://www.swebench.com/ -- Benchmark para agentes de codigo.
- AgentBench. "Evaluating LLMs as Agents." *ICLR*, 2024. https://github.com/THUDM/AgentBench -- Benchmark multi-tarea para agentes.

---

## Protocolos y multi-agente (Capitulos 12-13)

### Especificaciones

- Anthropic / Linux Foundation. "Model Context Protocol (MCP) Specification." noviembre 2025. https://modelcontextprotocol.io/specification/2025-11-25 -- Protocolo para conectar agentes con herramientas.
- Google. "Agent-to-Agent Protocol (A2A)." 2025. https://github.com/a2aproject/A2A -- Protocolo para comunicacion entre agentes.

### Papers

- "The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption." enero 2026. https://arxiv.org/abs/2601.13671 -- Survey de MCP, A2A y adopcion empresarial.
- "A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, and ANP." mayo 2025. https://arxiv.org/html/2505.02279v1 -- Comparativa de protocolos.

---

## Produccion y operaciones (Capitulos 14-16)

### Articulos

- Chase, H. "Why You Should Outsource Your Agentic Infrastructure, But Own Your Cognitive Architecture." blog.langchain.com, julio 2024. https://blog.langchain.com/why-you-should-outsource-your-agentic-infrastructure-but-own-your-cognitive-architecture/ -- Infraestructura delegada, arquitectura cognitiva propia.
- Huyen, C. "Agents." enero 2025. https://huyenchip.com/2025/01/07/agents.html -- Taxonomia de herramientas, planificacion, modos de fallo.
- Fowler, M. "Humans and Agents in Software Engineering Loops." 2026. https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html -- Framework "on the loop" vs "in the loop".

### Frameworks (Documentacion oficial)

- LangGraph: https://docs.langchain.com/oss/python/langgraph/overview
- CrewAI: https://docs.crewai.com
- Microsoft Agent Framework: https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- Anthropic Agent SDK: https://platform.claude.com/docs/en/agent-sdk/overview
- DSPy: Khattab, O. et al. "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." *ICLR*, 2024.

---

## Hardware e infraestructura (Capitulo 15)

- DeepSeek-R1. https://huggingface.co/deepseek-ai/DeepSeek-R1 -- Modelo open source de 671B parametros con razonamiento.
- DeepSeek-V3. https://github.com/deepseek-ai/DeepSeek-V3 -- Mixture of Experts con Multi-head Latent Attention.
- "Demystifying LLM Quantization: GPTQ, AWQ, GGUF." cast.ai. https://cast.ai/blog/demystifying-quantizations-llms/ -- Comparativa practica de metodos de cuantizacion.

---

## Libros recomendados

- Huyen, C. *AI Engineering: Building Applications with Foundation Models*. O'Reilly, 2025. -- Cobertura completa del stack de IA: modelos, evaluacion, RAG, agentes, despliegue.
- Dibia, V. *Designing Multi-Agent Systems: Principles, Patterns, and Implementation*. 2025. -- Framework "picoagents" desde cero, patrones multi-agente, evaluacion y seguridad.
- Ousterhout, J. *A Philosophy of Software Design*. 2da edicion, 2021. -- Principios de diseno de software aplicables a la arquitectura de agentes.
- Grootendorst, M. y Alammar, J. *An Illustrated Guide to AI Agents*. O'Reilly, 2025. -- Guia visual de agentes, cuantizacion y destilacion.

---

## Conferencias y talks

- LangChain Interrupt 2025. Grabaciones: https://blog.langchain.com/interrupt-2025-recap/ -- Keynotes de Chase y Ng, casos de LinkedIn, JP Morgan, BlackRock.
- NeurIPS 2024. Workshop on Safety of Agentic AI Systems. -- Papers sobre seguridad, razonamiento seguro y ataques adversarios.
- ICML 2025. Talks de IBM (Computer-Using Generalist Agents), Shopify (Sidekick Agent con MCP) y Capital One (MACAW multi-agente).

---
