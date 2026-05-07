---
title: "La migración a criptografía post-cuántica: qué necesitas saber como desarrollador"
date: 2026-02-15
author: "Héctor Patricio"
tags: ['criptografía', 'post-cuántica', 'quantum', 'seguridad', 'NIST', 'lattice', 'hash', 'TLS']
description: "La computación cuántica amenaza la criptografía actual. Aprende sobre los nuevos algoritmos estandarizados por NIST y qué pasos concretos debes tomar como desarrollador para migrar."
featuredImage: ""
draft: true
---

<!-- Palabra estimada total: ~4000-4500 palabras -->

Solo el 3% de las organizaciones han comenzado a implementar medidas de criptografía
post-cuántica, pero los mandatos gubernamentales ya están forzando la migración
en 2026. En artículos anteriores del blog hemos explorado a fondo los fundamentos
de la criptografía: hashes, cifrados de bloque, cifrados de flujo, MACs, e incluso
la relación entre criptografía y computación cuántica. Este artículo es la
continuación natural: ¿qué hacemos ahora que la amenaza cuántica se vuelve concreta?

## Recapitulación: por qué la computación cuántica amenaza la criptografía

<!-- ~400 palabras -->

Resumen breve de lo cubierto en el post "Criptografía VS computación cuántica".
El algoritmo de Shor y la factorización de números grandes en tiempo polinomial.
El algoritmo de Grover y la búsqueda en bases de datos no ordenadas (reduce la
seguridad de los hashes a la mitad). Qué algoritmos actuales están en riesgo:
RSA, ECDSA, ECDH (todos basados en problemas que Shor resuelve eficientemente).
Qué algoritmos NO están en riesgo: AES-256, SHA-3 (solo necesitan duplicar el
tamaño de clave).

### La amenaza "Harvest Now, Decrypt Later"

<!-- ~300 palabras -->

El escenario más preocupante y urgente: adversarios estatales están capturando
tráfico cifrado ahora para descifrarlo cuando tengan computadoras cuánticas
funcionales. Esto significa que datos cifrados hoy con RSA o ECDH ya están
comprometidos si necesitan permanecer secretos por más de 10-15 años. Ejemplos
concretos: secretos de estado, historiales médicos, propiedad intelectual,
comunicaciones diplomáticas. Por esto la migración es urgente AHORA, no cuando
exista la computadora cuántica.

## Los nuevos algoritmos: qué estandarizó NIST

<!-- ~800 palabras -->

### ML-KEM (antes CRYSTALS-Kyber): intercambio de claves

<!-- ~300 palabras -->

El reemplazo para ECDH y RSA-KEM. Basado en el problema de Learning With Errors
(LWE) sobre retículos (lattices). Explicar de forma intuitiva qué es un retículo
y por qué el problema es difícil incluso para computadoras cuánticas. Tres
niveles de seguridad: ML-KEM-512, ML-KEM-768, ML-KEM-1024. Tamaños de clave
y ciphertext comparados con RSA/ECDH (significativamente más grandes). Rendimiento:
sorprendentemente rápido, comparable o mejor que RSA.

### ML-DSA (antes CRYSTALS-Dilithium): firmas digitales

<!-- ~300 palabras -->

El reemplazo para ECDSA y RSA para firmas. También basado en retículos (problema
Module-LWE). Tres niveles de seguridad. Tamaños de firma y clave pública
(más grandes que ECDSA). Rendimiento de verificación y generación de firmas.
Caso de uso principal: certificados TLS, firmas de código, autenticación.

### SLH-DSA (antes SPHINCS+): firmas basadas en hash

<!-- ~200 palabras -->

La opción "conservadora": basada únicamente en la seguridad de funciones hash.
No depende de problemas matemáticos nuevos como los retículos. Firmas más grandes
pero con garantías de seguridad más estudiadas. Conectar con la serie del blog
sobre hashes y SHA-3: la seguridad de SLH-DSA descansa en las mismas propiedades
que hemos analizado (resistencia a preimagen, resistencia a colisiones).
Cuándo preferir SLH-DSA sobre ML-DSA.

