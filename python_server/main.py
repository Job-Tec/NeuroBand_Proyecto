"""
OBJETIVO: Servidor MQTT que procesa telemetría y evalúa crisis de ansiedad.
INTEGRANTES: 
* Sanchez Perez Brian Leonel 
* Navarro Ramos Mario Alberto - 22240328
* Estrada Mata José Job de Jesús - 21240142
PROYECTO: NeuroBand - Interfaz de Bio-Retroalimentación Cognitiva
"""
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# ==========================================
# CONFIGURACIÓN MQTT 
# ==========================================
BROKER = "172.20.10.2" 

# Tópicos
TOPICO_TELEMETRIA = "neuroband/telemetria/sensores/01"
TOPICO_COMANDO = "neuroband/comando/actuadores/01"

# ==========================================
# CALLBACKS
# ==========================================
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código:", rc)
    client.subscribe(TOPICO_TELEMETRIA)
    print(f"Escuchando telemetría en: {TOPICO_TELEMETRIA}")

def on_message(client, userdata, msg):
    # 1. Obtener la hora exacta
    hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # Decodificar el JSON que manda la ESP32
        payload = json.loads(msg.payload.decode('utf-8'))
        pulso = payload.get("pulso_bpm", 0)
        sudor = payload.get("sudoracion_pct", 0)
        movimiento = payload.get("en_movimiento", False)
        
        # Imprimir en consola con formato Timestamp 
        print(f"[{hora_actual}] Telemetría -> BPM: {pulso} | GSR: {sudor}% | Agitación: {movimiento}")
        
        # ---------------------------------------------------------
        # 2. LÓGICA DE DECISIÓN DE CRISIS
        # ---------------------------------------------------------
        # Si el pulso es mayor a 100 Y la persona está agitada (movimiento = True)
        if pulso > 100 and movimiento == True:
            print(f"[{hora_actual}] ¡ALERTA DE CRISIS DETECTADA! Enviando comando ACTIVAR_CALMA...")
             
             #Palabra clave para activar topico
            client.publish(TOPICO_COMANDO, "ACTIVAR_CALMA")
            
        else:
            # ¡Palabra clave para activar topico
            client.publish(TOPICO_COMANDO, "ESTADO_SEGURO")
            
    except Exception as e:
        print(f"[{hora_actual}] Error al procesar mensaje: {e}")

# ==========================================
# BUCLE PRINCIPAL
# ==========================================
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Iniciando servidor de monitoreo NeuroBand...")
# Nos conectamos al broker que está corriendo en la IP 
client.connect(BROKER, 1883, 60)
client.loop_forever()