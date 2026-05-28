# NeuroBand: Interfaz de Bio-Retroalimentación Cognitiva

**OBJETIVO:** Establecer el ecosistema de comunicación definitivo mediante MQTT para conectar una ESP32 con un servidor en Python, integrando sensores biométricos y actuadores hápticos. El proyecto garantiza el desacoplamiento del hardware mediante una capa HAL.
**PROYECTO:** NeuroBand

## Integrantes
* Estrada Mata José Job - 21240142
* Navarro Ramos Mario Alberto - 22240328
* Sanchez Perez Brian Leonel - 22240489

## Arquitectura de Datos
ESP32 -> MQTT (Topic: /bio_data) -> PC (Procesamiento IA) -> MQTT (Topic: /feedback) -> Actuadores (Vibración/OLED)

## Matriz de Tópicos MQTT (Estándar de 4 Niveles)

El sistema implementa canales de comunicación desacoplados basados en la arquitectura del proyecto:

| Nivel 1 (Proyecto) | Nivel 2 (Tipo Nodo) | Nivel 3 (Módulo) | Nivel 4 (ID) | Tópico Completo | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `neuroband` | `telemetria` | `sensores` | `01` | `neuroband/telemetria/sensores/01` | Envío de JSON con datos de MAX30102, GSR y MPU6050. |
| `neuroband` | `comando` | `actuadores` | `01` | `neuroband/comando/actuadores/01` | Recepción de órdenes de control (`ACTIVAR_CALMA` / `ESTADO_SEGURO`). |