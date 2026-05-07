# Recursos para "Ingenieria de Agentes de IA: De la Teoria a Produccion"

Recopilacion exhaustiva de recursos academicos, tecnicos y practicos.
Fecha de compilacion: 2026-03-25

---

## 1. PAPERS ACADEMICOS FUNDAMENTALES

### 1.1 Razonamiento y Planificacion de Agentes LLM

| Paper | Autores | Fecha | URL | Aporte al libro |
|-------|---------|-------|-----|-----------------|
| **ReAct: Synergizing Reasoning and Acting in Language Models** | Shunyu Yao, Jeffrey Zhao, Dian Yu et al. | Oct 2022 (ICLR 2023) | https://arxiv.org/abs/2210.03629 | Fundamento del patron ReAct: intercalar razonamiento y acciones. Base teorica del loop agentico. |
| **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** | Jason Wei, Xuezhi Wang, Dale Schuurmans et al. | Ene 2022 (NeurIPS 2022) | https://arxiv.org/abs/2201.11903 | Base de razonamiento paso a paso en LLMs. Prerequisito para entender planificacion agentica. |
| **Tree of Thoughts: Deliberate Problem Solving with Large Language Models** | Shunyu Yao, Dian Yu, Jeffrey Zhao et al. | May 2023 (NeurIPS 2023) | https://arxiv.org/abs/2305.10601 | Generalizacion de CoT con exploracion de multiples caminos de razonamiento y backtracking. |
| **Reflexion: Language Agents with Verbal Reinforcement Learning** | Noah Shinn, Federico Cassano, Ashwin Gopinath et al. | Mar 2023 (NeurIPS 2023) | https://arxiv.org/abs/2303.11366 | Aprendizaje por retroalimentacion verbal sin actualizar pesos. Memoria episodica para agentes. |
| **Language Agent Tree Search Unifies Reasoning, Acting, and Planning** | Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman et al. | Oct 2023 (ICML 2024) | https://arxiv.org/abs/2310.04406 | Unifica razonamiento, accion y planificacion via Monte Carlo Tree Search. 92.7% en HumanEval. |
| **Self-Consistency Improves Chain of Thought Reasoning in Language Models** | Xuezhi Wang, Jason Wei et al. | Mar 2022 | https://arxiv.org/abs/2203.11171 | Tecnica complementaria de votacion por mayoria para mejorar razonamiento CoT. |

### 1.2 Arquitectura BDI para Agentes

| Paper | Autores | Fecha | URL | Aporte al libro |
|-------|---------|-------|-----|-----------------|
| **BDI Agents: From Theory to Practice** | Anand S. Rao, Michael P. Georgeff | 1995 (ICMAS) | https://cdn.aaai.org/ICMAS/1995/ICMAS95-042.pdf | Paper fundacional de la arquitectura BDI (Belief-Desire-Intention) para agentes autonomos. |
| **The Belief-Desire-Intention Model of Agency** | Michael Georgeff et al. | 1999 | https://link.springer.com/chapter/10.1007/3-540-49057-4_1 | Formalizacion del modelo BDI, puente entre filosofia (Bratman) e IA. |
| **BDI Agent Architectures: A Survey** | Varios | 2020 (IJCAI) | https://www.ijcai.org/proceedings/2020/0684.pdf | Survey completo de 30 anios de arquitecturas BDI. Contexto historico para el libro. |

### 1.3 Framework PEAS (Russell & Norvig)

| Recurso | Autores | Fecha | URL | Aporte al libro |
|---------|---------|-------|-----|-----------------|
| **Artificial Intelligence: A Modern Approach, 4th Ed. - Cap. 2: Intelligent Agents** | Stuart Russell, Peter Norvig | 2020 | https://aima.cs.berkeley.edu/ | Definicion canonica de PEAS (Performance, Environment, Actuators, Sensors) y taxonomia de agentes. |
| **Cap. 2 PDF disponible** | Russell & Norvig | 2020 | http://aima.cs.berkeley.edu/4th-ed/pdfs/newchap02.pdf | Capitulo completo sobre agentes inteligentes con framework PEAS. |

### 1.4 Inference-Time Scaling / Compute-Optimal Inference

| Paper | Autores | Fecha | URL | Aporte al libro |
|-------|---------|-------|-----|-----------------|
| **Inference Scaling Laws: An Empirical Analysis of Compute-Optimal Inference for Problem-Solving with Language Models** | Yangzhen Wu et al. | Ago 2024 (ICLR 2025) | https://arxiv.org/abs/2408.00724 | Leyes de escalamiento en inferencia. Modelos pequenos + algoritmos avanzados superan a modelos grandes. |
| **Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters** | Charlie Snell et al. | Ago 2024 | https://arxiv.org/abs/2408.03314 | Demuestra que escalar computo en inferencia es mas efectivo que escalar parametros para razonamiento. |

### 1.5 Verificacion Formal de Agentes de IA

