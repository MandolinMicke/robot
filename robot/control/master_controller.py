from Communication import Network

import Commands as coms

import time

network = Network('master')
network.setup_publisher()

time.sleep(1)

# network.send(coms.direction('motor1',-1))

network.send(coms.speed('motor1',0.0005))

# network.send(coms.angle('motor1',3.14))

# network.send(coms.shutdown())


from pynput import keyboard

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()