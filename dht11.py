import time
import board
import adafruit_dht
import psutil

global sensor

def dht_initialize(dht_pin):
    global sensor
    # We first check if a libgpiod process is running. If yes, we kill it!
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()
    sensor = adafruit_dht.DHT11(dht_pin, use_pulseio=False)

def dht_run():
    global sensor
    temp = 0
    humidity = 0
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
    except RuntimeError as error:
        print("DHT11 Circuit Error")
        print(error.args[0])
    except Exception as error:
        sensor.exit()
        raise error

    return temp, humidity