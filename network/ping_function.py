__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import List, Union
# Third party libraries
from pythonping import ping
# Custom libraries


def ping_function(target: str) -> List[List[Union[str, float]]]:
    response = ping(target, count=1, verbose=False)
    return [["ping", response.rtt_avg_ms, "ms"]]
