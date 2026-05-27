# NeuroBand: Interfaz de Bio-Retroalimentación Cognitiva

**OBJETIVO:** Establecer el ecosistema de comunicación definitivo mediante MQTT para conectar una ESP32 con un servidor en Python, integrando sensores biométricos y actuadores hápticos. El proyecto garantiza el desacoplamiento del hardware mediante una capa HAL.
**PROYECTO:** NeuroBand

## Integrantes
* Estrada Mata José Job - [Código]
* Navarro Ramos Mario Alberto - [Código]
* Sanchez Perez Brian Leonel - [Código]

## Arquitectura de Datos
ESP32 -> MQTT (Topic: /bio_data) -> PC (Procesamiento IA) -> MQTT (Topic: /feedback) -> Actuadores (Vibración/OLED)