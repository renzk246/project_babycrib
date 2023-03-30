from gpiozero import Buzzer, Button, InputDevice
from time import sleep

global buzzer, button
buzzer_condition = False
button_condition = False
irsensor_condition = False

def extra_initialize(buzzer_pin, button_pin, irsensor_pin):
    global buzzer, button, irsensor
    buzzer = Buzzer(buzzer_pin)
    button = Button(button_pin)
    irsensor = InputDevice(irsensor_pin)


def buzzer_run(set):
    global buzzer, buzzer_condition

    if set:
        if not buzzer_condition:
            buzzer.beep(on_time=1,off_time=1,n=None,background=True)
            buzzer_condition = True
    else:
        buzzer.off()
        buzzer_condition = False

def buzzer_init():
    global buzzer
    buzzer.beep(on_time=0.2,off_time=0.2,n=None,background=True)
    sleep(2)
    buzzer.off()


def button_pressed():
    global buzzer, button, button_condition

    if button.is_pressed:
        button_condition = True
        buzzer.beep(on_time=0.2,off_time=0.2,n=None,background=True)
        sleep(1)
        buzzer.off()
        print("Button is Pressed \n")
    else:
        button_condition = False
        buzzer.off()

    return button_condition


def irsensor_sense():
    global irsensor, irsensor_condition

    if irsensor.is_active:
        irsensor_condition = False
    else:
        irsensor_condition = True

    return irsensor_condition