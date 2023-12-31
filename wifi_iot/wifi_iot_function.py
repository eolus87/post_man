__author__ = "Nicolas Gutierrez"

# Standard libraries
from urllib.request import urlopen
from typing import List, Union
# Third party libraries
from bs4 import BeautifulSoup
# Custom libraries

REQUEST_TIMEOUT = 2


def wifi_iot_request(target: str) -> List[List[Union[str, float]]]:
    """
    Parser of the wifi_iot_sensor/s from response code. Sensor info should be included
    as h3 header level and contain the following format:
    <h3>Sensor_Type Sensor_value Sensor_unit<\h3>

    :param target: ip of the sensor with response web interface
    :return: list with as many lists as sensors and 3 components correctly
    formatted as type_of_sensor, value and unit.
    """

    response = urlopen(f"http://{target}", timeout=REQUEST_TIMEOUT).read()
    soup = BeautifulSoup(response, features="html.parser")
    sensors = soup.find_all("h3")

    list_of_sensors = []
    for sensor in sensors:
        current_sensor = sensor.get_text().splitlines()
        list_of_sensors.append([
            current_sensor[0].strip(),
            float(current_sensor[1]),
            current_sensor[2].strip()
            ]
        )

    return list_of_sensors
