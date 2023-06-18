__author__ = "Nicolas Gutierrez"

# Standard libraries
from queue import Queue
import threading
from threading import Thread
import time
from typing import Dict, List, Callable
# Third party libraries
# Custom libraries
from labourers.worker import Worker


class Leader:
    def __init__(self, leader_config: Dict, work_function: Callable) -> None:
        self.__measures_queue = Queue(maxsize=len(leader_config["devices"])*10)
        self.__workers = self.__workers_instantiation(leader_config, self.__measures_queue, work_function)
        self.started_event = threading.Event()

        self.__management_thread_loop_sleep = 0.25
        self.__management_thread_exit_sleep = 0.25
        self.__keep_managing = True
        self.__management_thread = Thread(target=self.__leader_management, args=[print])

    @staticmethod
    def __workers_instantiation(config: Dict, data_queue: Queue, work_function: Callable) -> List[Worker]:
        list_of_threads = []
        for target_key in config["devices"].keys():
            list_of_threads.append(
                Worker(
                    config["sensor_type"],
                    config["devices"][target_key]["address"],
                    config["devices"][target_key]["rate"],
                    work_function,
                    data_queue
                )
            )
        return list_of_threads

    def start(self) -> None:
        # Starting the workers
        for worker in self.__workers:
            worker.start()

        # Starting the management of the leader
        self.__management_thread.start()

        self.started_event.set()

    def __leader_management(self, actuation_function: Callable) -> None:
        while self.__keep_managing:
            while not self.__measures_queue.empty():
                actuation_function(self.__measures_queue.get())
            time.sleep(self.__management_thread_loop_sleep)

    def stop(self) -> None:
        if self.started_event.is_set():
            # Stopping workers
            for worker in self.__workers:
                worker.join()

            # Stopping leader
            self.__keep_managing = False
            time.sleep(self.__management_thread_exit_sleep)
            self.__management_thread.join()
        else:
            raise Exception("Threads have not been started yet")
