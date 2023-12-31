__author__ = "Nicolas Gutierrez"

# Standard libraries
from dataclasses import dataclass, field
import datetime
# Third party libraries
# Custom libraries


@dataclass(frozen=True)
class DataPoint:
    """
    Data Class to store the data measured by a single sensor
    in a single point in time. It is frozen, so it will error
    if any method tries to modify the data on it.

    :param time_stamp: Time in format datetime of the data sampled
    :param type: String with the type of sensor, e.g. "power", "ping"...
    :param target: String with the ip of the sensor
    :param value: Data value extracted from the sensor
    :param unit: Unit of the value extracted from the sensor
    """

    time_stamp: datetime.datetime = field(init=True, repr=True)
    type: str = field(init=True, repr=True)
    target: str = field(init=True, repr=True)
    value: float = field(init=True, repr=True)
    unit: str = field(init=True, repr=True)