## Fundamentos matemáticos: criptografía basada en retículos

<!-- ~500 palabras -->

### ¿Qué es un retículo?

<!-- ~250 palabras -->

Definición intuitiva: una cuadrícula regular en un espacio de muchas dimensiones.
Formalmente: el conjunto de todas las combinaciones enteras de un conjunto de
vectores base. Visualización en 2D y 3D, y por qué en dimensiones altas los
problemas se vuelven extremadamente difíciles. Conectar con el post sobre
matemáticas para criptografía.

### El problema del vector más corto (SVP) y Learning With Errors (LWE)

<!-- ~250 palabras -->

SVP: dado un retículo, encontrar el vector más corto no nulo. LWE: dado un
sistema de ecuaciones lineales con "ruido" añadido, recuperar la solución
original. Por qué estos problemas son difíciles para computadoras clásicas Y
cuánticas (no se conoce un algoritmo cuántico eficiente). Relación con los
problemas NP del post anterior del blog. Nivel de confianza de la comunidad
criptográfica en estos problemas.

## Guía práctica de migración para desarrolladores

<!-- ~800 palabras -->

### Qué cambia en TLS y certificados

<!-- ~300 palabras -->

TLS 1.3 con intercambio de claves híbrido (clásico + post-cuántico). Los
navegadores ya soportan ML-KEM: Chrome desde 2024, Firefox desde 2025. El
enfoque híbrido: combinar X25519 con ML-KEM-768 (X25519Kyber768). Cómo
actualizar tu servidor web (nginx, Apache). Certificados X.509 con firmas
post-cuánticas. El problema del tamaño: certificados más grandes impactan
el handshake TLS.

### Qué cambia en tu código

<!-- ~250 palabras -->

Bibliotecas que ya soportan PQC: liboqs (Open Quantum Safe), BoringSSL,
AWS-LC. Ejemplos de código para intercambio de claves con ML-KEM. Cómo
actualizar firmas digitales en tu aplicación. El patrón de migración
recomendado: primero híbrido, luego solo post-cuántico. Testing: cómo
verificar que tu implementación es correcta.

### Impacto en rendimiento y almacenamiento

<!-- ~250 palabras -->

Tamaños de clave comparados: ECDH (32 bytes) vs ML-KEM-768 (1184 bytes clave
pública). Tamaños de firma comparados: ECDSA (64 bytes) vs ML-DSA-65 (3293
bytes). Impacto en ancho de banda, especialmente en IoT y dispositivos
limitados. Benchmarks de rendimiento: la buena noticia es que las operaciones
son rápidas. El cuello de botella es el tamaño, no la velocidad.

## La línea de tiempo: mandatos y urgencia

<!-- ~400 palabras -->

### Mandatos gubernamentales

<!-- ~200 palabras -->

NIST ha publicado los estándares finales (FIPS 203, 204, 205) en agosto 2024.
NSA CNSA 2.0: todas las agencias de EE.UU. deben migrar a PQC para 2033, con
hitos intermedios. La directiva de la Casa Blanca (NSM-10) requiere inventario
criptográfico para 2026. Europa: ENISA publicó guías de migración. China:
avances significativos en computación cuántica (el procesador Zuchongzhi).

### Tu plan de migración

<!-- ~200 palabras -->

Paso 1: Inventario criptográfico (qué algoritmos usas y dónde). Paso 2:
Priorizar por riesgo (datos de larga vida primero). Paso 3: Implementar
modo híbrido en TLS y comunicaciones. Paso 4: Migrar firmas digitales.
Paso 5: Auditoría y testing continuo. Herramientas para el inventario:
cbom (Cryptographic Bill of Materials).

## Conclusión

<!-- ~200 palabras -->

La migración a criptografía post-cuántica no es un problema del futuro, es un
problema del presente. La amenaza "harvest now, decrypt later" hace que cada día
que pase sin migrar sea un día de exposición. Los algoritmos están estandarizados,
las bibliotecas están disponibles, y los mandatos gubernamentales son claros.
Como desarrolladores, es nuestra responsabilidad entender estos cambios y
aplicarlos en nuestros sistemas.

