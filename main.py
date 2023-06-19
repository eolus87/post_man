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

# Load configuration
configuration_path = os.path.join("config", "config.yaml")
configuration = load_yaml(configuration_path)

# Interface initialization
postgre_interfacer = PostGreSQL(
    configuration["postgresql"]["ip"],
    configuration["postgresql"]["port"],
    configuration["postgresql"]["user"],
    configuration["postgresql"]["password"],
    configuration["postgresql"]["table_name"]
)

# Initialization of leaders
ping_leader = Leader(configuration["network"], ping_function, postgre_interfacer.insert_data)
power_leader = Leader(configuration["power"], power_function, postgre_interfacer.insert_data)
# Starting leaders
try:
    ping_leader.start()
    power_leader.start()
    while True:
        print("In the loop")
        time.sleep(1)
except KeyboardInterrupt as inst:
    print(f"Error: {inst}")

# Stopping and closing
print("Stopping Leaders")
ping_leader.stop()
power_leader.stop()
print("Stopped Leaders")
postgre_interfacer.close_connection()
print("Stopped interface")
print("Exiting code")
