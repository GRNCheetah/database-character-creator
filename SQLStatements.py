# Table Creation
tbl_character = \
"""CREATE TABLE IF NOT EXISTS Character (
    fName VARCHAR(255) NOT NULL,
    lName VARCHAR(255),
    id INTEGER,
    size VARCHAR(10),
    weight VARCHAR(10),
    race INTEGER,
    species VARCHAR(20),
    gender VARCHAR(6),
    PRIMARY KEY (id)
);"""

tbl_clothing = \
"""CREATE TABLE IF NOT EXISTS Clothing (
    char_id INTEGER,
    type VARCHAR(5),
    file_name VARCHAR(255),
    color CHAR(7),
    PRIMARY KEY (char_id, type),
    FOREIGN KEY (char_id) REFERENCES Character(id)
);"""

tbl_personality = \
"""CREATE TABLE IF NOT EXISTS Personality (
    char_id INTEGER,
    ope FLOAT,
    con FLOAT,
    ext FLOAT,
    agr FLOAT,
    neu FLOAT,
    PRIMARY KEY (char_id),
    FOREIGN KEY (char_id) REFERENCES Character(id)
);"""

tbl_job = \
"""CREATE TABLE IF NOT EXISTS Job (
    char_id INTEGER,
    descr VARCHAR(255) DEFAULT "No job",
    PRIMARY KEY (char_id),
    FOREIGN KEY (char_id) REFERENCES Character(id)
);"""

tbl_skill = \
"""CREATE TABLE IF NOT EXISTS Skill (
    char_id INTEGER,
    descr VARCHAR(255) DEFAULT "No skill",
    PRIMARY KEY (char_id),
    FOREIGN KEY(char_id) REFERENCES Character(id)
);"""

sel_characters = \
"""SELECT 
    fName, lName, species, gender, id
FROM
    Character"""


# Inserting into the database
ins_character = "INSERT INTO Character (fName, lName, size, weight, race, species, gender) VALUES (?, ?, ?, ?, ?, ?, ?);"
ins_clothing = "INSERT INTO Clothing (char_id, type, file_name, color) VALUES (?, ?, ?, ?);"
ins_personality = "INSERT INTO Personality (char_id, ope, con, ext, agr, neu) VALUES (?, ?, ?, ?, ?, ?);"
ins_job = "INSERT INTO Job (char_id, descr) VALUES (?, ?);"
ins_skill = "INSERT INTO Skill (char_id, descr) VALUES (?, ?);"

# Selecting rows from each table
# Could have done a combo statement but it would have messed up on the clothing, I think.
sel_character = "SELECT fName, lName, id, size, weight, race, species, gender FROM Character WHERE id = ?"
sel_clothing = "SELECT type, file_name, color FROM Clothing WHERE char_id = ?;"
sel_personality = "SELECT ope, con, ext, agr, neu FROM Personality WHERE char_id = ?;"
sel_job = "SELECT descr FROM Job WHERE char_id = ?;"
sel_skill = "SELECT descr FROM Skill WHERE char_id = ?;"

# Used to update data in the db when a character is updated.
update_character = \
"""UPDATE Character
SET fName = ?, lName = ?, size = ?, weight = ?, race = ?, species = ?, gender = ?
WHERE id = ?;"""

update_clothing = \
"""UPDATE Clothing
SET file_name = ?, color = ?
WHERE char_id = ? AND type = ?;"""

update_personality = \
"""UPDATE Personality
SET ope = ?, con = ?, ext = ?, agr = ?, neu = ?
WHERE char_id = ?;"""

update_job = \
"""UPDATE Job
SET descr = ?
WHERE char_id = ?;"""

update_skill = \
"""UPDATE Skill
SET descr = ?
WHERE char_id = ?;"""

