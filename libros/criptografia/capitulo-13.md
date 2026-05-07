# Capitulo 13: Protocolos y el mundo real -- como encaja todo

> "Las primitivas son los ladrillos. Los protocolos son los edificios. Y un edificio mal disenado se derrumba sin importar la calidad de sus ladrillos."

---

A lo largo de doce capitulos aprendiste a usar cada primitiva criptografica por separado: funciones hash para integridad, cifrados simetricos para confidencialidad, criptografia asimetrica para intercambio de llaves y firmas digitales, MACs para autenticacion, y algoritmos post-cuanticos para sobrevivir al futuro. Pero en el mundo real, ninguna primitiva trabaja sola.

Cuando abres tu navegador y visitas un sitio web con HTTPS, en menos de 100 milisegundos ocurre una coreografia precisa: tu navegador y el servidor negocian un intercambio de llaves efimero (capitulo 9), derivan llaves de sesion con HKDF (capitulo 5), cifran todo el trafico con AES-GCM o ChaCha20-Poly1305 (capitulos 7 y 8), y autentican cada paquete con un MAC integrado (capitulo 10). Un solo paso mal implementado y toda la seguridad se desmorona.

Este capitulo cierra el arco del libro conectando todas las piezas. Veremos como TLS 1.3 usa cada primitiva que estudiaste, como el protocolo Signal lleva el cifrado extremo a extremo a la mensajeria, y que tecnologias criptograficas emergentes estan transformando lo que es posible. Terminaremos con un principio de diseno que puede salvarte de la obsolescencia: la agilidad criptografica.

---

## 13.1 De primitivas a protocolos: por que necesitas algo mas

### 13.1.1 El patron fundamental del cifrado hibrido

En el capitulo 9 vimos que la criptografia asimetrica resuelve el problema de distribucion de llaves, pero es demasiado lenta para cifrar datos en volumen. La criptografia simetrica es rapida, pero requiere que ambas partes tengan la misma llave. La solucion, que ya conoces, es el **cifrado hibrido**:

```
1. Intercambio de llaves (asimetrico): acordar un secreto compartido
   -> X25519, ECDH, o ML-KEM-768

2. Derivacion de llave (KDF): convertir el secreto en llave(s) de sesion
   -> HKDF-SHA256

3. Cifrado de datos (simetrico + autenticado): proteger el trafico real
   -> AES-256-GCM o ChaCha20-Poly1305

4. Autenticacion del servidor (firma digital): probar identidad
   -> ECDSA, Ed25519, o ML-DSA-65
```

Este patron aparece en TLS, SSH, WireGuard, Signal y practicamente todo protocolo criptografico moderno. Las primitivas cambian, pero la estructura se repite.

### 13.1.2 Las suites criptograficas

Un **cipher suite** es una combinacion especifica de algoritmos que un protocolo usa para cada paso. En TLS 1.3, una suite se ve asi:

```
TLS_AES_256_GCM_SHA384

TLS     -> Protocolo
AES_256 -> Cifrado simetrico (256 bits)
GCM     -> Modo de operacion (autenticado)
SHA384  -> Funcion hash para derivacion de llaves (HKDF)
```

TLS 1.3 solo permite cinco cipher suites, todas seguras. Compara esto con TLS 1.2, que permitia mas de 300 combinaciones, muchas de ellas inseguras (RC4, 3DES, MD5, modos CBC sin autenticacion). La reduccion drastica fue una decision de diseno deliberada: menos opciones, menos errores.

Las cinco suites de TLS 1.3 son:

| Suite | Cifrado | Hash |
|-------|---------|------|
| TLS_AES_128_GCM_SHA256 | AES-128-GCM | SHA-256 |
| TLS_AES_256_GCM_SHA384 | AES-256-GCM | SHA-384 |
| TLS_CHACHA20_POLY1305_SHA256 | ChaCha20-Poly1305 | SHA-256 |
| TLS_AES_128_CCM_SHA256 | AES-128-CCM | SHA-256 |
| TLS_AES_128_CCM_8_SHA256 | AES-128-CCM (tag 8B) | SHA-256 |

El intercambio de llaves se negocia por separado, usando grupos como X25519, P-256, o el hibrido post-cuantico X25519MLKEM768 que vimos en el capitulo 12.

### 13.1.3 Por que las primitivas solas no son suficientes

Imagina que decides "proteger" la comunicacion entre tu cliente y tu servidor usando las primitivas correctas pero sin un protocolo bien disenado:

1. Generas un par de llaves RSA en el servidor.
2. El cliente cifra una llave AES con la llave publica RSA.
3. Ambos usan esa llave AES para cifrar mensajes.

Parece razonable, pero este esquema tiene problemas graves:

- **Sin forward secrecy.** Si alguien roba la llave privada RSA manana, puede descifrar todo el trafico grabado desde el dia uno. Porque la llave AES se transporto con RSA, no se derivo de un intercambio efimero.

- **Sin autenticacion del cliente.** El servidor no sabe con quien habla. Un atacante de intermediario (MITM) puede presentar su propia llave publica al cliente, interceptar la llave AES, y reenviarla al servidor real.

- **Sin proteccion contra repeticion.** Un atacante puede grabar un mensaje cifrado valido y reenviarlo. Sin timestamps ni contadores, el servidor lo acepta como nuevo.

- **Sin negociacion de algoritmos.** Si manana necesitas cambiar de RSA a X25519, debes reescribir todo el protocolo.

Estos son exactamente los problemas que TLS resuelve. Veamos como.

---

## 13.2 TLS 1.3: como usa todo lo que aprendiste

