def shutdown():
    return 'shutdown'

def speed(controllername,speed=None):
    basestr = 'speed' + controllername + ':'
    if speed != None:
        basestr += str(speed)
    return basestr

def get_controller_subs(controllername):
    return [shutdown(),
    speed(controllername)]

def sensor_distance(distance=None,angle=None,std=None):
    basestr = 'distance: '
    if distance != None:
        basestr += str(distance) + ',' + str(angle) + ',' + str(std)
    return basestr
