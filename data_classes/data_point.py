__author__ = "Nicolas Gutierrez"

# Standard libraries
from dataclasses import dataclass, field
import datetime
# Third party libraries
# Custom libraries


@dataclass(frozen=True)
class DataPoint:
    """
    Data Class to store the data measured by a single sensor in a single point in time.
    """

    time_stamp: datetime.datetime = field(init=True, repr=True)
    type: str = field(init=True, repr=True)
    target: str = field(init=True, repr=True)
    value: float = field(init=True, repr=True)
    unit: str = field(init=True, repr=True)


