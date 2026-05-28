# PROYECTO: NeuroBand: Interfaz de Bio-Retroalimentacion Cognitiva
# INTEGRANTES:
# *Sanchez Perez Brian Leonel. - 22240489
# *Navarro Ramos Mario Alberto. - 22240328
# *Estrada Mata José Job de Jesús. - 21240142
# DESCRIPCION: Biblioteca HAL (Hardware Abstraction Layer) que centraliza y 
# abstrae la lectura de los sensores (Pulso, GSR, MPU6050) y el control 
# de los actuadores (Motor ERM, OLED, Buzzer).

from machine import Pin, ADC, PWM, I2C
import time

class SensoresNeuroBand:
    """
    Clase encargada de la gestion, lectura y estabilizacion de los sensores biometricos.
    """
    def __init__(self):
        # 1. Sensor GSR (Respuesta Galvanica de la Piel) - Lectura Analogica
        self.sensor_gsr = ADC(Pin(32))
        self.sensor_gsr.atten(ADC.ATTN_11DB) 
        
        # Calibracion empirica del ADC para evitar no-linealidad en los extremos
        self.GSR_SECO_REF = 3500  # Valor base en estado de calma total
        self.GSR_SUDOR_REF = 1000 # Valor base bajo estrés/sudoracion maxima
        
        # Bus I2C compartido (NOTA HARDWARE: Asegurar resistencias pull-up 4.7kOhm hacia 3.3V en SDA y SCL)
        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        
        self.historial_pulso = [70, 70, 70] 

    def leer_sudoracion_porcentaje(self):
        """
        Lee el sensor GSR mediante ADC con mapeo calibrado.
        Retorna: El nivel de conductividad (0-100%).
        """
        valor_crudo = self.sensor_gsr.read()
        
        # Restriccion de limites para evitar porcentajes negativos o mayores a 100
        if valor_crudo > self.GSR_SECO_REF: valor_crudo = self.GSR_SECO_REF
        if valor_crudo < self.GSR_SUDOR_REF: valor_crudo = self.GSR_SUDOR_REF
        
        # Mapeo invertido: A menor resistencia (menor valor ADC), mayor porcentaje de sudoracion
        rango_total = self.GSR_SECO_REF - self.GSR_SUDOR_REF
        porcentaje = ((self.GSR_SECO_REF - valor_crudo) / rango_total) * 100.0
        return round(porcentaje, 1)

    def leer_pulso_estabilizado(self):
        lectura_actual = 85 
        self.historial_pulso.pop(0) 
        self.historial_pulso.append(lectura_actual) 
        promedio = sum(self.historial_pulso) / len(self.historial_pulso)
        return int(promedio)

    def detectar_movimiento(self):
        usuario_en_movimiento = False 
        return usuario_en_movimiento

    def obtener_resumen_sensores(self):
        return {
            "pulso_bpm": self.leer_pulso_estabilizado(),
            "sudoracion_pct": self.leer_sudoracion_porcentaje(),
            "en_movimiento": self.detectar_movimiento()
        }


class ActuadoresNeuroBand:
    """
    Clase encargada del control de actuadores para la bio-retroalimentacion.
    """
    def __init__(self):
        self.motor_haptico = PWM(Pin(18), freq=1000)
        self.motor_haptico.duty(0)
        
        self.zumbador = PWM(Pin(19))
        self.zumbador.duty(0)
        
        self.i2c_pantalla = I2C(1, scl=Pin(25), sda=Pin(26))

    def mostrar_mensaje_pantalla(self, linea1, linea2=""):
        print(f"[OLED] {linea1} | {linea2}") 

    def dar_pulso_haptico(self, intensidad, duracion_ms):
        self.motor_haptico.duty(intensidad)
        time.sleep_ms(duracion_ms)
        self.motor_haptico.duty(0)

    def emitir_frecuencia_relajacion(self):
        self.zumbador.freq(432) 
        self.zumbador.duty(512) 

    def apagar_zumbador(self):
        """Apaga la senal PWM del buzzer pasivo."""
        self.zumbador.duty(0)

    def iniciar_protocolo_calma(self):
        self.mostrar_mensaje_pantalla("Respira...", "Inhala profundo")
        self.emitir_frecuencia_relajacion()
        self.dar_pulso_haptico(800, 1000) 
        self.apagar_zumbador() 

    def estado_seguro(self):
        self.motor_haptico.duty(0)
        self.apagar_zumbador()
        self.mostrar_mensaje_pantalla("SISTEMA", "EN REPOSO")