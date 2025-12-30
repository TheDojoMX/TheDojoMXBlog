---
title: "HPC con GPU (3/22): Tensores en GPU con PyTorch — lo esencial"
date: 2025-01-29
author: "Héctor Iván Patricio Moreno"
tags: ['-', 'PyTorch']
description: "Aprende a mover datos entre CPU y GPU, entiende dtypes y pinned memory, y mide cuándo la transferencia domina sobre el cómputo."
featuredImage: "#TODO"
draft: true
---

## Objetivo

Dominar el **movimiento de tensores entre CPU y GPU** en PyTorch, entender el impacto de dtypes (FP32, FP16, INT8), usar pinned memory para transferencias rápidas, y medir cuándo el overhead de transferencia anula las ganancias de cómputo en GPU.

---

## Anatomía de un tensor en PyTorch

### CPU vs GPU: ¿dónde viven los datos?

```python
import torch

# Tensor en CPU (por defecto)
x_cpu = torch.randn(1000, 1000)
print(x_cpu.device)  # cpu

# Tensor en GPU
x_gpu = torch.randn(1000, 1000, device='cuda')
print(x_gpu.device)  # cuda:0

# Mover CPU → GPU
y_gpu = x_cpu.to('cuda')

# Mover GPU → CPU
z_cpu = x_gpu.to('cpu')
```

**Regla de oro**: PyTorch **NO** mueve datos automáticamente. Si mezclas tensores de CPU y GPU en una operación, obtienes error:

```python
x_cpu = torch.randn(10)
x_gpu = torch.randn(10, device='cuda')

# ❌ RuntimeError: Expected all tensors to be on the same device
result = x_cpu + x_gpu
```

---

## dtypes: precisión vs memoria vs velocidad

### Tipos comunes

| dtype | Bits | Rango | Uso típico |
|-------|------|-------|------------|
| `torch.float32` (FP32) | 32 | ±3.4e38, ~7 dígitos | Default, máxima precisión |
| `torch.float16` (FP16) | 16 | ±6.5e4, ~3 dígitos | Mixed precision, Tensor Cores |
| `torch.bfloat16` (BF16) | 16 | ±3.4e38, ~3 dígitos | Training estable, mejor rango que FP16 |
| `torch.int8` | 8 | -128 a 127 | Cuantización, inferencia |

### Crear tensores con dtype específico

```python
# FP32 (default)
x = torch.randn(1000, 1000)

# FP16
x_fp16 = torch.randn(1000, 1000, dtype=torch.float16, device='cuda')

# Convertir dtype
x_gpu = x.to(device='cuda', dtype=torch.float16)
```

### Impacto en memoria

```python
import torch

def print_memory(tensor, name):
    bytes_used = tensor.element_size() * tensor.nelement()
    print(f"{name}: {bytes_used / 1e6:.2f} MB")

x_fp32 = torch.randn(1000, 1000, device='cuda')
x_fp16 = x_fp32.half()  # conversión a FP16

print_memory(x_fp32, "FP32")  # 4.00 MB
print_memory(x_fp16, "FP16")  # 2.00 MB
```

**Lección**: FP16 usa **mitad de memoria** que FP32, crucial para modelos grandes.

---

## Transferencia CPU ↔ GPU: midiendo overhead

### Benchmark básico

```python
import torch
import time

def benchmark_transfer(size, device='cuda', dtype=torch.float32):
    # Crear tensor en CPU
    x_cpu = torch.randn(size, size, dtype=dtype)

    # Medir CPU → GPU
    start = time.perf_counter()
    x_gpu = x_cpu.to(device)
    torch.cuda.synchronize()  # ⚠️ IMPORTANTE: esperar a que termine
    transfer_time = time.perf_counter() - start

    # Calcular throughput
    bytes_transferred = x_cpu.element_size() * x_cpu.nelement()
    throughput_gb_s = (bytes_transferred / 1e9) / transfer_time

    print(f"Size: {size}x{size}, dtype: {dtype}")
    print(f"Transfer time: {transfer_time*1000:.2f} ms")
    print(f"Throughput: {throughput_gb_s:.2f} GB/s")
    print(f"Data size: {bytes_transferred / 1e6:.2f} MB\n")

    return x_gpu

# Probar diferentes tamaños
for size in [100, 1000, 5000]:
    benchmark_transfer(size, dtype=torch.float32)
```

