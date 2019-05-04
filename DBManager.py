import sqlite3
import SQLStatements as sql

import Character

class DBManager:

    def __init__(self):

        self.conn = sqlite3.connect('charcreation.db')
        self.cursor = self.conn.cursor()

        # new or edit
        # Change when Create or View button clicked on MainMenu
        self.mode = "new"

        self.C = Character.Character()

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

    def insertion(self, d_character, d_clothing, d_personality, d_job, d_skill):
        """Insert all information into the database.

        Will decide what id this character has or will have.
        """

        if self.mode == "new":
            self.insert_character(d_character)
            self.insert_clothing(d_clothing, self.cursor.lastrowid)
            self.insert_personality(d_personality, self.cursor.lastrowid)
            self.insert_job(d_job, self.cursor.lastrowid)
            self.insert_skill(d_skill, self.cursor.lastrowid)
        elif self.mode == "edit":
            print("modify character instead")

    def insert_character(self, data):
        """Inserts a character into the database.

        :param data: A dictionary of all the data to input into the Character table.
        :return: True if the statement went through
        """

        print(self.cursor.lastrowid)
        info = (data['fName'], data['lName'], data['size'], data['weight'], data['race'], data['species'], data['gender'])
        statement = "INSERT INTO Character (fName, lName, size, weight, race, species, gender) VALUES (?, ?, ?, ?, ?, ?, ?);"
        self.cursor.execute(statement, info)
        self.conn.commit()

        #self.cursor.execute(sql.insert_char)
        #self.cursor.execute(sql.insert_char2)
        #self.cursor.execute(sql.insert_char3)
        pass

    def insert_clothing(self, data, char_id):
        """Inserts all clothing into the database."""

        # Char_id, f_name, color
        info = [(char_id, "shirt", data['shirt'][0], data['shirt'][1]),
                (char_id, "pants", data['pants'][0], data['pants'][1]),
                (char_id, "shoes", data['shoes'][0], data['shoes'][1])]
        statement = "INSERT INTO Clothing (char_id, type, file_name, color) VALUES (?, ?, ?, ?);"
        self.cursor.executemany(statement, info)
        self.conn.commit()

    def insert_personality(self, data, char_id):
        """Inserts personality data into the database."""

        info = (char_id, data['ope'], data['con'], data['ext'], data['agr'], data['neu'])
        statement = "INSERT INTO Personality (char_id, ope, con, ext, agr, neu) VALUES (?, ?, ?, ?, ?, ?);"
        self.cursor.execute(statement, info)
        self.conn.commit()

    def insert_job(self, data, char_id):
        """Inserts job data into the database."""

        info = (char_id, data)
        statement = "INSERT INTO Job (char_id, descr) VALUES (?, ?);"
        self.cursor.execute(statement, info)
        self.conn.commit()

    def insert_skill(self, data, char_id):
        """Inserts skill data into the database."""

        info = (char_id, data)
        statement = "INSERT INTO Skill (char_id, descr) VALUES (?, ?);"
        self.cursor.execute(statement, info)
        self.conn.commit()


    def print_all_character(self):
        #self.cursor.execute(sql.print_all)
        self.cursor.execute("SELECT * FROM Character")
        result = self.cursor.fetchall()
        return result

    def get_all_characters(self):
        self.cursor.execute(sql.sel_characters)
        return self.cursor.fetchall()

    def get_character(self, id):
        """Gets a single character by it's id.

            Returns a character object.
        """

#        for row in self.conn.execute(sql.sel_char, (str(id))):
#            print(row.description)
#            print(type(row))

        self.cursor.execute(sql.sel_character, str(id))
        data = self.cursor.fetchone()
        self.C.settbl_character(data)

        self.cursor.execute(sql.sel_clothing, str(id))
        data = self.cursor.fetchall()
        self.C.settbl_clothing(data)

        self.cursor.execute(sql.sel_personality, str(id))
        data = self.cursor.fetchone()
        self.C.settbl_personality(data)

        self.cursor.execute(sql.sel_job, str(id))
        data = self.cursor.fetchone()
        self.C.settbl_job(data)

        self.cursor.execute(sql.sel_skill, str(id))
        data = self.cursor.fetchone()
        self.C.settbl_skill(data)


        print(self.C)
        return self.C


if __name__ == "__main__":
    d=DBManager()
    d.create_tables()
    d.insert_character()
    r=d.print_all_character()
    d.close_database()
