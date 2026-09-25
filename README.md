# Laboratorio 3: Conexión y Concurrencia IoT en Azure IoT Central

Este repositorio contiene la solución completa para el **Laboratorio 3**, enfocado en la transmisión simultánea de telemetría desde múltiples dispositivos hacia la plataforma **Azure IoT Central**.

---

## Dispositivos Configurados

### 1. `Dev-Python-VM` (`mqtt_explicit.py`)
* **Protocolo:** MQTT explícito sobre TLS (Puerto 8883) usando `paho-mqtt`.
* **Autenticación:** Firma HMAC-SHA256 con Token SAS derivado de la clave simétrica.
* **Telemetría enviada:** `temperatura`, `humedad` y `voltaje`.

### 2. `esp32-wokwi-01` (`wokwi_sim.py`)
* **Protocolo:** SDK oficial de Azure (`azure-iot-device`).
* **Autenticación:** Aprovisionamiento dinámico mediante **DPS** (`Scope ID: 0ne010B81EB`).
* **Telemetría enviada:** `temperatura`, `humedad` e `iluminacion`.

---

## Archivos del Repositorio
* `mqtt_explicit.py`: Script de la Máquina Virtual Python con firma SAS manual.
* `wokwi_sim.py`: Script del simulador ESP32 Wokwi con registro por DPS.
* `README.md`: Documentación del proyecto.

---

## Instrucciones de Ejecución

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/ANNNAAAAAA12/iotlab3.git](https://github.com/ANNNAAAAAA12/iotlab3.git)
   cd iotlab3
