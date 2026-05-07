# Capitulo 12: Los Limites Fisicos -- NPUs, Cuantizacion y la Ley de las Paredes

> "El cuello de botella no es el computo, es mover datos de la memoria al procesador."

---

En los capitulos anteriores construimos sistemas multi-agente con protocolos de comunicacion, mecanismos de consenso y observabilidad distribuida. Pero toda esa sofisticacion de software choca, tarde o temprano, contra una realidad que ningun framework puede resolver: los limites fisicos del hardware.

Mientras la industria se obsesiona con modelos mas grandes y algoritmos mas sofisticados, hay tres paredes que frenan el progreso de forma fundamental. No son paredes metaforicas: son restricciones impuestas por la fisica, la termodinamica y las matematicas. Entenderlas no es un ejercicio academico. Es lo que te permite tomar decisiones informadas sobre donde correr tu agente, que modelo usar y cuanto puedes esperar realistamente en terminos de latencia y costo.

Este capitulo explora esas restricciones y las tecnicas que la industria ha desarrollado para esquivarlas, con especial atencion a la cuantizacion -- la tecnica que permite correr modelos de miles de millones de parametros en tu telefono -- y a las NPUs, el hardware especializado que promete (pero no siempre cumple) acelerar la inferencia en el edge.

---

## 12.1 Contexto historico: las leyes que nos trajeron aqui

### La ley de Moore: lo que realmente dice

Gordon Moore predijo en 1965 que el numero de transistores en un circuito integrado se duplicaria cada dos anos. Esta prediccion se cumplio con notable precision durante cinco decadas. El chip Intel 4004 de 1971 tenia 2,300 transistores. El Apple M4 de 2024 tiene mas de 28 mil millones.

Pero hay una distincion critica que se pierde en la conversacion popular: la ley de Moore habla de **transistores**, no de **rendimiento**. Durante decadas, mas transistores significaban automaticamente mas rendimiento porque cada generacion de transistores era mas rapida y eficiente. Eso dejo de ser cierto alrededor de 2005 [Shalf, 2020].

La ley sigue viva en cantidad de transistores, pero murio en rendimiento por transistor. La brecha entre "cuantos transistores podemos fabricar" y "cuanto rendimiento obtenemos de ellos" se ha convertido en el problema central de la computacion moderna.

### El escalamiento de Dennard: la pared que nadie vio venir

Robert Dennard propuso en 1974 que al reducir el tamano de los transistores, el voltaje y la corriente se reducirian proporcionalmente, manteniendo la densidad de potencia constante. Esto significaba que podias hacer chips mas rapidos sin que consumieran mas energia por area.

El escalamiento de Dennard dejo de funcionar alrededor de 2006. La razon fue fisica: las corrientes de fuga a escalas nanometricas dejaron de escalar con el tamano del transistor. La consecuencia practica fue brutal: no podemos subir la frecuencia del reloj sin derretir el chip.

Desde ~2005, la frecuencia de los procesadores se estanco en el rango de 3-5 GHz. Toda la mejora de rendimiento desde entonces ha venido de **paralelismo** (mas nucleos) y **especializacion** (hardware dedicado para tareas especificas). Esta es exactamente la razon por la que existen las GPUs, las TPUs y las NPUs.

### La ley de Amdahl: el limite de la paralelizacion

Gene Amdahl formalizo en 1967 una observacion aparentemente obvia pero con consecuencias profundas: no importa cuantos nucleos tengas, la porcion secuencial de tu programa limita la aceleracion maxima.

La formula es:

```python
def amdahl_speedup(parallel_fraction: float, num_processors: int) -> float:
    """Calcula la aceleracion maxima segun la ley de Amdahl.

    Args:
        parallel_fraction: fraccion del programa que es paralelizable (0-1)
        num_processors: numero de procesadores disponibles

    Returns:
        Factor de aceleracion maximo
    """
    serial_fraction = 1.0 - parallel_fraction
    speedup = 1.0 / (serial_fraction + parallel_fraction / num_processors)
    return speedup


# Ejemplo: si el 95% de tu programa es paralelizable
for n_procs in [1, 2, 4, 8, 16, 64, 256, 1024, float('inf')]:
    sp = amdahl_speedup(0.95, n_procs)
    print(f"  {n_procs:>6} procesadores -> {sp:.2f}x aceleracion")

# Resultado:
#       1 procesadores -> 1.00x aceleracion
#       2 procesadores -> 1.90x aceleracion
#       4 procesadores -> 3.48x aceleracion
#       8 procesadores -> 5.93x aceleracion
#      16 procesadores -> 9.14x aceleracion
#      64 procesadores -> 15.42x aceleracion
#     256 procesadores -> 18.62x aceleracion
#    1024 procesadores -> 19.66x aceleracion
#     inf procesadores -> 20.00x aceleracion
```

Incluso con procesadores infinitos, un programa que es 95% paralelizable solo puede acelerarse 20 veces. El 5% secuencial impone un techo infranqueable.

Esto tiene relevancia directa para la inferencia de LLMs. La generacion de tokens es inherentemente secuencial: para generar el token N+1, necesitas el token N. No puedes generar todos los tokens en paralelo porque cada uno depende de los anteriores. Esta secuencialidad impone un limite fundamental a la velocidad de inferencia que ningun hardware puede superar [Semiconductor Engineering, 2024].

---

## 12.2 La pared de memoria: el verdadero cuello de botella

### Por que la inferencia esta limitada por memoria, no por computo

Aqui es donde la intuicion falla a la mayoria de los desarrolladores. Cuando pensamos en "hacer algo mas rapido", pensamos en procesadores mas rapidos, mas nucleos, mas FLOPS. Pero la inferencia de LLMs no funciona asi.

