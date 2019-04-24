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


    def __init__(self, species, gender):
        """Should initialize with the Species, Gender, and Color of the character.


        :param species:
        """
        self.species = ""
        self.gender = ""

        self.max_w = 50
        self.max_h = 150
        self.w = 0
        self.h = 0
        # Original image of the character
        self.character = Image.new("RGB", (self.max_w, self.max_h))
        self.mod = Image.new("RGB", (self.max_w, self.max_h))
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

        self.update_character(species, gender)



        # Masks for the different clothing items
        # Might need to be in lists or called only when needed


        #self.tshirt_mask = Image.open(os.path.join("assets", "tshirt_mask.gif"))
        #self.tshirt_mask = self.tshirt_mask.convert("L")

        # This is the color that the character is pasted onto.#


    def _open(self, f_name, mode):
        return Image.open(os.path.join("assets", f_name)).convert(mode)

    def update_character(self, s, g):
        """Run whenever an attribute of the chracter's phyisical being is changed."""

        self.species = s
        self.gender = g

        if self.species == "Human" and self.gender == "Female":
            self.character = self._open("fe_base.gif", "RGB")
            # Load clothing items
            self.shirts = [self._open("fe_m_blouse.gif", "L"),
                           self._open("fe_m_crop.gif", "L")]
            self.pants = [self._open("fe_m_jeans.gif", "L"),
                          self._open("fe_m_skirt.gif", "L")]
            self.shoes = []

        elif self.species == "Human" and self.gender == "Male":
            self.character = self._open("male.gif", "RGB")
            # Load clothing items
            self.shirts = [self._open("tshirt_mask.gif", "L")]

        # Convert so all the same
        #self.character = self.character.convert("RGB")
        self.w, self.h = self.character.size

        # Scaling
        self.ratio = min(self.max_w/self.w, self.max_h/self.h)
        self.w = int(self.w * self.ratio)
        self.h = int(self.h * self.ratio)
        # Resize character image
        self.character = self.character.resize((self.w, self.h), Image.ANTIALIAS)
        # Resize clothes
        for i in range(len(self.shirts)):
            self.shirts[i] = self.shirts[i].resize((self.w, self.h), Image.ANTIALIAS)
        for i in range(len(self.pants)):
            self.pants[i] = self.pants[i].resize((self.w, self.h), Image.ANTIALIAS)
        for i in range(len(self.shoes)):
            self.shoes[i] = self.shoes[i].resize((self.w, self.h), Image.ANTIALIAS)

        self.setAllColor()


    def setAllColor(self):
        self.setShirtColor(self.col_shirt)
        self.setPantsColor(self.col_pants)
        self.setShoesColor(self.col_shoes)


    def setShirtColor(self, rgbHex):
        """Creates and returns a tKinter image with the correct color shirt."""
        if self.shirts:
            print("Setting shirt default")
            self.col_shirt = rgbHex
            self.mod = Image.new("RGB", (self.w, self.h), self.col_shirt)
            # Pastes the color (mod) into the white area of the mask.
            self.character.paste(self.mod, mask=self.shirts[self.curr_shirt])
        print(self.character.mode)
        return ImageTk.PhotoImage(self.character)

    def setPantsColor(self, rgbHex):
        """Creates and returns a tKinter image with the correct color pants."""
        if self.pants:
            print("Setting pants default")
            self.col_pants = rgbHex
            self.mod = Image.new("RGB", (self.w, self.h), self.col_pants)
            self.character.paste(self.mod, mask=self.pants[self.curr_pants])
        print(self.character.mode)
        return ImageTk.PhotoImage(self.character)

    def setShoesColor(self, rgbHex):
        """Creates and returns a tKinter image with the correct color shoes."""
        if self.shoes:
            self.col_shoes = rgbHex
            self.mod = Image.new("RGB", (self.w, self.h), self.col_shoes)
            self.character.paste(self.mod, mask=self.shoes[self.curr_shoes])

        return ImageTk.PhotoImage(self.character)

    def returnGIF(self):
        return ImageTk.PhotoImage(self.character)





