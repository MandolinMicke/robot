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