TLS (Transport Layer Security) es el protocolo que protege la mayor parte del trafico en Internet. Cada vez que ves el candado en tu navegador, cada vez que tu aplicacion hace un request HTTPS, cada vez que tu API se comunica con otra, TLS esta trabajando.

TLS 1.3, definido en RFC 8446 [Rescorla, 2018], es la version actual del protocolo y representa una simplificacion radical respecto a TLS 1.2. Se elimino todo lo que era inseguro o innecesario: RSA para transporte de llaves, cifrados sin autenticacion, compresion, renegociacion, y docenas de cipher suites debiles.

### 13.2.1 El handshake TLS 1.3 paso a paso

El handshake es la fase donde el cliente y el servidor acuerdan los parametros criptograficos y establecen las llaves de sesion. En TLS 1.3, esto ocurre en **un solo round-trip** (1-RTT), contra dos round-trips en TLS 1.2.

```
HANDSHAKE TLS 1.3 (1-RTT)

Cliente                                         Servidor
   |                                               |
   |--- ClientHello -------------------------------->|
   |    - Versiones TLS soportadas                  |
   |    - Cipher suites soportadas                  |
   |    - Key shares (ej: X25519, X25519MLKEM768)   |
   |    - Extensiones (SNI, ALPN, etc.)             |
   |                                               |
   |<------------------------- ServerHello ---------|
   |    - Version TLS seleccionada (1.3)            |
   |    - Cipher suite seleccionada                 |
   |    - Key share del servidor                    |
   |                                               |
   |    [A partir de aqui, todo va cifrado]         |
   |                                               |
   |<---- {EncryptedExtensions} --------------------|
   |<---- {Certificate} ----------------------------|
   |<---- {CertificateVerify} ----------------------|
   |<---- {Finished} -------------------------------|
   |                                               |
   |--- {Finished} -------------------------------->|
   |                                               |
   |<========= Datos de aplicacion =========>      |
   |         (cifrados con AES-GCM o                |
   |          ChaCha20-Poly1305)                    |
```

Desglosemos cada paso y conectemoslo con lo que aprendiste:

**Paso 1: ClientHello**

El cliente envia un mensaje con:

- Las versiones de TLS que soporta.
- Las cipher suites que acepta (ej: TLS_AES_256_GCM_SHA384).
- Un **key share**: la parte publica de un intercambio de llaves efimero. El cliente "adivina" que grupo de intercambio preferira el servidor (por ejemplo, X25519) y envia su llave publica directamente. Esta es la optimizacion clave de TLS 1.3: en TLS 1.2, el cliente tenia que esperar a que el servidor eligiera el grupo antes de enviar su llave.
- Si el servidor soporta criptografia post-cuantica, el cliente puede enviar un key share hibrido X25519MLKEM768 (capitulo 12).

**Paso 2: ServerHello**

El servidor responde con:

- La version y cipher suite seleccionadas.
- Su propio key share para completar el intercambio de llaves.

En este punto, **ambas partes pueden calcular el secreto compartido**. Si usaron X25519, aplican la multiplicacion escalar de curvas elipticas (capitulo 9). Si usaron el modo hibrido, combinan los secretos de X25519 y ML-KEM-768 (capitulo 12).

**Paso 3: Derivacion de llaves con HKDF**

A partir del secreto compartido, TLS 1.3 usa HKDF (capitulo 5) para derivar multiples llaves:

```
secreto_compartido (de X25519 o hibrido)
    |
    v
HKDF-Extract (con sal derivada de los mensajes del handshake)
    |
    v
handshake_secret
    |
    +---> HKDF-Expand --> llave_cifrado_cliente_handshake
    +---> HKDF-Expand --> llave_cifrado_servidor_handshake
    +---> HKDF-Expand --> llave_iv_cliente_handshake
    +---> HKDF-Expand --> llave_iv_servidor_handshake
    |
    v
(Despues de Finished)
    |
    v
master_secret
    |
    +---> HKDF-Expand --> llave_cifrado_cliente_app
    +---> HKDF-Expand --> llave_cifrado_servidor_app
```

Nota como se derivan **llaves separadas** para cada direccion (cliente -> servidor y servidor -> cliente) y para cada fase (handshake y datos de aplicacion). Este nivel de separacion de llaves es lo que hace robusto al protocolo: comprometer una llave no compromete las demas.

**Paso 4: Autenticacion del servidor**

El servidor envia su certificado X.509 (que contiene su llave publica, firmada por una autoridad certificadora) y un mensaje **CertificateVerify** que firma el transcript completo del handshake con su llave privada. Esto prueba dos cosas: que el servidor posee la llave privada correspondiente al certificado, y que nadie altero los mensajes del handshake en transito.

La firma usa ECDSA (P-256), Ed25519, o RSA-PSS (capitulo 9). En el futuro, sera ML-DSA-65 (capitulo 12).

**Paso 5: Finished**

Tanto el servidor como el cliente envian un mensaje Finished que contiene un HMAC (capitulo 10) del transcript completo del handshake, usando la llave derivada con HKDF. Esto confirma que ambas partes calcularon las mismas llaves y que ningun atacante intermediario altero los mensajes.

**Paso 6: Datos de aplicacion**

A partir de aqui, todo el trafico se cifra con AES-256-GCM o ChaCha20-Poly1305 (capitulos 7 y 8), usando las llaves de aplicacion derivadas con HKDF. Cada registro TLS se cifra y autentica individualmente, con un numero de secuencia que previene ataques de reordenamiento y repeticion.

