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
### Matriz de Tópicos MQTT - Proyecto NeuroBand

| Nivel 1 (Raíz) | Nivel 2 (Flujo) | Nivel 3 (Hardware Mapeado) | Nivel 4 (Nodo) | Tópico Completo (Ruta MQTT) | Tipo de Payload | Descripción de la Trama |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `neuroband` | `telemetria` | `sensores` <br>*(MAX30102, MPU6050, ADC/GSR)* | `01` | **`neuroband/telemetria/sensores/01`** | **JSON** | Publicación (Tx) de la ESP32. Envía un paquete integrado con las 3 variables biométricas continuas: *pulso_bpm (Int), sudoracion_pct (Float), en_movimiento (Bool)*. |
| `neuroband` | `comando` | `actuadores` <br>*(OLED, Motor ERM, Buzzer)* | `01` | **`neuroband/comando/actuadores/01`** | **String** | Suscripción (Rx) de la ESP32. Recibe instrucciones absolutas del servidor (*"ACTIVAR_CALMA"* o *"ESTADO_SEGURO"*) para detonar acciones hápticas, visuales y sonoras. |

---

**Justificación de Arquitectura:**
Se eligió una topología centralizada. En lugar de crear un tópico distinto para cada micro-componente (ej. `.../sensor/pulso`, `.../sensor/giroscopio`), se agruparon los **3 sensores** en una sola ruta de telemetría mediante un empaquetado JSON. De igual forma, los **3 actuadores** responden simultáneamente a un único tópico de comando. Esto reduce drásticamente el tráfico en el Bróker MQTT, previene cuellos de botella en la red local y ahorra memoria RAM en el microcontrolador al gestionar una sola suscripción.
