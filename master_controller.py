from Communication import Network

import Commands as coms

import time

network = Network('own_master')
# network.setup_publisher()

# time.sleep(1)

# network.send(coms.direction('motor1',-1))

network.send(coms.speed('motor1',0.001))

# network.send(coms.angle('motor1',3.14))
network.send(coms.angle('motor1',3*3.14))
# network.send(coms.shutdown())
