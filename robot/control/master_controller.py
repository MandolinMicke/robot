from Communication import Network

import Commands as coms

import time

network = Network('master')
# network.setup_publisher()

# time.sleep(1)


network.send(coms.shutdown())


# network.send(coms.sensor_resolution(15))
# network.send(coms.sensor_fov(3.14))
# network.send(coms.sensor_mode(3))

# for i in range(20):
    
#     network.send(coms.sensor_mode(2))
#     time.sleep(1)