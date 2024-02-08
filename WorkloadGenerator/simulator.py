import random
import json
import paho.mqtt.client as mqtt
import time
import sys

if len(sys.argv) != 2:
    print("Usage: python3 simulator.py <SENSOR ID>")
    sys.exit(1)

indoor_temperature = random.uniform(18, 24) 
#outdoor_temperature = random.uniform(15, 30)  
indoor_humidity = random.uniform(30, 60)  
#outdoor_humidity = random.uniform(20, 70)  
atmospheric_pressure = random.uniform(1010, 1020) 
indoor_light = random.uniform(100, 500)  
#outdoor_light = random.uniform(5000, 10000) 
battery_level = random.uniform(80, 100)

#mqttBroker = "mqtt.eclipseprojects.io"
mqttBroker = "broker.hivemq.com"
mqttClient = mqtt.Client(str(time.time()))
mqttClient.connect(mqttBroker)

# system_id = random.randint(0,10000)
system_id = int(sys.argv[1])

def update_value(current_value, min_value, max_value, smoothing_factor=0.2):

    new_value = random.uniform(min_value, max_value)
    updated_value = (1 - smoothing_factor) * current_value + smoothing_factor * new_value
    return updated_value

def update_battery(currentcharge):
    updated_battery = currentcharge - 0.017
    return updated_battery

def simulate_data():
    global indoor_temperature, outdoor_temperature, indoor_humidity, outdoor_humidity, atmospheric_pressure, indoor_light, outdoor_light, battery_level

    indoor_temperature = update_value(indoor_temperature, 18, 24)
    #outdoor_temperature = update_value(outdoor_temperature, 15, 30)
    indoor_humidity = update_value(indoor_humidity, 30, 60)
    #outdoor_humidity = update_value(outdoor_humidity, 20, 70)
    atmospheric_pressure = update_value(atmospheric_pressure, 1010, 1020)
    indoor_light = update_value(indoor_light, 100, 500)
    #outdoor_light = update_value(outdoor_light, 5000, 10000)
    battery_level = update_battery(battery_level)

def main():
    print("Starting Standard Simulator:", system_id)
    while(True):
        simulate_data()
        sensorTag = {
            "system_id":  system_id,
            "model_number": "Simulated SensorTag",
            "timestamp": time.strftime("%m/%d/%Y %H:%M:%S"),
            "battery_level": int(battery_level),
            "ambient_temperature": indoor_temperature,
            "humidity": indoor_humidity,
            "pressure": atmospheric_pressure,
            "light": indoor_light
        }
        """print(f"Indoor Temperature: {indoor_temperature:.2f} °C")
        print(f"Outdoor Temperature: {outdoor_temperature:.2f} °C")
        print(f"Indoor Humidity: {indoor_humidity:.2f} %rH")
        print(f"Outdoor Humidity: {outdoor_humidity:.2f} %rH")
        print(f"Atmospheric Pressure: {atmospheric_pressure:.2f} mbar")
        print(f"Indoor Light: {indoor_light:.2f} lux")
        print(f"Outdoor Light: {outdoor_light:.2f} lux") """

        sensorJSON = json.dumps(sensorTag)
        response = mqttClient.publish("TISENSORTAGDATA", sensorJSON)
        response.wait_for_publish() 
        # print("-----------------------------------------")
        # print(response.is_published())
        # print("-----------------------------------------")
        

        time.sleep(5)

if __name__ == "__main__":
    main()