| Paper | Autores | Fecha | URL | Aporte al libro |
|-------|---------|-------|-----|-----------------|
| **Position: Trustworthy AI Agents Require the Integration of LLMs and Formal Methods** | Zhe Hou et al. | 2025 | https://openreview.net/forum?id=wkisIZbntD | Tesis: agentes confiables requieren integrar LLMs con metodos formales. |
| **AgentGuard: Runtime Verification of AI Agents** | Varios | 2025 | https://arxiv.org/html/2509.23864v1 | Framework para verificacion en tiempo de ejecucion de agentes de IA. |
| **SYSMOBENCH: Evaluating AI on Formally Modeling Complex Real-World Systems** | Varios | 2025 | https://arxiv.org/pdf/2509.23130 | Primer framework para evaluar IA en modelado formal de sistemas. Incluye TLA+. |

### 1.6 Guardrails, Circuit Breakers y Seguridad de Agentes

| Paper | Autores | Fecha | URL | Aporte al libro |
|-------|---------|-------|-----|-----------------|
| **Improving Alignment and Robustness with Circuit Breakers** | Andy Zou et al. (Gray Swan AI) | 2024 | https://github.com/GraySwanAI/circuit-breakers | Mecanismo de circuit breaker via Representation Rerouting para prevenir contenido danino. |
| **AGrail: A Lifelong Agent Guardrail** | Varios | 2025 (ACL) | https://aclanthology.org/2025.acl-long.399.pdf | Framework de guardrails para agentes que previene riesgos antes de ejecutar acciones. |
| **Current State of LLM Risks and AI Guardrails** | Suriya Ganesh Ayyamperumal et al. | Jun 2024 | https://arxiv.org/pdf/2406.12934 | Survey del estado actual de riesgos y guardrails para LLMs. |
| **Safeguarding Large Language Models: A Survey** | Varios | 2025 | https://link.springer.com/article/10.1007/s10462-025-11389-2 | Survey comprehensivo sobre mecanismos de proteccion para LLMs. |

### 1.7 Orquestacion Multi-Agente

| Paper | Autores | Fecha | URL | Aporte al libro |
|-------|---------|-------|-----|-----------------|
| **The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption** | Varios | Ene 2026 | https://arxiv.org/abs/2601.13671 | Survey exhaustivo de MCP, A2A, y adopcion empresarial de sistemas multi-agente. |
| **A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, and ANP** | Varios | May 2025 | https://arxiv.org/html/2505.02279v1 | Comparativa detallada de protocolos de interoperabilidad entre agentes. |
| **Multi-Agent Collaboration via Evolving Orchestration** | Varios | May 2025 | https://arxiv.org/abs/2505.19591 | Orquestacion adaptativa via RL donde un orquestador central dirige agentes dinamicamente. |
| **AgentOrchestra: Orchestrating Multi-Agent Intelligence with TEA Protocol** | Varios | Jun 2025 | https://arxiv.org/abs/2506.12508 | Protocolo TEA (Tool-Environment-Agent) para orquestacion unificada. |

### 1.8 Memoria y Estado en Agentes

| Paper | Autores | Fecha | URL | Aporte al libro |
|-------|---------|-------|-----|-----------------|
| **MemGPT: Towards LLMs as Operating Systems** | Charles Packer, Sarah Wooders et al. | Oct 2023 | https://arxiv.org/abs/2310.08560 | Gestion de memoria virtual para LLMs inspirada en sistemas operativos. Memoria jerarquica. |
| **A-MEM: Agentic Memory for LLM Agents** | Xu, Liang et al. | Feb 2025 | https://arxiv.org/abs/2502.12110 | Sistema de memoria agentica basado en Zettelkasten. Superior en tareas multi-hop. |

### 1.9 Evaluacion y Benchmarks de Agentes

| Paper | Autores | Fecha | URL | Aporte al libro |
|-------|---------|-------|-----|-----------------|
| **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** | Carlos E. Jimenez et al. | 2024 | https://www.swebench.com/ | Benchmark fundamental para evaluar agentes de codigo en issues reales de GitHub. |
| **AgentBench: Evaluating LLMs as Agents** | Varios | ICLR 2024 | https://github.com/THUDM/AgentBench | Benchmark multi-tarea para evaluar LLMs como agentes en 8 entornos distintos. |
| **AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents** | Chang Ma et al. | NeurIPS 2024 | https://proceedings.neurips.cc/paper_files/paper/2024/file/877b40688e330a0e2a3cb3c0402f7c71c70499c-Paper-Datasets_and_Benchmarks_Track.pdf | Evaluacion analitica de agentes LLM multi-turno. |

---

## 2. DOCUMENTACION TECNICA OFICIAL

### 2.1 Frameworks de Agentes

| Recurso | Organizacion | URL | Aporte al libro |
|---------|-------------|-----|-----------------|
| **LangGraph Documentation** | LangChain | https://docs.langchain.com/oss/python/langgraph/overview | Framework de orquestacion de agentes como grafos. Persistencia durable, human-in-the-loop. v1.0 disponible. |
| **LangChain Documentation** | LangChain | https://docs.langchain.com | Framework central para desarrollo de aplicaciones con LLMs. v1.0 con foco en agentes. |
| **CrewAI Documentation** | CrewAI Inc. | https://docs.crewai.com | Framework multi-agente con roles, metas, y backstories. Sin dependencias en LangChain. |
| **Microsoft Agent Framework** | Microsoft | https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview | Fusion de AutoGen + Semantic Kernel. Preview publica Oct 2025. Python y .NET. |
| **OpenAI Agents SDK** | OpenAI | https://developers.openai.com/api/docs/guides/agents-sdk | SDK de produccion con handoffs, guardrails, tracing, sessions. Sucesor de Swarm. |
| **OpenAI Agents SDK (Python)** | OpenAI | https://openai.github.io/openai-agents-python/ | Documentacion detallada y referencia API del SDK de Python. |
| **Anthropic Tool Use** | Anthropic | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | Documentacion oficial de tool use con Claude. Incluye Tool Search, Programmatic Tool Calling. |
| **Anthropic Agent SDK** | Anthropic | https://platform.claude.com/docs/en/agent-sdk/overview | SDK de agentes de Anthropic con tools integradas. |
| **Anthropic Agent Skills** | Anthropic | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Skills como carpetas de instrucciones/scripts que Claude carga dinamicamente. Beta Oct 2025. |

