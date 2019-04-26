import tkinter as tk
from PIL import Image, ImageTk, ImageColor
import numpy as np
import os

import ImageEdit as IE

LARGE_FONT = ("Verdana", 12)

class Creator(tk.Tk):

    def __init__(self):

        # Initializations
        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Pretty Patty
        tk.Tk.wm_title(self, "Character Creator")

        # Frame Stuff
        self.frames = {}

        for F in (MainMenu, CharacterCreate, CharacterView):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        """Pass a class (page) to bring to the front."""
        frame = self.frames[cont]
        frame.tkraise()
        #self.frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        """

        :param parent: The frame of the Creator
        :param controller: Creator self
        """
        tk.Frame.__init__(self, parent)

        # Top most part of the screen
        self.label = tk.Label(self, text="The Character Creator", font=LARGE_FONT)
        self.label.pack()

        # ------ Button attributes -----
        but_width = 16
        but_padx = '2m'
        but_pady = '1m'

        # ----- Create Character -------
        self.butCreate = tk.Button(self,
                                   text="Create Character",
                                   background="blue",
                                   command=lambda: controller.show_frame(CharacterCreate),
                                   width=but_width,
                                   padx=but_padx,
                                   pady=but_pady)
        self.butCreate.pack()
        self.butCreate.focus_force()

        # ----- View Characters --------
        self.butView = tk.Button(self,
                                 text="View Characters",
                                 background="blue",
                                 command=lambda: controller.show_frame(CharacterView),
                                 width=but_width,
                                 padx=but_padx,
                                 pady=but_pady)
        self.butView.pack()


class CharacterCreate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="green")

        label = tk.Label(self, text="Time To Design", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # ----- Information Frame -----
        lfInfo = tk.LabelFrame(self,
                               text="Character Information")
        lfInfo.pack(fill="both", expand="yes", side="left")

        # First name
        lblFName = tk.Label(lfInfo,
                            text="First Name:")
        lblFName.grid(row=0, column=0)
        self.entFName = tk.Entry(lfInfo)
        self.entFName.grid(row=0, column=1)

        # Last name
        lblLName = tk.Label(lfInfo,
                            text="Last Name:")
        lblLName.grid(row=1, column=0)
        self.entLName = tk.Entry(lfInfo)
        self.entLName.grid(row=1, column=1)

        # Height
        lblHeight = tk.Label(lfInfo,
                            text="Height:")
        lblHeight.grid(row=2, column=0)
        height_options = {"Short", "Average", "Tall"}
        self.height = tk.StringVar(lfInfo, value="Short")
        dropHeight = tk.OptionMenu(lfInfo, self.height, *height_options)
        dropHeight.grid(row=2, column=1)

        # Weight
        lblWeight = tk.Label(lfInfo,
                             text="Weight:")
        lblWeight.grid(row=3, column=0)
        weight_options = {"Light", "Average", "Heavy"}
        self.weight = tk.StringVar(lfInfo, value="Light")
        dropWeight = tk.OptionMenu(lfInfo, self.weight, *weight_options)
        dropWeight.grid(row=3, column=1)

        # Species
        lblSpecies = tk.Label(lfInfo,
                              text="Species:")
        lblSpecies.grid(row=4, column=0)
        self.speciesNum = tk.IntVar(0)
        self.species_list = ["Human", "Bear", "Alien"]
        self.species = tk.StringVar()
        self.species.set(self.species_list[0])
        sldSpecies = tk.Scale(lfInfo,
                              variable=self.speciesNum,
                              from_=0,
                              to=(len(self.species_list) - 1),
                              orient=tk.HORIZONTAL,
                              command=self.setSpecies)
        sldSpecies.grid(row=5, column=1)
        lblSpeciesDisp = tk.Label(lfInfo,
                                  textvariable=self.species)
        lblSpeciesDisp.grid(row=4, column=1)

        # Color
        lblColor = tk.Label(lfInfo,
                            text="Color:")
        lblColor.grid(row=6, column=0)
        self.colorNum = tk.IntVar(0)
        sldColor = tk.Scale(lfInfo,
                            variable=self.colorNum,
                            from_=0,
                            to=4,
                            orient=tk.HORIZONTAL,
                            command=self.setColor)
        sldColor.grid(row=6, column=1)

        # Gender
        lblGender = tk.Label(lfInfo,
                            text="Gender:")
        lblGender.grid(row=7, column=0)
        self.gender = tk.StringVar()
        self.gender.set("Male")
        rbMale = tk.Radiobutton(lfInfo,
                                text="Male",
                                variable=self.gender,
                                value="Male",
                                command=self.setGender)
        rbMale.grid(row=7, column=1)
        rbFemale = tk.Radiobutton(lfInfo,
                                  text="Female",
                                  variable=self.gender,
                                  value="Female",
                                  command=self.setGender)
        rbFemale.grid(row=8, column=1)

        # Skill
        lblSkill = tk.Label(lfInfo,
                            text="Skill:")
        lblSkill.grid(row=9, column=0)
        self.entSkill = tk.Entry(lfInfo)
        self.entSkill.grid(row=9, column=1)

        # Job
        lblJob = tk.Label(lfInfo,
                          text="Job:")
        lblJob.grid(row=10, column=0)
        self.entJob = tk.Entry(lfInfo)
        self.entJob.grid(row=10, column=1)


        # Info Next
        butInfoNext = tk.Button(lfInfo,
                                text="Next",
                                command=self.infoNextClick)
        butInfoNext.grid(row=11, column=1)

        # ----- Visual Frame -----
        lfVisual = tk.LabelFrame(self,
                                 text="Design Character")
        lfVisual.pack(fill="both", expand="yes", side="right")



        # Asset import
        imgLeftArrow = tk.PhotoImage(file=os.path.join("assets", "butLeft.gif"))
        imgRightArrow = tk.PhotoImage(file=os.path.join("assets", "butRight.gif"))

        # Middle Person, needs to be three sections, maybe four

        #imgPerson = tk.PhotoImage(file="person.gif")
        self.character = IE.CharacterManip(self.species.get(), self.gender.get(), self.colorNum.get())
        self.imgPerson = self.character.returnGIF()
        self.lblPerson = tk.Label(lfVisual,
                          image=self.imgPerson)
        self.lblPerson.image = self.imgPerson
        self.lblPerson.grid(row=1,
                    column=1,
                    rowspan=3)

        but_dim = 100

        # Top left
        butLeftShirt = tk.Button(lfVisual,
                                 image=imgLeftArrow,
                                 width=but_dim,
                                 height=but_dim,
                                 command=self.shirtLeft)
        butLeftShirt.image = imgLeftArrow
        butLeftShirt.grid(row=1, column=0)

        # Top Right
        butRightShirt = tk.Button(lfVisual,
                                 image=imgRightArrow,
                                 width=but_dim,
                                 height=but_dim,
                                 command=self.shirtRight)
        butRightShirt.image = imgRightArrow
        butRightShirt.grid(row=1, column=2)

        # Mid left
        butLeftPants = tk.Button(lfVisual,
                                 image=imgLeftArrow,
                                 width=but_dim,
                                 height=but_dim,
                                 command=self.pantsLeft)
        butLeftPants.immge = imgLeftArrow
        butLeftPants.grid(row=2, column=0)

        # Mid Right
        butRightPants = tk.Button(lfVisual,
                                  image=imgRightArrow,
                                  width=but_dim,
                                  height=but_dim,
                                  command=self.pantsRight)
        butRightPants.image = imgRightArrow
        butRightPants.grid(row=2, column=2)

        # Bot left
        butLeftShoes = tk.Button(lfVisual,
                                 image=imgLeftArrow,
                                 width=but_dim,
                                 height=but_dim,
                                 command=self.shoesLeft)
        butLeftShoes.image = imgLeftArrow
        butLeftShoes.grid(row=3, column=0)

        # Bot Right
        butRightShoes = tk.Button(lfVisual,
                                  image=imgRightArrow,
                                  width=but_dim,
                                  height=but_dim,
                                  command=self.shoesRight)
        butRightShoes.image = imgRightArrow
        butRightShoes.grid(row=3, column=2)

        # Top Slider
        self.shirtColor = tk.IntVar(0) # Represents hex number in decimal
        self.hexShirtColor = tk.StringVar()
        self.hexShirtColor.set("#ff0000")
        self.sldTopColor = tk.Scale(lfVisual,
                               variable=self.shirtColor,
                               from_=0,
                               to=360,
                               orient=tk.HORIZONTAL,
                               background=self.hexShirtColor.get())
        self.sldTopColor.config(command=self.handleShirtColor)
        self.sldTopColor.grid(row=1, column=3)

        # Mid Slider
        self.pantsColor = tk.IntVar(0)
        self.hexPantsColor = tk.StringVar()
        self.hexPantsColor.set("#ff0000")
        self.sldMidColor = tk.Scale(lfVisual,
                                    variable=self.pantsColor,
                                    from_=0,
                                    to=360,
                                    orient=tk.HORIZONTAL,
                                    background=self.hexPantsColor.get())
        self.sldMidColor.config(command=self.handlePantsColor)
        self.sldMidColor.grid(row=2, column=3)

        # Bot Slider
        self.shoesColor = tk.IntVar(0)
        self.hexShoesColor = tk.StringVar()
        self.hexShoesColor.set("#ff0000")
        self.sldBotColor = tk.Scale(lfVisual,
                                    variable=self.shoesColor,
                                    from_=0,
                                    to=360,
                                    orient=tk.HORIZONTAL,
                                    background=self.hexShoesColor.get())
        self.sldBotColor.config(command=self.handleShoesColor)
        self.sldBotColor.grid(row=3, column=3)

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb


    def handleShirtColor(self,  event):
        """Update the color of the slider and the shirt."""
        # Update the Slider
        rgb = ImageColor.getrgb("hsl(" + str(self.shirtColor.get()) + ", 100%, 50%)")
        newHex = self.rgb_to_hex(rgb)
        self.sldTopColor.config(bg=newHex)

        # Update the person
        self.imgPerson = self.character.setShirtColor(newHex)
        self.lblPerson.configure(image=self.imgPerson)
        self.lblPerson.image = self.imgPerson

    def handlePantsColor(self, event):
        """Update the color of the slider and the pants."""
        # Update the Slider
        rgb = ImageColor.getrgb("hsl(" + str(self.pantsColor.get()) + ", 100%, 50%)")
        newHex = self.rgb_to_hex(rgb)
        self.sldMidColor.config(bg=newHex)

        # Update the person
        self.imgPerson = self.character.setPantsColor(newHex)
        self.lblPerson.configure(image=self.imgPerson)
        self.lblPerson.image = self.imgPerson

    def handleShoesColor(self, event):
        """Update the color of the slider and the shoes."""
        # Update the Slider
        rgb = ImageColor.getrgb("hsl(" + str(self.shoesColor.get()) + ", 100%, 50%)")
        newHex = self.rgb_to_hex(rgb)
        self.sldBotColor.config(bg=newHex)

        # Update the person
        self.imgPerson = self.character.setShoesColor(newHex)
        self.lblPerson.configure(image=self.imgPerson)
        self.lblPerson.image = self.imgPerson

    def shirtLeft(self):
        self.character._shirtLeft()
        self.updateCharLabel()

    def shirtRight(self):
        self.character._shirtRight()
        self.updateCharLabel()

    def pantsLeft(self):
        self.character._pantsLeft()
        self.updateCharLabel()

    def pantsRight(self):
        self.character._pantsRight()
        self.updateCharLabel()

    def shoesLeft(self):
        self.character._shoesLeft()
        self.updateCharLabel()

    def shoesRight(self):
        self.character._shoesRight()
        self.updateCharLabel()

    def setSpecies(self, event):
        self.species.set(self.species_list[self.speciesNum.get()])

        # Update the character
        self.character.update_character(self.species.get(), self.gender.get(), self.colorNum.get())
        self.updateCharLabel()

    def setGender(self):
        # Update the character
        self.character.update_character(self.species.get(), self.gender.get(), self.colorNum.get())
        self.updateCharLabel()

    def setColor(self, event):
        self.character.update_character(self.species.get(), self.gender.get(), self.colorNum.get())
        self.updateCharLabel()


    def infoNextClick(self):
        print("yo")
        print(self.entFName.get())
        print(self.height.get())

    def updateCharLabel(self):
        self.imgPerson = self.character.returnGIF()
        self.lblPerson.configure(image=self.imgPerson)
        self.lblPerson.image = self.imgPerson

class CharacterView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Character View", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


app = Creator()
app.mainloop()