Para generar cada token, un modelo transformer necesita leer **todos** los pesos del modelo de la memoria. Un modelo de 70 mil millones de parametros en FP16 (2 bytes por parametro) ocupa 140 GB. Cada token generado requiere transferir esos 140 GB desde la memoria hacia las unidades de computo.

El ancho de banda de HBM3 (High Bandwidth Memory) en un GPU moderno es de ~2 TB/s. Dividamos:

```python
def tokens_per_second(
    model_params_billions: float,
    bytes_per_param: float,
    memory_bandwidth_tb_s: float,
) -> float:
    """Estima los tokens/s maximos basados en ancho de banda de memoria.

    Esta es una estimacion conservadora que asume que el cuello
    de botella es puramente la lectura de pesos.

    Args:
        model_params_billions: parametros del modelo en miles de millones
        bytes_per_param: bytes por parametro (2 para FP16, 1 para INT8, 0.5 para INT4)
        memory_bandwidth_tb_s: ancho de banda de memoria en TB/s

    Returns:
        Tokens por segundo estimados
    """
    model_size_bytes = model_params_billions * 1e9 * bytes_per_param
    bandwidth_bytes_s = memory_bandwidth_tb_s * 1e12
    return bandwidth_bytes_s / model_size_bytes


# GPU A100 80GB: ~2 TB/s de ancho de banda HBM2e
# GPU H100 80GB: ~3.35 TB/s de ancho de banda HBM3
print("=== Tokens/s estimados (limitados por ancho de banda) ===\n")

configs = [
    ("Llama 3.1 70B FP16", 70, 2.0),
    ("Llama 3.1 70B INT8", 70, 1.0),
    ("Llama 3.1 70B INT4", 70, 0.5),
    ("Llama 3.2 8B FP16", 8, 2.0),
    ("Llama 3.2 8B INT4", 8, 0.5),
    ("Phi-4 mini 3.8B INT4", 3.8, 0.5),
]

for name, params, bpp in configs:
    tps_a100 = tokens_per_second(params, bpp, 2.0)
    tps_h100 = tokens_per_second(params, bpp, 3.35)
    print(f"  {name:30s} -> A100: {tps_a100:7.1f} tok/s | H100: {tps_h100:7.1f} tok/s")

# Resultado:
#   Llama 3.1 70B FP16             -> A100:    14.3 tok/s | H100:    23.9 tok/s
#   Llama 3.1 70B INT8             -> A100:    28.6 tok/s | H100:    47.9 tok/s
#   Llama 3.1 70B INT4             -> A100:    57.1 tok/s | H100:    95.7 tok/s
#   Llama 3.2 8B FP16              -> A100:   125.0 tok/s | H100:   209.4 tok/s
#   Llama 3.2 8B INT4              -> A100:   500.0 tok/s | H100:   837.5 tok/s
#   Phi-4 mini 3.8B INT4           -> A100:  1052.6 tok/s | H100:  1763.2 tok/s
```

Observa las implicaciones: un modelo de 70B en FP16 genera apenas 14 tokens por segundo en un A100, **sin importar cuantos TFLOPS tenga el GPU**. El GPU tiene capacidad para realizar billones de operaciones por segundo, pero esta esperando a que los datos lleguen de la memoria. Es como tener una fabrica con 1,000 trabajadores y una sola puerta de entrada por la que solo cabe una persona a la vez.

### Arithmetic intensity y el modelo roofline

El **modelo roofline** [Yuan et al., 2024] formaliza esta intuicion. Define la **intensidad aritmetica** como la proporcion entre operaciones de computo y bytes transferidos:

```
intensidad_aritmetica = FLOPS realizados / bytes transferidos
```

Las operaciones con baja intensidad aritmetica estan limitadas por ancho de banda de memoria (memory-bound). Las operaciones con alta intensidad aritmetica estan limitadas por computo (compute-bound).

La decodificacion autoregresiva de transformers -- generar un token a la vez -- tiene una intensidad aritmetica extraordinariamente baja. Para cada token, realizas relativamente pocas operaciones por peso leido. Esto situa la inferencia firmemente en la zona memory-bound del modelo roofline.

El **entrenamiento** es diferente: multiplicas matrices grandes contra matrices grandes, reutilizando cada peso para muchas operaciones. El entrenamiento es compute-bound. Por eso optimizar entrenamiento e inferencia requiere hardware fundamentalmente diferente.

### La brecha creciente

El problema se agrava con el tiempo. Los datos de TrendForce [2024] y Gholami et al. [2024] muestran que el computo de chips de IA crece ~3x cada 2 anos, pero el ancho de banda de DRAM crece solo 1.6x y el de interconexion solo 1.4x. La brecha entre lo que podemos calcular y lo que podemos alimentar de datos se amplifica con cada generacion.

Wulf y McKee acunaron el termino "memory wall" (pared de memoria) en 1995. Su tesis central -- que el rendimiento de los sistemas estaria cada vez mas limitado por el acceso a memoria y no por la capacidad de computo -- es aun mas aguda en la era de la IA.

### Batch size: parche, no solucion

Aumentar el batch size mejora la eficiencia porque reutilizas los pesos del modelo para multiples secuencias simultaneamente. Si procesas 32 peticiones a la vez, lees los pesos una vez y los aplicas 32 veces. La intensidad aritmetica sube y te acercas al regimen compute-bound.

Pero el batching tiene limites practicos:

- **Latencia del primer token.** Si esperas a acumular un batch grande, el primer usuario espera mas.
- **Memoria para KV-cache.** Cada secuencia en el batch requiere su propio KV-cache, que crece linealmente con la longitud del contexto. Con secuencias largas, el KV-cache puede consumir mas memoria que el propio modelo.
- **No todos los casos de uso permiten batching.** Un agente interactivo que necesita responder en tiempo real no puede esperar a acumular un batch.

---

## 12.3 Cuantizacion: la matematica detras de correr LLMs en tu telefono

