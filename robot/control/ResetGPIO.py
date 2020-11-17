
import RPi.GPIO as gpio


ALLPINS = [
    2,3,4,
    17,27,22,
    10,9,11,
    5,6,13,19,26,
    18,
    23,24,
    25,8,7,
    12,
    16,20,21]

def reset_pins(pins = None):

    if pins == None:
        pins = ALLPINS
    gpio.setmode(gpio.BCM)
    for i in pins:
        gpio.setup(i,gpio.OUT)
        gpio.output(i,False)



if __name__ == "__main__":
    reset_pins()
    # gpio.cleanup()