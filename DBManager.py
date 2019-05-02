import sqlite3
import SQLStatements as sql

class DBManager:

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

    def insert_character(self):
        """Inserts a character into the database.


        :param data:
        :return:
        """

        self.cursor.execute(sql.insert_char)
        self.cursor.execute(sql.insert_char2)
        self.cursor.execute(sql.insert_char3)
        pass


    def print_all_character(self):
        #self.cursor.execute(sql.print_all)
        self.cursor.execute("SELECT * FROM Character")
        result = self.cursor.fetchall()
        return result
        pass

if __name__ == "__main__":
    d=DBManager()
    d.create_tables()
    d.insert_character()
    r=d.print_all_character()
    d.close_database()