### Representacion numerica: el problema fundamental

Los LLMs se entrenan tipicamente en FP16 (punto flotante de 16 bits) o BF16 (Brain Float 16). Cada parametro ocupa 2 bytes. Un modelo de 70B parametros requiere 140 GB solo para almacenar los pesos.

La cuantizacion reduce la precision numerica de los pesos. En lugar de usar 16 bits por peso, usamos 8, 4 o incluso menos. La pregunta es: cuanto se pierde?

Para entender por que funciona, necesitamos mirar como se distribuyen los pesos de un modelo entrenado.

### La distribucion de los pesos: por que funciona la cuantizacion

Los pesos de una red neuronal entrenada no estan distribuidos uniformemente. Siguen distribuciones aproximadamente gaussianas, centradas en cero con colas ligeras. La mayoria de los pesos son valores pequenos cercanos a cero, con pocos outliers [Gholami et al., 2021].

Esto significa que la mayoria de los valores estan concentrados en un rango pequeno. Si tenemos 16 niveles de cuantizacion (INT4), esos 16 niveles pueden capturar la estructura esencial de la distribucion porque la mayor densidad de valores esta en una region compacta.

### Cuantizacion uniforme: la idea basica

La cuantizacion uniforme mapea un rango continuo de valores de punto flotante a un conjunto discreto de valores enteros:

```python
import numpy as np
from dataclasses import dataclass


@dataclass
class QuantizationParams:
    """Parametros de cuantizacion uniforme."""
    scale: float
    zero_point: int
    bits: int

    @property
    def qmin(self) -> int:
        return 0

    @property
    def qmax(self) -> int:
        return (2 ** self.bits) - 1


def compute_quantization_params(
    weights: np.ndarray,
    bits: int = 8,
) -> QuantizationParams:
    """Calcula los parametros de cuantizacion para un tensor de pesos.

    Cuantizacion uniforme asimetrica:
    q = round((x - zero_point) / scale)
    x_reconstructed = q * scale + zero_point

    Args:
        weights: tensor de pesos en punto flotante
        bits: numero de bits objetivo (8, 4, etc.)

    Returns:
        Parametros de cuantizacion (scale, zero_point, bits)
    """
    w_min = float(weights.min())
    w_max = float(weights.max())
    qmax = (2 ** bits) - 1

    scale = (w_max - w_min) / qmax
    zero_point = round(-w_min / scale)
    zero_point = max(0, min(qmax, zero_point))

    return QuantizationParams(scale=scale, zero_point=zero_point, bits=bits)


def quantize(
    weights: np.ndarray,
    params: QuantizationParams,
) -> np.ndarray:
    """Cuantiza pesos de punto flotante a enteros."""
    q = np.round(weights / params.scale + params.zero_point)
    q = np.clip(q, params.qmin, params.qmax)
    return q.astype(np.uint8 if params.bits == 8 else np.int32)


def dequantize(
    quantized: np.ndarray,
    params: QuantizationParams,
) -> np.ndarray:
    """Reconstruye los pesos desde la representacion cuantizada."""
    return (quantized.astype(np.float32) - params.zero_point) * params.scale


# Ejemplo: cuantizar una capa simulada de un transformer
np.random.seed(42)
# Los pesos reales siguen distribuciones aprox. gaussianas
fake_weights = np.random.normal(0, 0.02, size=(4096, 4096)).astype(np.float32)

print("=== Cuantizacion de pesos (capa simulada 4096x4096) ===\n")
print(f"  Rango original: [{fake_weights.min():.4f}, {fake_weights.max():.4f}]")
print(f"  Media: {fake_weights.mean():.6f}, Std: {fake_weights.std():.6f}")
print(f"  Tamano FP32: {fake_weights.nbytes / 1e6:.1f} MB\n")

for bits in [8, 4, 2]:
    params = compute_quantization_params(fake_weights, bits=bits)
    q_weights = quantize(fake_weights, params)
    r_weights = dequantize(q_weights, params)

    # Error de cuantizacion
    error = np.abs(fake_weights - r_weights)
    size_mb = fake_weights.size * bits / 8 / 1e6

    print(f"  INT{bits}:")
    print(f"    Scale: {params.scale:.8f}")
    print(f"    Error medio: {error.mean():.6f}")
    print(f"    Error maximo: {error.max():.6f}")
    print(f"    Tamano: {size_mb:.1f} MB ({fake_weights.nbytes / 1e6 / size_mb:.1f}x compresion)")
    print()
```

### Tecnicas modernas de cuantizacion

La cuantizacion uniforme basica es el punto de partida, pero las tecnicas modernas son significativamente mas sofisticadas.

**GPTQ (Generative Pre-Trained Transformer Quantization).** Desarrollada por Frantar et al. [2023], GPTQ fue el primer metodo que demostro que se pueden comprimir LLMs a 3-4 bits con perdida minima de calidad. La idea central es cuantizar los pesos capa por capa, compensando el error de cuantizacion en los pesos restantes usando informacion del Hessiano (la matriz de segundas derivadas de la funcion de perdida). El proceso usa una pequena muestra de calibracion (~128 ejemplos) para estimar el impacto de la cuantizacion. GPTQ es ideal para despliegue en GPU.

**AWQ (Activation-Aware Weight Quantization).** Lin et al. [2024] observaron que no todos los pesos son igualmente importantes. Menos del 1% de los canales de pesos son "salientes" -- contribuyen desproporcionadamente a la salida del modelo porque multiplican activaciones de mayor magnitud. AWQ identifica estos pesos observando las activaciones durante una pasada de calibracion y los protege escalandolos antes de cuantizar. El resultado: mejor calidad que GPTQ con el mismo numero de bits. AWQ gano el premio al mejor paper en MLSys 2024.

