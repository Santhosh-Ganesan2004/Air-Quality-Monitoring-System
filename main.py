import machine
import time
import dht
import urequests
import json
import network
# WiFi credentials
ssid = #<hotspor name in ''>
password = #<hotspot password in ''>
# DHT and MQ135 sensor pins
dht_pin = machine.Pin(27)
mq135_pin = machine.ADC(26)
# DHT11 sensor object
dht_sensor = dht.DHT11(dht_pin)
# Firebase Realtime Database URL
firebase_url = #your firebase url''
# Blynk HTTP API
BLYNK_AUTH_TOKEN = # <your blynk authentication token>
blynk_base_url = f'https://blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}'
# Mapping of data to virtual pins for Blynk
blynk_virtual_pins = {
 'temperature': 'V0',
 'humidity': 'V1',
 'nh3': 'V2',
 'nox': 'V3',
 'alcohol': 'V4',
 'benzene': 'V5',
 'smoke': 'V6',
 'co2': 'V7'
}
# Simulated MQ135 sensor read (placeholder logic)
def read_mq135():
 raw_value = mq135_pin.read_u16()
 voltage = raw_value / 65535 * 3.3 # Convert raw ADC value to voltage
 # Simulated sensor data calculations
 nh3 = voltage * 10
 nox = voltage * 20
 alcohol = voltage * 30
 benzene = voltage * 40
 smoke = voltage * 50
 co2 = voltage * 60
 return nh3, nox, alcohol, benzene, smoke, co2
# Upload to Firebase
def send_to_firebase(data):
 try:
 response = urequests.post(firebase_url, headers={'Content-Type': 'application/json'},
data=json.dumps(data))
 print("Firebase Response:", response.text)
 response.close()
 except Exception as e:
 print("Failed to upload to Firebase:", e)
# Upload to Blynk
def send_to_blynk(data):
 try:
 for key, virtual_pin in blynk_virtual_pins.items():
 if key in data:
 url = f'{blynk_base_url}&{virtual_pin}={data[key]}'
 urequests.get(url).close()
 print("Data sent to Blynk")
 except Exception as e:
 print("Failed to send data to Blynk:", e)
# Connect to WiFi
def connect_wifi(ssid, password):
 wlan = network.WLAN(network.STA_IF)
 wlan.active(True)
 wlan.connect(ssid, password)

 # Wait for connection
 while not wlan.isconnected():
 print("Connecting to WiFi...")
 time.sleep(1)
 print("Connected to WiFi")
 print("IP Address:", wlan.ifconfig())
# Generate human-readable timestamp
def get_timestamp():
 # Get the current time (UNIX epoch time in seconds)
 unix_time = time.time()

 # Calculate hours, minutes, and seconds
 days = int(unix_time // (24 * 3600))
 hours = int((unix_time % (24 * 3600)) // 3600)
 minutes = int((unix_time % 3600) // 60)
 seconds = int(unix_time % 60)

 # Return formatted string
 return f"Days:{days} {hours:02}:{minutes:02}:{seconds:02}"
# Main loop
def main():
 connect_wifi(ssid, password)

 while True:
 try:
 # Read data from DHT11 sensor
 dht_sensor.measure()
 temp = dht_sensor.temperature()
 dht_sensor.humidity()
 # Read data from MQ135 sensor
 nh3, nox, alcohol, benzene, smoke, co2 = read_mq135()
 # Print sensor data
 print(f"Temp: {temp}°C Hum: {hum}%")
 print(f"CO2: {co2} ppm Smoke: {smoke} ppm NH3: {nh3} ppm")
 print(f"NOX: {nox} ppm Alcohol: {alcohol} ppm Benzene: {benzene} ppm")
 # Add timestamp and sensor data to dictionary
 timestamp = get_timestamp()
 data = {
 'timestamp': timestamp,
 'temperature': temp,
 'humidity': hum,
 'nh3': nh3,
 'nox': nox,
 'alcohol': alcohol,
 'benzene': benzene,
 'smoke': smoke,
 'co2': co2
 }
 # Send data to Firebase and Blynk
 send_to_firebase(data)
 send_to_blynk(data)
 except Exception as e:
 print("Error:", e)
 # Wait for 20 seconds before the next iteration
 time.sleep(20)
# Run the code
if _name_ == '_main_':
 main()
