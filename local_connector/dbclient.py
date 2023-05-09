from .dbconnector import Connector, Error

class Client:
    debug = False
    def __init__(self, db_config):
        self.connector = Connector(db_config = db_config)
        
    def query(self, query: str) -> tuple[list[str], list[tuple]]:
        self.connect
        # quering data base
        try:
            self.cur.execute(query)
            columns = self.cur.column_names
            result = self.cur.fetchall()

            return {k:v for k,v in [('columns',columns),('data', result)]}

        except Error as err:
            print(f'Error no: {err.errno}')
            print(f'Error message: {err.msg}')

        finally:
            self.close

    def statement(self, statement: str) -> None:
        # run stetements for create and delete tables
        self.connect

        try:
            self.cur.execute(statement)
            self.conn.commit()
            if self.debug:
                print('Statement was commited successfuly.')
        
        except Error as err:
            print(f'Error no: {err.errno}')
            print(f'Error message: {err.msg}')

        finally:
            self.close

    def command(self, statement: str, variable:list) -> None:
        # run commands for with variables
        self.connect

        try:
            self.cur.execute(statement, *variable)
            self.conn.commit()
            if self.debug:
                print('Statement was commited successfuly.')
        
        except Error as err:
            print(f'Error no: {err.errno}')
            print(f'Error message: {err.msg}')
        
        finally:
            self.close

    def call(self, procedure_name:str, procedure_params:tuple = (None,)):
        self.connect

        try:
            if procedure_params[0] == None:
                self.cur.callproc(procedure_name)
            else:
                self.cur.callproc(procedure_name, args = procedure_params)
            results = next(self.cur.stored_results())
            result = results.fetchall()
            columns = results.column_names
            return {k:v for k,v in [('columns',columns),('data', result)]}

        except Error as err:
            print(f'Error no: {err.errno}')
            print(f'Error message: {err.msg}')
        
        finally:
            self.close


    @property
    def close (self) -> None:
        self.cur.close()
        self.connector.close_connection

    @property
    def connect(self)->None:
        self.connector.connect
        self.conn = self.connector.conn
        self.cur = self.conn.cursor()

