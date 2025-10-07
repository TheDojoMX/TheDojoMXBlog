---
title: "HPC con GPU (2/22): Setup sin dolor — drivers, CUDA Toolkit y verificación"
date: 2025-01-22
author: Héctor Iván Patricio Moreno
comments: true
excerpt: "Instala el entorno completo para HPC con GPU: drivers NVIDIA, CUDA Toolkit, PyTorch con CUDA y Triton. Incluye troubleshooting para problemas comunes."
header:
  overlay_image: #TODO
  teaser: #TODO
  overlay_filter: rgba(0, 0, 0, 0.5)
categories:
  - GPU
  - HPC
  - CUDA
tags:
  - setup
  - CUDA
  - PyTorch
  - Triton
  - drivers
---

## Objetivo

Dejar tu entorno **listo para desarrollar con GPU**: drivers NVIDIA actualizados, CUDA Toolkit instalado, PyTorch con soporte CUDA y Triton funcionando. Al final, generarás un reporte de capacidades de tu GPU.

---

## Requisitos previos

### Hardware
- **GPU NVIDIA** con arquitectura Kepler o superior (GTX 600 series+, Tesla K40+, RTX cualquier generación)
- **8+ GB de RAM** del sistema
- **20+ GB de espacio libre** en disco

### Software
- **Linux** (Ubuntu 20.04+, CentOS 7+), **Windows 10/11**, o **macOS con GPU externa** (soporte limitado)
- Python 3.8+
- Permisos de administrador para instalar drivers

---

## Paso 1: Verificar GPU disponible

### Linux/Windows
```bash
lspci | grep -i nvidia  # Linux
# o
wmic path win32_VideoController get name  # Windows (PowerShell)
```

Debes ver algo como:
```
01:00.0 VGA compatible controller: NVIDIA Corporation GA102 [GeForce RTX 3080]
```

