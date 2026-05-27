"""
OBJETIVO: Conectar a Wi-Fi y Broker MQTT. Publicar telemetria de sensores y suscribirse a comandos de actuadores invocando la HAL.
INTEGRANTES:
* Sanchez Perez Brian Leonel.
* Navarro Ramos Mario Alberto.
* Estrada Mata José Job de Jesús.
PROYECTO: NeuroBand
"""

import time
import network
import ujson
from umqtt.simple import MQTTClient
from dispositivos import SensoresNeuroBand, ActuadoresNeuroBand

# --- CONFIGURACIÓN DE RED Y MQTT ---
WIFI_SSID = ""
WIFI_PASS = ""
MQTT_BROKER = "192.168.1.71"
CLIENT_ID = "NeuroBand_ESP32_01"

# Tópicos basados en el estándar de tu rúbrica
TOPIC_TELEMETRIA = b"neuroband/telemetria/sensores/01"
TOPIC_COMANDOS = b"neuroband/comando/actuadores/01"

# Inicializar HAL (Hardware Abstraction Layer)
sensores = SensoresNeuroBand()
actuadores = ActuadoresNeuroBand()

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
    print("Wi-Fi Conectado:", wlan.ifconfig())

def recepcion_comandos(topic, msg):
    """Callback: Se ejecuta cuando la PC manda una orden por MQTT"""
    comando = msg.decode()
    print(f"Comando recibido en {topic}: {comando}")
    
    # Invocar a la HAL dependiendo del comando recibido
    if comando == "ACTIVAR_CALMA":
        actuadores.iniciar_protocolo_calma()
    elif comando == "ESTADO_SEGURO":
        actuadores.estado_seguro()

def main():
    actuadores.mostrar_mensaje_pantalla("NeuroBand", "Iniciando RED...")
    conectar_wifi()
    
    # Configurar cliente MQTT
    cliente = MQTTClient(CLIENT_ID, MQTT_BROKER)
    cliente.set_callback(recepcion_comandos)
    cliente.connect()
    cliente.subscribe(TOPIC_COMANDOS)
    
    print("Conectado a MQTT. Publicando en:", TOPIC_TELEMETRIA)
    actuadores.mostrar_mensaje_pantalla("Sistema", "En Linea (MQTT)")
    time.sleep(2)
    
    try:
        while True:
            # 1. Revisar si llegaron mensajes (comandos)
            cliente.check_msg()
            
            # 2. Leer sensores usando la HAL
            datos = sensores.obtener_resumen_sensores()
            
            # 3. Formatear datos como JSON y publicar
            payload = ujson.dumps(datos)
            cliente.publish(TOPIC_TELEMETRIA, payload.encode())
            
            print(f"Enviado -> {payload}")
            actuadores.mostrar_mensaje_pantalla(f"BPM:{datos['pulso_bpm']}", f"GSR:{datos['sudoracion_pct']}%")
            
            # Pequeño delay no bloqueante para evitar saturar el broker
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nDesconectando...")
        actuadores.estado_seguro()
        cliente.disconnect()

if __name__ == "__main__":
    main()