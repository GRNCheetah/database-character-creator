import tkinter as tk
from PIL import ImageColor, Image, ImageTk
import os
import ImageEdit as IE
import DBManager as DB
import Character

LARGE_FONT = ("Verdana", 12)
LITTLE_FONT = ("fixedsys", 10)
CLR_WHITE = "#ffffff"
CLR_MAIN = "#f6dd95"
CLR_LAVENDER = "#f2d9ff"


class Creator(tk.Tk):

    def __init__(self):
        # Initializations
        tk.Tk.__init__(self)
        container = tk.Frame(self)

        # Centering
        self.w = 800
        self.h = 600
        screen_w = container.winfo_screenwidth()
        screen_h = container.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, int((screen_w/2) - (self.w/2)), int((screen_h/2) - (self.h/2))))

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        # Database stuff
        self.d = DB.DBManager()
        self.d.create_tables()

        # Pretty Patty
        tk.Tk.wm_title(self, "Character Creator")

        self.curr_character = Character.Character()

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
        # self.frame.tkraise()

    def on_close(self):
        self.d.close_database()
        tk.Tk.destroy(self)
        exit() # Kills all windows, maybe not the best way but it works

    def popup(self, msg):
        pop = tk.Tk()
        pop.wm_title("Wait!")
        pop.focus_force()

        w = 220
        h = 50

        pop.geometry('%dx%d+%d+%d' % (w, h, int((pop.winfo_screenwidth()/2) - (w/2)), int((pop.winfo_screenheight()/2) - (h/2))))

        lbl = tk.Label(pop, text=msg)
        lbl.grid(row=0, column=0)
        button = tk.Button(pop, text="Ok", command=pop.destroy)
        button.grid(row=1, column=0)
        pop.mainloop()