**SmoothQuant.** Xiao et al. [2023] atacaron un problema diferente: las activaciones (no los pesos) pueden tener outliers enormes que dificultan la cuantizacion. SmoothQuant migra la dificultad de cuantizacion de las activaciones a los pesos aplicando un factor de escala por canal:

```
Y = (X * diag(s)^-1) * (diag(s) * W)
```

Esto "suaviza" las activaciones y "rugosiza" los pesos. Como los pesos tienen distribuciones mas uniformes, son mas faciles de cuantizar. El resultado es INT8 sin perdida perceptible con 1.56x de aceleracion.

**bitsandbytes.** La biblioteca de Dettmers et al. [2022] introdujo un enfoque pragmatico: descomposicion mixed-precision. La mayoria de los pesos van a INT8 o INT4, pero los outliers (valores extremos) se mantienen en FP16. Esta es la unica opcion que soporta entrenamiento (via QLoRA), lo que la hace indispensable para fine-tuning con recursos limitados.

### De 16 bits a 4 bits: que se pierde y que se conserva

La degradacion de calidad depende del numero de bits y de la tecnica:

```python
"""
Tabla de referencia: degradacion de perplexidad por nivel de cuantizacion.

Datos aproximados de benchmarks publicos para modelos de la familia
Llama en WikiText-2 y evaluaciones MMLU.
"""

QUANTIZATION_BENCHMARKS = [
    # (modelo, bits, metodo, perplexidad_relativa, mmlu_delta)
    ("Llama 3.1 70B", 16, "FP16 (base)", 1.000, 0.0),
    ("Llama 3.1 70B", 8, "GPTQ-INT8", 0.998, -0.2),
    ("Llama 3.1 70B", 4, "GPTQ-INT4", 0.985, -1.1),
    ("Llama 3.1 70B", 4, "AWQ-INT4", 0.990, -0.7),
    ("Llama 3.1 70B", 3, "GPTQ-INT3", 0.960, -3.5),
    ("Llama 3.1 70B", 2, "QuIP#-2bit", 0.940, -5.8),
]

print(f"{'Modelo':20s} {'Bits':>4s} {'Metodo':15s} {'Perpl. rel.':>11s} {'MMLU delta':>10s}")
print("-" * 65)
for model, bits, method, perp, mmlu in QUANTIZATION_BENCHMARKS:
    print(f"{model:20s} {bits:>4d} {method:15s} {perp:>11.3f} {mmlu:>+10.1f}%")
```

La regla empirica validada por multiples benchmarks: **un modelo grande cuantizado a 4 bits generalmente supera a un modelo pequeno en 16 bits con la misma huella de memoria**. Llama 70B en INT4 (~35 GB) es mejor que Llama 8B en FP16 (~16 GB) en la mayoria de las tareas.

### GGUF: el formato que democratizo la inferencia local

llama.cpp, creado por Georgi Gerganov, es el proyecto que hizo posible correr LLMs en hardware de consumo. Escrito en C/C++ puro, corre en CPU, GPU Apple Silicon, NVIDIA y AMD [Gerganov et al., 2023].

El formato GGUF (GPT-Generated Unified Format) empaqueta pesos cuantizados con metadatos. Los niveles de cuantizacion mas comunes son:

```python
"""
Guia de seleccion de nivel de cuantizacion GGUF.
"""

GGUF_LEVELS = {
    "Q2_K": {
        "bits_promedio": 2.5,
        "calidad_retenida": 0.85,
        "uso": "Solo si tu hardware no tiene otra opcion",
        "ram_70b_gb": 22,
    },
    "Q3_K_M": {
        "bits_promedio": 3.5,
        "calidad_retenida": 0.92,
        "uso": "Aceptable para tareas simples",
        "ram_70b_gb": 30,
    },
    "Q4_K_M": {
        "bits_promedio": 4.5,
        "calidad_retenida": 0.95,
        "uso": "Mejor relacion calidad/tamano para la mayoria",
        "ram_70b_gb": 40,
    },
    "Q5_K_M": {
        "bits_promedio": 5.5,
        "calidad_retenida": 0.97,
        "uso": "Calidad alta con ahorro significativo",
        "ram_70b_gb": 48,
    },
    "Q6_K": {
        "bits_promedio": 6.5,
        "calidad_retenida": 0.99,
        "uso": "Casi sin perdida perceptible",
        "ram_70b_gb": 55,
    },
    "Q8_0": {
        "bits_promedio": 8.0,
        "calidad_retenida": 0.995,
        "uso": "Virtualmente identico a FP16",
        "ram_70b_gb": 70,
    },
}

print(f"{'Nivel':10s} {'Bits':>5s} {'Calidad':>8s} {'RAM 70B':>8s}  {'Recomendacion'}")
print("-" * 80)
for level, info in GGUF_LEVELS.items():
    print(
        f"{level:10s} {info['bits_promedio']:>5.1f} "
        f"{info['calidad_retenida']:>7.1%} "
        f"{info['ram_70b_gb']:>6d} GB  "
        f"{info['uso']}"
    )
```

Para la mayoria de los casos, **Q4_K_M** ofrece la mejor relacion calidad/tamano. Retiene ~95% de la calidad del modelo original con una compresion de ~4x.

### El verdadero impacto: no solo memoria, sino velocidad

Aqui esta la clave que muchos pasan por alto: la cuantizacion no solo ahorra memoria. Al reducir el tamano de los pesos, reduces la cantidad de datos que necesitas transferir de la memoria al procesador en cada token. Si cuantizas de FP16 a INT4, reduces 4x la cantidad de bytes a leer. Dado que la inferencia esta limitada por ancho de banda de memoria, esto acelera la generacion ~3-4x.

Es por eso que nuestro calculo de tokens por segundo al inicio del capitulo mostraba mejoras dramaticas con INT4: no porque el GPU calcule mas rapido, sino porque alimenta datos al GPU mas rapido.

