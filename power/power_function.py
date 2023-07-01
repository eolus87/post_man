__author__ = "Nicolas Gutierrez"

# Standard libraries
import platform
import asyncio
from typing import List, Union
# Third party libraries
import kasa
# Custom libraries

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def power_request(target: str) -> float:
    plug = kasa.SmartPlug(target)
    await plug.update()
    power = plug.emeter_realtime.power
    del plug
    return power


def power_function(target: str) -> List[List[Union[float, str]]]:
    power = asyncio.run(power_request(target))
    return [["power", power, "W"]]
