
STATION_ADDRESS = "192.168.10.61" 
SELF = "192.168.10.68"

# STATION_ADDRESS = "192.168.8.106" 
# SELF = "192.168.8.110"

nodes = dict()
nodes['master'] = [STATION_ADDRESS,8000]
nodes['joystick'] = [STATION_ADDRESS,8001]
nodes['own_master'] = [SELF,8000]
nodes['motor1'] = [SELF,8010]
nodes['motor2'] = [SELF,8011]
nodes['uss1'] = [SELF,8020]
nodes['uss2'] = [SELF,8021]
