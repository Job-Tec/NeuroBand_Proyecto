# Reporte de Análisis Individual - Proyecto NeuroBand

**OBJETIVO:** Documentar los problemas técnicos individuales, soluciones aplicadas y conclusiones sobre el desarrollo del proyecto.
**PROYECTO:** NeuroBand

---

## 1. Integrante: Sanchez Perez Brian Leonel - 22240489

* **Problema encontrado:** Al principio batallamos mucho porque cuando queríamos correr el programa en la ESP32, nos salía el error `ImportError: no module named 'dispositivos'`. Además, al inicio teníamos toda la lógica de los `if` metida en la misma placa, lo cual no cumplía con la regla de separar las cosas por MQTT.
* **Solución aplicada:** Nos dimos cuenta que el archivo de los sensores solo estaba en la computadora y no en la pulsera. Usamos Thonny para guardar `dispositivos.py` directamente en la memoria de la ESP32. También, borramos las decisiones de la placa y pasamos todo ese código al script de Python de la compu.
* **Conclusión personal:** Aprendí que es mucho mejor dejar que la computadora haga el trabajo pesado (pensar y tomar decisiones) y que la ESP32 solo se dedique a recolectar datos y hacer vibrar el motor. Así el microcontrolador no se satura y el sistema corre más fluido.

---

## 2. Integrante: Navarro Ramos Mario Alberto - 22240328

* **Problema encontrado:** A la hora de conectar algunos sensores en físico, tuvimos detalles con el hardware. El sensor de sudor (GSR) nos daba valores muy inestables y hasta negativos. Y por otro lado, cuando mandábamos la orden para relajar al usuario, el zumbador empezaba a sonar pero nunca se callaba, se quedaba pitando para siempre.
* **Solución aplicada:** En el archivo de los sensores (la HAL), le pusimos límites fijos al GSR (un valor para seco y otro para mojado) para que no se saliera de los rangos. Para el zumbador, tuvimos que crear una función nueva llamada `apagar_zumbador()` y ponerla justo al final del ciclo de relajación para cortarle la corriente.
* **Conclusión personal:** Hacer la capa HAL fue una salvación. Gracias a que teníamos los sensores separados en otro archivo, pudimos estar haciendo pruebas, moviendo cables y cambiando números sin miedo a echar a perder la conexión MQTT que ya nos había costado trabajo hacer funcionar.

---

## 3. Integrante: Estrada Mata José Job de Jesús - 21240142

* **Problema encontrado:** Configurar el servidor en Windows fue un dolor de cabeza. Primero, la terminal no me dejaba instalar la librería `paho-mqtt` por un conflicto con otras versiones de Python que tenía instaladas. Luego, cuando por fin conectó a Mosquitto, el programa crasheaba y se cerraba al recibir el primer dato de la placa porque no entendía el mensaje.
* **Solución aplicada:** Para que instalara bien la librería, tuve que obligar a Windows a usar el Python principal usando el comando `py -m pip`. Para el error de los mensajes, modificamos el código agregando `.payload.decode()` para desempaquetar el texto plano antes de intentar leerlo como JSON.
* **Conclusión personal:** Hacer que dos dispositivos se comuniquen en red local tiene sus mañas, especialmente por los puertos y los entornos de Windows. También me quedó claro que en MQTT no puedes nomás leer el mensaje directo, tienes que decodificar la carga útil (payload) para que Python entienda los datos.