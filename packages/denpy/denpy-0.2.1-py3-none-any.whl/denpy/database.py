import mysql.connector
import inspect
import denpy

class Database:
    def __init__(self, endpoint, database_name, username, password):
        self.database = None
        self.cursor = None
        self.data = [endpoint, database_name, username, password]
        self.database_name = database_name

    def connect(self):
        self.database = mysql.connector.connect(host=self.data[0], user=self.data[2], password=self.data[3], database=self.data[1])
        self.cursor = self.database.cursor()

    def disconnect(self, commit: bool = False):
        if commit is True:
            self.database.commit()
        self.cursor.close()
        self.database.close()

    def add(self, table_name: str, columns: list, values: list):
        self.connect()
        values = ", ".join(f'"{value}"' for value in values)
        self.cursor.execute(f'INSERT INTO {self.database_name}.{table_name} ({", ".join(columns)}) VALUES ({values});')
        self.disconnect(commit=True)

    def get(self, table_name: str, columns: list, where: str = None, fetchall: bool = False):
        self.connect()
        if where is None:
            self.cursor.execute(f'SELECT {", ".join(columns)} FROM {self.database_name}.{table_name};')
        else:
            self.cursor.execute(f'SELECT {", ".join(columns)} FROM {self.database_name}.{table_name} WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
        if fetchall is False:
            result = self.cursor.fetchone()
        else:
            result = self.cursor.fetchall()
        if result is not None and len(result) == 1:
            result = result[0]
        self.disconnect()
        return result

    def delete(self, table_name: str, colum: str = None, where: str = None):
        self.connect()
        if where is None:
            if colum is None:
                self.cursor.execute(f'DELETE FROM {self.database_name}.{table_name};')
            else:
                self.cursor.execute(f'DELETE {colum} FROM {self.database_name}.{table_name};')
        else:
            if colum is None:
                self.cursor.execute(f'DELETE FROM {self.database_name}.{table_name} WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
            else:
                self.cursor.execute(f'DELETE {colum} FROM {self.database_name}.{table_name} WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
        self.disconnect(commit=True)

    def edit(self, table_name: str, column: list, value: list, where: str = None):
        self.connect()
        if where is None:
            for i in range(len(column)):
                self.cursor.execute(f'UPDATE {self.database_name}.{table_name} SET {column[i]} = "{value[i]}";')
        else:
            for i in range(len(column)):
                self.cursor.execute(f'UPDATE {self.database_name}.{table_name} SET {column[i]} = "{value[i]}" WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
        self.disconnect(commit=True)

    def table(self, table_name: str, columns: list, values: list, delete: bool = False):
        self.connect()
        if delete is True:
            self.cursor.execute(f'DROP TABLE IF EXISTS `{self.database_name}`.`{table_name}`;')
        else:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS `{self.database_name}`.`{table_name}` ({", ".join([f"{column} {value}" for column, value in zip(columns, values)])});')
        self.disconnect(commit=True)