---

## 12.4 NPUs y hardware especializado: el futuro del edge AI

### Que hay dentro de una NPU moderna

Las NPUs (Neural Processing Units) son procesadores disenados especificamente para operaciones de redes neuronales. A diferencia de una GPU general que puede hacer graficos, computo cientifico y machine learning, una NPU esta optimizada exclusivamente para multiplicaciones de matrices y operaciones tensoriales.

Los tres principales fabricantes de NPUs moviles son:

**Apple Neural Engine.** Presente en todos los chips de la serie A y M. El A19 Pro entrega 35 TOPS (billones de operaciones por segundo). Integrado con la Unified Memory Architecture (UMA) de Apple, que elimina la necesidad de copiar datos entre CPU y GPU/NPU.

**Qualcomm Hexagon.** El NPU dentro de los chips Snapdragon. El Snapdragon X Elite alcanza 45+ TOPS. Su arquitectura combina HVX (Hexagon Vector eXtension) para operaciones vectoriales y HMX (Hexagon Matrix eXtension) para operaciones tensoriales [The Chip Letter, 2024].

**Google Tensor.** Los chips Tensor en los Pixel integran una TPU movil optimizada para los modelos de Google, especialmente Gemini Nano.

### Los TOPS son enganosos

Los fabricantes promocionan sus NPUs con cifras de TOPS cada vez mas altas. Pero hay un problema fundamental: esos TOPS asumen precision INT8 y 100% de utilizacion. En la practica, la utilizacion rara vez supera el 60% porque la NPU pasa tiempo esperando datos [Xu et al., 2025].

Ademas, las operaciones de IA en la vida real no son todas multiplicaciones de matrices INT8. Las capas de atencion, las funciones de activacion, las normalizaciones -- todas requieren operaciones que no mapean perfectamente al hardware de la NPU.

### El problema de la decodificacion: NPUs subutilizadas

El desafio mas serio para las NPUs en inferencia de LLMs es la fase de decodificacion autoregresiva. La NPU esta disenada para paralelismo masivo: puede multiplicar matrices enormes con miles de operaciones simultaneas. Pero durante la generacion de tokens, cada paso produce **un solo token**. No hay suficiente trabajo paralelo para mantener ocupada a la NPU.

Es como tener una fabrica con 1,000 trabajadores para producir una sola pieza a la vez. Los trabajadores estan alli, las maquinas estan alli, pero 999 de cada 1,000 estan ociosos en cada paso.

```python
"""
Estimacion de utilizacion de NPU durante fases de inferencia.
"""

from dataclasses import dataclass


@dataclass
class NPUUtilization:
    """Modelo simplificado de utilizacion de NPU por fase."""
    phase: str
    ops_per_step: int  # operaciones por paso
    npu_capacity: int  # operaciones que la NPU puede hacer por paso
    description: str

    @property
    def utilization(self) -> float:
        return min(1.0, self.ops_per_step / self.npu_capacity)


npu_tops = 45  # TOPS del Snapdragon X Elite
npu_ops_per_ms = npu_tops * 1e9  # operaciones por milisegundo

phases = [
    NPUUtilization(
        phase="Prefill (prompt 2048 tokens)",
        ops_per_step=int(2048 * 8192 * 8192 * 2),  # aprox para un modelo 8B
        npu_capacity=int(npu_ops_per_ms * 100),  # ventana de 100ms
        description="Matriz grande: NPU bien utilizada",
    ),
    NPUUtilization(
        phase="Decode (1 token)",
        ops_per_step=int(1 * 8192 * 8192 * 2),
        npu_capacity=int(npu_ops_per_ms * 100),
        description="Vector * matriz: NPU subutilizada",
    ),
]

print("=== Utilizacion estimada de NPU (Snapdragon X Elite, 45 TOPS) ===\n")
for p in phases:
    print(f"  {p.phase}:")
    print(f"    Utilizacion: {p.utilization:.1%}")
    print(f"    {p.description}\n")
```

La fase de prefill (procesar todo el prompt de entrada) mantiene a la NPU razonablemente ocupada porque procesa muchos tokens en paralelo. Pero la fase de decode, que es la que genera la respuesta token por token, subutiliza dramaticamente el hardware.

### ExecuTorch y la madurez de la inferencia movil

Meta lanzo ExecuTorch 1.0, un runtime optimizado para inferencia en dispositivos moviles y edge. ExecuTorch compila modelos PyTorch a formatos optimizados para NPUs, GPUs moviles y CPUs ARM.

El estado actual (2026) permite correr modelos de hasta 3-4 mil millones de parametros con latencia aceptable en dispositivos de gama alta. Pero "aceptable" significa 10-30 tokens por segundo, no los 100+ que obtienes en un GPU de datacenter.

Para agentes de IA en dispositivos, esto tiene implicaciones directas: puedes correr un agente con un modelo de 3B localmente para tareas de triage rapido, pero las tareas complejas que requieren razonamiento profundo siguen necesitando el cloud.

---

## 12.5 La ley de las paredes: energetica, de Amdahl, de rendimientos decrecientes

### La pared de computo

Entrenar GPT-4 requirio aproximadamente 2x10^25 FLOPS. Los modelos frontera de 2026 requieren ordenes de magnitud mas computo. Pero la mejora en FLOPS por chip crece linealmente, no exponencialmente.

Los datos de la industria muestran un patron preocupante:

- Capacidad de computo de chips de IA: ~3x cada 2 anos
- Demanda de computo de modelos frontera: ~10x cada 2 anos

La brecha se cierra con mas chips, no con chips mas rapidos. Esto explica por que los clusters de entrenamiento de IA tienen miles y decenas de miles de GPUs. Y esos clusters tienen sus propios cuellos de botella: la comunicacion entre GPUs se convierte en el factor limitante (la ley de Amdahl otra vez, pero ahora el "componente secuencial" es la sincronizacion entre nodos).