**Salida típica (PCIe 3.0 x16)**:
```
Size: 100x100, dtype: torch.float32
Transfer time: 0.15 ms
Throughput: 2.67 GB/s
Data size: 0.04 MB

Size: 1000x1000, dtype: torch.float32
Transfer time: 0.51 ms
Throughput: 7.84 GB/s
Data size: 4.00 MB

Size: 5000x5000, dtype: torch.float32
Transfer time: 11.23 ms
Throughput: 8.91 GB/s
Data size: 100.00 MB
```

**Observaciones**:
- Throughput **aumenta** con tamaños grandes (latencia de lanzamiento amortizada)
- PCIe 3.0 x16 teórico: ~16 GB/s; real: ~8-12 GB/s
- Transferencias pequeñas: **latencia domina** sobre bandwidth

---

## Pinned memory: acelerando transferencias

### ¿Qué es pinned memory?

Por defecto, memoria CPU es **pageable** (puede moverse a swap). La GPU no puede acceder directamente a memoria pageable, requiere copia intermedia.

**Pinned (page-locked) memory**: memoria CPU fija en RAM física, la GPU puede acceder vía DMA (Direct Memory Access).

### Uso en PyTorch

```python
import torch
import time

def compare_pinned_vs_normal(size=5000):
    # Normal (pageable)
    x_normal = torch.randn(size, size)

    # Pinned
    x_pinned = torch.randn(size, size).pin_memory()

    # Benchmark normal
    start = time.perf_counter()
    x_gpu_normal = x_normal.to('cuda')
    torch.cuda.synchronize()
    time_normal = time.perf_counter() - start

    # Benchmark pinned
    start = time.perf_counter()
    x_gpu_pinned = x_pinned.to('cuda', non_blocking=True)
    torch.cuda.synchronize()
    time_pinned = time.perf_counter() - start

    print(f"Normal: {time_normal*1000:.2f} ms")
    print(f"Pinned: {time_pinned*1000:.2f} ms")
    print(f"Speedup: {time_normal/time_pinned:.2f}x")

compare_pinned_vs_normal()
```

**Salida esperada**:
```
Normal: 11.45 ms
Pinned: 7.32 ms
Speedup: 1.56x
```

**Trade-off**: pinned memory es **recurso limitado** (típicamente <10% de RAM total). Úsala solo para buffers de transferencia frecuente.

---

## Transferencia vs cómputo: ¿cuándo vale la pena GPU?

### Benchmark CPU vs GPU con transferencia incluida

```python
import torch
import time

def benchmark_cpu_vs_gpu(size=1000, include_transfer=True):
    x = torch.randn(size, size)

    # CPU
    start = time.perf_counter()
    y_cpu = torch.matmul(x, x)
    time_cpu = time.perf_counter() - start

    # GPU (con transferencia)
    start = time.perf_counter()
    if include_transfer:
        x_gpu = x.to('cuda')
    else:
        x_gpu = torch.randn(size, size, device='cuda')

    y_gpu = torch.matmul(x_gpu, x_gpu)
    torch.cuda.synchronize()
    time_gpu = time.perf_counter() - start

    if include_transfer:
        # Transferir resultado de vuelta
        y_cpu_back = y_gpu.to('cpu')

    print(f"Size: {size}x{size}")
    print(f"CPU time: {time_cpu*1000:.2f} ms")
    print(f"GPU time (con transfer): {time_gpu*1000:.2f} ms")
    print(f"Speedup: {time_cpu/time_gpu:.2f}x")

    # FLOPS
    flops = 2 * size**3  # matmul: 2n³ ops
    gflops_cpu = flops / time_cpu / 1e9
    gflops_gpu = flops / time_gpu / 1e9
    print(f"CPU: {gflops_cpu:.2f} GFLOPS")
    print(f"GPU: {gflops_gpu:.2f} GFLOPS\n")

# Diferentes tamaños
for size in [100, 500, 1000, 5000]:
    benchmark_cpu_vs_gpu(size, include_transfer=True)
```

