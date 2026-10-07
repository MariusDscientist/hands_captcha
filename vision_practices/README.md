# 🧪 Laboratorio de Prácticas de Visión

Este directorio contiene tutoriales, experimentos y pruebas de concepto (PoC) diseñados para dominar las herramientas y fundamentos de visión computacional, tracking gestual y procesamiento en tiempo real antes de ensamblar el pipeline final de **Air-Draw CAPTCHA**.

---

## 📋 Índice de Prácticas

| Práctica | Nombre / Enfoque | Tecnologías Clave | Estado |
| :--- | :--- | :--- | :---: |
| [01](#-práctica-01-reconocimiento-de-gestos-y-telemetría-con-rerun) | **MediaPipe Gesture Recognition & Rerun SDK** | `mediapipe.tasks`, `opencv`, `rerun` | Concluida |
| [02](#-práctica-02-piano-aéreo-gestual-air-piano) | **Air Piano: Detección de Flexión y Audio Interactivo** | `mediapipe.solutions`, `opencv`, `pygame` | Concluida |

---

## 🔬 Práctica 01: Reconocimiento de Gestos y Telemetría con Rerun

- **Archivo fuente:** [`practice_01.py`](file:///home/jhon-mario-cano-torres/Desktop/workspace/vision_practice/vision_practices/practice_01.py)
- **Tema:** Pipeline moderno de MediaPipe Tasks + Telemetría espacial en tiempo real.

### 🎯 Objetivo
Explorar la nueva API de MediaPipe Tasks (`GestureRecognizer`) en modo video, capturar landmarks de la mano y enviar telemetría en tiempo real a la plataforma de visualización espacial **Rerun**.

### ⚙️ Conceptos y Fundamentos Técnicos
- **MediaPipe Tasks Architecture:**
  - Inicialización a través de `BaseOptions` y `GestureRecognizerOptions`.
  - Operación en `RunningMode.VIDEO` sincronizada mediante marcas de tiempo en nanosegundos (`frame_time_nano`), requerida para suavizado temporal interno del modelo.
- **Espacios de Coordenadas:**
  - Conversión de landmarks normalizados $[0.0, 1.0]$ a coordenadas absolutas de píxeles $(x, y)$ de la imagen para rendering.
- **Telemetría y Visualización Desacoplada (Rerun SDK):**
  - Configuración de `AnnotationContext` con las conexiones anatómicas oficiales de la mano (`HAND_CONNECTIONS`).
  - Registro de landmarks tridimensionales (`Hand3D`) bajo orientación diestra (`ViewCoordinates.RIGHT_HAND_X_DOWN`).

### 📦 Requisitos y Recursos
- Modelo preentrenado: `gesture_recognizer.task` en el directorio de ejecución.
- Servidor / Visor de Rerun inicializado (`rerun.init`).

---

## 🎹 Práctica 02: Piano Aéreo Gestual (Air Piano)

- **Archivo fuente:** [`practice_02.py`](file:///home/jhon-mario-cano-torres/Desktop/workspace/vision_practice/vision_practices/practice_02.py)
- **Tema:** Detección de estado cinemático de dedos y disparadores de audio en tiempo real.

### 🎯 Objetivo
Construir un instrumento musical virtual ("Air Piano") capaz de detectar la flexión independiente de los dedos de ambas manos frente a la cámara web y activar notas musicales sintetizadas sin latencia perceptible.

### ⚙️ Conceptos y Fundamentos Técnicos
- **Geometría de Puntos Articulares (Landmarks):**
  - Mapeo de la articulación metacarpofalángica (`MCP`: nudillo base) y la punta distal (`TIP`) de cada dedo:
    - Índice: MCP = 5, TIP = 8
    - Medio: MCP = 9, TIP = 12
    - Anular: MCP = 13, TIP = 16
  - **Cálculo de Flexión (`is_finger_down`):** En el sistema de coordenadas de imagen de OpenCV/MediaPipe, el origen $(0,0)$ reside en la esquina superior izquierda (el eje $Y$ crece hacia abajo). Por lo tanto:
    $$\text{Pulsado} \iff y_{\text{tip}} > y_{\text{mcp}}$$
- **Soporte Multimanual y Asignación de Canales:**
  - Configuración de `mp_hands.Hands(max_num_hands=2)`.
  - Indexación dinámica de 6 canales independientes ($3 \text{ dedos} \times 2 \text{ manos}$):
    $$\text{canal} = i + h \times 3$$
- **Máquina de Estados y Antirrebote (Debouncing):**
  - Vector de estados booleanos (`finger_state = [False]*6`) para registrar transiciones de estado.
  - El sonido se dispara exclusivamente en el flanco ascendente (de `False` a `True`), evitando que el audio se reproduzca de forma repetitiva en cada frame mientras el dedo permanezca abajo.
- **Motor de Audio con Pygame:**
  - Inicialización de `pygame.mixer` y precarga de archivos WAV en memoria para reproducción de baja latencia con `.play()`.

### 📦 Requisitos y Recursos
- Banco de muestras sonoras en formato WAV en [`vision_practices/data/sounds/`](file:///home/jhon-mario-cano-torres/Desktop/workspace/vision_practice/vision_practices/data/sounds/):
  - `#fa.WAV`, `la.WAV`, `re.WAV` (Mano izquierda)
  - `#do.WAV`, `#sol.WAV`, `si.WAV` (Mano derecha)