### 13.2.2 Mapa de primitivas en TLS 1.3

Aqui esta el mapa completo de primitivas que TLS 1.3 usa, conectadas con los capitulos donde las estudiaste:

```
PRIMITIVAS CRIPTOGRAFICAS EN TLS 1.3
=====================================================

Paso del protocolo        Primitiva          Capitulo
-----------------------------------------------------
Intercambio de llaves     X25519 (ECDH)      Cap 9
                          ML-KEM-768 (PQC)   Cap 12

Derivacion de llaves      HKDF-SHA256/384    Cap 5

Cifrado de datos          AES-256-GCM        Cap 7
                          ChaCha20-Poly1305  Cap 8

Autenticacion de datos    GHASH (en GCM)     Cap 7
                          Poly1305           Cap 8

Autenticacion del server  ECDSA / Ed25519    Cap 9
                          RSA-PSS            Cap 9
                          ML-DSA-65 (futuro) Cap 12

Integridad del handshake  HMAC-SHA256/384    Cap 10

Hash del transcript       SHA-256 / SHA-384  Cap 1, 3

Certificados              X.509 + CA chain   Cap 9
```

Cada primitiva que estudiaste tiene un lugar concreto en TLS. Ninguna funciona sola; todas colaboran para lograr las cuatro propiedades que necesita una comunicacion segura: confidencialidad, integridad, autenticacion y forward secrecy.

### 13.2.3 Forward secrecy: por que las llaves efimeras importan

TLS 1.3 impone **forward secrecy** (secreto hacia adelante) en todas las conexiones. Esto significa que cada sesion usa llaves efimeras que se generan, usan y destruyen. Si un atacante graba trafico cifrado hoy y manana roba la llave privada del servidor, **no puede descifrar el trafico grabado**, porque las llaves de sesion ya no existen.

Esto fue un cambio critico respecto a TLS 1.2, donde era comun usar RSA para transportar llaves: el cliente generaba una llave aleatoria, la cifraba con la llave publica RSA del servidor, y la enviaba. Si alguien obtenia la llave privada RSA, podia descifrar todas las sesiones pasadas.

TLS 1.3 elimino por completo el transporte de llaves con RSA. Solo permite intercambio efimero Diffie-Hellman (ECDHE o equivalente). Es una decision de diseno que sacrifica compatibilidad en favor de seguridad.

### 13.2.4 Que mejoro respecto a TLS 1.2

| Aspecto | TLS 1.2 | TLS 1.3 |
|---------|---------|---------|
| Round-trips del handshake | 2-RTT | 1-RTT |
| Forward secrecy | Opcional | Obligatorio |
| Cipher suites | 300+ (muchas inseguras) | 5 (todas seguras) |
| RSA key transport | Permitido | Eliminado |
| Compresion | Permitida (CRIME attack) | Eliminada |
| Renegociacion | Permitida (Triple Handshake) | Eliminada |
| Cifrado del handshake | Parcial | Casi completo (desde ServerHello) |
| 0-RTT | No existia | Disponible (con reservas) |

La simplificacion no es cosmetica. Cada feature eliminado de TLS 1.2 habia sido vector de ataque: CRIME explotaba la compresion, BEAST y POODLE explotaban CBC, Triple Handshake explotaba la renegociacion, y Logjam explotaba grupos DH debiles. TLS 1.3 aprendio de cada uno de estos errores.

### 13.2.5 Inspeccionando una conexion TLS real con Python

Vamos a escribir codigo que conecta a un servidor real y examina los parametros criptograficos negociados:

```python
"""
inspeccionar_tls.py

Conecta a un servidor HTTPS y reporta los parametros
criptograficos negociados en la sesion TLS.

Mapea cada parametro a las primitivas estudiadas en el libro.
"""

import ssl
import socket
import datetime


def inspeccionar_tls(hostname: str, puerto: int = 443) -> dict:
    """
    Conecta a un servidor y extrae informacion de la sesion TLS.
    """
    context = ssl.create_default_context()

    with socket.create_connection((hostname, puerto), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            # Informacion de la sesion
            version = ssock.version()
            cipher = ssock.cipher()
            cert = ssock.getpeercert()

            # Extraer datos del certificado
            subject = dict(x[0] for x in cert.get("subject", ()))
            issuer = dict(x[0] for x in cert.get("issuer", ()))
            not_after = cert.get("notAfter", "")

            return {
                "hostname": hostname,
                "version_tls": version,
                "cipher_suite": cipher[0],
                "protocolo_cipher": cipher[1],
                "bits_cifrado": cipher[2],
                "subject_cn": subject.get("commonName", "N/A"),
                "issuer_cn": issuer.get("commonName", "N/A"),
                "issuer_org": issuer.get("organizationName", "N/A"),
                "expira": not_after,
            }


def mapear_primitivas(info: dict) -> None:
    """
    Mapea los parametros de la sesion TLS a las primitivas del libro.
    """
    suite = info["cipher_suite"]

    print(f"\n{'=' * 65}")
    print(f"ANALISIS TLS: {info['hostname']}")
    print(f"{'=' * 65}")

    print(f"\n--- Sesion TLS ---")
    print(f"Version:       {info['version_tls']}")
    print(f"Cipher suite:  {suite}")
    print(f"Bits cifrado:  {info['bits_cifrado']}")

    print(f"\n--- Certificado ---")
    print(f"Sujeto:        {info['subject_cn']}")
    print(f"Emisor:        {info['issuer_cn']} ({info['issuer_org']})")
    print(f"Expira:        {info['expira']}")

    # Mapear cipher suite a primitivas
    print(f"\n--- Mapa de primitivas (conexion con el libro) ---")

    if "AES_256_GCM" in suite:
        print(f"Cifrado:           AES-256-GCM (Cap. 7)")
        print(f"  -> Cifrado de bloque AES con modo Galois/Counter")
        print(f"  -> Autenticacion integrada via GHASH")
    elif "AES_128_GCM" in suite:
        print(f"Cifrado:           AES-128-GCM (Cap. 7)")
    elif "CHACHA20_POLY1305" in suite:
        print(f"Cifrado:           ChaCha20-Poly1305 (Cap. 8)")
        print(f"  -> Cifrado de flujo ChaCha20 + MAC Poly1305")

    if "SHA384" in suite:
        print(f"Hash (HKDF):       SHA-384 (Cap. 3)")
    elif "SHA256" in suite:
        print(f"Hash (HKDF):       SHA-256 (Cap. 3)")

    print(f"Key exchange:      ECDHE (X25519 o P-256) (Cap. 9)")
    print(f"  -> Forward secrecy: SI (llaves efimeras)")

    if info["version_tls"] == "TLSv1.3":
        print(f"Derivacion llaves: HKDF (Cap. 5)")
        print(f"Integridad:        HMAC integrado en Finished (Cap. 10)")

    print(f"\nNota: si el servidor soporta PQC, el key exchange")
    print(f"podria ser X25519MLKEM768 (Cap. 12).")


# --- Analizar varios sitios ---
sitios = [
    "www.google.com",
    "github.com",
    "www.cloudflare.com",
]

for sitio in sitios:
    try:
        info = inspeccionar_tls(sitio)
        mapear_primitivas(info)
    except Exception as e:
        print(f"\nError conectando a {sitio}: {e}")
```