### 2.2 Protocolos de Comunicacion

| Recurso | Organizacion | URL | Aporte al libro |
|---------|-------------|-----|-----------------|
| **Model Context Protocol (MCP) Specification** | Anthropic / Linux Foundation | https://modelcontextprotocol.io/specification/2025-11-25 | Protocolo abierto para conectar agentes con herramientas y datos. Spec Nov 2025. Donado a Linux Foundation. |
| **MCP GitHub Repository** | Anthropic | https://github.com/modelcontextprotocol/modelcontextprotocol | Codigo fuente de la especificacion y documentacion del protocolo. |
| **Agent-to-Agent Protocol (A2A)** | Google | https://github.com/a2aproject/A2A | Protocolo abierto para comunicacion entre agentes via HTTPS + JSON-RPC 2.0. v0.3 disponible. |
| **A2A Announcement** | Google | https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ | Blog post de anuncio con arquitectura y Agent Cards. Abr 2025. |

### 2.3 Seguridad y Gobernanza

| Recurso | Organizacion | Fecha | URL | Aporte al libro |
|---------|-------------|-------|-----|-----------------|
| **OWASP Top 10 for LLM Applications 2025** | OWASP | Nov 2024 | https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/ | Las 10 vulnerabilidades principales en apps LLM. Incluye riesgos de RAG y agentes autonomos. |
| **OWASP Top 10 for LLMs - PDF** | OWASP | Nov 2024 | https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf | Documento PDF completo con descripciones detalladas de cada vulnerabilidad. |
| **NIST AI Risk Management Framework (AI RMF 1.0)** | NIST | Ene 2023 | https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf | Framework voluntario para gestionar riesgos de IA. Referencia para gobernanza. |
| **NIST AI RMF Generative AI Profile** | NIST | Jul 2024 | https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.600-1.pdf | Perfil especifico para riesgos de IA generativa. Complemento al AI RMF 1.0. |

---

## 3. BLOG POSTS Y ARTICULOS TECNICOS DE REFERENCIA

### 3.1 Articulos Fundamentales

| Articulo | Autor | Fecha | URL | Aporte al libro |
|----------|-------|-------|-----|-----------------|
| **LLM Powered Autonomous Agents** | Lilian Weng (OpenAI) | Jun 2023 | https://lilianweng.github.io/posts/2023-06-23-agent/ | EL articulo de referencia. Define agente = LLM + memoria + planificacion + herramientas. Cubre CoT, ToT, ReAct, Reflexion, MRKL, HuggingGPT. |
| **Building Effective Agents** | Anthropic | Dic 2024 | https://www.anthropic.com/research/building-effective-agents | 5 patrones de workflows (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) + agentes. "Empieza simple." |
| **Harness Engineering** | Birgitta Bockeler (via Martin Fowler) | 2026 | https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html | Define harness engineering: context engineering + restricciones arquitectonicas + gestion de entropia. |
| **Harness Engineering: Leveraging Codex in an Agent-First World** | OpenAI | Feb 2026 | https://openai.com/index/harness-engineering/ | Caso practico: 1M lineas de codigo en 5 meses con Codex. Define harness = scaffolding + constraints + feedback loops. |
| **Agents** | Chip Huyen | Ene 2025 | https://huyenchip.com/2025/01/07/agents.html | Taxonomia de herramientas (knowledge, capability, write actions), planificacion, modos de fallo. Adaptado de su libro AI Engineering. |
| **Humans and Agents in Software Engineering Loops** | Martin Fowler | 2026 | https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html | Framework "on the loop" vs "in the loop" para colaboracion humano-agente. |

### 3.2 Simon Willison sobre Agentes

| Articulo | Fecha | URL | Aporte al libro |
|----------|-------|-----|-----------------|
| **"I think 'agent' may finally have a widely enough agreed upon definition"** | 2025 | https://simonw.substack.com/p/i-think-agent-may-finally-have-a | Define agente como "LLM que ejecuta herramientas en un loop para lograr un objetivo". |
| **The Lethal Trifecta for AI Agents** | 2025 | https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents | Riesgo critico: datos privados + contenido no confiable + comunicacion externa = robo de datos. |
| **Agentic Engineering Patterns** | 2025-2026 | https://simonw.substack.com/p/agentic-engineering-patterns | Patrones emergentes para ingenieria con agentes de codigo (Claude Code, Codex). |
| **2025: The Year in LLMs** | Dic 2025 | https://simonw.substack.com/p/2025-the-year-in-llms | Revision anual del estado del arte en LLMs y agentes. |