### La pared de energia

Un cluster de entrenamiento de un modelo frontera consume la energia equivalente a una ciudad pequena. Los datos son reveladores [MIT Technology Review, 2025; Google, 2025]:

- Los data centers de IA en Estados Unidos consumieron 53-76 TWh en 2024.
- Las proyecciones para 2028 son de 165-326 TWh.
- La inferencia (no el entrenamiento) ya domina el consumo: 60-70% del total en 2025.
- Google reporta que la mediana de un prompt en Gemini consume 0.24 Wh.

La inferencia domina el consumo porque aunque cada consulta individual consume poco, el volumen es enorme. Si millones de usuarios hacen docenas de consultas al dia, la energia acumulada supera al entrenamiento, que es un evento unico (o poco frecuente).

Para modelos de razonamiento como DeepSeek-R1 u o1, el problema se agrava: estos modelos pueden consumir 100x mas computo por consulta que un modelo estandar porque "piensan mas tiempo" antes de responder [Introl, 2025].

### La pared de rendimientos decrecientes

Mas alla de las paredes fisicas, hay una pared economica. Los rendimientos decrecientes de escalar modelos estan bien documentados:

- Duplicar el tamano del modelo no duplica la calidad. Las mejoras son logaritmicas, no lineales.
- Las leyes de escalamiento (Chinchilla, Hoffmann et al., 2022) muestran que para obtener mejoras lineales de calidad, necesitas incrementos exponenciales de datos y computo.
- El costo marginal de cada punto porcentual de mejora en benchmarks se incrementa con cada generacion.

Esta es la razon por la que la industria se ha movido hacia **inference-time scaling** (dedicar mas computo a cada consulta individual, como en chain-of-thought) y hacia **Mixture of Experts** (activar solo una fraccion del modelo por token).

---

## 12.6 Mixture of Experts: la respuesta de la industria a la pared de memoria

### Como MoE esquiva el cuello de botella

En un modelo denso, todos los parametros se activan para cada token. En un modelo Mixture of Experts (MoE), solo una fraccion de los parametros se activa -- tipicamente 2 de 8 expertos. Un router (otro pequeno modelo) decide que expertos son relevantes para cada token.

La ventaja para inferencia es directa: si tu modelo tiene 671 mil millones de parametros (como DeepSeek-V3) pero solo activa 37 mil millones por token, reduces la carga de ancho de banda de memoria ~18x. En lugar de leer 671B * 2 bytes = 1.34 TB por token, lees ~37B * 2 bytes = 74 GB [DeepSeek-AI, 2024].

```python
"""
Comparacion de carga de memoria: modelo denso vs MoE.
"""

@dataclass
class ModelConfig:
    name: str
    total_params_b: float  # parametros totales en miles de millones
    active_params_b: float  # parametros activos por token
    bytes_per_param: float = 2.0  # FP16 por defecto

    @property
    def total_size_gb(self) -> float:
        return self.total_params_b * 1e9 * self.bytes_per_param / 1e9

    @property
    def active_size_gb(self) -> float:
        return self.active_params_b * 1e9 * self.bytes_per_param / 1e9

    @property
    def bandwidth_ratio(self) -> float:
        """Ratio de reduccion de ancho de banda vs modelo denso equivalente."""
        return self.total_params_b / self.active_params_b


models = [
    ModelConfig("Llama 3.1 70B (denso)", 70, 70),
    ModelConfig("Llama 3.1 405B (denso)", 405, 405),
    ModelConfig("DeepSeek-V3 (MoE)", 671, 37),
    ModelConfig("Mixtral 8x22B (MoE)", 141, 39),
    ModelConfig("Qwen2-MoE-57B", 57, 14),
]

print(f"{'Modelo':30s} {'Total':>8s} {'Activo':>8s} {'Ratio':>6s}")
print("-" * 55)
for m in models:
    print(
        f"{m.name:30s} {m.total_size_gb:>7.0f}GB "
        f"{m.active_size_gb:>7.0f}GB "
        f"{m.bandwidth_ratio:>5.1f}x"
    )
```

### Trade-offs de MoE

MoE no es gratis:

- **Mayor tamano total.** Aunque activas menos parametros, necesitas almacenar todos en memoria (o en disco con offloading). DeepSeek-V3 en FP16 ocupa 1.3 TB.
- **Routing impredecible.** No sabes de antemano que expertos se activaran, lo que dificulta la optimizacion de scheduling y prefetching.
- **Complejidad de entrenamiento.** Entrenar modelos MoE requiere balancear la carga entre expertos y evitar que algunos expertos "mueran" (dejen de ser seleccionados).

A pesar de estos trade-offs, MoE se ha convertido en la arquitectura dominante para modelos frontera. El 60%+ de los modelos frontera en 2025-2026 usan MoE. La razon es simple: es la forma mas practica de escalar la capacidad de un modelo sin escalar proporcionalmente el costo de inferencia.

---

## 12.7 Lo que viene: hardware emergente

### HBM4 y el futuro del ancho de banda

La siguiente generacion de High Bandwidth Memory (HBM4) promete ~2.8 TB/s por stack, casi el doble de HBM3. Esto ayudara, pero no resuelve el problema fundamental: la demanda de ancho de banda crece mas rapido que la oferta.

### Computacion in-memory: eliminar el movimiento de datos

Si el cuello de botella es mover datos de la memoria al procesador, la solucion radical es **no moverlos**. La computacion in-memory (CIM) realiza operaciones MAC (multiply-accumulate) directamente en los arrays de memoria, eliminando el cuello de botella de von Neumann [arXiv:2406.08413, 2024].

Las primeras implementaciones comerciales empiezan a aparecer, pero la tecnologia esta en etapas tempranas para LLMs.

