import asyncio
import json
import random
from azure.iot.device.aio import ProvisioningDeviceClient, IoTHubDeviceClient
from azure.iot.device import Message

# Datos de tu dispositivo
SCOPE_ID = "0ne010B81EB"
DEVICE_ID = "esp32-wokwi-01"
GROUP_KEY = "IRrqiazJyBWP0HdAAHOZV3W1EImTudCY6IS2478hbvI="
PROVISIONING_HOST = "global.azure-devices-provisioning.net"

async def main():
    print(f"1. Aprovisionando {DEVICE_ID} mediante DPS en Azure IoT Central...")
    
    # Cliente DPS que registra el dispositivo automáticamente usando el Scope ID
    provisioning_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=PROVISIONING_HOST,
        registration_id=DEVICE_ID,
        id_scope=SCOPE_ID,
        symmetric_key=GROUP_KEY
    )

    # Registrar el dispositivo
    results = await provisioning_client.register()

    if results.status == "assigned":
        print(f"-> Aprovisionamiento exitoso!")
        print(f"-> Conectando a IoT Hub: {results.registration_state.assigned_hub}")

        # Cliente IoT Hub con los datos obtenidos por DPS
        device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=GROUP_KEY,
            hostname=results.registration_state.assigned_hub,
            device_id=results.registration_state.device_id
        )

        await device_client.connect()
        print("\n--- ESP32 WOKWI CONECTADO EXITOSAMENTE A AZURE ---")

        contador = 0
        while True:
            datos = {
                "temperatura": round(21.5 + (contador % 6) * 0.5, 2),
                "humedad": round(55.0 + (contador % 4) * 1.5, 2),
                "iluminacion": random.randint(550, 780)
            }
            msg = Message(json.dumps(datos))
            msg.content_encoding = "utf-8"
            msg.content_type = "application/json"

            await device_client.send_message(msg)
            print(f"-> [WOKWI ESP32] Telemetría enviada: {datos}")
            
            contador += 1
            await asyncio.sleep(10)
    else:
        print(f"Error al aprovisionar el dispositivo: {results.status}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSimulador detenido.")