### 3.3 Harrison Chase (LangChain) sobre Arquitecturas de Agentes

| Articulo | Fecha | URL | Aporte al libro |
|----------|-------|-----|-----------------|
| **Why You Should Outsource Your Agentic Infrastructure, But Own Your Cognitive Architecture** | Jul 2024 | https://blog.langchain.com/why-you-should-outsource-your-agentic-infrastructure-but-own-your-cognitive-architecture/ | Distincion clave entre infraestructura agentica y arquitectura cognitiva. |
| **Reflections on Three Years of Building LangChain** | Oct 2025 | https://blog.langchain.com/three-years-langchain/ | Evolucion de patrones de agentes desde 2023. "Los mejores patrones estan mucho mas entendidos hoy." |
| **Context Engineering for Agents** | 2025 | https://blog.langchain.com/context-engineering-for-agents/ | Context engineering como disciplina central para agentes fiables. |
| **State of Agent Engineering** | 2025 | https://www.langchain.com/state-of-agent-engineering | Informe del estado de la ingenieria de agentes basado en datos de la comunidad. |

### 3.4 Andrew Ng sobre IA Agentica

| Recurso | Fecha | URL | Aporte al libro |
|---------|-------|-----|-----------------|
| **4 Agentic Design Patterns** (Twitter/X thread + talks) | Mar 2024 | https://x.com/AndrewYNg/status/1773393357022298617 | Los 4 patrones: Reflection, Tool Use, Planning, Multi-agent Collaboration. GPT-3.5 + loop agentico = 95.1% en HumanEval vs 48.1% zero-shot. |
| **Agentic AI Course** (DeepLearning.AI) | 2025 | https://www.deeplearning.ai/courses/agentic-ai/ | Curso practico sobre sistemas agenticos con los 4 patrones. |
| **AI Agentic Design Patterns with AutoGen** (DeepLearning.AI) | 2024 | https://www.linkedin.com/posts/andrewyng_new-agentic-ai-short-course-ai-agentic-design-activity-7201611168363290627-KJJk | Short course de patrones agenticos con AutoGen de Microsoft. |

### 3.5 Anthropic sobre Seguridad de Agentes

| Recurso | Fecha | URL | Aporte al libro |
|---------|-------|-----|-----------------|
| **Sabotage Evaluations for Frontier Models** | 2024 | https://www.anthropic.com/research/sabotage-evaluations | Framework para evaluar capacidades de sabotaje en modelos frontera. 5 componentes de sabotaje agentico. |
| **Pilot Sabotage Risk Report (Summer 2025)** | 2025 | https://alignment.anthropic.com/2025/sabotage-risk-report/ | Evaluacion de riesgo de sabotaje de Claude Opus 4. Riesgo "muy bajo pero no totalmente negligible". |
| **Bloom: Automated Behavioral Evaluations** | 2025 | https://alignment.anthropic.com/2025/bloom-auto-evals/ | Herramienta open source para evaluaciones conductuales automatizadas de modelos. |
| **Recommendations for Technical AI Safety Research Directions** | 2025 | https://alignment.anthropic.com/2025/recommended-directions/ | Direcciones recomendadas para investigacion en seguridad de IA. |
| **Effective Context Engineering for AI Agents** | 2025 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Guia practica de context engineering para agentes. |
| **Writing Tools for Agents** | 2025 | https://www.anthropic.com/engineering/writing-tools-for-agents | Como disenar herramientas efectivas para que los agentes las usen. |

### 3.6 RAG en Produccion

| Articulo | Autor/Fuente | URL | Aporte al libro |
|----------|-------------|-----|-----------------|
| **Six Lessons Learned Building RAG Systems in Production** | Towards Data Science | https://towardsdatascience.com/six-lessons-learned-building-rag-systems-in-production/ | Lecciones practicas: chunking semantico, reranking, evaluacion. |
| **Building a Generative AI Platform** | Chip Huyen | https://huyenchip.com/2024/07/25/genai-platform.html | Arquitectura de plataforma GenAI completa incluyendo RAG. Jul 2024. |

---

## 4. LIBROS DE REFERENCIA