Salida tipica:

```
=================================================================
ANALISIS TLS: www.google.com
=================================================================

--- Sesion TLS ---
Version:       TLSv1.3
Cipher suite:  TLS_AES_256_GCM_SHA384
Bits cifrado:  256

--- Certificado ---
Sujeto:        www.google.com
Emisor:        WR2 (Google Trust Services)
Expira:        Jun 23 08:23:57 2026 GMT

--- Mapa de primitivas (conexion con el libro) ---
Cifrado:           AES-256-GCM (Cap. 7)
  -> Cifrado de bloque AES con modo Galois/Counter
  -> Autenticacion integrada via GHASH
Hash (HKDF):       SHA-384 (Cap. 3)
Key exchange:      ECDHE (X25519 o P-256) (Cap. 9)
  -> Forward secrecy: SI (llaves efimeras)
Derivacion llaves: HKDF (Cap. 5)
Integridad:        HMAC integrado en Finished (Cap. 10)

Nota: si el servidor soporta PQC, el key exchange
podria ser X25519MLKEM768 (Cap. 12).
```

Cada linea de esa salida conecta con algo que ya estudiaste. El proposito de este ejercicio es que veas que las primitivas no son abstracciones academicas: estan operando ahora mismo en cada conexion HTTPS de tu navegador.

---

## 13.3 Signal Protocol: cifrado extremo a extremo

TLS protege datos *en transito* entre tu dispositivo y un servidor. Pero el servidor puede leer los datos en texto plano. Cuando envias un mensaje por una aplicacion de mensajeria que usa TLS pero no cifrado extremo a extremo, el proveedor del servicio puede leer tus mensajes.

El **Signal Protocol**, disenado por Moxie Marlinspike y Trevor Perrin, resuelve este problema. Es el protocolo de cifrado extremo a extremo mas influyente del mundo: lo usan Signal, WhatsApp (mas de 2 mil millones de usuarios), Google Messages y Facebook Messenger [Marlinspike y Perrin, 2016].

### 13.3.1 El problema del cifrado extremo a extremo

En un sistema de cifrado extremo a extremo (E2E), solo el emisor y el receptor pueden leer los mensajes. El servidor que los transmite solo ve datos cifrados. Esto plantea desafios unicos:

1. **Los usuarios no siempre estan en linea al mismo tiempo.** No puedes hacer un intercambio de llaves interactivo como en TLS.
2. **Los mensajes deben ser seguros incluso si las llaves se comprometen despues.** Necesitas forward secrecy por mensaje, no solo por sesion.
3. **Si un atacante compromete tu telefono y despues lo recuperas,** los mensajes futuros deben volver a ser seguros. Esto se llama **seguridad post-compromiso**.

### 13.3.2 X3DH: el apretón de manos asincronico

Para resolver el problema de que los usuarios no siempre estan conectados, Signal usa el protocolo **X3DH** (Extended Triple Diffie-Hellman) [Marlinspike y Perrin, 2016]:

```
PROTOCOLO X3DH (simplificado)
==============================

Preparacion (cuando Alice instala la app):
  Alice genera y sube al servidor:
  - Identity key (IK_A): llave a largo plazo (Ed25519/X25519)
  - Signed pre-key (SPK_A): llave a mediano plazo, firmada con IK_A
  - One-time pre-keys (OPK_A): llaves de un solo uso

Cuando Bob quiere enviar un mensaje a Alice (que esta offline):
  1. Bob descarga del servidor: IK_A, SPK_A, OPK_A
  2. Bob genera su llave efimera (EK_B)
  3. Bob calcula CUATRO intercambios Diffie-Hellman:
     DH1 = DH(IK_B, SPK_A)    -- identidad de Bob + pre-key de Alice
     DH2 = DH(EK_B, IK_A)     -- efimera de Bob + identidad de Alice
     DH3 = DH(EK_B, SPK_A)    -- efimera de Bob + pre-key de Alice
     DH4 = DH(EK_B, OPK_A)    -- efimera de Bob + one-time de Alice
  4. Secreto compartido = KDF(DH1 || DH2 || DH3 || DH4)
  5. Bob envia: IK_B, EK_B, identificador de OPK, y el mensaje cifrado

Cuando Alice se conecta:
  - Alice descarga el mensaje y repite los mismos calculos DH
  - Obtiene el mismo secreto compartido
  - Descifra el mensaje
```

