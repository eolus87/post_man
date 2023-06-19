__author__ = "Nicolas Gutierrez"

# Standard Libraries
import psycopg2
from psycopg2.extensions import connection
# Third party libraries
# Custom Libraries
from data_classes.data_point import DataPoint

creation_command = (
    """
    CREATE TABLE IF NOT EXISTS {0}(
            time_stamp TIMESTAMP,
            type TEXT,
            target TEXT,
            value NUMERIC(6,2),
            unit TEXT,
            PRIMARY KEY (time_stamp , type, target)
    )
    """)

insertion_command = (
        """INSERT INTO {0}(time_stamp, type, target, value, unit) 
        VALUES('{1}', '{2}', '{3}', {4}, '{5}')
        """)


class PostGreSQL:
    def __init__(self, ip: str, port: int, user: str, password: str, table_name: str) -> None:
        # Inputs
        self.table_name = table_name
        # Connection to the db
        self.conn = self.__connect_to_db(ip, port, user, password)
        # Init table
        self.__init_table(table_name)

    @staticmethod
    def __connect_to_db(ip: str, port: int, user: str, password: str) -> connection:
        conn = psycopg2.connect(host=ip, port=port, user=user, password=password)
        conn.autocommit = True
        return conn

    def __init_table(self, table_name: str) -> None:
        table_creation_command = creation_command.format(table_name)
        self.__execute_cursor(table_creation_command)

    def __execute_cursor(self, command: str) -> None:
        cur = self.conn.cursor()
        cur.execute(command)
        cur.close()

    def insert_data(self, data_point: DataPoint) -> None:
        data_insertion_command = insertion_command.format(
            self.table_name,
            data_point.time_stamp,
            data_point.type,
            data_point.target,
            data_point.value,
            data_point.unit
        )
        self.__execute_cursor(data_insertion_command)

    def close_connection(self) -> None:
        self.conn.close()