| Libro | Autor(es) | Editorial | Fecha | URL | Aporte al libro |
|-------|-----------|-----------|-------|-----|-----------------|
| **AI Engineering: Building Applications with Foundation Models** | Chip Huyen | O'Reilly | 2025 | https://www.oreilly.com/library/view/ai-engineering/9781098166298/ | Cobertura completa del AI stack: modelos, evaluacion, RAG, agentes, despliegue. El libro mas leido en O'Reilly desde su lanzamiento. |
| **Designing Multi-Agent Systems: Principles, Patterns, and Implementation** | Victor Dibia | Self-published | Nov 2025 | https://www.amazon.com/Designing-Multi-Agent-Systems-Principles-Implementation/dp/B0G2BCQQJY | 15 capitulos, 395 paginas. Construye framework "picoagents" desde cero. Patrones multi-agente, evaluacion, despliegue, seguridad. |
| **Artificial Intelligence: A Modern Approach, 4th Ed.** | Stuart Russell, Peter Norvig | Pearson | 2020 | https://aima.cs.berkeley.edu/ | Cap. 2 define PEAS y taxonomia de agentes. Referencia canonica de IA. |
| **AI Agents in Action** (2nd Ed.) | Micheal Lanham | Manning | 2024-2025 | https://www.manning.com/books/ai-agents-in-action-second-edition | 11 capitulos cubriendo agentes con OpenAI API, LangChain, AutoGen, CrewAI. 2a ed. incluye MCP. |
| **An Illustrated Guide to AI Agents** | Maarten Grootendorst, Jay Alammar | O'Reilly | Sep 2025 | https://www.oreilly.com/library/view/an-illustrated-guide/9798341662681/ | Cientos de ilustraciones. Cubre LLMs de razonamiento, agentes multimodales, agentes de codigo, quantizacion, destilacion. |
| **LLM Design Patterns** | Ken Huang | Packt | 2025 | https://www.amazon.com/LLM-Design-Patterns-Practical-Efficient/dp/1836207034 | Guia practica de patrones de diseno para sistemas con LLMs robustos y eficientes. |
| **Recursos GitHub del libro de Chip Huyen** | Chip Huyen | GitHub | 2025 | https://github.com/chiphuyen/aie-book | Material de apoyo para AI Engineering con notebooks y ejemplos. |
| **Designing Multi-Agent Systems - GitHub** | Victor Dibia | GitHub | 2025 | https://github.com/victordibia/designing-multiagent-systems | Codigo fuente del libro incluyendo picoagents framework. |

---

## 5. REPOSITORIOS DE CODIGO

### 5.1 Harness e Infraestructura de Agentes

| Repositorio | Descripcion | URL |
|-------------|-------------|-----|
| **langchain-ai/deepagents** | Agent harness con LangGraph: planning tool, filesystem backend, subagentes | https://github.com/langchain-ai/deepagents |
| **haasonsaas/agent-harness** | Harness para hot-swapping entre OpenAI Agents SDK y Anthropic Claude SDK | https://github.com/haasonsaas/agent-harness |
| **princeton-pli/hal-harness** | Harness estandarizado para evaluaciones reproducibles de agentes | https://github.com/princeton-pli/hal-harness |
| **MattMagg/agent-harness** | Docs-first harness para coding agents con guardrails claros | https://github.com/MattMagg/agent-harness |
| **BulloRosso/etienne** | Coding Agent Harness para agentes de IA personalizados | https://github.com/BulloRosso/etienne |

### 5.2 Circuit Breakers para LLMs

| Repositorio | Descripcion | URL |
|-------------|-------------|-----|
| **GraySwanAI/circuit-breakers** | Circuit breakers via representation engineering para prevenir generacion danina | https://github.com/GraySwanAI/circuit-breakers |
| **hanzalagithub/llm-circuit-breaker** | Wrapper para API calls de LLM con patron circuit breaker + retry + backoff | https://github.com/hanzalagithub/llm-circuit-breaker |
| **GoogleCloudPlatform/apigee-samples (LLM circuit breaking)** | Circuit breaking enterprise-grade con Apigee entre RAG apps y LLM endpoints | https://github.com/GoogleCloudPlatform/apigee-samples/blob/main/llm-circuit-breaking/ |

### 5.3 Frameworks de Agentes (Repos Oficiales)

| Repositorio | Descripcion | URL |
|-------------|-------------|-----|
| **langchain-ai/langgraph** | Framework de orquestacion de agentes como grafos. Produccion-ready. | https://github.com/langchain-ai/langgraph |
| **langchain-ai/langgraph-example** | Ejemplo de agente para deploy con LangGraph Cloud | https://github.com/langchain-ai/langgraph-example |
| **crewAIInc/crewAI** | Framework multi-agente con roles autonomos y colaboracion | https://github.com/crewAIInc/crewAI |
| **crewAIInc/crewAI-examples** | Coleccion de ejemplos end-to-end con CrewAI (Flows, crews, integraciones) | https://github.com/crewAIInc/crewAI-examples |
| **microsoft/agent-framework** | Fusion de AutoGen + Semantic Kernel. Python y .NET. | https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview |
| **openai/openai-agents-python** | SDK oficial de OpenAI para agentes. Handoffs, guardrails, tracing. | https://github.com/openai/openai-agents-python |
| **langroid/langroid** | Framework para aprovechar LLMs con programacion multi-agente | https://github.com/langroid/langroid |

### 5.4 Benchmarks y Evaluacion

| Repositorio | Descripcion | URL |
|-------------|-------------|-----|
| **SWE-bench/SWE-bench** | Benchmark para evaluar LLMs resolviendo issues reales de GitHub | https://github.com/SWE-bench/SWE-bench |
| **THUDM/AgentBench** | Benchmark multi-tarea para LLMs como agentes | https://github.com/THUDM/AgentBench |
| **safety-research/bloom** | Evaluaciones conductuales automatizadas de modelos (Anthropic) | https://github.com/safety-research/bloom |
| **zhangxjohn/LLM-Agent-Benchmark-List** | Lista curada de benchmarks para agentes LLM | https://github.com/zhangxjohn/LLM-Agent-Benchmark-List |
| **luo-junyu/Awesome-Agent-Papers** | Survey actualizado de papers sobre agentes LLM | https://github.com/luo-junyu/Awesome-Agent-Papers |

