from gpiozero import Motor
from time import sleep

motor_on = False
last_speed = 0
stop_value = 0.3

def motor_initialize(L_PWM, R_PWM, EN):
  global motor
  motor = Motor(L_PWM, R_PWM, EN)


def motor_run(value, max_speed, motor_timeRise, irsensor_status):
  global motor, status, motor_on, last_speed
  global stop_value

  if value:
    if not motor_on:
      for i in range(101):
        speed = mapf(i, 0, 100, 0, max_speed)
        motor.forward(speed)
        sleep(motor_timeRise)
      motor_on = True
    status = "forward"

  else:
    if motor_on:
      for i in range(101):
        speed = mapf(i, 0, 100, max_speed, stop_value)
        last_speed = speed
        motor.forward(speed)
        sleep(motor_timeRise)
      motor_on = False

    else:
      if ((last_speed <= stop_value) and (irsensor_status)):
        motor.forward(0)
        motor.stop()
        status = "stop"

  return status


### Mapping Value
def mapf(value: float, fromLow: float, fromHigh: float, toLow: float, toHigh: float):
  result = (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow
  return result
