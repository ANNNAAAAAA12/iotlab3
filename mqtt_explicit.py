import time
import json
import base64
import hmac
import hashlib
import urllib.parse
import ssl
import paho.mqtt.client as mqtt
from azure.iot.device import ProvisioningDeviceClient

# --- CREDENCIALES EXACTAS DE TU MENSAJE ---
ID_SCOPE = "0ne010B81EB"
DEVICE_ID = "26a1012qbj0"
PRIMARY_KEY = "d6ODIUmamaN88mljj0DeC605Rvho65ymOTrzR3CAhkg="

# 1. Obtención del IoT Hub mediante DPS
print(f"Obteniendo IoT Hub para {DEVICE_ID}...")
prov_client = ProvisioningDeviceClient.create_from_symmetric_key(
    provisioning_host="global.azure-devices-provisioning.net",
    registration_id=DEVICE_ID,
    id_scope=ID_SCOPE,
    symmetric_key=PRIMARY_KEY,
)

reg_result = prov_client.register()
IOT_HUB_HOSTNAME = reg_result.registration_state.assigned_hub
PORT = 8883
print(f"-> ¡ÉXITO! IoT Hub resuelto: {IOT_HUB_HOSTNAME}")

# 2. Generación del token SAS para Paho MQTT
def generate_sas_token(uri, key, expiry=3600):
    ttl = int(time.time()) + expiry
    sign_key = base64.b64decode(key)
    to_sign = f"{urllib.parse.quote_plus(uri)}\n{ttl}".encode('utf-8')
    signature = hmac.new(sign_key, to_sign, hashlib.sha256).digest()
    raw_sig = base64.b64encode(signature).decode('utf-8')
    return f"SharedAccessSignature sr={urllib.parse.quote_plus(uri)}&sig={urllib.parse.quote_plus(raw_sig)}&se={ttl}"

username = f"{IOT_HUB_HOSTNAME}/{DEVICE_ID}/?api-version=2021-04-12"
password = generate_sas_token(f"{IOT_HUB_HOSTNAME}/devices/{DEVICE_ID}", PRIMARY_KEY)
telemetry_topic = f"devices/{DEVICE_ID}/messages/events/"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\n[MQTT Explícito] ¡Conectado correctamente a Azure IoT Central!")
    else:
        print(f"\n[MQTT Explícito] Error de conexión: {rc}")

def on_publish(client, userdata, mid):
    print(f"[MQTT Explícito] Telemetría enviada a Azure (MID: {mid})")

# 3. Configuración del cliente MQTT
client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(username=username, password=password)
client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)

client.on_connect = on_connect
client.on_publish = on_publish

print(f"Conectando a {IOT_HUB_HOSTNAME}:{PORT}...")
client.connect(IOT_HUB_HOSTNAME, PORT, keepalive=60)
client.loop_start()

try:
    contador = 0
    while True:
        payload = {
            "temperatura": round(21.0 + (contador % 6) * 0.5, 2),
            "humedad": round(50.0 + (contador % 4) * 1.5, 2),
            "voltaje": round(3.3 - (contador % 3) * 0.1, 2)
        }
        json_data = json.dumps(payload)
        client.publish(telemetry_topic, json_data, qos=1)
        print(f"-> Publicando: {json_data}")
        contador += 1
        time.sleep(10)
except KeyboardInterrupt:
    print("\nDeteniendo...")
    client.loop_stop()
    client.disconnect()