### 5.5 TLA+ y Verificacion Formal

| Repositorio | Descripcion | URL |
|-------------|-------------|-----|
| **tlaplus/Examples** | Coleccion de especificaciones TLA+ de diversa complejidad | https://github.com/tlaplus/Examples |
| **tlaplus/awesome-tlaplus** | Lista curada de recursos TLA+ | https://github.com/tlaplus/awesome-tlaplus |

### 5.6 Protocolos

| Repositorio | Descripcion | URL |
|-------------|-------------|-----|
| **modelcontextprotocol/modelcontextprotocol** | Especificacion y documentacion de MCP | https://github.com/modelcontextprotocol/modelcontextprotocol |
| **a2aproject/A2A** | Protocolo Agent-to-Agent de Google | https://github.com/a2aproject/A2A |
| **anthropics/anthropic-cookbook (agents patterns)** | Cookbook con implementaciones de patrones de agentes | https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents |

### 5.7 Quantizacion de Modelos

| Repositorio | Descripcion | URL |
|-------------|-------------|-----|
| **pprp/Awesome-LLM-Quantization** | Lista exhaustiva de papers y repos de quantizacion para LLMs | https://github.com/pprp/Awesome-LLM-Quantization |
| **ThreeSR/Awesome-Inference-Time-Scaling** | Lista de papers sobre inference-time scaling | https://github.com/ThreeSR/Awesome-Inference-Time-Scaling |

---

## 6. CONFERENCIAS Y TALKS

### 6.1 LangChain Interrupt 2025

| Talk | Ponente | URL | Aporte al libro |
|------|---------|-----|-----------------|
| **Keynote: Agent Engineering as a New Discipline** | Harrison Chase | https://blog.langchain.com/interrupt-2025-recap/ | Define agent engineering = software engineering + prompting + product + ML. |
| **State of AI Agents** | Andrew Ng | (Disponible en grabaciones) | Perspectiva sobre adopcion y patrones agenticos en la industria. |
| **Agent Patterns from LinkedIn, JP Morgan, BlackRock** | Varios | (Grabaciones disponibles) | Casos reales de agentes en produccion a escala enterprise. |

**Todas las sesiones grabadas disponibles:** https://blog.langchain.com/interrupt-2025-recap/

### 6.2 NeurIPS 2024

| Recurso | Descripcion | URL |
|---------|-------------|-----|
| **Workshop on Safety of Agentic AI Systems** | Papers sobre seguridad de agentes: razonamiento seguro, ataques adversarios, control | https://www.mlsafety.org/events/neurips/2024 |
| **Reflective Multi-Agent Collaboration based on LLMs** | Paper sobre colaboracion reflexiva multi-agente | https://proceedings.neurips.cc/paper_files/paper/2024/ |
| **Lista de papers LLM en NeurIPS 2024** | Compilacion de papers aceptados sobre LLMs | https://github.com/Persdre/NeurIPS-2024-LLM-Papers |

### 6.3 ICLR 2025

| Recurso | Descripcion | URL |
|---------|-------------|-----|
| **Workshop on Reasoning and Planning for LLMs** | Explorar capacidades de razonamiento y planificacion de LLMs (ej. o1) | https://workshop-llm-reasoning-planning.github.io/ |
| **LLMs Can Plan Only If We Tell Them** | Paper sobre limitaciones de planificacion en LLMs | https://proceedings.iclr.cc/paper_files/paper/2025/ |
| **Inference Scaling Laws** (paper conferencia) | Paper sobre leyes de escalamiento en inferencia | https://proceedings.iclr.cc/paper_files/paper/2025/ |

### 6.4 ICML 2025

| Talk/Workshop | Descripcion | URL |
|---------------|-------------|-----|
| **Computer-Using Generalist Agents (IBM)** | Agentes autonomos que operan browsers, apps desktop, APIs enterprise | https://icml.cc/virtual/2025/ |
| **Sidekick Agent (Shopify)** | Agente con MCP, post-training, structured generation | https://icml.cc/virtual/2025/ |
| **MACAW: Multi-Agentic Conversational AI (Capital One)** | Workflow multi-agente para razonamiento financiero cuantitativo | https://icml.cc/virtual/2025/ |

### 6.5 Talks y Keynotes Adicionales

| Talk | Ponente | Fuente | URL |
|------|---------|--------|-----|
| **Deep Agents: The Next Evolution in Autonomous AI** | Harrison Chase | ODSC AI West 2025 | https://opendatascience.com/harrison-chase-on-deep-agents-the-next-evolution-in-autonomous-ai/ |
| **Context Engineering Long-Horizon Agents** | Harrison Chase | Sequoia Capital podcast | https://sequoiacap.com/podcast/context-engineering-our-way-to-long-horizon-agents-langchains-harrison-chase/ |
| **Agentic Reasoning** | Andrew Ng | Sequoia AI Ascent 2024 | https://octetdata.com/blog/notes-andrew-ng-agentic-reasoning-2024/ |

---

## 7. RECURSOS ADICIONALES POR TEMA DEL LIBRO

### 7.1 DeepSeek y el "Momento Linux" de la IA