Los cuatro intercambios DH proporcionan propiedades complementarias: DH1 autentica a Bob, DH2 y DH3 proporcionan forward secrecy, y DH4 (con la llave de un solo uso) proporciona proteccion contra ataques de repeticion.

Todo esto usa X25519 (capitulo 9) y HKDF (capitulo 5), las mismas primitivas de TLS pero combinadas de una manera diferente para resolver un problema diferente.

### 13.3.3 Double Ratchet: forward secrecy por mensaje

Una vez establecida la sesion con X3DH, Signal usa el algoritmo **Double Ratchet** para cifrar cada mensaje con una llave diferente. El nombre viene de la analogia con un trinquete mecanico: un dispositivo que solo puede girar en una direccion [Perrin y Marlinspike, 2016].

El Double Ratchet combina dos mecanismos:

**Ratchet simetrico (cadena de llaves):** Cada mensaje usa una llave derivada de la anterior mediante una KDF. Conocer la llave del mensaje N no te permite calcular la llave del mensaje N-1. Esto garantiza forward secrecy: si alguien obtiene tu llave actual, no puede descifrar mensajes anteriores.

```
Cadena de llaves (symmetric ratchet):

llave_cadena_0 --> KDF --> llave_cadena_1 --> KDF --> llave_cadena_2
      |                         |                         |
      v                         v                         v
 llave_msg_0              llave_msg_1              llave_msg_2
```

**Ratchet Diffie-Hellman (asimetrico):** Cada vez que ambas partes envian un mensaje, intercambian nuevas llaves publicas efimeras y realizan un nuevo DH. Esto "reinicia" la cadena de llaves y proporciona **seguridad post-compromiso**: incluso si un atacante roba tu llave privada actual, despues de unos pocos mensajes la sesion se "recupera" porque las nuevas llaves efimeras reemplazan a las comprometidas.

```
Double Ratchet (simplificado):

Alice envia:  ratchet_pub_A1 + mensaje cifrado con llave_msg
Bob recibe:   hace DH(ratchet_priv_B, ratchet_pub_A1)
              -> nueva cadena de llaves
Bob responde: ratchet_pub_B1 + mensaje cifrado
Alice recibe: hace DH(ratchet_priv_A, ratchet_pub_B1)
              -> nueva cadena de llaves (otra vez)
...y asi sucesivamente, con cada intercambio de mensajes
```

La combinacion de ambos ratchets es lo que da el nombre "double": el ratchet simetrico avanza con cada mensaje, y el ratchet DH avanza con cada intercambio de turno.

### 13.3.4 Primitivas del libro en el protocolo Signal

| Paso | Primitiva | Capitulo |
|------|-----------|----------|
| Identidad del usuario | Ed25519 (firma) | 9 |
| Intercambio de llaves (X3DH) | X25519 (Diffie-Hellman) | 9 |
| Derivacion de llaves | HKDF-SHA256 | 5 |
| Ratchet simetrico | HMAC-SHA256 como KDF | 10 |
| Cifrado de mensajes | AES-256-CBC + HMAC-SHA256 | 7, 10 |
| Hash del transcript | SHA-256 | 1, 3 |

Signal esta migrando a un esquema post-cuantico llamado PQXDH, que agrega ML-KEM al proceso X3DH [Signal, 2023]. Esto conecta directamente con lo que estudiamos en el capitulo 12: la misma estrategia hibrida de TLS, aplicada a mensajeria.

---

## 13.4 Criptografia de proxima generacion: un panorama

Mas alla de TLS y Signal, hay tres areas de la criptografia que estan expandiendo lo que es posible. No las necesitas para tu trabajo diario hoy, pero debes saber que existen porque en 5-10 anios podrian ser tan ubicuas como TLS.

### 13.4.1 Pruebas de conocimiento cero (Zero-Knowledge Proofs)

Una **prueba de conocimiento cero** (ZKP) permite que una parte (el probador) convenza a otra (el verificador) de que una afirmacion es verdadera, **sin revelar ninguna informacion adicional**.

La analogia clasica: imagina una cueva con dos entradas (A y B) que se conectan por dentro con una puerta que solo se abre con una contrasena. Quieres probar que conoces la contrasena sin revelarla. El verificador se para afuera y te pide que entres por A y salgas por B (o viceversa). Si puedes hacerlo repetidamente con instrucciones aleatorias, el verificador se convence de que conoces la contrasena, pero nunca la ve [Quisquater et al., 1989].

En terminos practicos:

- **Verificacion de edad sin revelar la fecha de nacimiento.** Puedes probar "tengo mas de 18 anios" sin mostrar tu identificacion completa.
- **Prueba de solvencia sin revelar el monto.** Un banco puede probar que tiene suficientes reservas sin revelar el balance exacto.
- **Verificacion de computo sin repetirlo.** Un servidor puede probar que ejecuto un calculo correctamente sin que el verificador lo repita.

Las implementaciones mas importantes son:

