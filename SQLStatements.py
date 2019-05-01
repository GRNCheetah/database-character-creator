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
    color INT,
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