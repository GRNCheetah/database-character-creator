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