---

## Resumen de investigación

La migración a criptografía post-cuántica (PQC) representa la transición criptográfica más significativa desde la introducción de criptografía de clave pública en los 1970s. El algoritmo de Shor rompería completamente RSA y ECC resolviendo factorización y logaritmo discreto en tiempo polinomial. El algoritmo de Grover ofrece speedup cuadrático contra cifrados simétricos, reduciendo la seguridad a la mitad (AES-128 tendría solo 64 bits de seguridad cuántica, haciendo AES-256 el mínimo recomendado).

La amenaza más urgente es "Harvest Now, Decrypt Later" (HNDL): adversarios estatales ya capturan tráfico cifrado hoy para descifrarlo cuando tengan computadoras cuánticas funcionales. Esto hace la migración urgente para datos que deben permanecer confidenciales 10-15+ años.

NIST concluyó un proceso de estandarización de 8 años en agosto 2024: FIPS 203 (ML-KEM/Kyber), FIPS 204 (ML-DSA/Dilithium) y FIPS 205 (SLH-DSA/SPHINCS+). Todos se basan en problemas de lattice (Module Learning With Errors), para los cuales no existe algoritmo cuántico con speedup exponencial. NIST IR 8547 establece deprecación de RSA/ECC para 2030 y prohibición para 2035. NSA CNSA 2.0 exige cumplimiento total para 2035 con hitos desde 2025. La Comisión Europea establece: planes nacionales para 2026, sistemas de alto riesgo migrados para 2030, transición completa para 2035.

La estrategia recomendada son esquemas híbridos (X25519 + ML-KEM-768). Cloudflare y Google ya despliegan esto en producción (~1.8% de conexiones TLS 1.3 post-quantum en early 2024). liboqs, OpenSSL 3.5+ y BoringSSL proveen soporte de bibliotecas.

---

### Referencias y fuentes clave

#### Estándares NIST