class MainMenu(tk.Frame):
    """Shown at the start of the program.

    Allows for the user to select between creating a character, and viewing all characters.
    """

    def __init__(self, parent, controller):
        """

        :param parent: The frame of the Creator
        :param controller: Creator self
        """
        tk.Frame.__init__(self, parent, bg=CLR_MAIN)
        # Top most part of the screen
        img = Image.open(os.path.join("assets", "title.jpg"))
        img = img.resize((int(controller.w*.8), int(controller.h*.45)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.title = tk.Label(self,
                              image=img,
                              borderwidth=0,
                              highlightthickness=0)
        self.title.image = img
        self.title.pack()


        self.controller = controller
        # ------ Button attributes -----
        but_width = 16
        but_padx = '2m'
        but_pady = '5m'

        # ----- Create Character -------
        self.butCreate = tk.Button(self,
                                   text="Create Character",
                                   background=CLR_LAVENDER,
                                   command=self.toCreateClick,
                                   width=but_width,
                                   padx=but_padx,
                                   pady=but_pady,
                                   font=("fixedsys", 20))
        self.butCreate.pack()
        self.butCreate.focus_force()

        # ----- View Characters --------
        self.butView = tk.Button(self,
                                 text="View Characters",
                                 background=CLR_LAVENDER,
                                 command=self.toViewClick,
                                 width=but_width,
                                 padx=but_padx,
                                 pady=but_pady,
                                 font=("fixedsys", 20))
        self.butView.pack()

        # ----- Quit --------
        self.butQuit = tk.Button(self,
                                 text="Quit",
                                 background=CLR_LAVENDER,
                                 command=controller.on_close,
                                 width=but_width,
                                 padx=but_padx,
                                 pady=but_pady,
                                 font=("fixedsys", 20))
        self.butQuit.pack()

    def toCreateClick(self):
        self.controller.d.set_mode("new")
        self.controller.show_frame(CharacterCreate)

    def toViewClick(self):
        self.controller.d.set_mode("edit")
        self.controller.frames[CharacterView].update_page()
        self.controller.show_frame(CharacterView)


class CharacterCreate(tk.Frame):
    """The first frame of the character creator.

    Handles the visual effects of the character, as well as the name, job, skill, etc.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CLR_MAIN)
        self.controller = controller

        label = tk.Label(self, text="Time To Design", font=("fixedsys", 20, "bold"), bg=CLR_MAIN)
        label.grid(row=0, column=1, columnspan=2)

        # ----- Information Frame -----
        lfInfo = tk.LabelFrame(self,
                               text="Character Information", font=("fixedsys", 16, "bold"),
                               bg="white", borderwidth=0, highlightthickness=0)

        lfInfo.grid(row=1, column=0)

        # First name
        lblFName = tk.Label(lfInfo,
                            text="First Name:", bg=CLR_WHITE, font=LITTLE_FONT)
        lblFName.grid(row=0, column=0)
        self.entFName = tk.Entry(lfInfo)
        self.entFName.grid(row=0, column=1)
        # Last name
        lblLName = tk.Label(lfInfo,
                            text="Last Name:", bg=CLR_WHITE, font=LITTLE_FONT)
        lblLName.grid(row=1, column=0)
        self.entLName = tk.Entry(lfInfo)
        self.entLName.grid(row=1, column=1)
        # Height
        lblHeight = tk.Label(lfInfo,
                             text="Height:", bg=CLR_WHITE, font=LITTLE_FONT)
        lblHeight.grid(row=2, column=0)
        height_options = {"Short", "Average", "Tall"}
        self.height = tk.StringVar(lfInfo, value="Short")
        dropHeight = tk.OptionMenu(lfInfo, self.height, *height_options)
        dropHeight.configure(bg=CLR_WHITE,
                             borderwidth=1,
                             highlightthickness=0,
                             font=LITTLE_FONT)
        dropHeight.grid(row=2, column=1)

        # Weight
        lblWeight = tk.Label(lfInfo,
                             text="Weight:", bg=CLR_WHITE, font=LITTLE_FONT)
        lblWeight.grid(row=3, column=0)
        weight_options = {"Light", "Average", "Heavy"}
        self.weight = tk.StringVar(lfInfo, value="Light")
        dropWeight = tk.OptionMenu(lfInfo, self.weight, *weight_options)
        dropWeight.configure(bg=CLR_WHITE,
                             borderwidth=1,
                             highlightthickness=0,
                             font=LITTLE_FONT)
        dropWeight.grid(row=3, column=1)

        # Species
        lblSpecies = tk.Label(lfInfo,
                              text="Species:", bg=CLR_WHITE, font=LITTLE_FONT)
        lblSpecies.grid(row=4, column=0)
        self.speciesNum = tk.IntVar(0)
        self.species_list = ["Human", "Bear", "Alien"]
        self.species = tk.StringVar()
        self.species.set(self.species_list[0])
        sldSpecies = tk.Scale(lfInfo,
                              variable=self.speciesNum,
                              from_=0,
                              to=(len(self.species_list) - 2),
                              orient=tk.HORIZONTAL,
                              command=self.setSpecies,
                              bg=CLR_WHITE,
                              borderwidth=0,
                              highlightthickness=0,
                              showvalue=0,
                              font=LITTLE_FONT)
        sldSpecies.grid(row=5, column=1, pady=5)
        lblSpeciesDisp = tk.Label(lfInfo,
                                  textvariable=self.species,
                                  bg=CLR_WHITE,
                                  borderwidth=0,
                                  highlightthickness=0,
                                  font=LITTLE_FONT)
        lblSpeciesDisp.grid(row=4, column=1)

        # Color
        lblColor = tk.Label(lfInfo,
                            text="Skin Tone:", bg=CLR_WHITE, borderwidth=0, highlightthickness=0, font=LITTLE_FONT)
        lblColor.grid(row=6, column=0)
        self.colorNum = tk.IntVar(0)
        sldColor = tk.Scale(lfInfo,
                            variable=self.colorNum,
                            from_=0,
                            to=4,
                            orient=tk.HORIZONTAL,
                            command=self.setColor,
                            bg=CLR_WHITE,
                            borderwidth=0,
                            highlightthickness=0,
                            showvalue=0)
        sldColor.grid(row=6, column=1, pady=5)

        # Gender
        lblGender = tk.Label(lfInfo,
                             text="Gender:", bg=CLR_WHITE, borderwidth=0, highlightthickness=0, font=LITTLE_FONT)
        lblGender.grid(row=7, column=0)
        self.gender = tk.StringVar()
        self.gender.set("Male")
        rbMale = tk.Radiobutton(lfInfo,
                                text="Male",
                                variable=self.gender,
                                value="Male",
                                command=self.setGender,
                                bg=CLR_WHITE,borderwidth=0, highlightthickness=0,
                                font=LITTLE_FONT)
        rbMale.grid(row=7, column=1)
        rbFemale = tk.Radiobutton(lfInfo,
                                  text="Female",
                                  variable=self.gender,
                                  value="Female",
                                  command=self.setGender,
                                  bg=CLR_WHITE, borderwidth=0, highlightthickness=0,
                                  font=LITTLE_FONT)
        rbFemale.grid(row=8, column=1)

        # Skill
        lblSkill = tk.Label(lfInfo,
                            text="Skill:", bg=CLR_WHITE, borderwidth=0, highlightthickness=0, font=LITTLE_FONT)
        lblSkill.grid(row=9, column=0)
        self.entSkill = tk.Entry(lfInfo)
        self.entSkill.grid(row=9, column=1)

        # Job
        lblJob = tk.Label(lfInfo,
                          text="Job:", bg=CLR_WHITE, borderwidth=0, highlightthickness=0, font=LITTLE_FONT)
        lblJob.grid(row=10, column=0)
        self.entJob = tk.Entry(lfInfo)
        self.entJob.grid(row=10, column=1)

        # ----- Visual Frame -----
        lfVisual = tk.LabelFrame(self,
                                 text="Design Character",
                                 font=("fixedsys", 16, "bold"),
                                 bg="white", borderwidth=0, highlightthickness=0)
        lfVisual.grid(row=1, column=2)

        # Asset import
        imgLeftArrow = tk.PhotoImage(file=os.path.join("assets", "butLeft.gif"))
        imgRightArrow = tk.PhotoImage(file=os.path.join("assets", "butRight.gif"))

        self.character = IE.CharacterManip()
        self.character.update_character(self.species.get(), self.gender.get(), self.colorNum.get())
        self.imgPerson = self.character.returnGIF()
        self.lblPerson = tk.Label(lfVisual,
                                  image=self.imgPerson,
                                  bg="white")
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
                                 command=self.shirtLeft, bg=CLR_WHITE, borderwidth=0, highlightthickness=0)
        butLeftShirt.image = imgLeftArrow
        butLeftShirt.grid(row=1, column=0)

        # Top Right
        butRightShirt = tk.Button(lfVisual,
                                  image=imgRightArrow,
                                  width=but_dim,
                                  height=but_dim,
                                  command=self.shirtRight, bg=CLR_WHITE, borderwidth=0, highlightthickness=0)
        butRightShirt.image = imgRightArrow
        butRightShirt.grid(row=1, column=2)

        # Mid left
        butLeftPants = tk.Button(lfVisual,
                                 image=imgLeftArrow,
                                 width=but_dim,
                                 height=but_dim,
                                 command=self.pantsLeft, bg=CLR_WHITE, borderwidth=0, highlightthickness=0)
        butLeftPants.immge = imgLeftArrow
        butLeftPants.grid(row=2, column=0)

        # Mid Right
        butRightPants = tk.Button(lfVisual,
                                  image=imgRightArrow,
                                  width=but_dim,
                                  height=but_dim,
                                  command=self.pantsRight, bg=CLR_WHITE, borderwidth=0, highlightthickness=0)
        butRightPants.image = imgRightArrow
        butRightPants.grid(row=2, column=2)

        # Bot left
        butLeftShoes = tk.Button(lfVisual,
                                 image=imgLeftArrow,
                                 width=but_dim,
                                 height=but_dim,
                                 command=self.shoesLeft, bg=CLR_WHITE, borderwidth=0, highlightthickness=0)
        butLeftShoes.image = imgLeftArrow
        butLeftShoes.grid(row=3, column=0)

        # Bot Right
        butRightShoes = tk.Button(lfVisual,
                                  image=imgRightArrow,
                                  width=but_dim,
                                  height=but_dim,
                                  command=self.shoesRight, bg=CLR_WHITE, borderwidth=0, highlightthickness=0)
        butRightShoes.image = imgRightArrow
        butRightShoes.grid(row=3, column=2)

        # Top Slider
        self.shirtColor = tk.IntVar(0)  # Represents hex number in decimal
        self.hexShirtColor = tk.StringVar()
        self.hexShirtColor.set("#ff0000")
        self.sldTopColor = tk.Scale(lfVisual,
                                    variable=self.shirtColor,
                                    from_=0,
                                    to=360,
                                    orient=tk.HORIZONTAL,
                                    background=self.hexShirtColor.get(),  borderwidth=0, highlightthickness=0, showvalue=0)
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
                                    background=self.hexPantsColor.get(), borderwidth=0, highlightthickness=0, showvalue=0)
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
                                    background=self.hexShoesColor.get(), borderwidth=0, highlightthickness=0, showvalue=0)
        self.sldBotColor.config(command=self.handleShoesColor)
        self.sldBotColor.grid(row=3, column=3)

        # ----- Forward-Backward Frame -----
        lfBot = tk.LabelFrame(self,
                              text="Ready to Move",
                              bg="white")
        lfBot.grid(row=2, column=0, columnspan=2)

        butBack2Main = tk.Button(lfBot,
                                 text="Back",
                                 command=lambda: self.are_you_sure(),
                                 bg="#f46e42")
        butBack2Main.grid(row=0, column=0)

        butForward2Pers = tk.Button(lfBot,
                                    text="Next",
                                    command=self.forward2PersClick,
                                    bg="#4af441")
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

    def are_you_sure(self):
        """Pop up to make sure user knows progress will be lost."""

        pop = tk.Tk()
        pop.wm_title("Wait!")
        pop.focus_force()

        w = 200
        h = 75

        pop.geometry('%dx%d+%d+%d' % (w, h, int((pop.winfo_screenwidth()/2) - (w/2)), int((pop.winfo_screenheight()/2) - (h/2))))
        msg = tk.Label(pop, text="Are you sure you want quit?\nProgress will be lost.")
        msg.grid(row=0, column=0, columnspan=2)
        butYes = tk.Button(pop, text="Yes", bg="#4af441", command=lambda: self.back2MainClick(pop))
        butYes.grid(row=1, column=0)
        butNo = tk.Button(pop, text="No", bg="#f46e42", command=pop.destroy)
        butNo.grid(row=1, column=1)

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

    def back2MainClick(self, pop):
        """Will go to Main Menu or View screen depending on the database mode."""
        # When going back to main, clear this screen and personality choices
        self.set_defaults()
        self.controller.frames[PersonalityTest].set_defaults()
        pop.destroy()

        if self.controller.d.mode == "new":
            self.controller.show_frame(MainMenu)
        elif self.controller.d.mode == "edit":
            self.controller.show_frame(CharacterView)

    def forward2PersClick(self):
        if self.not_null():
            if self.controller.d.mode == "new": # New character
                self.controller.show_frame(PersonalityTest)
            elif self.controller.d.mode == "edit": # Skip the personality test
                self.controller.frames[CharacterSubmit].update_page()
                self.controller.show_frame(CharacterSubmit)
        else:
            self.controller.popup("First and Last name must have a value.")

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
        tk.Frame.__init__(self, parent, bg="white", borderwidth=0, highlightthickness=0)

        self.controller = controller

        label = tk.Label(self, text="Personality Test", font=("fixedsys", 20, "bold"),
        bg="white", borderwidth=0, highlightthickness=0)
        # label.pack(pady=10, padx=10)
        label.grid(row=0, column=0, columnspan=2)

        instr = """For each question, answer how true the statement is to your character. The \
results of this quiz will determine the personality of your character.

"""

        lblInstructions = tk.Label(self, text=instr,
        bg="white", borderwidth=0, highlightthickness=0)
        # lblInstructions.pack(pady=10, padx=10)
        lblInstructions.grid(row=1, column=0, columnspan=2)
        lblCat=tk.Label(self, text="(Very Disagree, Disagree, Neutral, Agree, Very Agree)",
        bg="white", borderwidth=0, highlightthickness=0)
        lblCat.grid(row=2, column=1)
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
            labels.append(tk.Label(self, text=questions[y], bg="white", borderwidth=0, highlightthickness=0))
            labels[y].grid(row=3 + y, column=0)

            questionFrames.append(tk.LabelFrame(self))
            questionFrames[y].grid(row=3 + y, column=1)

            self.rbArray.append([])

            for x in range(5):
                self.rbArray[y].append(tk.Radiobutton(questionFrames[y], variable=self.answers[y], value=x, bg="white", borderwidth=0, highlightthickness=0))
                self.rbArray[y][x].grid(row=0, column=x + 1)

        butBack = tk.Button(self, text="Back", command=self.back2CharClick, bg="#f46e42")
        butBack.grid(row=50, column=0)

        butForward = tk.Button(self, text="Next", command=self.forward2PreviewClick, bg="#4af441")
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
        tk.Frame.__init__(self, parent, bg="white")

        self.controller = controller

        # Title at the top of the screen
        title = tk.Label(self, text="Finalize Character", font=("fixedsys", 20, "bold"),
        bg="white", borderwidth=0, highlightthickness=0)
        title.grid(row=0, column=0, columnspan=3)

        # Data setup for database submission
        self.d_character = {}
        self.d_clothing = {}
        self.d_personality = {}
        self.d_job = {}
        self.d_skill = {}

        self.lblList = []
        self.lfVisual = tk.LabelFrame(self, text="Visuals", font=("fixedsys", 16, "bold"),
        bg="white", borderwidth=0, highlightthickness=0)
        self.lfVisual.grid(row=1, column=1)
        self.lfPers = tk.LabelFrame(self, text="Personality", font=("fixedsys", 16, "bold"),
        bg="white", borderwidth=0, highlightthickness=0)
        self.lfPers.grid(row=1, column=2)
        self.lfRightButt = tk.LabelFrame(self, text="Second Chance", font=("fixedsys", 16, "bold"),
        bg="white", borderwidth=0, highlightthickness=0)
        self.lfRightButt.grid(row=1, column=3)

        self.lblPerson = tk.Label(self.lfVisual, font=("fixedsys", 16, "bold"),
        bg="white", borderwidth=0, highlightthickness=0)
        self.lblPerson.grid(row=0, column=0)

        # ----- Bottom = Submit button -----
        butSubmit = tk.Button(self,
                              text="Submit",
                              command=self.butSubmitClick,
                              bg="#4af441", borderwidth=1, highlightthickness=0)
        butSubmit.grid(row=2, column=1)

        # ----- Second middle
        self.lblPers = [tk.Label(self.lfPers, text=str(self.controller.curr_character.ope),bg="white"),
                        tk.Label(self.lfPers, text=str(self.controller.curr_character.con),bg="white"),
                        tk.Label(self.lfPers, text=str(self.controller.curr_character.ext),bg="white"),
                        tk.Label(self.lfPers, text=str(self.controller.curr_character.agr),bg="white"),
                        tk.Label(self.lfPers, text=str(self.controller.curr_character.neu),bg="white")]
        for c, label in enumerate(self.lblPers):
            label.grid(row=c, column=0)

        # ----- Right side = Buttons to go back -----
        self.butHome = tk.Button(self.lfRightButt,
                                 text="Quit",
                                 command=self.are_you_sure,
                                 bg=CLR_LAVENDER, borderwidth=1, highlightthickness=0)

        self.butEditChar = tk.Button(self.lfRightButt,
                                     text="To Edit Character",
                                     command=self.butEditCharClick,
                                     bg=CLR_LAVENDER, borderwidth=1, highlightthickness=0)

        self.butEditPers = tk.Button(self.lfRightButt,
                                     text="To Edit Personality",
                                     command=self.butEditPersClick,
                                     bg=CLR_LAVENDER, borderwidth=1, highlightthickness=0)

        self.butEditChar.grid(row=0, column=0)
        self.butEditPers.grid(row=1, column=0)
        self.butHome.grid(row=2, column=0)

        # self.aggregate_data()

    def aggregate_data(self):
        """Accesses all other frames to grab all their data and format it for the database.

        Use when creating the characters.
        """

        # Character Table
        self.controller.curr_character.fName = self.controller.frames[CharacterCreate].entFName.get()
        self.controller.curr_character.lName = self.controller.frames[CharacterCreate].entLName.get()
        self.controller.curr_character.size = self.controller.frames[CharacterCreate].height.get()  # Known as height
        self.controller.curr_character.weight = self.controller.frames[CharacterCreate].weight.get()
        self.controller.curr_character.species = self.controller.frames[CharacterCreate].species.get()
        self.controller.curr_character.race = self.controller.frames[CharacterCreate].colorNum.get()  # Known as color, int
        self.controller.curr_character.gender = self.controller.frames[CharacterCreate].gender.get()

        # Clothing Table
        # [file_name, rgbHex val]
        ieChar = self.controller.frames[CharacterCreate].character
        self.controller.curr_character.shirt_f_name = ieChar.f_shirts[ieChar.curr_shirt]
        self.controller.curr_character.shirt_color = ieChar.col_shirt
        self.controller.curr_character.pants_f_name = ieChar.f_pants[ieChar.curr_pants]
        self.controller.curr_character.pants_color = ieChar.col_pants
        self.controller.curr_character.shoes_f_name = ieChar.f_shoes[ieChar.curr_shoes]
        self.controller.curr_character.shoes_color = ieChar.col_shoes

        if self.controller.d.mode == "new":
            # Only need to get personality when we first create the character.
            # Personality Table
            ans = self.controller.frames[PersonalityTest].answers
            self.controller.curr_character.ope = round((ans[0].get() + ans[1].get() + ans[2].get()) / 12, 2)
            self.controller.curr_character.con = round((ans[3].get() + ans[4].get() + ans[5].get()) / 12, 2)
            self.controller.curr_character.ext = round((ans[6].get() + ans[7].get() + ans[8].get()) / 12, 2)
            self.controller.curr_character.agr = round((ans[9].get() + ans[10].get() + ans[11].get()) / 12, 2)
            self.controller.curr_character.neu = round((ans[12].get() + ans[13].get() + ans[14].get()) / 12, 2)

        # Job Table
        self.controller.curr_character.job_desc = self.controller.frames[CharacterCreate].entJob.get()
        # Skill Table
        self.controller.curr_character.skill_desc = self.controller.frames[CharacterCreate].entSkill.get()

    def update_page(self):
        self.aggregate_data()

        # ----- Left side = Character Info -----
        self.lfCharInfo = tk.LabelFrame(self, text="Character\nInformation",font=("fixedsys", 16, "bold"),
        bg="white", borderwidth=0, highlightthickness=0)
        self.lfCharInfo.grid(row=1, column=0)
        for label in self.lblList:
            label.grid_remove()
        self.lblList = []
        self.lblList = [tk.Label(self.lfCharInfo, text="First Name: " + self.controller.curr_character.fName,bg="white"),
                        tk.Label(self.lfCharInfo, text="Last Name: " + self.controller.curr_character.lName,bg="white"),
                        tk.Label(self.lfCharInfo, text="Size: " + self.controller.curr_character.size,bg="white"),
                        tk.Label(self.lfCharInfo, text="Weight: " + self.controller.curr_character.weight,bg="white"),
                        tk.Label(self.lfCharInfo, text="Gender: " + self.controller.curr_character.gender,bg="white")]
        i = 0
        for label in self.lblList:
            label.grid(row=i, column=0)
            i += 1

        # ----- Middle = Picture of Character -----
        self.character = IE.CharacterManip()
        self.character.define_character(self.controller.curr_character)

        self.imgPerson = self.character.returnGIF()
        self.lblPerson.configure(image=self.imgPerson)
        self.lblPerson.image = self.imgPerson

        # ----- Second middle = Personality Results -----
        self.lblPers[0].configure(text="Openness: " + str(self.controller.curr_character.ope))
        self.lblPers[1].configure(text="Conscientiousness: " + str(self.controller.curr_character.con))
        self.lblPers[2].configure(text="Extroversion: " + str(self.controller.curr_character.ext))
        self.lblPers[3].configure(text="Agreeableness: " + str(self.controller.curr_character.agr))
        self.lblPers[4].configure(text="Neuroticism: " + str(self.controller.curr_character.neu))


        if self.controller.d.mode == "edit":
            self.butEditPers.grid_remove()
        elif self.controller.d.mode == "new":
            self.butEditPers.grid(row=1, column=0)


    def are_you_sure(self):
        """Pop up to make sure user knows progress will be lost."""

        pop = tk.Tk()
        pop.wm_title("Wait!")
        pop.focus_force()

        w = 200
        h = 75

        pop.geometry('%dx%d+%d+%d' % (w, h, int((pop.winfo_screenwidth()/2) - (w/2)), int((pop.winfo_screenheight()/2) - (h/2))))
        msg = tk.Label(pop, text="Are you sure you want quit?\nProgress will be lost.")
        msg.grid(row=0, column=0, columnspan=2)
        butYes = tk.Button(pop, text="Yes", bg="#4af441", command=lambda: self.butHomeClick(pop))
        butYes.grid(row=1, column=0)
        butNo = tk.Button(pop, text="No", bg="#f46e42", command=pop.destroy)
        butNo.grid(row=1, column=1)


    def butEditCharClick(self):
        self.controller.show_frame(CharacterCreate)

    def butEditPersClick(self):
        self.controller.show_frame(PersonalityTest)

    def butHomeClick(self, pop):
        pop.destroy()
        self.controller.frames[CharacterCreate].set_defaults()
        self.controller.frames[PersonalityTest].set_defaults()
        if self.controller.d.mode == "new":
            self.controller.show_frame(MainMenu)
        elif self.controller.d.mode == "edit":
            self.controller.show_frame(CharacterView)

    def butSubmitClick(self):
        """Will upload the character to the database and clear all screens used."""
        self.controller.d.insertion(self.controller.curr_character)
        self.controller.frames[CharacterCreate].set_defaults()
        self.controller.frames[PersonalityTest].set_defaults()


        if self.controller.d.mode == "new": # Go to Main
            self.controller.show_frame(MainMenu)
        elif self.controller.d.mode == "edit": # Go back to the view after editing
            self.controller.frames[CharacterView].update_page()
            self.controller.show_frame(CharacterView)


class CharacterView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CLR_MAIN)

        label = tk.Label(self, text="Character View", font=("fixedsys", 20, "bold"))
        label.grid(row=0, column=0, columnspan=2)

        self.controller = controller
        self.data = []
        self.lblChars = []


        # Top level headers
        lblHeaders = [tk.Label(self, text="First Name",bg=CLR_MAIN, highlightthickness=0, borderwidth=0),
                      tk.Label(self, text="Last Name",bg=CLR_MAIN, highlightthickness=0, borderwidth=0),
                      tk.Label(self, text="Species",bg=CLR_MAIN, highlightthickness=0, borderwidth=0),
                      tk.Label(self, text="Gender",bg=CLR_MAIN, highlightthickness=0, borderwidth=0)]
        for i, label in enumerate(lblHeaders):
            label.bind("<Button-1>", lambda event, e=i: self.sort_chars(event, e))
            label.grid(row=1, column=i)

        # Back button
        butMain = tk.Button(self, text="Back", command=self.onBackClick,
        bg=CLR_LAVENDER, highlightthickness=0, borderwidth=1)
        butMain.grid(row=90, column=0, columnspan=20)

    def update_page(self):
        """Updates all the widgets on this page when something updates."""

        # List of tuples
        # Each tuple represents a different character
        self.data = self.controller.d.get_all_characters()
        # List of tuples
        # Each tuple represents a different label full of data
        self.show_labels()

    def show_labels(self):

        # Get rid of all the old labels
        for lbl in self.lblChars:
            for lblbl in lbl:
                lblbl.grid_forget()
        self.lblChars = []

        for charNum, row in enumerate(self.data):
            self.lblChars.append([tk.Label(self, text=row[0],bg=CLR_MAIN, highlightthickness=0, borderwidth=0),
                                  tk.Label(self, text=row[1],bg=CLR_MAIN, highlightthickness=0, borderwidth=0),
                                  tk.Label(self, text=row[2],bg=CLR_MAIN, highlightthickness=0, borderwidth=0),
                                  tk.Label(self, text=row[3],bg=CLR_MAIN, highlightthickness=0, borderwidth=0),
                                  tk.Button(self, text="Delete",bg=CLR_LAVENDER, highlightthickness=0, borderwidth=1, command=lambda x=row[4]: self.are_you_sure(x))])

            # Place on grid
            for attrNum, label in enumerate(self.lblChars[charNum]):
                if attrNum < len(self.lblChars[charNum]) - 1:
                    label.bind("<Button-1>", lambda event, x=row[4]: self.onLabelClick(event, x))
                    label.grid(row=2+charNum, column=attrNum)
                else:
                    label.grid(row=2+charNum, column=attrNum)

    def are_you_sure(self, id):
        pop = tk.Tk()
        pop.wm_title("Wait!")
        pop.focus_force()

        w = 300
        h = 50

        pop.geometry('%dx%d+%d+%d' % (w, h, int((pop.winfo_screenwidth()/2) - (w/2)), int((pop.winfo_screenheight()/2) - (h/2))))
        msg = tk.Label(pop, text="Are you sure you want to delete this character?")
        msg.grid(row=0, column=0, columnspan=2)
        butYes = tk.Button(pop, text="Yes", bg="#4af441", command=lambda: self.del_char(id, pop))
        butYes.grid(row=1, column=0)
        butNo = tk.Button(pop, text="No", bg="#f46e42", command=pop.destroy)
        butNo.grid(row=1, column=1)

    def sort_chars(self, event, num):
        self.data = sorted(self.data, key=lambda li: li[num].lower())
        self.show_labels()

    def del_char(self, id, pop):
        """Delete character with id."""
        pop.destroy()
        self.controller.d.del_char(id)
        self.update_page()

    def onBackClick(self):
        self.controller.show_frame(MainMenu)

    def onLabelClick(self, event, id):
        """Whenever a label is clicked, will go to that character's submit screen.

        Will do so by updating all data on the character creation screen.

        """
        # A character object
        self.controller.curr_character = self.controller.d.get_character(id)
        screen = self.controller.frames[CharacterCreate]

        screen.entFName.insert(0, self.controller.curr_character.fName)
        screen.entLName.insert(0, self.controller.curr_character.lName)
        screen.height.set(self.controller.curr_character.size)
        screen.weight.set(self.controller.curr_character.weight)
        screen.species.set(self.controller.curr_character.species)
        screen.speciesNum.set(screen.species_list.index(self.controller.curr_character.species))
        screen.colorNum.set(self.controller.curr_character.race)
        screen.gender.set(self.controller.curr_character.gender)
        screen.entJob.insert(0, self.controller.curr_character.job_desc)
        screen.entSkill.insert(0, self.controller.curr_character.skill_desc)

        screen.character = IE.CharacterManip()
        screen.shirtColor.set(self.rgb_to_hsv(self.controller.curr_character.shirt_color))
        screen.hexShirtColor.set(self.controller.curr_character.shirt_color)
        screen.sldTopColor.config(background=self.controller.curr_character.shirt_color)
        screen.pantsColor.set(self.rgb_to_hsv(self.controller.curr_character.pants_color))
        screen.hexPantsColor.set(self.controller.curr_character.pants_color)
        screen.sldMidColor.config(background=self.controller.curr_character.pants_color)
        screen.shoesColor.set(self.rgb_to_hsv(self.controller.curr_character.shoes_color))
        screen.hexShoesColor.set(self.controller.curr_character.shoes_color)
        screen.sldBotColor.config(background=self.controller.curr_character.shoes_color)

        screen.character.define_character(self.controller.curr_character)

        screen.updateCharLabel()

        self.controller.show_frame(CharacterCreate)

    def rgb_to_hsv(self, rgb_hex):
        r = int(rgb_hex[1:3], 16) / 255
        g = int(rgb_hex[3:5], 16) / 255
        b = int(rgb_hex[5:], 16) / 255

        c_max = max(r, g, b)
        c_min = min(r, g, b)

        hue = 0

        delta = c_max - c_min

        if c_max == r:
            hue = 60 * (((g - b) / delta) % 6)
        elif c_max == g:
            hue = 60 * (((b - r) / delta) + 2)
        elif c_max == b:
            hue = 60 * (((r - g) / delta) + 4)

        return int(hue)

app = Creator()
app.protocol("WM_DELETE_WINDOW", app.on_close)
app.mainloop()
