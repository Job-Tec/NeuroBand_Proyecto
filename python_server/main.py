"""
OBJETIVO: Recibir la telemetría de la ESP32 con timestamps, procesar los datos biométricos con la lógica de decisión de la NeuroBand y publicar comandos de control.
INTEGRANTES:
* Sanchez Perez Brian Leonel.
* Navarro Ramos Mario Alberto.
* Estrada Mata José Job de Jesús.
PROYECTO: NeuroBand
"""

import json
import time
from datetime import datetime
import paho.mqtt.client as mqtt

# --- CONFIGURACIÓN MQTT ---
MQTT_BROKER = "localhost"
TOPIC_TELEMETRIA = "neuroband/telemetria/sensores/01"
TOPIC_COMANDOS = "neuroband/comando/actuadores/01"

def on_connect(client, userdata, flags, rc):
    print(f"Servidor conectado al broker con código: {rc}")
    client.subscribe(TOPIC_TELEMETRIA)
    print(f"Escuchando telemetría en: {TOPIC_TELEMETRIA}")

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    try:
        # CORRECCIÓN: Extraer el payload antes de decodificar
        payload = msg.payload.decode()
        datos = json.loads(payload)
        
        pulso = datos["pulso_bpm"]
        sudor = datos["sudoracion_pct"]
        en_movimiento = datos["en_movimiento"]
        
        print(f"[{timestamp}] RECV -> BPM: {pulso} | GSR: {sudor}% | Movimiento: {en_movimiento}")
        
        # LÓGICA DE DECISIÓN
        if pulso > 100 and sudor > 60.0 and not en_movimiento:
            print(f"[{timestamp}] ¡ALERTA! Crisis detectada. Publicando comando de mitigación...")
            client.publish(TOPIC_COMANDOS, "ACTIVAR_CALMA")
        else:
            client.publish(TOPIC_COMANDOS, "ESTADO_NORMAL")
            
    except Exception as e:
        print(f"Error al procesar el mensaje MQTT: {e}")

def main():
    # CORRECCIÓN: Declarar explícitamente la API v1 para evitar el DeprecationWarning
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message

    print("Iniciando el Servidor de Procesamiento NeuroBand...")
    client.connect(MQTT_BROKER, 1883, 60)

    client.loop_forever()

if __name__ == "__main__":
    main()