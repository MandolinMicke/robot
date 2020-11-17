from Communication import Network

import Commands as coms

import time

network = Network('own_master')
# network.setup_publisher()

# time.sleep(1)


# network.send(coms.shutdown())




network.send(coms.sensor_mode('full'))