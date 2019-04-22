from PIL import Image, ImageTk



class CharacterManip:
    """The goal of this object is to represent the Character as a whole.

    Will take in information about what the character should look like. Will then manipulate
    the image to represent the given input. After will return data that TKinter will be able
    to display.
    """


    def __init__(self):

        self.character = Image.open("person.gif")

    def setShirtColor(self, hsvColor):

        w, h = self.character.size()

        bg = Image.new("HSV", (w, h), (hsvColor, 100, 50))

        bg.paste(self.character)

    def returnGIF(self):
        return ImageTk.PhotoImage(self.character)





