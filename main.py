__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
import time
# Custom libraries
# Third party libraries
from utilities.utilities import load_yaml
from labourers.leader import Leader
from network.ping_function import ping_function
from power.power_function import power_function
from interfaces.postgresql import PostGreSQL


configuration_path = os.path.join("config", "config.yaml")
configuration = load_yaml(configuration_path)

# Intefaces initialization
# postgre_interfacer = PostGreSQL(
#     configuration["database"]["ip"],
#     configuration["database"]["port"],
#     configuration["database"]["user"],
#     configuration["database"]["password"],
#     configuration["database"]["tablename"]
# )

# Initialization network
ping_leader = Leader(configuration["network"], ping_function)
try:
    ping_leader.start()
    while True:
        print("In the loop")
        time.sleep(1)
except KeyboardInterrupt as inst:
    print(f"Error: {inst}")

print("Stopping Ping Leader")
ping_leader.stop()
print("Stopped Ping Leader")
print("Exiting code")

# Initialization energy
# power_leader = Leader(configuration["energy"], power_function)
# power_leader.start()

