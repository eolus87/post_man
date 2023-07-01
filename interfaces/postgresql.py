__author__ = "Nicolas Gutierrez"

# Standard Libraries
import logging
# Third party libraries
import psycopg2
from psycopg2.extensions import connection
# Custom Libraries
from data_classes.data_point import DataPoint

table_creation_query = (
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

data_insertion_query = (
        """INSERT INTO {0}(time_stamp, type, target, value, unit) 
        VALUES('{1}', '{2}', '{3}', {4}, '{5}')
        """)


class PostGreSQL:
    def __init__(
            self,
            address: str,
            port: int,
            user: str,
            password: str,
            table_name: str
    ) -> None:
        # Logger
        self.__logger = logging.getLogger(f"post_man.{__name__}")
        # Inputs
        self.__address = address
        self.__port = port
        self.__user = user
        self.__password = password
        self.__table_name = table_name
        # Init table
        self.__init_table(table_name)

    def __connect_to_db(self) -> connection:
        """
        Function to connect to the PostGreSQL DB using the package psycopg2.
        It sets up autocommit as True automatically.

        :return: It returns the DB connection
        """
        conn = psycopg2.connect(
            host=self.__address,
            port=self.__port,
            user=self.__user,
            password=self.__password
        )
        conn.autocommit = True
        return conn

    def __init_table(self, table_name: str) -> None:
        """
        Initializes the table in the DB. This is always done when this class
        is instantiated. It is recommended the query includes a condition
        in case the table exists.

        :param table_name: String with the name of the table
        """
        conn = self.__connect_to_db()
        try:
            table_creation_command = table_creation_query.format(table_name)
            self.__execute_cursor(conn, table_creation_command)
        except Exception as inst:
            self.__logger.error(f"Error while creating DB table: {inst}")
        finally:
            self.__close_connection(conn)

    @staticmethod
    def __execute_cursor(conn: connection, command: str) -> None:
        """
        Auxiliary methods that instantiates a cursor, executes and close it.

        :param command: String with the query to execute
        """
        cur = conn.cursor()
        cur.execute(command)
        cur.close()

    def insert_data(self, data_point: DataPoint) -> None:
        """
        Method that inserts the data into the DB. It sets up the query
        message using a data_class data_point and executes the query
        of insertion.

        :param data_point: DataPoint dataclass with the information
        of the sensor
        """
        conn = self.__connect_to_db()
        try:
            data_insertion_command = data_insertion_query.format(
                self.__table_name,
                data_point.time_stamp,
                data_point.type,
                data_point.target,
                data_point.value,
                data_point.unit
            )
            self.__execute_cursor(conn, data_insertion_command)
        except Exception as inst:
            self.__logger.error(f"Error while inserting data into DB: {inst}")
        finally:
            self.__close_connection(conn)

    @staticmethod
    def __close_connection(conn: connection) -> None:
        """
        Wrapper to close connection.
        """
        conn.close()