**Salida típica (RTX 3080)**:
```
Size: 100x100
CPU time: 0.08 ms
GPU time (con transfer): 0.42 ms
Speedup: 0.19x  # ⚠️ CPU gana!

Size: 500x500
CPU time: 2.15 ms
GPU time (con transfer): 1.87 ms
Speedup: 1.15x

Size: 1000x1000
CPU time: 12.34 ms
GPU time (con transfer): 2.56 ms
Speedup: 4.82x

Size: 5000x5000
CPU time: 1834.12 ms
GPU time (con transfer): 78.45 ms
Speedup: 23.38x
```

**Lección clave**: para matrices **pequeñas (<500×500)**, overhead de transferencia anula beneficio de GPU.

---

## Estrategias para minimizar transferencias

### 1. Mantener datos en GPU tanto como sea posible

❌ **Malo**:
```python
for i in range(100):
    x_cpu = torch.randn(1000, 1000)
    x_gpu = x_cpu.to('cuda')
    y_gpu = some_operation(x_gpu)
    y_cpu = y_gpu.to('cpu')  # Transferencia innecesaria
    process(y_cpu)
```

✅ **Bueno**:
```python
for i in range(100):
    x_gpu = torch.randn(1000, 1000, device='cuda')
    y_gpu = some_operation(x_gpu)
# Solo transferir al final si necesitas en CPU
results_cpu = [y.to('cpu') for y in all_results_gpu]
```

### 2. Batch processing

❌ **Malo** (transferencia por elemento):
```python
for img in images:  # 1000 imágenes
    img_gpu = img.to('cuda')
    result = model(img_gpu)
```

✅ **Bueno** (batch):
```python
batch = torch.stack(images).to('cuda')  # Una transferencia
results = model(batch)
```

### 3. DataLoader con `pin_memory=True`

```python
from torch.utils.data import DataLoader

# Para training loops
dataloader = DataLoader(
    dataset,
    batch_size=32,
    pin_memory=True,  # Acelera transferencias
    num_workers=4
)

for batch in dataloader:
    inputs = batch.to('cuda', non_blocking=True)
    # ...
```

---

## Práctica guiada: micro-benchmark elementwise

**Objetivo**: medir cuándo GPU supera a CPU en operaciones simples.

```python
import torch
import time

def elementwise_benchmark(size, operation='add'):
    x = torch.randn(size)
    y = torch.randn(size)

    # CPU
    start = time.perf_counter()
    if operation == 'add':
        z_cpu = x + y
    elif operation == 'mul':
        z_cpu = x * y
    elif operation == 'exp':
        z_cpu = torch.exp(x)
    time_cpu = time.perf_counter() - start

    # GPU (con transferencia)
    start = time.perf_counter()
    x_gpu = x.to('cuda')
    y_gpu = y.to('cuda')
    if operation == 'add':
        z_gpu = x_gpu + y_gpu
    elif operation == 'mul':
        z_gpu = x_gpu * y_gpu
    elif operation == 'exp':
        z_gpu = torch.exp(x_gpu)
    torch.cuda.synchronize()
    time_gpu = time.perf_counter() - start

    print(f"{operation.upper()}, size={size:>10}: CPU {time_cpu*1e6:>8.2f} μs | GPU {time_gpu*1e6:>8.2f} μs | Speedup: {time_cpu/time_gpu:>5.2f}x")

# Probar
for op in ['add', 'mul', 'exp']:
    print(f"\n=== {op.upper()} ===")
    for size in [100, 1000, 10000, 100000, 1000000]:
        elementwise_benchmark(size, op)
```

**Ejercicio**: ejecuta este script y responde:
1. ¿A partir de qué tamaño GPU supera a CPU en cada operación?
2. ¿Qué operación se beneficia más de GPU?
3. ¿Cambiaría si **no** incluyes transferencias (datos ya en GPU)?

---

## Pitfalls comunes

### 1. Olvidar `torch.cuda.synchronize()`

```python
# ❌ INCORRECTO: tiempo no incluye ejecución real
start = time.perf_counter()
y = torch.matmul(x_gpu, x_gpu)
end = time.perf_counter()  # Kernel puede no haber terminado

# ✅ CORRECTO
start = time.perf_counter()
y = torch.matmul(x_gpu, x_gpu)
torch.cuda.synchronize()  # Espera a que termine
end = time.perf_counter()
```

### 2. Comparar CPU single-threaded vs GPU

