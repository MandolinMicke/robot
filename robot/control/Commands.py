#### common

def decoder(message):
    data =  message.split(':')[1]
    if ',' in data:
        return [float(x) for x in data.split(',')]
    else:
        return float(data)


#### geneneric

def shutdown():
    return 'shutdown'



#### for motor control

def speed(controllername,speed=None):
    basestr = 'speed' + controllername + ':'
    if speed != None:
        basestr += str(speed)
    return basestr


#### commands for sensors
def sensor_distance(distance=None,angle=None,std=None):
    basestr = 'distance: '
    if distance != None:
        basestr += str(distance) + ',' + str(angle) + ',' + str(std)
    return basestr

def sensor_mode(mode=None):
    basestr = 'mode: ' 
    if mode:
        basestr += mode
    return basestr

def sensor_resolution(res=None):
    basestr = 'resolution: ' 
    if res:
        basestr += res
    return basestr   

def sensor_fov(fov=None):
    basestr = 'fov: ' 
    if fov:
        basestr += fov
    return basestr


#### subscriptions
def get_controller_subs(controllername):
    return [shutdown(),
    speed(controllername)]

def get_uss_subs():
    return [shutdown(),
    sensor_resolution(),
    sensor_fov(),
    sensor_mode()]