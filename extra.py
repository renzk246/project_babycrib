from gpiozero import Buzzer, Button

global buzzer, button
buzzer_condition = False
button_condition = True

def extra_initialize(buzzer_pin, button_pin):
    global buzzer, button
    buzzer = Buzzer(buzzer_pin)
    button = Button(button_pin)


def buzzer_run(set):
    global buzzer, buzzer_condition

    if set:
        if not buzzer_condition:
            buzzer.beep(on_time=1,off_time=1,n=None,background=True)
            buzzer_condition = True
    else:
        buzzer.off()
        buzzer_condition = False


def button_pressed():
    global button, button_condition

    if button.is_pressed:
        button_condition = not button_condition
        print("Button is Pressed \n")

    return button_condition