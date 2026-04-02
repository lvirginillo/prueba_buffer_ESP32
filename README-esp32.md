# ESP32 — Streaming ADC en tiempo real vía TCP

Proyecto de prueba de concepto para streaming binario de lecturas ADC desde un ESP32 hacia una PC, con visualización en tiempo real usando Python y Matplotlib.

> Autor: [Lautaro Virginillo](https://www.linkedin.com/in/lautaro-virginillo/)

---

## ¿Qué hace?

El ESP32 lee continuamente un pin analógico (~1000 muestras/segundo) y envía los datos como bytes crudos (`uint16_t`, 2 bytes por muestra) a través de un socket TCP. Un script Python recibe el stream, lo acumula en un buffer circular y lo grafica en tiempo real.

---

## Arquitectura

```
[GPIO36 - ADC] ──► [ESP32 WiFi Server :1234] ──TCP──► [Python Client] ──► [Matplotlib]
                    envío binario uint16_t                buffer circular     animación en vivo
```

---

## Estructura del proyecto

```
prueba_buffer_ESP32/
├── src/
│   ├── main.cpp        # Firmware ESP32 (PlatformIO)
│   └── lectura.py      # Cliente Python — recepción y visualización
├── include/            # Headers (vacío en este proyecto)
├── lib/                # Librerías locales (vacío en este proyecto)
├── test/               # Tests PlatformIO
└── platformio.ini      # Configuración del proyecto
```

---

## Hardware

- ESP32 (cualquier variante con WiFi)
- Pin ADC: GPIO36 (ADC1_CH0) — recomendado por compatibilidad con WiFi activo
- Rango ADC: 0–4095 (12 bits)

---

## Firmware (ESP32)

Desarrollado con PlatformIO. El ESP32 actúa como servidor TCP: espera una conexión, y una vez establecida envía las lecturas ADC de forma continua en formato binario little-endian.

**Configuración antes de flashear:**

Editá `src/main.cpp` y reemplazá las credenciales WiFi:

```cpp
const char* ssid     = "TU_SSID";
const char* password = "TU_PASSWORD";
```

> ⚠️ No commitees las credenciales reales. Podés usar un archivo `secrets.h` ignorado por git.

**Flashear:**

```bash
pio run --target upload
pio device monitor  # ver IP asignada por DHCP
```

---

## Cliente Python

```bash
pip install matplotlib numpy
```

Editá `src/lectura.py` con la IP que mostró el monitor serie:

```python
HOST = '192.168.x.x'  # IP del ESP32
PORT = 1234
```

Ejecutar:

```bash
python src/lectura.py
```

---

## Parámetros configurables

| Parámetro | Archivo | Default | Descripción |
|---|---|---|---|
| `HOST` | `lectura.py` | — | IP del ESP32 en la red local |
| `PORT` | ambos | `1234` | Puerto TCP |
| `WINDOW_SIZE` | `lectura.py` | `1000` | Muestras visibles en el gráfico |
| `delayMicroseconds` | `main.cpp` | `1000` | Intervalo entre muestras (~1000 mps) |

---

## Rendimiento observado

- ~1000 muestras/segundo con `delayMicroseconds(1000)`
- Transferencia binaria (2 bytes/muestra) vs texto: ~10x menos overhead
- Buffer circular con `deque(maxlen=1000)` — sin crecimiento de memoria

---

## Dependencias

**Python:**
- `matplotlib`
- `numpy`
- `socket`, `threading` (stdlib)

**PlatformIO:**
- Framework: Arduino
- Platform: espressif32
- Librería: `WiFi.h` (incluida en el framework)

---

## Notas

- GPIO36 es input-only y no tiene resistencia pull-up interna — ideal para ADC con WiFi activo
- El envío es little-endian (`byteorder='little'`) — consistente con la arquitectura del ESP32
- Este proyecto es una prueba de concepto; no incluye reconexión automática ni manejo de errores de red