1. **NIST. (2024).** "FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM)." [https://csrc.nist.gov/pubs/fips/203/final](https://csrc.nist.gov/pubs/fips/203/final) — Estándar de ML-KEM (antes Kyber) para encapsulación de claves. Parámetros ML-KEM-512/768/1024.

2. **NIST. (2024).** "FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA)." [https://csrc.nist.gov/pubs/fips/204/final](https://csrc.nist.gov/pubs/fips/204/final) — Estándar de ML-DSA (antes Dilithium) para firmas digitales. Reemplaza ECDSA y RSA-PSS.

3. **NIST. (2024).** "FIPS 205: Stateless Hash-Based Digital Signature Standard (SLH-DSA)." [https://csrc.nist.gov/pubs/fips/205/final](https://csrc.nist.gov/pubs/fips/205/final) — SLH-DSA (antes SPHINCS+): backup de diversidad basado en hashes, no en lattices.

4. **NIST. (2024).** "NIST Releases First 3 Finalized Post-Quantum Encryption Standards." [https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) — Comunicado oficial del proceso de 8 años.

5. **NIST IR 8547. (2024).** "Transition to Post-Quantum Cryptography Standards." [https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf) — Timelines concretos: RSA/ECC deprecados después de 2030, prohibidos después de 2035.

#### Amenaza cuántica

6. **Federal Reserve. (2025).** "Harvest Now, Decrypt Later: Post-Quantum Cryptography and Data Privacy Risks." [https://www.federalreserve.gov/econres/feds/harvest-now-decrypt-later-examining-post-quantum-cryptography-and-the-data-privacy-risks-for-distributed-ledger-networks.htm](https://www.federalreserve.gov/econres/feds/harvest-now-decrypt-later-examining-post-quantum-cryptography-and-the-data-privacy-risks-for-distributed-ledger-networks.htm) — Formalización del modelo HNDL y su impacto en el sector financiero.

7. **MDPI Cryptography. (2022).** "Harvest-Now, Decrypt-Later: A Temporal Cybersecurity Risk in the Quantum Transition." [https://www.mdpi.com/2673-4001/6/4/100](https://www.mdpi.com/2673-4001/6/4/100) — Análisis formal de ventanas de exposición por sector. Datos médicos y gubernamentales enfrentan décadas de exposición.

8. **Kudelski Security. (2024).** "Quantum Attack Resource Estimate: Using Shor's Algorithm to Break RSA vs DH/DSA vs ECC." [https://kudelskisecurity.com/research/quantum-attack-resource-estimate-using-shors-algorithm-to-break-rsa-vs-dh-dsa-vs-ecc](https://kudelskisecurity.com/research/quantum-attack-resource-estimate-using-shors-algorithm-to-break-rsa-vs-dh-dsa-vs-ecc) — Estimaciones concretas de qubits y operaciones necesarias para romper cada algoritmo.

9. **Grassl, M., et al. (2016).** "Applying Grover's Algorithm to AES: Quantum Resource Estimates." *Lecture Notes in Computer Science, Springer*. [https://arxiv.org/abs/1512.04965](https://arxiv.org/abs/1512.04965) — AES-256 retiene ~128 bits de seguridad cuántica. Base para recomendar AES-256 como mínimo.

#### Fundamentos matemáticos

10. **Regev, O. (2010).** "The Learning with Errors Problem." *Computational Complexity Conference*. [https://cims.nyu.edu/~regev/papers/lwesurvey.pdf](https://cims.nyu.edu/~regev/papers/lwesurvey.pdf) — Survey fundacional de LWE, la base matemática de ML-KEM y ML-DSA.

11. **Red Hat. (2024).** "Post-Quantum Cryptography: Lattice-Based Cryptography." [https://www.redhat.com/en/blog/post-quantum-cryptography-lattice-based-cryptography](https://www.redhat.com/en/blog/post-quantum-cryptography-lattice-based-cryptography) — Explicación accesible de LWE, Ring-LWE y Module-LWE para desarrolladores.

#### Mandatos gubernamentales y roadmaps

12. **NSA. (2022, actualizado 2024).** "Commercial National Security Algorithm Suite 2.0 (CNSA 2.0)." [https://media.defense.gov/2025/May/30/2003728741/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS.PDF](https://media.defense.gov/2025/May/30/2003728741/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS.PDF) — Mandato para National Security Systems: AES-256, ML-KEM, ML-DSA. Deadlines agresivos desde 2025, cumplimiento total 2033-2035.

13. **European Commission. (2024).** "A Coordinated Implementation Roadmap for the Transition to Post-Quantum Cryptography." [https://digital-strategy.ec.europa.eu/en/library/coordinated-implementation-roadmap-transition-post-quantum-cryptography](https://digital-strategy.ec.europa.eu/en/library/coordinated-implementation-roadmap-transition-post-quantum-cryptography) — Tres hitos: planes nacionales 2026, alto riesgo migrado 2030, transición completa 2035.

14. **UK NCSC. (2025).** "Timelines for Migration to Post-Quantum Cryptography." [https://www.ncsc.gov.uk/guidance/pqc-migration-timelines](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines) — Tres fases: Discover & Plan (2028), Prioritize & Pilot (2028-2031), Complete Adoption (2031-2035).

15. **PQCC. (2025).** "Post-Quantum Cryptography Migration Roadmap." [https://pqcc.org/post-quantum-cryptography-migration-roadmap/](https://pqcc.org/post-quantum-cryptography-migration-roadmap/) — Guía paso a paso más operativa que los documentos NIST.

16. **CISA. (2024).** "Strategy for Migrating to Automated PQC Discovery and Inventory Tools." [https://www.cisa.gov/sites/default/files/2024-09/Strategy-for-Migrating-to-Automated-PQC-Discovery-and-Inventory-Tools.pdf](https://www.cisa.gov/sites/default/files/2024-09/Strategy-for-Migrating-to-Automated-PQC-Discovery-and-Inventory-Tools.pdf) — Framework para descubrir uso de RSA/ECC en sistemas.

#### TLS y protocolos

17. **IETF. (2024-2025).** "draft-ietf-tls-ecdhe-mlkem: Post-Quantum Hybrid ECDHE-MLKEM Key Agreement for TLS 1.3." [https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/](https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/) — Draft de estandarización de X25519MLKEM768 para TLS 1.3.

18. **IETF. (2024).** "draft-ietf-tls-hybrid-design: Hybrid Key Exchange in TLS 1.3." [https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/16/](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/16/) — Diseño general de key exchange híbrido: atacante debe romper ambos algoritmos.

#### Despliegues en producción

19. **Cloudflare. (2024).** "The State of the Post-Quantum Internet." [https://blog.cloudflare.com/pq-2024/](https://blog.cloudflare.com/pq-2024/) — ~1.8% de conexiones TLS 1.3 ya son post-quantum. Desafíos de protocol ossification.

20. **Cloudflare. (2024).** "NIST's First Post-Quantum Standards." [https://blog.cloudflare.com/nists-first-post-quantum-standards/](https://blog.cloudflare.com/nists-first-post-quantum-standards/) — Explicación técnica de FIPS 203/204/205 desde perspectiva de operador de infraestructura.

21. **Meta Engineering. (2024).** "Post-Quantum Readiness for TLS at Meta." [https://engineering.fb.com/2024/05/22/security/post-quantum-readiness-tls-pqr-meta/](https://engineering.fb.com/2024/05/22/security/post-quantum-readiness-tls-pqr-meta/) — Experiencia de Meta desplegando PQC TLS a escala.

#### Bibliotecas y herramientas

22. **Open Quantum Safe. (ongoing).** "liboqs: C Library for Quantum-Resistant Cryptography." [https://openquantumsafe.org/liboqs/](https://openquantumsafe.org/liboqs/) — Biblioteca principal open-source con bindings para C, C++, Go, Java, Python y Rust.

23. **Open Quantum Safe. (2024-2025).** "oqs-provider: OpenSSL 3 Provider for Post-Quantum Algorithms." [https://github.com/open-quantum-safe/oqs-provider](https://github.com/open-quantum-safe/oqs-provider) — Habilita ML-KEM y ML-DSA en OpenSSL 3.x antes de soporte nativo en 3.5+.

24. **World Quantum Summit. (2025).** "Open-Source PQC Libraries Compared: liboqs, OpenSSL 3.4, and BoringSSL." [https://wqs.events/open-source-pqc-libraries-compared-liboqs-openssl-3-4-and-boringssl-implementation-analysis/](https://wqs.events/open-source-pqc-libraries-compared-liboqs-openssl-3-4-and-boringssl-implementation-analysis/) — Comparación de cobertura, madurez, rendimiento e integración.

25. **arXiv. (2025).** "A Survey of Post-Quantum Cryptography Support in Cryptographic Libraries." [https://arxiv.org/html/2508.16078v1](https://arxiv.org/html/2508.16078v1) — Survey sistemático de soporte PQC en bibliotecas criptográficas.

#### Contexto adicional

26. **ENISA. (2021).** "Post-Quantum Cryptography: Current State and Quantum Mitigation." [https://www.enisa.europa.eu/publications/post-quantum-cryptography-current-state-and-quantum-mitigation](https://www.enisa.europa.eu/publications/post-quantum-cryptography-current-state-and-quantum-mitigation) — Documento fundacional de política UE. Recomienda X25519 + Kyber como mitigación inmediata.

27. **NIST NCCoE. (2022-2024).** "Migration to Post-Quantum Cryptography: Crypto-Agility Considerations." [https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms](https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms) — Patrones arquitectónicos para cripto-agilidad.

- Posts del blog: "Criptografía VS computación cuántica", "Matemáticas para criptografía", "Algoritmos criptográficos: ¿qué es un hash?", "Crea hashes resistentes a balas con Keccak (SHA-3)", "Criptografía para desarrolladores: códigos de autenticación de mensajes"