### Computacion fotonica: procesar con luz

Startups como Lightmatter (valuacion de $4.4 mil millones en 2024) proponen usar fotones en lugar de electrones para las multiplicaciones de matrices. Ventajas teoricas: velocidad de la luz, casi cero calor. Estado actual: prometedor pero muy temprano para despliegue en produccion.

### Cerebras WSE-3: el enfoque radical

Cerebras tomo una decision opuesta a todo el mundo: en lugar de chips pequenos conectados con interconexiones lentas, fabricar un solo chip del tamano de un wafer completo. El WSE-3 tiene 4 billones de transistores, 900,000 nucleos y 21 PB/s de ancho de banda on-chip. Al integrar SRAM masiva directamente en el chip, elimina la latencia de DRAM para modelos que caben on-chip [Cerebras, 2024].

---

## 12.8 Implicaciones para la arquitectura de agentes

### Tabla de decision: donde correr tu agente

Los limites fisicos que hemos explorado tienen consecuencias directas para las decisiones de arquitectura:

```python
"""
Framework de decision para seleccion de infraestructura de agentes.
"""

from dataclasses import dataclass
from enum import Enum


class InfraTarget(Enum):
    LOCAL_DEVICE = "Dispositivo local (telefono/laptop)"
    EDGE_SERVER = "Servidor edge (oficina/on-premise)"
    CLOUD_GPU = "GPU en la nube (A100/H100)"
    CLOUD_API = "API de proveedor (OpenAI/Anthropic/Google)"


@dataclass
class AgentRequirements:
    """Requisitos del agente que determinan la infraestructura."""
    max_latency_ms: int
    privacy_critical: bool
    model_size_billions: float
    reasoning_depth: str  # "simple", "moderate", "deep"
    budget_per_query_usd: float
    internet_required: bool
    batch_volume_per_day: int


def recommend_infrastructure(reqs: AgentRequirements) -> dict:
    """Recomienda infraestructura basada en requisitos del agente."""
    recommendations = []

    # Caso 1: Privacidad critica -> local o edge
    if reqs.privacy_critical:
        if reqs.model_size_billions <= 4:
            recommendations.append({
                "target": InfraTarget.LOCAL_DEVICE,
                "model_suggestion": "Phi-4 mini 3.8B Q4 o Llama 3.2 3B Q4",
                "reason": "Privacidad critica + modelo pequeno = viable en dispositivo",
                "estimated_tokens_s": "15-30 tok/s en Apple M4",
            })
        else:
            recommendations.append({
                "target": InfraTarget.EDGE_SERVER,
                "model_suggestion": "Llama 3.1 70B Q4 en servidor con 48+ GB RAM",
                "reason": "Privacidad critica + modelo grande = servidor on-premise",
                "estimated_tokens_s": "20-40 tok/s con GPU dedicada",
            })

    # Caso 2: Latencia baja + volumen alto -> cloud GPU
    if reqs.max_latency_ms < 2000 and reqs.batch_volume_per_day > 10000:
        recommendations.append({
            "target": InfraTarget.CLOUD_GPU,
            "model_suggestion": "Modelo cuantizado en vLLM/TGI",
            "reason": "Alto volumen requiere GPUs dedicadas con batching",
            "estimated_tokens_s": "100-500 tok/s con batching",
        })

    # Caso 3: Razonamiento profundo -> API o cloud con modelo grande
    if reqs.reasoning_depth == "deep":
        recommendations.append({
            "target": InfraTarget.CLOUD_API,
            "model_suggestion": "Claude/GPT-4/DeepSeek-R1 via API",
            "reason": "Razonamiento profundo requiere modelos frontera",
            "estimated_tokens_s": "30-80 tok/s (limitado por proveedor)",
        })

    # Caso 4: Presupuesto muy limitado + volumen bajo
    if reqs.budget_per_query_usd < 0.001 and reqs.batch_volume_per_day < 100:
        recommendations.append({
            "target": InfraTarget.LOCAL_DEVICE,
            "model_suggestion": "Modelo 1-3B cuantizado Q4 via Ollama",
            "reason": "Costo cero por consulta despues de la inversion inicial",
            "estimated_tokens_s": "20-50 tok/s en laptop moderna",
        })

    return {
        "recommendations": recommendations,
        "key_tradeoff": (
            "Calidad vs Costo vs Privacidad vs Latencia. "
            "No puedes optimizar las cuatro a la vez."
        ),
    }
```

### Arquitectura hibrida: lo mejor de ambos mundos

La arquitectura que emerge como optima para la mayoria de los sistemas con agentes es **hibrida**: un modelo pequeno local para triage rapido y un modelo grande en la nube para tareas complejas.