- **zk-SNARKs** (Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge): pruebas muy pequenas y rapidas de verificar, usadas extensamente en blockchain (Zcash, Ethereum).
- **zk-STARKs** (Scalable Transparent ARguments of Knowledge): sin necesidad de una "ceremonia de confianza" para generar parametros iniciales, y resistentes a computadoras cuanticas.
- **Bulletproofs**: pruebas eficientes para rangos de valores, sin trusted setup.

El estado actual (2026): las ZKP ya se usan en produccion para privacidad en blockchain y verificacion de identidad. Las bibliotecas mas maduras son circom/snarkjs (JavaScript), bellman (Rust) y gnark (Go). Sin embargo, disenar circuitos ZKP sigue siendo complejo y requiere conocimiento especializado.

### 13.4.2 Cifrado homomorfico

El **cifrado homomorfico** (HE, Homomorphic Encryption) permite hacer computaciones sobre datos cifrados sin descifrarlos. El resultado de la computacion, una vez descifrado, es identico al resultado de hacer la misma computacion sobre los datos en texto plano.

```
Cifrado homomorfico:

cifrar(3) + cifrar(5) = cifrar(8)

El servidor calcula cifrar(3) + cifrar(5) sin saber
que los valores son 3 y 5.
El cliente descifra el resultado y obtiene 8.
```

Los tres tipos principales son:

- **Parcialmente homomorfico (PHE):** Permite una operacion (suma o multiplicacion). RSA, por ejemplo, es multiplicativamente homomorfico: cifrar(a) * cifrar(b) = cifrar(a*b). Esto se conoce desde los anios 70.
- **Somewhat homomorfico (SHE):** Permite sumas y multiplicaciones, pero con un numero limitado de operaciones antes de que el "ruido" interno haga imposible descifrar.
- **Totalmente homomorfico (FHE):** Permite cualquier numero de sumas y multiplicaciones --es decir, cualquier computacion. Craig Gentry lo demostro teoricamente posible en 2009 [Gentry, 2009].

El estado actual (2026): FHE es funcionalmente posible pero todavia es lento. Una operacion homomorfica es entre 1,000 y 1,000,000 de veces mas lenta que la misma operacion en texto plano, dependiendo del esquema y la implementacion. Sin embargo, el progreso es rapido: investigadores de Google, Cornell y MIT publicaron en 2025 resultados usando TPUs (procesadores de inteligencia artificial) para acelerar FHE, logrando mejoras de 10x o mas [Google Research, 2025]. Empresas como Zama y Duality Technologies ofrecen compiladores FHE que simplifican el desarrollo.

Casos de uso actuales: analisis de datos medicos sin revelarlos al analista, evaluacion de modelos de machine learning sobre datos cifrados, y busquedas en bases de datos cifradas.

### 13.4.3 Computacion multipartita segura (MPC)

La **computacion multipartita segura** (MPC, Secure Multi-Party Computation) permite que varias partes calculen conjuntamente una funcion sobre sus datos privados, sin que ninguna parte revele sus datos a las demas.

El ejemplo clasico: dos millonarios quieren saber quien es mas rico, pero ninguno quiere revelar su patrimonio al otro. Con MPC, pueden calcular "quien tiene mas?" sin que ninguno aprenda el valor del otro [Yao, 1982].

```
Computacion multipartita segura:

Partido A tiene: salario_A = $80,000
Partido B tiene: salario_B = $95,000
Partido C tiene: salario_C = $72,000

Quieren calcular: promedio de salarios
Sin revelar: ningun salario individual

MPC calcula: ($80,000 + $95,000 + $72,000) / 3 = $82,333

Cada partido solo aprende el resultado ($82,333),
no los salarios de los demas.
```

El estado actual (2026): MPC se usa en produccion para:
- **Custodia de llaves privadas en fintech:** Empresas como Fireblocks dividen una llave privada entre multiples servidores. Para firmar una transaccion, los servidores ejecutan un protocolo MPC que produce la firma sin que ninguno reconstruya la llave completa.
- **Subastas electronicas:** Calcular el precio de mercado sin revelar las ofertas individuales.
- **Analisis de datos entre competidores:** Dos hospitales pueden entrenar un modelo de IA sobre sus datos combinados sin compartir historiales de pacientes.

Partisia demostro en 2025 un sistema de identidad digital en Japon que usa reconocimiento facial con MPC: el matching biometrico se realiza sin descifrar los datos biometricos en ningun momento [Partisia, 2025].

### 13.4.4 El hilo comun

ZKP, FHE y MPC comparten un objetivo: **realizar operaciones utiles sobre informacion privada sin revelarla**. Son complementarias:

| Tecnologia | Que permite | Limitacion principal (2026) |
|-----------|------------|---------------------------|
| ZKP | Probar algo sin revelarlo | Disenar circuitos es complejo |
| FHE | Computar sobre datos cifrados | 1000-1M veces mas lento |
| MPC | Calcular entre multiples partes | Comunicacion entre partes |

Estas tres tecnologias convergen hacia un futuro donde puedes usar datos sin verlos. Estan basadas en las mismas primitivas que ya conoces: funciones hash, cifrado simetrico, curvas elipticas y reticulos. La diferencia es como se combinan.

---

## 13.5 Agilidad criptografica: disena para poder cambiar

### 13.5.1 Por que necesitas agilidad criptografica

A lo largo de este libro vimos una constante: los algoritmos se rompen. MD5 se rompio. SHA-1 se rompio. DES se rompio. RC4 se rompio. Y eventualmente, los algoritmos que usamos hoy tambien se romperan o se volveran obsoletos --sea por avances matematicos, computadoras cuanticas, o simplemente porque aparecen alternativas mejores.

