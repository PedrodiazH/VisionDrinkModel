# VisionDrinkModel
Regression model for estimating alcohol consumption through facial expressions.

## Objetivo
Este repositorio contiene el pipeline de procesamiento y modelado para estimar la ingesta acumulada de alcohol mediante visión por computadora. Por motivos de privacidad, el set de imágenes original se mantiene en un almacenamiento externo (Drive).

Luego, la idea es llevarlo a un modelo de regresión que infiera el BAC a través de expresiones faciales. Para ponderarlo con otras variables de interés y encapsularlo en una App Movil.

[Ver estado y métricas del Dataset](DATASET_SUMMARY.md)

## Arquitectura 
- **Código y Metadatos (GitHub):** Contiene scripts, arquitecturas de red y el archivo `dataset.csv` (etiquetas y variables).
- **Imágenes (Local/Drive):** Los PNGs crudos y aumentados quedan excluidos del control de versiones (`.gitignore`). 

## Pipeline de Preprocesamiento y Data Augmentation
Para compensar el tamaño reducido de la muestra y evitar sobreajuste, el pipeline incluye:
1. **Face Alignment:** Normalización de la rotación del rostro.
2. **Data Augmentation (Post-Split):** Variaciones de iluminación (brillo/contraste), ruido gaussiano y flips horizontales aplicados exclusivamente al set de entrenamiento.

## Arquitectura del Modelo 
El problema se aborda como una regresión lineal
- **Input:** Imagen facial (tensor) + vector tabular (peso, tiempo transcurrido).
- **Backbone:** CNN (ej. ResNet50) para la extracción de características visuales.
- **Output:** Un único valor continuo (Gramos de alcohol acumulados).
- **Loss Function:** Mean Squared Error (MSE).

### Fundamentos tecnológicos y analíticos
La arquitectura del modelo se sostiene bajo los siguientes tópicos de investigación y desarrollo:
- **Reconocimiento de expresiones faciales (FER)**
- **Deep Learning Multimodal**
- Stack tecnológico: PyTorch, OpenCV, Albumentations para Data Augmentation
### Future approach
- XAI (Grad-CAM o SHAP) para zonas del rostro que determinan la inferencia de BAC
- Ponderar bajo otros métodos de estimación de BAC