| Recurso | Fecha | URL | Aporte |
|---------|-------|-----|--------|
| **DeepSeek-V3 (GitHub)** | Dic 2024 | https://github.com/deepseek-ai/DeepSeek-V3 | MoE con 671B params. Multi-head Latent Attention. |
| **DeepSeek-R1 (HuggingFace)** | Ene 2025 | https://huggingface.co/deepseek-ai/DeepSeek-R1 | Razonamiento comparable a o1. Open source completo. |
| **DeepSeek Open Source Week** | Feb 2025 | https://apidog.com/blog/deepseek-open-source-week/ | 5 repos: FlashMLA, DeepEP, DeepGEMM, DualPipe, 3FS. |
| **"DeepSeek's Open Source Movement"** (InfoWorld) | 2025 | https://www.infoworld.com/article/3960764/deepseeks-open-source-movement.html | Analisis de la comparacion con el momento Linux. |

### 7.2 Cuantizacion de Modelos

| Recurso | URL | Aporte |
|---------|-----|--------|
| **Demystifying LLM Quantization: GPTQ, AWQ, GGUF** | https://cast.ai/blog/demystifying-quantizations-llms/ | Comparativa practica de metodos de cuantizacion. |
| **Which Quantization Method is Right for You?** (Maarten Grootendorst) | https://newsletter.maartengrootendorst.com/p/which-quantization-method-is-right | Guia de decision entre GPTQ, GGUF, AWQ. |

### 7.3 Criptografia Post-Cuantica

| Recurso | Organizacion | Fecha | URL | Aporte |
|---------|-------------|-------|-----|--------|
| **NIST IR 8547: Transition to Post-Quantum Cryptography Standards** | NIST | Nov 2024 | https://csrc.nist.gov/pubs/ir/8547/ipd | Plan de transicion a PQC. Meta: adopcion generalizada para 2035. |
| **FIPS 203, 204, 205 (PQC Standards)** | NIST | Ago 2024 | https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization | Estandares finalizados: CRYSTALS-Kyber, CRYSTALS-Dilithium, SPHINCS+. |
| **Post-Quantum Cryptography** (NIST portal) | NIST | 2024-2025 | https://www.nist.gov/pqc | Portal central del proyecto PQC de NIST. |

### 7.4 NPUs y Limites Fisicos de la IA

| Recurso | URL | Aporte |
|---------|-----|--------|
| **CPU vs GPU vs TPU vs NPU: AI Hardware Architecture Guide 2025** | https://www.thepurplestruct.com/blog/cpu-vs-gpu-vs-tpu-vs-npu-ai-hardware-architecture-guide-2025 | Comparativa de arquitecturas de hardware para IA. |
| **Edge AI in Practice: Neural Networks on Embedded Systems** (MDPI) | https://www.mdpi.com/2079-9292/14/24/4877 | Survey academico de IA en edge con restricciones practicas. |

### 7.5 Mojo vs Rust para IA

| Recurso | URL | Aporte |
|---------|-----|--------|
| **Mojo vs. Rust: What are the differences?** (Modular) | https://www.modular.com/blog/mojo-vs-rust | Comparativa oficial de Modular. Mojo sobre MLIR, Rust sobre LLVM. |
| **Rust vs Mojo 2026: Which Language Rules AI Infrastructure** | https://markaicode.com/rust-vs-mojo-ai-infrastructure-2026/ | Analisis actualizado: Rust para seguridad, Mojo para rendimiento AI. |

### 7.6 Context Window Management

| Recurso | URL | Aporte |
|---------|-----|--------|
| **Cutting Through the Noise: Smarter Context Management** (JetBrains Research) | https://blog.jetbrains.com/research/2025/12/efficient-context-management/ | Investigacion de JetBrains sobre gestion eficiente de contexto para agentes. |
| **Context Engineering** (LangChain Blog) | https://blog.langchain.com/context-engineering-for-agents/ | Write, select, compress, isolate como estrategias de contexto. |
| **Memory Blocks: Key to Agentic Context Management** (Letta) | https://www.letta.com/blog/memory-blocks | Abstraccion de bloques de memoria para gestion de contexto. |

### 7.7 Patrones de Diseno para Sistemas con IA

| Recurso | URL | Aporte |
|---------|-----|--------|
| **Emerging Architectures for LLM Applications** (a16z) | https://a16z.com/emerging-architectures-for-llm-applications/ | Patrones arquitectonicos emergentes para apps LLM por Andreessen Horowitz. |
| **Generative AI Design Patterns: A Comprehensive Guide** (TDS) | https://towardsdatascience.com/generative-ai-design-patterns-a-comprehensive-guide-41425a40d7d0/ | Guia comprehensiva de patrones de diseno para IA generativa. |
| **SALLMA: A Software Architecture for LLM-Based Multi-Agent Systems** | https://robertoverdecchia.github.io/papers/SATrends_2025.pdf | Arquitectura de software para sistemas multi-agente basados en LLM. |

---

## 8. ORGANIZACION POR CAPITULO SUGERIDO DEL LIBRO

### Cap 1: Que es realmente un agente (De PEAS y BDI a los LLMs modernos)
- Russell & Norvig Cap. 2 (PEAS)
- Rao & Georgeff 1995 (BDI)
- Lilian Weng blog post
- Chip Huyen "Agents"
- Simon Willison definicion de agente

