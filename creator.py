import tkinter as tk
from PIL import Image, ImageTk, ImageColor
import numpy as np
import os
import ImageEdit as IE
import DBManager as DB

LARGE_FONT = ("Verdana", 12)

class Creator(tk.Tk):

    def __init__(self):

        # Initializations
        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.d=DB.DBManager()
        self.d.create_tables()
        print("HI")
        #self.d.insert_character()
        #self.d.print_all_character()


        # Pretty Patty
        tk.Tk.wm_title(self, "Character Creator")
        #tk.Tk.protocol("WM_DELETE_WINDOW", self.on_close)

        # Frame Stuff
        self.frames = {}

        for F in (MainMenu, CharacterCreate, CharacterView, PersonalityTest, CharacterSubmit):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        """Pass a class (page) to bring to the front."""
        frame = self.frames[cont]
        frame.tkraise()
        #self.frame.tkraise()

    def on_close(self):
        print("Closing")
        self.d.close_database()
        tk.Tk.destroy(self)


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
        # Top most part of the screen
        self.label = tk.Label(self, text="The Character Creator", font=LARGE_FONT)
        self.label.pack()

        self.controller = controller
        # ------ Button attributes -----
        but_width = 16
        but_padx = '2m'
        but_pady = '1m'

        # ----- Create Character -------
        self.butCreate = tk.Button(self,
                                   text="Create Character",
                                   background="blue",
                                   command=self.toCreateClick,
                                   width=but_width,
                                   padx=but_padx,
                                   pady=but_pady)
        self.butCreate.pack()
        self.butCreate.focus_force()

        # ----- View Characters --------
        self.butView = tk.Button(self,
                                 text="View Characters",
                                 background="blue",
                                 command=self.toViewClick,
                                 width=but_width,
                                 padx=but_padx,
                                 pady=but_pady)
        self.butView.pack()

    def toCreateClick(self):
        self.controller.d.set_mode("new")
        self.controller.show_frame(CharacterCreate)

    def toViewClick(self):
        self.controller.d.set_mode("edit")
        self.controller.show_frame(CharacterView)


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

        self.character = IE.CharacterManip()
        self.character.update_character(self.species.get(), self.gender.get(), self.colorNum.get())
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

        self.character = IE.CharacterManip()
        self.character.update_character(self.species.get(), self.gender.get(), self.colorNum.get())
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

    def not_null(self):
        """Makes sure the proper entries are not null for proper SQL statements."""
        return (self.entFName.get() and self.entLName.get())

    def back2MainClick(self):
        # When going back to main, clear this screen and personality choices
        self.set_defaults()
        self.controller.frames[PersonalityTest].set_defaults()
        self.controller.show_frame(MainMenu)

    def forward2PersClick(self):
        if self.not_null():
            self.controller.show_frame(PersonalityTest)
        else:
            print("Fill out first and last name.")

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
results of this quiz will determine the personality of your character.
(Very Much Disagree, Neutral, Very Much Agree)
"""

        lblInstructions = tk.Label(self, text=instr)
        #lblInstructions.pack(pady=10, padx=10)
        lblInstructions.grid(row=1, column=0, columnspan=2)

        labels = []
        questionFrames = []
        questions = ["I have a rich imagination.",
                     "I enjoy hearing new/unique ideas.",
                     "I am open to trying new things.",
                     "I complete tasks thoroughly and accurately.",
                     "I like to tidy up and keep things clean.",
                     "I am often aware of my surroundings.",
                     "I make friends easily.",
                     "I ama very social and outgoing person.",
                     "I feel comfortable around people.",
                     "I am interested in other people's problems.",
                     "I believe that everyone is equal.",
                     "I like to help others.",
                     'I tend to worry about things and panic easily.',
                     "I easily get anxious.",
                     "I can get irritated and stressed over any little thing very quickly."]
        self.rbArray = []

        self.answers = [tk.IntVar(value=2) for i in range(len(questions))]

        for y in range(len(questions)):
            labels.append(tk.Label(self, text=questions[y]))
            labels[y].grid(row=2 + y, column=0)

            questionFrames.append(tk.LabelFrame(self))
            questionFrames[y].grid(row=2 + y, column=1)

            self.rbArray.append([])

            for x in range(5):
                self.rbArray[y].append(tk.Radiobutton(questionFrames[y], variable=self.answers[y], value=x))
                self.rbArray[y][x].grid(row=0, column=x + 1)


        butBack = tk.Button(self, text="Back", command=self.back2CharClick)
        butBack.grid(row=50,column=0)

        butForward = tk.Button(self, text="Next", command=self.forward2PreviewClick)
        butForward.grid(row=50, column=1)

    def set_defaults(self):
        for var in self.answers:
            var.set(2)

    def back2CharClick(self):
        # Nothing needs updated when going back
        self.controller.show_frame(CharacterCreate)

    def forward2PreviewClick(self):
        # When going forward, make sure the page is updated
        self.controller.frames[CharacterSubmit].update_page()
        self.controller.show_frame(CharacterSubmit)


class CharacterSubmit(tk.Frame):
    """This will display a character for submission.

    Will show the character information up to this point in the program, and then
    submit it to the database.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Title at the top of the screen
        title = tk.Label(self, text="Finalize Character", font=LARGE_FONT)
        title.grid(row=0, column=0, columnspan=3)

        # Data setup for database submission
        self.d_character = {}
        self.d_clothing = {}
        self.d_personality = {}
        self.d_job = {}
        self.d_skill = {}

        #self.aggregate_data()



    def aggregate_data(self):
        """Accesses all other frames to grab all their data and format it for the database.

        Use when creating the characters.
        """
        # Character Table
        self.d_character['fName'] = self.controller.frames[CharacterCreate].entFName.get()
        self.d_character['lName'] = self.controller.frames[CharacterCreate].entLName.get()
        self.d_character['size'] = self.controller.frames[CharacterCreate].height.get()  # Known as height
        self.d_character['weight'] = self.controller.frames[CharacterCreate].weight.get()
        self.d_character['species'] = self.controller.frames[CharacterCreate].species.get()
        self.d_character['race'] = self.controller.frames[CharacterCreate].colorNum.get()  # Known as color, int
        self.d_character['gender'] = self.controller.frames[CharacterCreate].gender.get()

        # Clothing Table
        # [file_name, rgbHex val]
        char = self.controller.frames[CharacterCreate].character
        self.d_clothing['shirt'] = [char.f_shirts[char.curr_shirt], char.col_shirt]
        self.d_clothing['pants'] = [char.f_pants[char.curr_pants], char.col_pants]
        self.d_clothing['shoes'] = [char.f_shoes[char.curr_shoes], char.col_shoes]

        # Personality Table
        ans = self.controller.frames[PersonalityTest].answers
        self.d_personality['ope'] = (ans[0].get() + ans[1].get() + ans[2].get()) / 12
        self.d_personality['con'] = (ans[3].get() + ans[4].get() + ans[5].get()) / 12
        self.d_personality['ext'] = (ans[6].get() + ans[7].get() + ans[8].get()) / 12
        self.d_personality['agr'] = (ans[9].get() + ans[10].get() + ans[11].get()) / 12
        self.d_personality['neu'] = (ans[12].get() + ans[13].get() + ans[14].get()) / 12

        # Job Table
        self.d_job = self.controller.frames[CharacterCreate].entJob.get()
        # Skill Table
        self.d_skill = self.controller.frames[CharacterCreate].entSkill.get()



        print(self.d_character)
        print(self.d_clothing)
        print(self.d_personality)

    def update_page(self):
        self.aggregate_data()

        # ----- Left side = Character Info -----
        self.lfCharInfo = tk.LabelFrame(self, text="Character Information")
        self.lfCharInfo.grid(row=1, column=0)
        self.lblList = []
        self.lblList = [tk.Label(self.lfCharInfo, text="First Name: " + self.d_character['fName']),
                        tk.Label(self.lfCharInfo, text="Last Name: " + self.d_character['lName']),
                        tk.Label(self.lfCharInfo, text="Size: " + self.d_character['size']),
                        tk.Label(self.lfCharInfo, text="Weight: " + self.d_character['weight']),
                        tk.Label(self.lfCharInfo, text="Gender: " + self.d_character['gender'])]
        print(self.d_character['fName'])
        i = 0
        for label in self.lblList:
            label.grid(row=i, column=0)
            i += 1

        # ----- Middle = Picture of Character -----
        self.lfVisual = tk.LabelFrame(self, text="Visuals")
        self.lfVisual.grid(row=1, column=1)

        self.character = IE.CharacterManip()
        self.character.define_character(self.d_character, self.d_clothing)

        self.imgPerson = self.character.returnGIF()
        self.lblPerson = tk.Label(self.lfVisual, image=self.imgPerson)
        self.lblPerson.image = self.imgPerson
        self.lblPerson.grid(row=0, column=0)

        # ----- Second middle = Personality Results -----
        self.lfPers = tk.LabelFrame(self, text="Personality")
        self.lfPers.grid(row=1, column=2)

        lblPers = [tk.Label(self.lfPers, text=str(self.d_personality['ope'])),
                   tk.Label(self.lfPers, text=str(self.d_personality['con'])),
                   tk.Label(self.lfPers, text=str(self.d_personality['ext'])),
                   tk.Label(self.lfPers, text=str(self.d_personality['agr'])),
                   tk.Label(self.lfPers, text=str(self.d_personality['neu']))]
        for c, label in enumerate(lblPers):
            label.grid(row=c, column=0)



        # ----- Right side = Buttons to go back -----
        self.lfRightButt = tk.LabelFrame(self, text="Second Chance")
        self.lfRightButt.grid(row=1, column=3)

        butEditChar = tk.Button(self.lfRightButt,
                                text="To Edit Character",
                                command=self.butEditCharClick)
        butEditChar.grid(row=0, column=0)

        butEditPers = tk.Button(self.lfRightButt,
                                text="To Edit Personality",
                                command=self.butEditPersClick)
        butEditPers.grid(row=1, column=0)

        # ----- Bottom = Submit button -----
        butSubmit = tk.Button(self,
                              text="Submit",
                              command=self.butSubmitClick)
        butSubmit.grid(row=2, column=1)


    def butEditCharClick(self):
        self.controller.show_frame(CharacterCreate)

    def butEditPersClick(self):
        self.controller.show_frame(PersonalityTest)

    def butSubmitClick(self):
        """Will upload the character to the database and clear all screens used."""
        self.controller.d.insertion(self.d_character, self.d_clothing, self.d_personality, self.d_job, self.d_skill)

        pass

class CharacterView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        row_num=0
        label = tk.Label(self, text="Character View", font=LARGE_FONT)
        label.grid(row=0, column=1, columnspan=2)

        self.header = tk.Label(self, text="First Name\tLast Name\tSpecies\tGender", font=LARGE_FONT)
        self.header.grid(row=1,column=1)
        row_num+=1

        data=controller.d.print_all_character()
        Chars=[]

        for counter, r in enumerate(data):
            Chars.append([tk.Label(self, text=r[0])])
            for I, label in enumerate(Chars[counter]):
                label.grid(row=counter, column=I)




app = Creator()
app.protocol("WM_DELETE_WINDOW", app.on_close)
app.mainloop()