PyTorch usa MKL/OpenBLAS multi-threaded en CPU. Para benchmark justo:
```python
# Limitar threads CPU
torch.set_num_threads(1)
```

### 3. No calentar GPU antes de benchmark

Primera ejecución incluye tiempo de inicialización:
```python
# Warmup
_ = torch.matmul(x_gpu, x_gpu)
torch.cuda.synchronize()

# Ahora sí benchmark
start = time.perf_counter()
# ...
```

---

## Entrega: comparativa CPU vs GPU en tu hardware

**Acción**: ejecuta `elementwise_benchmark` con tus datos y crea una tabla:

| Operación | Tamaño mínimo para speedup >2× | Speedup a 1M elementos |
|-----------|--------------------------------|------------------------|
| ADD | | |
| MUL | | |
| EXP | | |

**Preguntas**:
1. ¿Transferencias dominan en qué porcentaje de casos?
2. Si tus datos típicos son <1000 elementos, ¿vale la pena GPU?

---

## Qué estudiar para escribir este artículo

### Fundamentos necesarios

1. **Modelo de memoria CPU vs GPU**
   - Conceptos: memoria unificada vs separada, latencia PCIe, bandwidth
   - Recursos: CUDA Programming Guide (Cap. 3: Programming Interface)

2. **Tipos de datos numéricos**
   - Conceptos: FP32, FP16, BF16, INT8; precisión vs rango; denormalized numbers
   - Recursos: IEEE 754 standard (resumen), documentación PyTorch dtypes

3. **Pinned memory y DMA**
   - Conceptos: page-locked memory, Direct Memory Access, copy engines
   - Recursos: CUDA Best Practices Guide (sección Memory Optimizations)

4. **Benchmarking correcto en GPU**
   - Conceptos: async execution, synchronization, warmup, amortización de latencia
   - Recursos: PyTorch Performance Tuning Guide

### Lecturas recomendadas

- **CUDA C Programming Guide**: Capítulo 3 (Memory), Capítulo 5 (Performance)
- **PyTorch Documentation**:
  - [Tensor Attributes](https://pytorch.org/docs/stable/tensor_attributes.html)
  - [CUDA Semantics](https://pytorch.org/docs/stable/notes/cuda.html)
- **NVIDIA CUDA Best Practices**: sección 9 (Memory Optimizations)

### Práctica previa

1. **Benchmarking básico**
   - Usar `time.perf_counter()`, `timeit`, entender varianza
   - Conocer warmup y cómo evitar optimizaciones del compilador

2. **PyTorch fundamentals**
   - Crear tensores, operaciones básicas (matmul, elementwise)
   - DataLoader y transforms

3. **Análisis de transferencias**
   - Calcular throughput (bytes/segundo)
   - Entender latencia vs bandwidth

### Experimentos previos necesarios

Antes de escribir, debes haber:
- ✅ Medido transferencia CPU→GPU en tu hardware con diferentes tamaños
- ✅ Comparado pinned vs normal memory
- ✅ Reproducido el "break-even point" donde GPU supera CPU (con transferencias)
- ✅ Validado que `torch.cuda.synchronize()` afecta tiempos medidos

### Conceptos avanzados (opcional para mencionar)

- **Unified Memory (CUDA Managed Memory)**: ventajas/desventajas
- **GPUDirect**: transferencias GPU↔GPU sin pasar por CPU
- **Streams**: overlapping de compute y transferencias (tema del post 15)

### Tiempo estimado de estudio

- **Si eres nuevo en PyTorch**: 8-10 horas (tutoriales + experimentar con tensores + benchmarks)
- **Si usas PyTorch pero no optimizas**: 4-6 horas (profundizar en memoria + pinned + medir overhead)
- **Si ya optimizas modelos**: 2-3 horas (documentar edge cases + crear ejemplos didácticos)

### Recursos de validación

- Reproducir benchmarks de documentación oficial PyTorch
- Comparar tus mediciones con especificaciones de tu GPU (PCIe version, bandwidth teórico)
- Validar que speedups observados coinciden con literatura (papers de optimización)

---

## Siguiente

En el **próximo artículo** (4/22): escribirás tu primer kernel en **Triton** para suma de vectores. Aprenderás sobre bloques, grids y medirás speedup vs PyTorch nativo.

