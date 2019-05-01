import sqlite3
import SQLStatements as sql

class DatabaseManager:

    def __init__(self):

        self.conn = sqlite3.connect('charcreation.db')
        self.cursor = self.conn.cursor()

    def close_database(self):
        self.cursor.close()
        self.conn.close()

    def create_tables(self):
        self.cursor.execute(sql.tbl_character)
        self.cursor.execute(sql.tbl_clothing)
        self.cursor.execute(sql.tbl_personality)

    def insert_character(self, data):
        """Inserts a character into the database.


        :param data:
        :return:
        """

        sql_statement = '''INSERT INTO me '''

        pass
