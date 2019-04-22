import tkinter as tk

class MainMenu:

    def __init__(self, myParent):
        '''Used to create the start screen of the application.

        All of the different functions we defined will be represented as a button.
        I think each different function will have it's own class, but that might
        change.
        '''
        # This is a container
        self.conMain = tk.Frame(myParent)
        self.conMain.pack(side="top", fill="both", expand=True)
        self.conMain.grid_rowconfigure(0, weight=1)
        self.conMain.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = Menu(self.conMain, self)
        self.frames[Menu] = frame

        frame.grid(row=0, column=0, sticky="nsew")


        #------ Button attributes -----
        but_width = 16
        but_padx = '2m'
        but_pady = '1m'

        #----- Create Character -------
        self.butCreate = Button(self.conMain,
                                text="Create Character",
                                background="blue",
                                command=self.butCreateClick,
                                width=but_width,
                                padx=but_padx,
                                pady=but_pady)
        self.butCreate.pack()
        self.butCreate.focus_force()
        self.butCreate.bind("<Return>", self.butCreateClick_a)

        #----- Edit Character ---------
        self.butEdit = Button(self.conMain,
                              text="Edit Character",
                              background="blue",
                              command=self.butEditClick,
                              width=but_width,
                              padx=but_padx,
                              pady=but_pady)
        self.butEdit.pack()
        self.butEdit.bind("<Return>", self.butEditClick_a)

        #----- View Characters --------
        self.butView = Button(self.conMain,
                              text="View Characters",
                              background="blue",
                              command=self.butViewClick,
                              width=but_width,
                              padx=but_padx,
                              pady=but_pady)
        self.butView.pack()
        self.butView.bind("<Return>", self.butViewClick_a)

    def self.show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


    def butCreateClick_a(self, event):
        '''Wrapper since bind needs event, command doesn't.'''
        self.butCreateClick()

    def butCreateClick(self):
        '''Runs when Create is left clicked.'''
        if self.butCreate['background'] == "blue":
            self.butCreate['background'] = "green"
        else:
            self.butCreate['background'] = "blue"

    def butEditClick_a(self, event):
        '''Wrapper since bind needs event, command doesn't.'''
        self.butEditClick()

    def butEditClick(self):
        '''Runs when Edit is left clicked.'''
        self.conMain.destroy()

    def butViewClick_a(self, event):
        '''Wrapper since bind needs event, command doesn't.'''
        self.butViewClick()

    def butViewClick(self):
        print("View clicked.")


class CreateChar:

    def __init__(self, myParent):
        self.main = Frame(myParent)
        self.main.pack()

        # ------ Button attributes -----
        but_width = 16
        but_padx = '2m'
        but_pady = '1m'

        # ----- Create Character -------
        self.butCreate = Button(self.main,
                                text="Create Character",
                                background="blue",
                                command=self.butCreateClick,
                                width=but_width,
                                padx=but_padx,
                                pady=but_pady)
        self.butCreate.pack()
        self.butCreate.focus_force()
        self.butCreate.bind("<Return>", self.butCreateClick_a)


root = Tk()
myapp = MainMenu(root)
root.mainloop()
