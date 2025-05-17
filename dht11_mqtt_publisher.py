import paho.mqtt.client as mqtt
import time
import json
import Adafruit_DHT

# MQTT Configuration
MQTT_BROKER = "broker.hivemq.com"  # Change to your broker IP if needed
MQTT_PORT = 1883
MQTT_TOPIC = "pi/dht"
CLIENT_ID = "8y1TqdmY45"

# Sensor Setup
SENSOR = Adafruit_DHT.DHT11
SENSOR_PIN = 4

# MQTT Connection Callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Connection failed with code {rc}")

# Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT)

# Read Sensor Data Function
def read_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, SENSOR_PIN)
    if humidity is not None and temperature is not None:
        return {"temp": temperature, "humidity": humidity}
        print(temperature + humidity )
    return None

# Start MQTT Loop and Publish Data
try:
    client.loop_start()
    while True:
        data = read_sensor()
        print(data)
        if data:
            client.publish(MQTT_TOPIC, json.dumps(data), qos=1)
            print(f"Published: {data}")
        time.sleep(5)  # Send every 5 seconds
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Script stopped.")
