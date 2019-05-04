class Character:
    """This will hold all information about a character that goes into and out
    of the database.

    There should only be one instance in the entire program. It represents the
    character that is currently being created or edited.
    """

    def __init__(self):

        # Character
        self.fName = ""
        self.lName = ""
        self.id = -1
        self.size = ""
        self.weight = ""
        self.race = -1
        self.species = ""
        self.gender = ""

        # Clothing
        self.shirt_f_name = ""
        self.shirt_color = ""
        self.pants_f_name = ""
        self.pants_color = ""
        self.shoes_f_name = ""
        self.shoes_color = ""

        # Personality
        self.ope = -1
        self.con = -1
        self.ext = -1
        self.agr = -1
        self.neu = -1

        # Job
        self.job_desc = ""

        # Skill
        self.skill_desc = ""

    def settbl_character(self, data):
        """data is a tuple"""
        self.fName = data[0]
        self.lName = data[1]
        self.id = data[2]
        self.size = data[3]
        self.weight = data[4]
        self.race = data[5]
        self.species = data[6]
        self.gender = data[7]

    def settbl_clothing(self, data):
        """data is a list of tuples"""
        for item in data:
            if item[0] == "shirt":
                self.shirt_f_name = item[1]
                self.shirt_color = item[2]
            elif item[0] == "pants":
                self.pants_f_name = item[1]
                self.pants_color = item[2]
            elif item[0] == "shoes":
                self.shoes_f_name = item[1]
                self.shoes_color = item[2]

    def settbl_personality(self, data):
        """data is a tuple"""
        self.ope = data[0]
        self.con = data[1]
        self.ext = data[2]
        self.agr = data[3]
        self.neu = data[4]

    def settbl_job(self, data):
        """data is a tuple"""
        self.job_desc = data[0]

    def settbl_skill(self, data):
        """data is a tuple"""
        self.skill_desc = data[0]

    def __str__(self):
        return self.fName + " " + self.lName + " " + str(self.id)