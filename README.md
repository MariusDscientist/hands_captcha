# 🖐️ Hands CAPTCHA

> **Sistema de verificación de presencia humana basado en trazado gestual en el aire y validación mediante redes neuronales.**

---

## 📌 Visión del Proyecto

El objetivo de este proyecto es construir un **sistema de CAPTCHA interactivo** en el que un usuario demuestra ser humano dibujando en el aire una secuencia de **4 dígitos aleatorios** solicitados por la pantalla, usando únicamente la punta de su dedo índice frente a su cámara web.

Una vez trazados los números:

1. Las trayectorias se segmentan y procesan en imágenes de trazo normalizadas.
2. Una **red neuronal** clasifica los dígitos ingresados.
3. El sistema valida si los dígitos dibujados coinciden con el token propuesto para conceder el acceso.

---

## 💡 Filosofía y Propósito

Este repositorio es un **laboratorio personal de estudio y experimentación**. El propósito central no es la perfección del código a través de atajos o generación automática, sino el **aprendizaje profundo y práctico** de los fundamentos:

- Manejo de streams de video y pipelines en tiempo real con **OpenCV**.
- Extracción de landmarks y análisis cinemático con **MediaPipe Tasks**.
- Telemetría, registro y visualización de datos espaciales con **Rerun**.
- Procesamiento geométrico de coordenadas y segmentación con **NumPy**.
- Diseño, entrenamiento e inferencia con **Redes Neuronales**.

---

## 📐 Flujo Arquitectónico

```text
[ Desafío: Token (ej. 7 - 3 - 0 - 9) ]
                 │
                 ▼
[ Captura de Video (OpenCV) ]
                 │
                 ▼
[ Detección de Landmarks y Gestos (MediaPipe) ]
                 │
                 ▼
[ Trazado en Lienzo Virtual (Dedo Índice) ]
                 │
                 ▼
[ Segmentación y Normalización de Dígitos ]
                 │
                 ▼
[ Inferencia con Red Neuronal ]
                 │
                 ▼
[ ¿Dígitos Coinciden? ──> Sí: Humano Verificado / No: Acceso Denegado ]
```

---

## 🧪 Prácticas de Laboratorio

El directorio [`vision_practices/`](file:///home/jhon-mario-cano-torres/Desktop/workspace/vision_practice/vision_practices/) reúne los experimentos y pruebas de concepto previas a la integración del core del proyecto (detección de gestos, tracking multimanual, telemetría y audio interactivo).

Consulta la documentación detallada de cada práctica en el [README del Laboratorio](file:///home/jhon-mario-cano-torres/Desktop/workspace/vision_practice/vision_practices/README.md).

---

## 🛠️ Tecnologías y Librerías

- **Lenguaje:** Python 3
- **Visión Computacional:** [OpenCV](https://opencv.org/) (`opencv-python`), [MediaPipe Tasks](https://developers.google.com/mediapipe)
- **Visualización y Telemetría:** [Rerun](https://rerun.io/)
- **Cálculo Matricial:** [NumPy](https://numpy.org/)
- **Machine Learning / Deep Learning:** PyTorch (planificado para la fase de clasificación)

---

## 🚀 Hoja de Ruta (Roadmap)

- [X] **Fase 0: Exploración y Setup**
  - [X] Configuración de entorno y dependencias.
  - [X] Práctica 01: Detección de gestos y landmarks con MediaPipe + Rerun.
- [ ] **Fase 1: Trazador Aéreo (Air-Drawing)**
  - [ ] Tracking exclusivo del índice (`INDEX_FINGER_TIP`).
  - [ ] Lógica de activación de trazo (e.g. gesto de "escribir" vs "pausa/desplazar").
  - [ ] Lienzo virtual (canvas) con suavizado de curvas.
- [ ] **Fase 2: Segmentación y Procesamiento de Dígitos**
  - [ ] Detección de fin de trazo por dígito.
  - [ ] Bounding box, centrado y reescalado (28x28 píxeles estilo MNIST).
- [ ] **Fase 3: Red Neuronal de Clasificación**
  - [ ] Definición de arquitectura (CNN / MLP).
  - [ ] Entrenamiento con dataset de dígitos manuscritos y prueba con trazos aéreos.
- [ ] **Fase 4: Motor de CAPTCHA y Juego Completo**
  - [ ] Generador de 4 dígitos aleatorios.
  - [ ] Comparación de predicciones vs token objetivo.
  - [ ] Interfaz interactiva para el usuario.