```python
"""
Patron de agente hibrido: local para triage, cloud para complejidad.
"""

from abc import ABC, abstractmethod


class ModelBackend(ABC):
    """Interfaz para backends de modelo."""

    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int) -> str:
        ...

    @abstractmethod
    def estimated_cost_per_token(self) -> float:
        ...


class LocalModel(ModelBackend):
    """Modelo local cuantizado (Ollama/llama.cpp)."""

    def __init__(self, model_name: str = "phi4-mini:q4"):
        self.model_name = model_name

    async def generate(self, prompt: str, max_tokens: int) -> str:
        # Llamada a Ollama local
        # En produccion: httpx.AsyncClient -> localhost:11434
        return f"[respuesta de {self.model_name}]"

    def estimated_cost_per_token(self) -> float:
        return 0.0  # Sin costo variable


class CloudModel(ModelBackend):
    """Modelo cloud via API."""

    def __init__(self, provider: str = "anthropic", model: str = "claude-sonnet"):
        self.provider = provider
        self.model = model

    async def generate(self, prompt: str, max_tokens: int) -> str:
        # Llamada a API cloud
        return f"[respuesta de {self.provider}/{self.model}]"

    def estimated_cost_per_token(self) -> float:
        return 0.000003  # ~$3/M tokens


class HybridAgent:
    """Agente que decide dinamicamente entre modelo local y cloud.

    Usa el modelo local para clasificacion inicial y tareas simples.
    Escala al modelo cloud solo cuando la complejidad lo justifica.
    """

    def __init__(
        self,
        local: LocalModel,
        cloud: CloudModel,
        complexity_threshold: float = 0.7,
    ):
        self.local = local
        self.cloud = cloud
        self.complexity_threshold = complexity_threshold

    async def classify_complexity(self, task: str) -> float:
        """Usa el modelo local para estimar la complejidad de la tarea.

        Returns:
            Score de 0.0 (trivial) a 1.0 (requiere razonamiento profundo)
        """
        classification_prompt = f"""Clasifica la complejidad de esta tarea
        en una escala de 0.0 a 1.0:
        - 0.0-0.3: pregunta factual simple, lookup
        - 0.3-0.7: analisis moderado, sintesis de informacion
        - 0.7-1.0: razonamiento complejo, planificacion multi-paso

        Tarea: {task}
        Responde SOLO con el numero."""

        result = await self.local.generate(classification_prompt, max_tokens=10)
        try:
            return float(result.strip())
        except ValueError:
            return 0.5  # default: complejidad media

    async def execute(self, task: str) -> dict:
        """Ejecuta la tarea seleccionando el backend apropiado."""
        complexity = await self.classify_complexity(task)

        if complexity < self.complexity_threshold:
            backend = self.local
            backend_name = "local"
        else:
            backend = self.cloud
            backend_name = "cloud"

        result = await backend.generate(task, max_tokens=2048)

        return {
            "result": result,
            "backend_used": backend_name,
            "complexity_score": complexity,
            "estimated_cost": backend.estimated_cost_per_token() * len(result),
        }
```

Este patron reduce costos drasticamente: si el 70% de las consultas son simples y se resuelven localmente, tu costo promedio cae ~70%.

---

## Takeaway del capitulo

Los limites fisicos del hardware no son problemas de ingenieria de software que puedas resolver con una mejor abstraccion. Son restricciones fundamentales impuestas por la fisica:

- **La pared de memoria** es el cuello de botella dominante para la inferencia de LLMs. La velocidad de generacion de tokens esta limitada por el ancho de banda de memoria, no por la capacidad de computo.

- **La cuantizacion** ataca directamente este cuello de botella: reducir la precision de los pesos reduce la cantidad de datos que deben transferirse. INT4 (GPTQ, AWQ, GGUF Q4_K_M) ofrece la mejor relacion calidad/compresion para la mayoria de los casos.

- **Las NPUs** son poderosas para la fase de prefill pero estan subutilizadas durante la decodificacion autoregresiva, que es donde se pasa la mayor parte del tiempo de inferencia.

- **MoE** es la respuesta arquitectonica a la pared de memoria: activa solo una fraccion de los parametros por token, reduciendo drasticamente los requisitos de ancho de banda.

- **La ley de Amdahl** limita la aceleracion maxima de cualquier optimizacion individual. La parte secuencial de la generacion de tokens impone un techo que ningun hardware puede superar.

- Para **agentes en produccion**, la arquitectura hibrida (modelo pequeno local + modelo grande en cloud) es la respuesta pragmatica a estos limites.

Entiende los limites fisicos para tomar mejores decisiones de diseno. No luches contra la fisica; disenala a tu favor.

---

## Referencias

- Shalf, J. "The future of computing beyond Moore's Law." *Philosophical Transactions of the Royal Society A*, 378(2166), 2020.
- Wulf, W. A. y McKee, S. A. "Hitting the Memory Wall: Implications of the Obvious." *ACM SIGARCH*, 23(1), 1995.
- Gholami, A., et al. "AI and Memory Wall." *arXiv:2403.14123*, 2024.
- Yuan, Z., et al. "LLM Inference Unveiled: Survey and Roofline Model Insights." *arXiv:2402.16363*, 2024.
- Gholami, A., et al. "A Survey of Quantization Methods for Efficient Neural Network Inference." *arXiv:2103.13630*, 2021.
- Frantar, E., et al. "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers." *ICLR*, 2023.
- Lin, J., et al. "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration." *MLSys 2024 Best Paper*, 2024.
- Xiao, G., et al. "SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models." *ICML*, 2023.
- Dettmers, T., et al. "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale." *arXiv:2208.07339*, 2022.
- Ma, S., et al. "The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits." *arXiv:2402.17764*, 2024.
- Gerganov, G. et al. "llama.cpp: LLM Inference in C/C++." github.com/ggml-org/llama.cpp, 2023.
- Xu, D., et al. "Fast On-device LLM Inference with NPUs." *ASPLOS*, 2025.
- The Chip Letter. "Qualcomm's Hexagon AI Accelerators." 2024.
- DeepSeek-AI. "DeepSeek-V3 Technical Report." *arXiv:2412.19437*, 2024.
- Hoffmann, J., et al. "Training Compute-Optimal Large Language Models." *NeurIPS*, 2022.
- MIT Technology Review. "We did the math on AI's energy footprint." 2025.
- Google. "Measuring the environmental impact of delivering AI at Google Scale." *arXiv:2508.15734*, 2025.
- Introl Blog. "Inference-Time Scaling." 2025.
- Cerebras Systems. "WSE-3: World's Fastest AI Chip." 2024.
- TrendForce. "Memory Wall Bottleneck: AI Compute Sparks Memory Supercycle." 2024.
- Semiconductor Engineering. "Amdahl Limits On AI." 2024.
- Hennessy, J. L. y Patterson, D. A. *Computer Architecture: A Quantitative Approach*. 6ta edicion.