La pregunta no es **si** tendras que cambiar de algoritmo, sino **cuando**. Y la pregunta practica es: **que tan dificil sera?**

La **agilidad criptografica** (crypto agility) es la capacidad de tu sistema para reemplazar algoritmos criptograficos sin reescribir la logica de aplicacion. En diciembre de 2025, el NIST publico el Cybersecurity Whitepaper 39 (CSWP 39), dedicado exclusivamente a este tema, senalando que la agilidad criptografica debe ser una prioridad estrategica para todas las organizaciones [NIST, 2025].

### 13.5.2 Principios de diseno para agilidad criptografica

El CSWP 39 del NIST identifica cinco principios clave:

**1. Modularidad: la criptografia como componente intercambiable.**

Los algoritmos criptograficos deben estar encapsulados detras de interfaces bien definidas. Tu codigo de aplicacion no debe llamar a `AES-256-GCM` directamente; debe llamar a `cifrar(datos, llave)`, y la implementacion concreta debe ser configurable.

```python
"""
crypto_agility.py

Ejemplo de diseno con agilidad criptografica.
La aplicacion usa una interfaz abstracta;
el algoritmo concreto se configura externamente.
"""

from abc import ABC, abstractmethod
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
import os
import json


class CifradoAutenticado(ABC):
    """Interfaz abstracta para cifrado autenticado."""

    @abstractmethod
    def cifrar(self, datos: bytes, aad: bytes = b"") -> bytes:
        pass

    @abstractmethod
    def descifrar(self, datos_cifrados: bytes, aad: bytes = b"") -> bytes:
        pass

    @abstractmethod
    def nombre_algoritmo(self) -> str:
        pass


class CifradoAESGCM(CifradoAutenticado):
    """Implementacion con AES-256-GCM."""

    def __init__(self, llave: bytes):
        if len(llave) != 32:
            raise ValueError("AES-256 requiere llave de 32 bytes")
        self._aesgcm = AESGCM(llave)

    def cifrar(self, datos: bytes, aad: bytes = b"") -> bytes:
        nonce = os.urandom(12)
        ct = self._aesgcm.encrypt(nonce, datos, aad)
        return nonce + ct  # Prepend nonce

    def descifrar(self, datos_cifrados: bytes, aad: bytes = b"") -> bytes:
        nonce = datos_cifrados[:12]
        ct = datos_cifrados[12:]
        return self._aesgcm.decrypt(nonce, ct, aad)

    def nombre_algoritmo(self) -> str:
        return "AES-256-GCM"


class CifradoChaCha(CifradoAutenticado):
    """Implementacion con ChaCha20-Poly1305."""

    def __init__(self, llave: bytes):
        if len(llave) != 32:
            raise ValueError("ChaCha20 requiere llave de 32 bytes")
        self._chacha = ChaCha20Poly1305(llave)

    def cifrar(self, datos: bytes, aad: bytes = b"") -> bytes:
        nonce = os.urandom(12)
        ct = self._chacha.encrypt(nonce, datos, aad)
        return nonce + ct

    def descifrar(self, datos_cifrados: bytes, aad: bytes = b"") -> bytes:
        nonce = datos_cifrados[:12]
        ct = datos_cifrados[12:]
        return self._chacha.decrypt(nonce, ct, aad)

    def nombre_algoritmo(self) -> str:
        return "ChaCha20-Poly1305"


# --- Configuracion externa ---
# El algoritmo se elige por configuracion, no por codigo.

ALGORITMOS_DISPONIBLES = {
    "AES-256-GCM": CifradoAESGCM,
    "ChaCha20-Poly1305": CifradoChaCha,
    # Manana puedes agregar:
    # "AES-256-GCM-SIV": CifradoAESGCMSIV,
    # "XSalsa20-Poly1305": CifradoXSalsa,
}


def crear_cifrado(config: dict, llave: bytes) -> CifradoAutenticado:
    """
    Factory que crea el cifrado segun configuracion.

    config = {"algoritmo": "AES-256-GCM"}
    """
    nombre = config.get("algoritmo", "AES-256-GCM")
    clase = ALGORITMOS_DISPONIBLES.get(nombre)

    if clase is None:
        raise ValueError(
            f"Algoritmo '{nombre}' no soportado. "
            f"Disponibles: {list(ALGORITMOS_DISPONIBLES.keys())}"
        )

    return clase(llave)


# --- Uso ---
config = {"algoritmo": "AES-256-GCM"}
llave = os.urandom(32)
cifrado = crear_cifrado(config, llave)

mensaje = b"Datos sensibles"
cifrado_bytes = cifrado.cifrar(mensaje)
descifrado = cifrado.descifrar(cifrado_bytes)

print(f"Algoritmo: {cifrado.nombre_algoritmo()}")
print(f"Original:   {mensaje}")
print(f"Descifrado: {descifrado}")
print(f"Coinciden:  {mensaje == descifrado}")

# Cambiar de algoritmo: solo cambias la configuracion
config["algoritmo"] = "ChaCha20-Poly1305"
cifrado2 = crear_cifrado(config, llave)
print(f"\nCambiado a: {cifrado2.nombre_algoritmo()}")
```

**2. Separacion de politica y mecanismo.**

Las politicas criptograficas (que algoritmos usar, que tamanos de llave, que suites permitir) deben almacenarse en archivos de configuracion o consolas de administracion, no hardcodeadas en el codigo fuente. Cambiar un algoritmo debe ser un cambio de configuracion, no un cambio de codigo.

