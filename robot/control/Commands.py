def shutdown():
    return 'shutdown'

def direction(controllername,direction = None):
    basestr = 'direction' + controllername +':'
    if direction != None:
        basestr += str(direction)
    return basestr

def angle(controllername,angle=None):
    basestr = 'angle' + controllername + ':'
    if angle != None:
        basestr += str(angle)
    return basestr

def speed(controllername,speed=None):
    basestr = 'speed' + controllername + ':'
    if speed != None:
        basestr += str(speed)
    return basestr

def get_controller_subs(controllername):
    return [shutdown(),
    direction(controllername),
    angle(controllername),
    speed(controllername)]

