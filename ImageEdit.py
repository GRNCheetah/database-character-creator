from PIL import Image, ImageTk
import os



class CharacterManip:
    """The goal of this object is to represent the Character as a whole.

    Will take in information about what the character should look like. Will then manipulate
    the image to represent the given input. After will return data that TKinter will be able
    to display.

    Each funtion should return the new image. You should NEVER have to edit self.character/
    whatever we come up with. We want to keep loading to a minumum.
    """


    def __init__(self):
        """Should initialize with the Species, Gender, and Color of the character.


        :param species:
        """
        self.species = ""
        self.gender = ""
        self.color = 0 # int

        self.human_colors = ["#ffdbac",
                             "#f1c27d",
                             "#e0ac69",
                             "#c68642",
                             "#8d5524"]

        self.bear_colors = ["#ffe7b5",
                            "#ffde58",
                            "#d76300",
                            "#633800",
                            "#eff5eb"]

        self.max_w = 300
        self.max_h = 500
        self.w = 0
        self.h = 0
        # Original image of the character
        self.character = Image.new("RGB", (self.max_w, self.max_h))
        self.base = Image.new("RGB", (self.max_w, self.max_h))
        self.mod = Image.new("RGB", (self.max_w, self.max_h))
        self.m_skin = Image.new("L", (self.max_w, self.max_h))
        # List of clothes filenames
        self.f_shirts = []
        self.f_pants = []
        self.f_shoes = []
        # List of clothes masks
        self.shirts = []
        self.pants = []
        self.shoes = []

        self.curr_shirt = 0
        self.curr_pants = 0
        self.curr_shoes = 0

        self.def_col = "#ff0000"
        self.col_shirt = self.def_col
        self.col_pants = self.def_col
        self.col_shoes = self.def_col
        #self.col_skin = self.human_colors[color] # String
        self.col_skin = self.human_colors[0]

        #self.update_character(species, gender, color)



        # Masks for the different clothing items
        # Might need to be in lists or called only when needed


        #self.tshirt_mask = Image.open(os.path.join("assets", "tshirt_mask.gif"))
        #self.tshirt_mask = self.tshirt_mask.convert("L")

        # This is the color that the character is pasted onto.#


    def _open(self, f_name, mode):
        return Image.open(os.path.join("assets", f_name)).convert(mode)


    def define_character(self, char_data, clothing_data):
        """Run whenever a character needs to be put back together.

        Usually for the display character at the end of creation or before editing.

        :return:
        """

        self.species = char_data["species"]
        self.gender = char_data["gender"]
        self.color = char_data["race"]

        self._update_clothes_arrays()

        self.curr_shirt = self.f_shirts.index(clothing_data['shirt'][0])
        self.curr_pants = self.f_pants.index(clothing_data['pants'][0])
        self.curr_shoes = self.f_shoes.index(clothing_data['shoes'][0])

        self.col_shirt = clothing_data['shirt'][1]
        self.col_pants = clothing_data['pants'][1]
        self.col_shoes = clothing_data['shoes'][1]

        self.setAllColor()

    def update_character(self, s, g, c):
        """Run whenever an attribute of the chracter's phyisical being is changed.

        Use this function during the character creation process.
        """

        self.species = s
        self.gender = g
        self.color = c

        self.curr_shirt = 0
        self.curr_pants = 0
        self.curr_shoes = 0

        self._update_clothes_arrays()

        self.setAllColor()

    def _update_clothes_arrays(self):
        self.shirts = []
        self.pants = []
        self.shoes = []

        if self.species == "Human" and self.gender == "Female":
            self.character = self._open("fe_base.gif", "RGB")
            self.m_skin = self._open("fe_m_skin.gif", "L")
            # Load clothing file names
            self.f_shirts = ["fe_m_blouse.gif",
                             "fe_m_crop.gif"]
            self.f_pants = ["fe_m_jeans.gif",
                            "fe_m_skirt.gif"]
            self.f_shoes = ["fe_m_tennis_shoes.gif",
                            "fe_m_boots.gif"]

        elif self.species == "Human" and self.gender == "Male":
            self.character = self._open("ma_base.gif", "RGB")
            self.m_skin = self._open("ma_m_skin.gif", "L")
            # Load clothing file names
            self.f_shirts = ["ma_m_t_shirt.gif",
                             "ma_m_long_sleeve.gif"]
            self.f_pants = ["ma_m_shorts.gif",
                            "ma_m_long_jeans.gif"]
            self.f_shoes = ["ma_m_loafers.gif",
                            "ma_m_tennis_shoes.gif"]

        elif self.species == "Bear" and self.gender == "Male":
            self.character = self._open("bm_base.gif", "RGB")
            self.m_skin = self._open("bm_m_skin.gif", "L")
            # Load clothing file names
            self.f_shirts = ["bm_m_t_shirt.gif",
                             "bm_m_button_up.gif"]
            self.f_pants = ["bm_m_shorts.gif",
                            "bm_m_jeans.gif"]
            self.f_shoes = ["bm_m_tennis_shoes.gif"]

        elif self.species == "Bear" and self.gender == "Female":
            self.character = self._open("bf_base.gif", "RGB")
            self.m_skin = self._open("bf_m_skin.gif", "L")
            # Load clothing file names
            # Using the male clothes cuz im lazy
            self.f_shirts = ["bm_m_t_shirt.gif",
                             "bm_m_button_up.gif"]
            self.f_pants = ["bm_m_shorts.gif",
                            "bm_m_jeans.gif"]
            self.f_shoes = ["bm_m_tennis_shoes.gif"]

        for f_name in self.f_shirts:
            self.shirts.append(self._open(f_name, "L"))
        for f_name in self.f_pants:
            self.pants.append(self._open(f_name, "L"))
        for f_name in self.f_shoes:
            self.shoes.append(self._open(f_name, "L"))

        self.w, self.h = self.character.size
        # Scaling
        self.ratio = min(self.max_w / self.w, self.max_h / self.h)
        self.w = int(self.w * self.ratio)
        self.h = int(self.h * self.ratio)
        # Resize character image
        self.character = self.character.resize((self.w, self.h), Image.ANTIALIAS)
        self.base = self.character.copy()
        if self.m_skin:
            self.m_skin = self.m_skin.resize((self.w, self.h), Image.ANTIALIAS)


        # Resize clothes
        for i in range(len(self.shirts)):
            self.shirts[i] = self.shirts[i].resize((self.w, self.h), Image.ANTIALIAS)
        for i in range(len(self.pants)):
           self.pants[i] = self.pants[i].resize((self.w, self.h), Image.ANTIALIAS)
        for i in range(len(self.shoes)):
            self.shoes[i] = self.shoes[i].resize((self.w, self.h), Image.ANTIALIAS)






    def setAllColor(self):
        if self.species == "Human" and self.m_skin:
            self.setSkinColor(self.human_colors[self.color])
        elif self.species == "Bear" and self.m_skin:
            self.setSkinColor(self.bear_colors[self.color])

        self.setShirtColor(self.col_shirt)
        self.setPantsColor(self.col_pants)
        self.setShoesColor(self.col_shoes)

    def setSkinColor(self, rgbHex):
        self.col_skin = rgbHex
        self.mod=Image.new("RGB", (self.w, self.h), self.col_skin)
        self.character.paste(self.mod, mask=self.m_skin)

    def setShirtColor(self, rgbHex):
        """Creates and returns a tKinter image with the correct color shirt."""
        self.col_shirt = rgbHex
        if self.shirts:
            self.mod = Image.new("RGB", (self.w, self.h), self.col_shirt)
            # Pastes the color (mod) into the white area of the mask.
            self.character.paste(self.mod, mask=self.shirts[self.curr_shirt])
        return ImageTk.PhotoImage(self.character)

    def setPantsColor(self, rgbHex):
        """Creates and returns a tKinter image with the correct color pants."""
        self.col_pants = rgbHex
        if self.pants:
            self.mod = Image.new("RGB", (self.w, self.h), self.col_pants)
            self.character.paste(self.mod, mask=self.pants[self.curr_pants])
        return ImageTk.PhotoImage(self.character)

    def setShoesColor(self, rgbHex):
        """Creates and returns a tKinter image with the correct color shoes."""
        self.col_shoes = rgbHex
        if self.shoes:
            self.mod = Image.new("RGB", (self.w, self.h), self.col_shoes)
            self.character.paste(self.mod, mask=self.shoes[self.curr_shoes])

        return ImageTk.PhotoImage(self.character)

    def _shirtLeft(self):
        self.curr_shirt -= 1
        if (self.curr_shirt <= -1):
            self.curr_shirt = len(self.shirts) - 1
        self.character = self.base.copy()
        self.setAllColor()


    def _shirtRight(self):
        self.curr_shirt += 1
        if (self.curr_shirt >= len(self.shirts)):
            self.curr_shirt = 0
        self.character = self.base.copy()
        self.setAllColor()

    def _pantsLeft(self):
        self.curr_pants -= 1
        if (self.curr_pants <= -1):
            self.curr_pants = len(self.pants) - 1
        self.character = self.base.copy()
        self.setAllColor()


    def _pantsRight(self):
        self.curr_pants += 1
        if (self.curr_pants >= len(self.pants)):
            self.curr_pants = 0
        self.character = self.base.copy()
        self.setAllColor()

    def _shoesLeft(self):
        self.curr_shoes -= 1
        if (self.curr_shoes <= -1):
            self.curr_shoes = len(self.shoes) - 1
        self.character = self.base.copy()
        self.setAllColor()


    def _shoesRight(self):
        self.curr_shoes += 1
        if (self.curr_shoes >= len(self.shoes)):
            self.curr_shoes = 0
        self.character = self.base.copy()
        self.setAllColor()




    def returnGIF(self):
        return ImageTk.PhotoImage(self.character)