**3. Identificadores de algoritmo en datos persistidos.**

Cuando cifras datos y los almacenas, incluye un identificador del algoritmo y version usados. Sin esto, si cambias de algoritmo, no podras descifrar los datos antiguos.

```python
# MAL: no sabes con que se cifro
datos_cifrados = cifrar(datos)

# BIEN: el header identifica el algoritmo
header = {
    "alg": "AES-256-GCM",
    "v": 1,
    "kid": "llave-produccion-2026-03"
}
datos_cifrados = json.dumps(header).encode() + b"\n" + cifrar(datos)

# Cuando descifras, lees el header primero y eliges el algoritmo
```

**4. Inventario criptografico (CBOM).**

Ya vimos esto en el capitulo 12: mantener un registro actualizado de todos los algoritmos que usa tu sistema, donde se usan, y quien los controla. Sin un inventario, no puedes migrar.

**5. Testing automatizado de la capa criptografica.**

Si puedes cambiar algoritmos por configuracion, necesitas tests que validen que cada configuracion funciona. Esto incluye tests de compatibilidad hacia atras: datos cifrados con el algoritmo anterior deben poder descifrarse con el sistema actual.

### 13.5.3 Anti-patrones de agilidad criptografica

Estos son errores comunes que hacen que cambiar de algoritmo sea doloroso o imposible:

```
ANTI-PATRON                      CONSECUENCIA
--------------------------------------------------------------
Hardcodear "AES-256" en 50       Cambiar requiere modificar
archivos diferentes               50 archivos

Almacenar datos cifrados          No puedes descifrar datos
sin identificador de algoritmo    antiguos despues de migrar

Usar primitivas de bajo nivel     Cada uso tiene bugs
en lugar de una biblioteca        potenciales diferentes

No tener tests para la capa       No sabes si la migracion
criptografica                     rompio algo

Depender de un solo proveedor     Si el proveedor no soporta
de KMS sin abstraccion            PQC, no puedes migrar
```

El NIST introduce un modelo de madurez para la agilidad criptografica, desde el nivel mas bajo ("no estructurado, sin plan") hasta el mas alto ("programa adaptativo integrado en la gestion de riesgos empresarial"). La mayoria de las organizaciones hoy estan en los niveles mas bajos. La migracion post-cuantica es la oportunidad --y la urgencia-- para subir de nivel [NIST CSWP 39, 2025].

---

## 13.6 Ejercicio integrador: mapea las primitivas en un protocolo real

**Objetivo:** Elegir un protocolo criptografico real y mapear cada una de sus primitivas a los capitulos de este libro.

**Instrucciones:**

1. **Elige un protocolo** de la siguiente lista:
   - SSH (RFC 4253)
   - WireGuard (whitepaper de Jason Donenfeld)
   - Signal Protocol (especificacion de signal.org)
   - Let's Encrypt / ACME (RFC 8555)
   - Age (herramienta de cifrado de archivos, filippo.io/age)

2. **Lee la especificacion o documentacion** del protocolo elegido. No necesitas leer el RFC completo; busca resumenes tecnicos o diagramas del protocolo.

3. **Crea una tabla como la siguiente:**

```
PROTOCOLO: [nombre]

Paso                  Primitiva usada         Capitulo    Proposito
-------------------------------------------------------------------
Autenticacion         Ed25519                 Cap 9       Verificar identidad
Intercambio llaves    X25519                  Cap 9       Forward secrecy
Derivacion llaves     HKDF-BLAKE2             Cap 5       Multiples llaves
Cifrado               ChaCha20-Poly1305       Cap 8       Confidencialidad
Integridad            Poly1305 (integrado)    Cap 10      Autenticacion datos
Hash                  BLAKE2s                 Cap 4       Integridad general
```

4. **Responde estas preguntas:**
   - Que pasa si una de las primitivas se rompe? El protocolo sobrevive?
   - El protocolo tiene forward secrecy? Como lo logra?
   - Que cambiaria si necesitas hacerlo post-cuantico?
   - Tiene agilidad criptografica? Es decir, puedes cambiar algoritmos sin reescribir el protocolo?

5. **Extension avanzada:** Implementa una version simplificada del protocolo en Python. No necesita ser segura para produccion; el objetivo es que entiendas la mecanica de combinar primitivas. Usa las bibliotecas `cryptography` y `pynacl`.

---

## Resumen del capitulo

Las primitivas criptograficas son herramientas poderosas, pero adquieren su verdadero valor cuando se combinan en protocolos bien disenados. TLS 1.3 es el ejemplo canonico: usa hashes (SHA-256/384), intercambio de llaves efimero (X25519, ML-KEM-768), derivacion de llaves (HKDF), cifrado autenticado (AES-GCM, ChaCha20-Poly1305), firmas digitales (ECDSA, Ed25519) y MACs (HMAC) en una coreografia cuidadosamente disenada.

El protocolo Signal demuestra que las mismas primitivas pueden combinarse de manera diferente para resolver un problema diferente: cifrado extremo a extremo asincrono con forward secrecy por mensaje y seguridad post-compromiso.

Mas alla de los protocolos actuales, la criptografia avanzada --pruebas de conocimiento cero, cifrado homomorfico y computacion multipartita-- esta expandiendo lo que es posible sin comprometer la privacidad.

Y el principio que unifica todo esto es la agilidad criptografica: disena tus sistemas para que puedas cambiar de algoritmo cuando --no si-- sea necesario. Los algoritmos se rompen. Los estandares cambian. Tu arquitectura debe sobrevivir a ambos.

---
