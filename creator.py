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

        for F in (MainMenu, CharacterCreate, CharacterView, PersonalityTest):

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
    """Shown at the start of the program.

    Allows for the user to select between creating a character, and viewing all characters.
    """

    def __init__(self, parent, controller):
        """

        :param parent: The frame of the Creator
        :param controller: Creator self
        """
        tk.Frame.__init__(self, parent)
        print("MEME ALERT")
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
    """The first frame of the character creator.

    Handles the visual effects of the character, as well as the name, job, skill, etc.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="green")
        self.controller = controller

        label = tk.Label(self, text="Time To Design", font=LARGE_FONT)
        #label.pack(pady=10, padx=10)
        label.grid(row=0, column=0, columnspan=2)

        # ----- Information Frame -----
        lfInfo = tk.LabelFrame(self,
                               text="Character Information")
        #lfInfo.pack(fill="both", expand="yes", side="left")
        lfInfo.grid(row=1, column=0)

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




        # ----- Visual Frame -----
        lfVisual = tk.LabelFrame(self,
                                 text="Design Character")
        #lfVisual.pack(fill="both", expand="yes", side="right")
        lfVisual.grid(row=1, column=1)


        # Asset import
        imgLeftArrow = tk.PhotoImage(file=os.path.join("assets", "butLeft.gif"))
        imgRightArrow = tk.PhotoImage(file=os.path.join("assets", "butRight.gif"))

        # Middle Person, needs to be three sections, maybe four

        self.character = IE.CharacterManip(self.species.get(), self.gender.get(), self.colorNum.get())
        self.imgPerson = self.character.returnGIF()
        self.lblPerson = tk.Label(lfVisual,
                          image=self.imgPerson)
        self.lblPerson.image = self.imgPerson
        self.lblPerson.grid(row=1,
                            column=1,
                            rowspan=3)

        but_dim = 50

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

        # ----- Forward-Backward Frame -----
        lfBot = tk.LabelFrame(self,
                              text="Ready to Move")
        lfBot.grid(row=2, column=0, columnspan=2)

        butBack2Main = tk.Button(lfBot,
                                 text="Back",
                                 command=self.back2MainClick)
        butBack2Main.grid(row=0, column=0)

        butForward2Pers = tk.Button(lfBot,
                                    text="Next",
                                    command=self.forward2PersClick)
        butForward2Pers.grid(row=0, column=1)

    def set_defaults(self):
        """Sets everything to default when you go back to main menu."""
        self.entFName.delete(0, tk.END)
        self.entLName.delete(0, tk.END)
        self.height.set("Short")
        self.weight.set("Light")
        self.speciesNum.set(0)
        self.species.set(self.species_list[0])
        self.colorNum.set(0)
        self.gender.set("Male")
        self.entSkill.delete(0, tk.END)
        self.entJob.delete(0, tk.END)

        self.character = IE.CharacterManip(self.species.get(), self.gender.get(), self.colorNum.get())
        self.updateCharLabel()
        self.shirtColor.set(0)
        self.hexShirtColor.set("#ff0000")
        self.sldTopColor.config(background=self.hexShirtColor.get())
        self.pantsColor.set(0)
        self.hexPantsColor.set("#ff0000")
        self.sldMidColor.config(background=self.hexPantsColor.get())
        self.shoesColor.set(0)
        self.hexShoesColor.set("#ff0000")
        self.sldBotColor.config(background=self.hexShoesColor.get())


    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb

    def handleShirtColor(self, event):
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


    def back2MainClick(self):
        print("yo")
        print(self.entFName.get())
        print(self.height.get())
        self.set_defaults()
        self.controller.show_frame(MainMenu)

    def forward2PersClick(self):
        self.controller.show_frame(PersonalityTest)

    def updateCharLabel(self):
        self.imgPerson = self.character.returnGIF()
        self.lblPerson.configure(image=self.imgPerson)
        self.lblPerson.image = self.imgPerson

class PersonalityTest(tk.Frame):
    """The second page of the character creator.

    The personality quiz of the character, not the human.

    (OPE)
    Openness - High scores tend to belong to those who like to learn and experience new things.
        ex) Insightful and Imaginative
    (CON)
    Conscientiousness - High scores belong to those who are reliable and prompt.
        ex) Organized, methodic, thorough
    (EXT)
    Extraversion - Where you get your energy from, others or yourself.
        ex) Energetic, talkative, assertive
    (AGR)
    Agreeableness - High scores trend towards being friendly, cooperative, and compassionate.
    (NEU)
    Neuroticism - Emotional stability. High scores experience emotional instability and neg emotions.
        ex) Moody, tense
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Personality Test", font=LARGE_FONT)
        #label.pack(pady=10, padx=10)
        label.grid(row=0, column=0, columnspan=2)

        instr = """For each question, answer how true the statement is to your character. The \
results of this quiz will determine the personality of your character."""

        lblInstructions = tk.Label(self, text=instr)
        #lblInstructions.pack(pady=10, padx=10)
        lblInstructions.grid(row=1, column=0, columnspan=2)

        labels = []
        questionFrames = []
        questions = ["1",
                     "2",
                     "3",
                     "4",
                     "5",
                     "6",
                     "7",
                     "8",
                     "9",
                     "10"]
        self.rbArray = []


        self.answers = [tk.IntVar() for i in range(10)]

        for y in range(10):
            labels.append(tk.Label(self, text=questions[y]))
            labels[y].grid(row=2 + y, column=0)

            questionFrames.append(tk.LabelFrame(self))
            questionFrames[y].grid(row=2 + y, column=1)

            self.rbArray.append([])
            #print(rbArray)

            for x in range(5):
                self.rbArray[y].append(tk.Radiobutton(questionFrames[y], variable=self.answers[y], value=x))
                self.rbArray[y][x].grid(row=0, column=x + 1)


        butBack = tk.Button(self, text="Back", command=self.back2CharClick)
        butBack.grid(row=50,column=0)

        butForward = tk.Button(self, text="Next", command=self.forward2PreviewClick)
        butForward.grid(row=50, column=1)

        """
        # ----- Q1 -----
        lfQ1 = tk.LabelFrame(self,
                             text="Question 1")
        #lfQ1.pack(fill="both", expand="yes", side="top")
        lfQ1.grid(row=2, column=0)

        lblQ1 = tk.Label(lfQ1,
                         text="This is a test question.")
        lblQ1.grid(row=0, column=0, columnspan=5)

        self.Q1 = tk.IntVar()
        rbQ1 = []
        for x in range(5):
            rbQ1.append(tk.Radiobutton(lfQ1, variable=self.Q1, value=x))
            rbQ1[x].grid(row=0, column=x+1)

        # ----- Q2 -----
        lfQ2 = tk.LabelFrame(self,
                             text="Question 2")
        lfQ2.grid(row=3, column=0)

        lblQ2 = tk.Label(lfQ2,
                         text="This is a test question.")
        lblQ2.grid(row=0, column=0, columnspan=5)

        self.Q2 = tk.IntVar()
        rbQ2 = []
        for x in range(5):
            rbQ2.append(tk.Radiobutton(lfQ2, variable=self.Q2, value=x))
            rbQ2[x].grid(row=0, column=x+1)

        # ----- Q3 -----
        lfQ3 = tk.LabelFrame(self,
                             text="Question 3")
        lfQ3.grid(row=4, column=0)

        lblQ3 = tk.Label(lfQ3,
                         text="This is a test question.")
        lblQ3.grid(row=0, column=0, columnspan=5)

        self.Q3 = tk.IntVar()
        rbQ3 = []
        for x in range(5):
            rbQ3.append(tk.Radiobutton(lfQ3, variable=self.Q3, value=x))
            rbQ3[x].grid(row=0, column=x+1)

        # ----- Q4 -----
        lfQ4 = tk.LabelFrame(self,
                             text="Question 4")
        lfQ4.grid(row=5, column=0)

        lblQ4 = tk.Label(lfQ4,
                         text="This is a test question.")
        lblQ4.grid(row=0, column=0, columnspan=5)

        self.Q4 = tk.IntVar()
        rbQ4 = []
        for x in range(5):
            rbQ4.append(tk.Radiobutton(lfQ4, variable=self.Q4, value=x))
            rbQ4[x].grid(row=0, column=x+1)

        # ----- Q5 -----
        lfQ5 = tk.LabelFrame(self,
                             text="Question 5")
        lfQ5.grid(row=6, column=0)

        lblQ5 = tk.Label(lfQ5,
                         text="This is a test question.")
        lblQ5.grid(row=0, column=0, columnspan=5)

        self.Q5 = tk.IntVar()
        rbQ5 = []
        for x in range(5):
            rbQ5.append(tk.Radiobutton(lfQ5, variable=self.Q5, value=x))
            rbQ5[x].grid(row=0, column=x+1)

        # ----- Q6 -----
        lfQ6 = tk.LabelFrame(self,
                             text="Question 6")
        lfQ6.grid(row=7, column=0)

        lblQ6 = tk.Label(lfQ6,
                         text="This is a test question.")
        lblQ6.grid(row=0, column=0, columnspan=5)

        self.Q6 = tk.IntVar()
        rbQ6 = []
        for x in range(5):
            rbQ6.append(tk.Radiobutton(lfQ6, variable=self.Q6, value=x))
            rbQ6[x].grid(row=0, column=x+1)

        # ----- Q7 -----
        lfQ7 = tk.LabelFrame(self,
                             text="Question 7")
        lfQ7.grid(row=8, column=0)

        lblQ7 = tk.Label(lfQ7,
                         text="This is a test question.")
        lblQ7.grid(row=0, column=0, columnspan=5)

        self.Q7 = tk.IntVar()
        rbQ7 = []
        for x in range(5):
            rbQ7.append(tk.Radiobutton(lfQ7, variable=self.Q7, value=x))
            rbQ7[x].grid(row=0, column=x+1)

        # ----- Q8 -----
        lfQ8 = tk.LabelFrame(self,
                             text="Question 8")
        lfQ8.grid(row=9, column=0)

        lblQ8 = tk.Label(lfQ8,
                         text="This is a test question.")
        lblQ8.grid(row=0, column=0, columnspan=5)

        self.Q8 = tk.IntVar()
        rbQ8 = []
        for x in range(5):
            rbQ8.append(tk.Radiobutton(lfQ8, variable=self.Q8, value=x))
            rbQ8[x].grid(row=0, column=x+1)

        # ----- Q9 -----
        lfQ9 = tk.LabelFrame(self,
                             text="Question 9")
        lfQ9.grid(row=10, column=0)

        lblQ9 = tk.Label(lfQ9,
                         text="This is a test question.")
        lblQ9.grid(row=0, column=0, columnspan=5)

        self.Q9 = tk.IntVar()
        rbQ9 = []
        for x in range(5):
            rbQ9.append(tk.Radiobutton(lfQ9, variable=self.Q9, value=x))
            rbQ9[x].grid(row=0, column=x+1)

        # ----- Q10 -----
        lfQ10 = tk.LabelFrame(self,
                              text="Question 10")
        lfQ10.grid(row=11, column=0)

        lblQ10 = tk.Label(lfQ10,
                          text="This is a test question.")
        lblQ10.grid(row=0, column=0, columnspan=5)

        self.Q10 = tk.IntVar()
        rbQ10 = []
        for x in range(5):
            rbQ10.append(tk.Radiobutton(lfQ10, variable=self.Q10, value=x))
            rbQ10[x].grid(row=0, column=x+1)

        # Buttons to move forward and backwards
        """












    def test(self):
        # This is how to go back
        for x in range(10):
            print("Q" + str(x) + ":", self.answers[x].get())
        print(self.answers[0].get())
        print("NAME:", self.controller.frames[CharacterCreate].entFName.get())

    def back2CharClick(self):
        self.controller.show_frame(CharacterCreate)

    def forward2PreviewClick(self):
        #self.controller.show_frame()
        pass


class CharacterView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Character View", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


app = Creator()
app.mainloop()