### Sin GPU física: usar Google Colab
Si no tienes GPU:
1. Ve a [Google Colab](https://colab.research.google.com)
2. Runtime → Change runtime type → Hardware accelerator: **GPU**
3. Verifica con `!nvidia-smi`

El resto del tutorial asume GPU local. Para Colab, salta a **Paso 4**.

---

## Paso 2: Instalar drivers NVIDIA

### Linux (Ubuntu/Debian)
```bash
# Agregar repositorio oficial
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Detectar driver recomendado
ubuntu-drivers devices

# Instalar (ejemplo: driver 535)
sudo apt install nvidia-driver-535

# Reiniciar
sudo reboot
```

### Windows
1. Descargar desde [NVIDIA Driver Downloads](https://www.nvidia.com/Download/index.aspx)
2. Seleccionar tu GPU
3. Instalar con opciones por defecto
4. Reiniciar

### Verificar instalación
```bash
nvidia-smi
```

**Salida esperada**:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03   Driver Version: 535.129.03   CUDA Version: 12.2    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0  On |                  N/A |
```

**Puntos clave**:
- `Driver Version`: número del driver instalado
- `CUDA Version`: versión CUDA soportada por el driver (NO es CUDA Toolkit instalado)

---

## Paso 3: Instalar CUDA Toolkit

### ¿Por qué necesitas CUDA Toolkit si el driver ya incluye CUDA?

El **driver** incluye runtime básico. El **Toolkit** añade:
- `nvcc` (compilador CUDA C++)
- Librerías de desarrollo (cuBLAS, cuDNN)
- Herramientas de debugging (cuda-gdb, compute-sanitizer)

### Instalación

#### Linux (Ubuntu)
```bash
# Descargar instalador desde https://developer.nvidia.com/cuda-downloads
wget https://developer.download.nvidia.com/compute/cuda/12.3.0/local_installers/cuda_12.3.0_545.23.06_linux.run

# Ejecutar (NO instalar driver si ya lo tienes)
sudo sh cuda_12.3.0_545.23.06_linux.run

# Durante instalación: desmarcar "Driver" si ya instalaste en Paso 2
# Marcar: CUDA Toolkit, samples, documentation
```

#### Windows
1. Descargar desde [CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive)
2. Ejecutar instalador
3. Seleccionar "Custom" y desmarcar driver si ya está actualizado

### Configurar PATH

#### Linux (agregar a `~/.bashrc`)
```bash
export PATH=/usr/local/cuda-12.3/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.3/lib64:$LD_LIBRARY_PATH
```

Recargar:
```bash
source ~/.bashrc
```

#### Windows
El instalador configura PATH automáticamente. Verifica en PowerShell:
```powershell
nvcc --version
```

### Verificar CUDA Toolkit
```bash
nvcc --version
```

**Salida esperada**:
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Tue_Sep_19_21:08:59_PDT_2023
Cuda compilation tools, release 12.3, V12.3.52
```

---

## Paso 4: Instalar PyTorch con soporte CUDA

### Crear entorno virtual (recomendado)
```bash
python3 -m venv ~/venv-gpu
source ~/venv-gpu/bin/activate  # Linux/Mac
# o
~/venv-gpu\Scripts\activate  # Windows
```

### Instalar PyTorch
Visita [PyTorch Get Started](https://pytorch.org/get-started/locally/) y selecciona tu configuración. Ejemplo para CUDA 12.1:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

⚠️ **Importante**: la versión CUDA de PyTorch debe ser **compatible** (no necesariamente idéntica) con tu driver. Ejemplo:
- Driver soporta CUDA 12.3 → puedes usar PyTorch con CUDA 12.1, 11.8, etc.
- Driver soporta CUDA 11.6 → NO uses PyTorch con CUDA 12.x

### Verificar PyTorch + CUDA
```python
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version (PyTorch): {torch.version.cuda}")
print(f"Device count: {torch.cuda.device_count()}")
print(f"Device name: {torch.cuda.get_device_name(0)}")
```

**Salida esperada**:
```
PyTorch version: 2.1.0+cu121
CUDA available: True
CUDA version (PyTorch): 12.1
Device count: 1
Device name: NVIDIA GeForce RTX 3080
```

Si `CUDA available: False`:
- Verifica que instalaste la versión **cu121** (no **cpu**)
- Reinstala con el comando correcto desde pytorch.org

---

## Paso 5: Instalar Triton

```bash
pip install triton
```

Verificar:
```python
import triton
print(f"Triton version: {triton.__version__}")
```

**Salida esperada**:
```
Triton version: 2.1.0
```

---

## Paso 6: Reporte de capacidades del dispositivo

Ejecuta este script y guarda la salida:

```python
# device_info.py
import torch

if not torch.cuda.is_available():
    print("⚠️  CUDA no disponible")
    exit(1)

device = torch.device('cuda:0')
props = torch.cuda.get_device_properties(device)

print("=== Reporte de GPU ===")
print(f"Nombre: {props.name}")
print(f"Compute Capability: {props.major}.{props.minor}")
print(f"Memoria total: {props.total_memory / 1e9:.2f} GB")
print(f"SMs (Streaming Multiprocessors): {props.multi_processor_count}")
print(f"Max threads por bloque: {props.max_threads_per_block}")
print(f"Max threads por SM: {props.max_threads_per_multi_processor}")
print(f"Warp size: {props.warp_size}")
print(f"Memoria compartida por bloque: {props.shared_memory_per_block / 1024:.1f} KB")
print(f"Registros por bloque: {props.regs_per_block}")

# Información de software
print("\n=== Software ===")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA (PyTorch): {torch.version.cuda}")
print(f"Driver CUDA: {torch.cuda.get_device_capability(device)}")

# Test rápido
x = torch.randn(1000, 1000, device=device)
y = torch.matmul(x, x)
print("\n✅ Matmul en GPU exitoso")
```

Ejecutar:
```bash
python device_info.py
```

**Ejemplo de salida**:
```
=== Reporte de GPU ===
Nombre: NVIDIA GeForce RTX 3080
Compute Capability: 8.6
Memoria total: 10.00 GB
SMs (Streaming Multiprocessors): 68
Max threads por bloque: 1024
Max threads por SM: 1536
Warp size: 32
Memoria compartida por bloque: 48.0 KB
Registros por bloque: 65536

=== Software ===
PyTorch: 2.1.0+cu121
CUDA (PyTorch): 12.1
Driver CUDA: (8, 6)

✅ Matmul en GPU exitoso
```

---

## Troubleshooting común

### Problema 1: `nvidia-smi` funciona pero PyTorch no ve GPU

**Causa**: versión CUDA de PyTorch incompatible con driver.

**Solución**:
1. Verifica versión CUDA del driver: `nvidia-smi` (esquina superior derecha)
2. Reinstala PyTorch con versión compatible desde [pytorch.org](https://pytorch.org)

---

### Problema 2: WSL2 en Windows no detecta GPU

**Causa**: WSL2 requiere drivers específicos.

**Solución**:
1. Actualiza Windows a 21H2+
2. Instala [NVIDIA CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)
3. **NO** instales drivers dentro de WSL, usa los de Windows

Verificar en WSL:
```bash
nvidia-smi
```

---

### Problema 3: CUDA out of memory al primer test

**Causa**: otra aplicación usa GPU (navegador, display manager).

**Solución**:
```python
# Limpiar caché antes de test
torch.cuda.empty_cache()
```

O reduce tamaño del tensor de prueba:
```python
x = torch.randn(100, 100, device=device)  # en vez de 1000x1000
```

---

### Problema 4: `nvcc` no se encuentra después de instalar CUDA Toolkit

**Causa**: PATH no configurado.

**Solución**: revisa **Paso 3** sobre configurar PATH. Verifica:
```bash
echo $PATH  # Linux
echo %PATH%  # Windows
```

Debe incluir `/usr/local/cuda-XX.X/bin`.

---

### Problema 5: Versiones CUDA/PyTorch incompatibles

**Regla general**:
- Driver CUDA ≥ versión PyTorch CUDA
- Driver CUDA 12.x soporta PyTorch con CUDA 11.x, 12.x
- Driver CUDA 11.x **NO** soporta PyTorch con CUDA 12.x

**Solución**: si tienes driver viejo, usa PyTorch con CUDA antigua:
```bash
# Para driver CUDA 11.6
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

## Entrega: reporte de tu entorno

Ejecuta `device_info.py` y **guarda la salida**. Necesitarás estos datos para:
- Calcular occupancy en posts futuros
- Configurar tamaños de bloque óptimos
- Entender límites de memoria compartida

**Acción**: crea un archivo `mi_gpu.txt` con la salida completa.

---

## Qué estudiar para escribir este artículo

### Fundamentos necesarios

1. **Drivers vs CUDA Runtime vs CUDA Toolkit**
   - Conceptos: diferencias entre componentes, compatibilidad de versiones
   - Recursos: [NVIDIA CUDA Installation Guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)

2. **Compute Capability**
   - Conceptos: arquitecturas GPU (Kepler, Pascal, Ampere, etc.), features por generación
   - Recursos: [CUDA Compute Capability](https://developer.nvidia.com/cuda-gpus)

3. **Gestión de entornos Python**
   - Conceptos: venv, conda, pip, dependencias
   - Recursos: documentación oficial Python

4. **Troubleshooting de hardware**
   - Conceptos: PCI, drivers de kernel, compatibilidad OS
   - Recursos: foros NVIDIA, Stack Overflow

### Lecturas recomendadas

- **NVIDIA CUDA Installation Guide**: guía oficial paso a paso
- **PyTorch Installation Docs**: matriz de compatibilidad CUDA/PyTorch
- **Triton Documentation**: requisitos y instalación
- **CUDA Toolkit Release Notes**: cambios entre versiones

### Práctica previa

- Experiencia instalando software de línea de comandos
- Conocimientos básicos de PATH y variables de entorno
- Haber usado pip/conda antes
- (Opcional) Familiaridad con compiladores (gcc, clang)

### Problemas comunes que debes conocer

1. **Incompatibilidad driver/toolkit**: documentar matriz de compatibilidad
2. **WSL2 peculiaridades**: drivers híbridos Windows/Linux
3. **Múltiples versiones CUDA**: cómo cambiar entre ellas
4. **Fallback a CPU**: cómo detectar y qué hacer

### Recursos para troubleshooting

- [NVIDIA Developer Forums](https://forums.developer.nvidia.com/)
- [PyTorch GitHub Issues](https://github.com/pytorch/pytorch/issues)
- [CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/)

### Tiempo estimado de estudio

- **Si nunca instalaste CUDA**: 6-8 horas (leer guías + intentar instalación + troubleshooting)
- **Si ya usas PyTorch con GPU**: 2-3 horas (documentar edge cases + WSL2 + versiones)
- **Si administras servidores con GPU**: 1-2 horas (recopilar casos comunes de usuarios)

### Validación práctica

Antes de escribir, debes haber:
- ✅ Instalado CUDA Toolkit en al menos 2 sistemas diferentes (Linux + Windows/WSL2)
- ✅ Resuelto al menos 3 problemas comunes de instalación
- ✅ Verificado compatibilidad con 2+ versiones de PyTorch
- ✅ Documentado output de `nvidia-smi`, `nvcc`, y `torch.cuda` en diferentes configuraciones

---

## Siguiente

En el **próximo artículo** (3/22): aprenderás a mover tensores entre CPU y GPU con PyTorch, medir overhead de transferencia vs cómputo, y hacer tu primer benchmark CPU vs GPU.

