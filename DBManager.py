import sqlite3
import SQLStatements as sql

class DBManager:

    def __init__(self):

        self.conn = sqlite3.connect('charcreation.db')
        self.cursor = self.conn.cursor()

        # new or edit
        # Change when Create or View button clicked on MainMenu
        self.mode = "new"

    def close_database(self):
        self.cursor.close()
        self.conn.close()

    def create_tables(self):
        self.cursor.execute(sql.tbl_character)
        self.cursor.execute(sql.tbl_clothing)
        self.cursor.execute(sql.tbl_personality)
        self.cursor.execute(sql.tbl_job)
        self.cursor.execute(sql.tbl_skill)

    def set_mode(self, mode):
        print(mode)
        self.mode = mode

    def insertion(self, d_character, d_clothing):
        """Insert all information into the database.

        Will decide what id this character has or will have.
        """




    def insert_character(self, data):
        """Inserts a character into the database.

        Has two modes, must decide when we get here. If this character is in the database, we just need
        to update it. If this character is new, we need to insert it. Might do this check in a parent
        function.

        :param data: A dictionary of all the data to input into the Character table.
        :return: True if the statement went through
        """

        print(self.cursor.lastrowid)
        info = (data['fName'], data['lName'], data['size'], data['weight'], data['race'], data['species'], data['gender'])
        statement = "INSERT INTO Character (fName, lName, size, weight, race, species, gender) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(statement, info)
        self.conn.commit()

        #self.cursor.execute(sql.insert_char)
        #self.cursor.execute(sql.insert_char2)
        #self.cursor.execute(sql.insert_char3)
        pass

    def insert_clothing(self, data):
        """Inserts all clothing into the database."""


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
