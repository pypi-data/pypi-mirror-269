import sqlite3
from pathlib import Path

class LocalDatabase:
    def __init__(self, filename):
        self.database = None
        self.cursor = None
        self.filename = filename

    def connect(self):
        self.database = sqlite3.connect(f'{Path(__file__).parents[1]}/{self.filename}.db')
        self.cursor = self.database.cursor()

    def disconnect(self, commit=False):
        if commit is True:
            self.database.commit()
        self.cursor.close()
        self.database.close()

    def add(self, table_name, columns, values: list):
        self.connect()
        fragezeichen = ', '.join('?' * len(values))
        self.cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({fragezeichen})', tuple(values))
        self.disconnect(commit=True)

    def get(self, table_name, columns, where=None, fetchall=False):
        self.connect()
        if where is None:
            self.cursor.execute(f'SELECT {columns} FROM {table_name}')
        else:
            self.cursor.execute(f'SELECT {columns} FROM {table_name} WHERE {where.split(" = ")[0]} = ?', (where.split(" = ")[1],))
        if fetchall is False:
            result = self.cursor.fetchone()
        else:
            result = self.cursor.fetchall()
        self.disconnect()
        return result

    def delete(self, table_name, colum=None, where=None):
        self.connect()
        if where is None:
            if colum is None:
                self.cursor.execute(f'DELETE FROM {table_name};')
            else:
                self.cursor.execute(f'DELETE {colum} FROM {table_name};')
        else:
            if colum is None:
                self.cursor.execute(f'DELETE FROM {table_name} WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
            else:
                self.cursor.execute(f'DELETE {colum} FROM {table_name} WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
        self.disconnect(commit=True)

    def edit(self, table_name, column, value, where=None):
        self.connect()
        if where is None:
            self.cursor.execute(f'UPDATE {table_name} SET {column} = {value}')
        else:
            self.cursor.execute(f'UPDATE {table_name} SET {column} = ? WHERE {where.split(" = ")[0]} = ?', (value, where.split(" = ")[1]))
        self.disconnect(commit=True)

    def default(self, table_name, columns: list):
        self.connect()
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(columns)})')
        self.disconnect(commit=True)