### Cap 2: El loop agentico (anatomia del ciclo razonamiento-accion)
- ReAct paper (Yao et al.)
- Chain-of-Thought (Wei et al.)
- Anthropic "Building Effective Agents"
- Andrew Ng 4 patrones agenticos

### Cap 3: Como razonan los LLMs (de Turing a inference-time scaling)
- Chain-of-Thought, Tree of Thoughts, Reflexion
- Inference Scaling Laws papers
- LATS paper

### Cap 4: Agent Harness (el arnes que controla a tu agente)
- Martin Fowler harness engineering
- OpenAI harness engineering blog
- LangGraph / CrewAI documentation
- OpenAI Agents SDK, Anthropic Agent SDK

### Cap 5: Memoria y estado en agentes
- MemGPT paper
- A-MEM paper
- Context window management resources
- Memory Blocks (Letta)

### Cap 6: La ventana de contexto como recurso escaso
- Context engineering resources (LangChain, Anthropic, JetBrains)
- Inference scaling papers
- Chip Huyen sobre planificacion y contexto

### Cap 7: RAG en produccion (2026)
- Six Lessons Learned RAG in Production
- Chip Huyen GenAI Platform
- OWASP (riesgos de RAG)

### Cap 8: Contratos tipados para agentes (JSON Schemas a verificacion formal)
- SYSMOBENCH paper
- TLA+ repos y papers
- AgentGuard paper
- Trustworthy AI Agents position paper

### Cap 9: Testing de agentes
- SWE-bench
- AgentBench
- Bloom (Anthropic)
- AgentBoard

### Cap 10: Verificacion formal de agentes
- Position paper LLMs + Formal Methods
- AgentGuard
- TLA+ resources
- SYSMOBENCH

### Cap 11: OWASP Top 10 para LLMs
- OWASP Top 10 for LLMs 2025 (documento completo)
- NIST AI RMF 1.0 y GenAI Profile
- Simon Willison "Lethal Trifecta"
- Anthropic sabotage evaluations

### Cap 12: Orquestacion multi-agente
- Multi-agent orchestration survey (arXiv 2601.13671)
- Agent interoperability protocols survey
- CrewAI docs y examples
- Microsoft Agent Framework

### Cap 13: El protocolo que falta (comunicacion entre agentes)
- MCP specification
- A2A protocol
- Survey de protocolos (MCP, ACP, A2A, ANP)
- SALLMA architecture paper

### Cap 14: Patrones de diseno para sistemas con IA
- a16z Emerging Architectures
- Anthropic 5 workflow patterns
- Andrew Ng design patterns
- Harrison Chase cognitive architecture vs agentic infrastructure

### Cap 15: De agentes teoricos a agentes en produccion
- LangChain Interrupt 2025 talks (LinkedIn, JP Morgan, BlackRock)
- OpenAI harness engineering
- ICML 2025 talks (IBM, Shopify, Capital One)
- State of Agent Engineering (LangChain)

### Cap 16: Cuantizacion de modelos
- GPTQ, AWQ, GGUF comparativas
- Awesome-LLM-Quantization repo
- An Illustrated Guide to AI Agents (cap. sobre Tiny Agent)

### Cap 17: DeepSeek y el momento Linux de la IA
- DeepSeek-V3, DeepSeek-R1 papers/repos
- DeepSeek Open Source Week
- Analisis comparativo con Linux

### Cap 18: Mojo vs Rust para IA
- Modular blog comparativa
- Benchmarks y casos de uso
- Ecosistema y madurez 2025

### Cap 19: Limites fisicos de la IA (NPUs, ancho de banda)
- Hardware architecture guide
- Edge AI survey (MDPI)
- NPU specs y limitaciones

### Cap 20: Migracion a criptografia post-cuantica
- NIST IR 8547
- FIPS 203, 204, 205
- Plan de transicion 2035

---

## 9. SURVEYS Y META-RECURSOS

| Recurso | URL | Descripcion |
|---------|-----|-------------|
| **Awesome-Agent-Papers** | https://github.com/luo-junyu/Awesome-Agent-Papers | Survey actualizado con papers categorizados sobre agentes LLM |
| **Awesome-LangGraph** | https://github.com/von-development/awesome-LangGraph | Indice completo del ecosistema LangChain + LangGraph |
| **Agent-Memory-Paper-List** | https://github.com/Shichun-Liu/Agent-Memory-Paper-List | Papers sobre memoria para agentes de IA |
| **Awesome-Inference-Time-Scaling** | https://github.com/ThreeSR/Awesome-Inference-Time-Scaling | Papers sobre inference-time scaling |
| **Awesome-LLM-Quantization** | https://github.com/pprp/Awesome-LLM-Quantization | Papers y repos de cuantizacion para LLMs |
| **Awesome-TLA+** | https://github.com/tlaplus/awesome-tlaplus | Recursos curados de TLA+ |
| **Noteworthy LLM Research Papers of 2024** (Sebastian Raschka) | https://sebastianraschka.com/blog/2025/llm-research-2024.html | Resumen de papers notables de 2024 |
| **State of LLMs 2025** (Sebastian Raschka) | https://magazine.sebastianraschka.com/p/state-of-llms-2025 | Progreso y predicciones en LLMs |
