tbl_character = \
"""CREATE TABLE IF NOT EXISTS Character (
    fName VARCHAR(255),
    lName VARCHAR(255),
    id INT,
    size VARCHAR(10),
    weight VARCHAR(10),
    race INT,
    species VARCHAR(20),
    gender CHAR(1),
    PRIMARY KEY (id)
);"""

tbl_clothing = \
"""CREATE TABLE IF NOT EXISTS Clothing (
    char_id INT,
    file_name VARCHAR(255),
    color CHAR(7),
    PRIMARY KEY (char_id, file_name),
    FOREIGN KEY (char_id) REFERENCES Character(id)
);"""

tbl_personality = \
"""CREATE TABLE IF NOT EXISTS Personality (
    char_id INT,
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
    char_id INT,
    desc VARCHAR(255),
    PRIMARY KEY (char_id),
    FOREIGN KEY (char_id) REFERENCES Character(id)
);"""

tbl_skill = \
"""CREATE TABLE IF NOT EXISTS Skill (
    char_id INT,
    desc VARCHAR(255),
    PRIMARY KEY (char_id),
    FOREIGN KEY(char_id) REFERENCES Character(id)
);"""