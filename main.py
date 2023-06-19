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
from utilities.init_logger import init_logger

logger = init_logger("post_man_logs.txt")

logger.info("Reading configuration")
configuration_path = os.path.join("config", "config.yaml")
configuration = load_yaml(configuration_path)

logger.info("Initializing PostGreSQL")
postgre_interfacer = PostGreSQL(
    configuration["postgresql"]["ip"],
    configuration["postgresql"]["port"],
    configuration["postgresql"]["user"],
    configuration["postgresql"]["password"],
    configuration["postgresql"]["table_name"]
)

logger.info("Initializing leaders")
ping_leader = Leader(configuration["network"], ping_function, postgre_interfacer.insert_data)
power_leader = Leader(configuration["power"], power_function, postgre_interfacer.insert_data)
try:
    logger.info("Starting leaders")
    ping_leader.start()
    power_leader.start()
    logger.info("Leaders started")
    while True:
        time.sleep(1)
except KeyboardInterrupt as inst:
    logger.error(f"Code stopped by Keyboard Interrupt: {inst}")

# Stopping and closing
logger.info("Stopping Leaders")
ping_leader.stop()
power_leader.stop()
logger.info("Stopped Leaders")
postgre_interfacer.close_connection()
logger.info("Stopped interface")
logger.info("Exiting code")
