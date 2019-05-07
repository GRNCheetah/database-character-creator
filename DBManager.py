import sqlite3
import SQLStatements as sql

import Character

class DBManager:

    def __init__(self):

        self.conn = sqlite3.connect('charcreation.db')
        self.cursor = self.conn.cursor()
        self.conn.execute("pragma foreign_keys=on;")
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
        self.mode = mode

    def insertion(self, char):
        """Insert all information into the database.

        Will decide what id this character has or will have.
        """

        if self.mode == "new":
            self.insert_character(char.get_character_tuple("new"))
            char.id = self.cursor.lastrowid
            self.insert_clothing(char.get_clothing_list("new"))
            self.insert_personality(char.get_personality_tuple("new"))
            self.insert_job(char.get_job_tuple("new"))
            self.insert_skill(char.get_skill_tuple("new"))
        elif self.mode == "edit":
            self.update_all(char)

    def insert_character(self, data):
        """Inserts a character into the database.

        :param data: A dictionary of all the data to input into the Character table.
        :return: True if the statement went through
        """
        self.cursor.execute(sql.ins_character, data)
        self.conn.commit()


    def insert_clothing(self, data):
        """Inserts all clothing into the database."""

        # Char_id, f_name, color
        self.cursor.executemany(sql.ins_clothing, data)
        self.conn.commit()

    def insert_personality(self, data):
        """Inserts personality data into the database."""

        self.cursor.execute(sql.ins_personality, data)
        self.conn.commit()

    def insert_job(self, data):
        """Inserts job data into the database."""

        self.cursor.execute(sql.ins_job, data)
        self.conn.commit()

    def insert_skill(self, data):
        """Inserts skill data into the database."""

        self.cursor.execute(sql.ins_skill, data)
        self.conn.commit()

    def update_all(self, char):
        self.cursor.execute(sql.update_character, char.get_character_tuple("edit"))
        self.cursor.executemany(sql.update_clothing, char.get_clothing_list("edit"))
        self.cursor.execute(sql.update_personality, char.get_personality_tuple("edit"))
        self.cursor.execute(sql.update_job, char.get_job_tuple("edit"))
        self.cursor.execute(sql.update_skill, char.get_skill_tuple("edit"))
        self.conn.commit()

    def get_all_characters(self):
        self.cursor.execute(sql.sel_characters)
        return self.cursor.fetchall()

    def get_character(self, id):
        """Gets a single character by it's id.

            Returns a character object.
        """

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

        return self.C

    def del_char(self, id):
        """Deletes a charcter with a given id."""

        self.cursor.execute(sql.del_character, str(id))
        self.conn.commit()
        '''self.cursor.execute(sql.del_clothing, str(id))
        self.cursor.execute(sql.del_personality, str(id))
        self.cursor.execute(sql.del_, str(id))
        self.cursor.execute(sql.del_character, str(id))'''


if __name__ == "__main__":
    d=DBManager()
    d.create_tables()
    d.insert_character()
    r=d.print_all_character()
    d.close_database()
