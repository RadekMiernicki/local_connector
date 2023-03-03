import mysql.connector as MySql
from mysql.connector.pooling import MySQLConnectionPool as Pool
from mysql.connector import Error
import json

class Connector:
    # Class for seting connection to MySQL DB
    def __init__(self, db_config: dict, use_pool:bool = False, msg:bool = False) -> object:       
        self.use_pool = use_pool
        self.pool = None
        self.guest: str = "Me"
        self.db_config = db_config
        self.msg = msg

    def create_pool(self, pool_name: str = "pool_a", pool_size: int = 2) -> Pool:
        # Method for creatin pool of connection to db
        try:
            self.pool = Pool(pool_name = pool_name,
                            pool_size = pool_size,
                            **self.db_config)
            print(f"The connection pool was created with a name: {self.pool.pool_name}")
            print(f"The pool size is: {self.pool.pool_size}")
            return self

        except Error as err:
            print(F"Error code: {err.errno}")
            print(f"Error message: {err.msg}")

            # Create a connection
            try:
                con = MySql.connect(**self.db_config)
                # Add the connection into the pool
                self.pool.add_connection(cnx=con)
                print('A new connection is added in the pool.\n')

                self.conn = self.pool.get_connection()
                print(f'{self.guest} is connected.\n')
                return self
            except Error as err:
                print(F"Error code: {err.errno}")
                print(f"Error message: {err.msg}")

    @property
    def connect (self) -> object:
        # method create connection to db
        if self.pool:
            try:
                self.conn = self.pool.get_connection()
                print(f"User {self.guest}@{self.db_config['host']} is connected to {self.conn.database}"+\
                    f"with ID: {self.conn.connection_id}")
                return self

            except:
                print (f"No more connection are available.")
        
        else:
            try:
                self.conn = MySql.connect(**self.db_config)
                if self.msg:
                    print('The connection was established.')
                return self
            except Error as err:
                print(f"Error code {err.errno}")
                print(f"Error message {err.msg}")

    @property
    def close_connection (self) -> object:
        self.conn.close()
        if self.msg:
            print('Coonection was closed.')

    def set_guest_name(self, name: str) -> None:
        self.guest = name
        if self.msg:
            print(f"Guest name was set to {self.guest}")