import os

from audioClassification import *
from dht11 import *
from extra import *
from motor import *


#=====  SETTINGS  =====#
# Model Yamnet Setting
model = 'yamnet.tflite'                         # Model File Path.
max_results = 5                                 # Max number of results to output.
score_threshold = 0.0                           # The score threshold of classification results.
overlapping_factor = 0.5                        # Target overlapping between adjacent inferences. Value must be in (0, 1).
num_threads = 4                                 # Number of CPU threads to run the model.
enable_edgetpu = False                          # Whether to run the model on EdgeTPU.

# Pin Assignments
dht_pin = board.D23                             # DHT11 Pin
buzzer_pin = 21                                 # Buzzer Pin
button_pin = 16                                 # Button Pin
L_PWM = 26                                      # H-Bridge Controller L-PWM Pin
R_PWM = 19                                      # H-Bridge Controller R-PWM Pin
EN = 13                                         # H-Bridge Controller ENABLE Pin

# Function Settings
max_temp = 35                                   # Maximum Temperature of the Environment.
min_humidity = 70                               # Minimum Humidity of the Environment.
max_speed = 0.5                                 # Maximum Speed Value (0-1).
motor_delay = 10                                # Delay for a Motor to stop after it cannot detect a sound of a baby crying (seconds).
motor_maxTime = 30                              # Maximum time for a Motor run and trigger the alarm (seconds).


#=====   MAIN    =====#
def main():
    global current_time, previous_time, time_count, time_debug, time_dht, time_motor, maxtime_motor
    global temp, humidity, max_temp, min_humidity, max_speed, motor_switch, motor_buzzer, button_status, audio_detected

    # Audio Classification
    indexes, category_results, score_results = audio_run(max_results)

    # DHT11
    if ((time_count-time_dht) >= 1):
        dht_sense = dht_run()
        if ((dht_sense[0] != None) and (dht_sense[1] != None)):
            if ((dht_sense[0] > 0) and (dht_sense[1] > 0)):
                temp, humidity = dht_sense
        time_dht = time_count


    # Motor
    if button_status and not motor_buzzer:
        for i in range(max_results):
            index = indexes[i]
            if (index == 20):                       # 20 for Baby Crying; 19 for Crying
                motor_switch = True
                time_motor = time_count
                audio_detected = True
                if (maxtime_motor == 0):
                    maxtime_motor = time_count
        if audio_detected:
            if ((time_count-maxtime_motor) > motor_maxTime):
                motor_switch = False
                maxtime_motor = 0
                motor_buzzer = True
                audio_detected = False
            elif ((time_count-time_motor) > motor_delay):
                motor_switch = False
                maxtime_motor = 0
                audio_detected = False
    motor_status = motor_run(motor_switch, max_speed, time_count)


    # Buzzer
    if button_pressed():
        if not motor_buzzer:
            if ((temp > max_temp) or (humidity < min_humidity)):
                if ((temp > 0) or (humidity > 0)):
                    buzzer_run(True)
            else:
                 buzzer_run(False)
        else:
            buzzer_run(True)
        button_status = True
    else:
        buzzer_run(False)
        motor_buzzer = False
        motor_switch = False
        button_status = False

    # Debug Print
    if ((time_count-time_debug)>=1):
        print(f'Current event: \n')
        for i in range(max_results):
            index = indexes[i]
            category_result = category_results[i]
            score_result = score_results[i]
            print('    {:}: {:12s}: {:.3f} \n'.format(index, category_result, score_result))
        print('  temp: {}, humidity: {}, motor: {}, button: {}\n'.format(temp, humidity, motor_status, button_status))
        print("===========================================================")
        time_debug = time_count



if __name__ == '__main__':
    # Timer
    current_time = time.time()
    previous_time = time.time()
    time_count = 0
    time_debug = 0
    time_dht = 0

    # Model Initialization
    audio_initialize(model, max_results, score_threshold,
                    overlapping_factor, num_threads, enable_edgetpu)
    audio_detected = False

    # DHT11 Initialization
    dht_initialize(dht_pin)
    temp = 0.0
    humidity = 0.0

    # Motor Driver
    motor_initialize(L_PWM, R_PWM, EN)
    motor_switch = False
    time_motor = 0
    maxtime_motor = 0
    motor_buzzer = False

    # Extra Initialization
    extra_initialize(buzzer_pin, button_pin)
    button_status = True

    while True:
        main()

        # Timer
        time_count = current_time - previous_time
        current_time = time.time()