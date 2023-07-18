__author__ = "Nicolas Gutierrez"

# Standard libraries
import logging
from typing import Callable
import datetime
import time
from threading import Thread
from queue import Queue
# Third party libraries
import numpy as np
# Custom libraries
from data_classes.data_point import DataPoint


class Worker(Thread):
    def __init__(self, target_address: str, rate: float, work_function: Callable, data_queue: Queue) -> None:
        self.__logger = logging.getLogger(f"post_man.{__name__}")

        self.__target_address = target_address
        self.__period = 1/rate
        self.__work_function = work_function
        self.__data_queue = data_queue

        self.__worker_thread_exit_sleep = 0.25
        self.__keep_working = False
        super().__init__()

    def run(self) -> None:
        self.__keep_working = True
        while self.__keep_working:
            initial_time = time.time()
            try:
                data_list = self.__work_function(self.__target_address)
                for data in data_list:
                    data_point = DataPoint(time_stamp=datetime.datetime.now(),
                                           type=data[0],
                                           target=self.__target_address,
                                           value=data[1],
                                           unit=data[2])
                    self.__data_queue.put(data_point)
            except Exception as inst:
                self.__logger.error(
                    f"Error while using {self.__work_function}"
                    f"-target{self.__target_address}: {inst}"
                )

            final_time = time.time()
            sleeping_time = self.__period - (final_time-initial_time)
            sleeping_time = float(np.clip(sleeping_time, a_min=0, a_max=None))

            time.sleep(sleeping_time)

    def join(self, timeout=None) -> None:
        self.__stop()
        super().join(timeout)

    def __stop(self) -> None:
        self.__keep_working = False
        time.sleep(self.__worker_thread_exit_sleep)
