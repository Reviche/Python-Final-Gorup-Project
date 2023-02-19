from tkinter import *
from tkinter import ttk
from datetime import date
from ParseReport import ParseReport

mainWindow = Tk()
mainWindow.title("Bull Rush Budgeting")
mainWindow.geometry('675x550')
currentDate = date.today().strftime("%B %d, %Y")

class BudgetGUI:

    def __init__(self, master):
        self.listOfActual = {}
        self.listOfActualExpEarn = {}
        self.master = master
        self.top = Toplevel(mainWindow)
        self.top.geometry("300x300")
        self.top.title("Bull Rush Budgeting: Welcome!")
        self.topLevelNameLabel = Label(self.top, text="Please enter your name: ", font=("Times New Roman", 15))
        self.topLevelNameLabel.place(x=75, y=115)
        self.topLevelNameEntry = Entry(self.top, width=10)
        self.topLevelNameEntry.place(x=95, y=140)
        self.topLevelButton = Button(self.top, text="Enter", command=self.getNameAndExit)
        self.topLevelButton.place(x=110, y=170)
        mainWindow.withdraw()
        self.categories = []
        self.currentBudgetPositionY = 200

        self.currentDateLabel = Label(master, text=currentDate)
        self.currentDateLabel.pack()

        self.terminateSessionButton = Button(master, text="Terminate Session", command=master.destroy)
        self.terminateSessionButton.place(x=500, y=500)

        self.reportPathLabel = Label(master, text="File Path")
        self.reportPathLabel.place(x=375, y=75)

        self.ReportEntry = Entry(master, width=15)
        self.ReportEntry.place(x=435, y=75)

        self.ReportGenerate = Button(master, text="Go", command=self.updateTreeView)
        self.ReportGenerate.place(x=585, y=75)

        self.budgetCategoryEntry = Entry(master, width=15)
        self.budgetCategoryEntry.insert(0, "Add New Category...")
        self.budgetCategoryEntry.place(x=435, y=125)
        self.budgetCategoryEntry.bind("<FocusIn>", self.temp_text)

        self.budgetAddCategory = Button(master, text="Add", command=lambda: [self.addCategory()])
        self.budgetAddCategory.place(x=585, y=125)

        self.frame = Frame(master)
        self.frame.pack(side="left")

        self.tree = ttk.Treeview(self.frame, height=20)
        self.tree.pack()

        self.computeButton = Button(master, text="Compute", command=self.computeIt)
        self.computeButton.place(x=250, y=500)

        self.dropDownOptions = ttk.Combobox(master, width=8, values=self.categories)
        self.dropDownOptions.insert(0, "Category")
        self.dropDownOptions.place(x=20, y=500)

        self.linkButton = Button(master, text="Link", command=self.linkCategoriesToActual)
        self.linkButton.place(x=125, y=500)

        budgetSubTitle = Label(mainWindow, text="Budget", font=("Times New Roman", 15))
        budgetSubTitle.place(x=445, y=175)

        actualSubTitle = Label(mainWindow, text="Actual", font=("Times New Roman", 15))
        actualSubTitle.place(x=560, y=175)

        self.salaryCategoryLabel = Label(mainWindow, text="Salary")
        self.salaryCategoryLabel.place(x=350, y=self.currentBudgetPositionY)
        self.salaryCategoryEntry = Entry(mainWindow, width=8)
        self.salaryCategoryEntry.insert(0, 0)
        self.salaryCategoryEntry.place(x=545, y=self.currentBudgetPositionY)
        self.listOfActual['Salary'] = self.salaryCategoryEntry

        self.PAndLTitle = Label(mainWindow, text="Profit/Loss")
        self.PAndLTitle.place(x=445, y=475)

        self.PAndLEntry = Entry(mainWindow, width=8)
        self.PAndLEntry.place(x=545, y=475)

    def getNameAndExit(self):
        budgetTitle = Label(self.master, text="Welcome! " + self.topLevelNameEntry.get(), font=("Times New Roman", 20))
        budgetTitle.place(x=265, y=20)
        self.top.destroy()
        mainWindow.deiconify()

    def updateTreeView(self):
        csvFileParsed = ParseReport(self.callReportToGenerate())
        column = tuple(csvFileParsed.getHeadings())
        self.tree.destroy()
        self.tree = ttk.Treeview(self.frame, columns=column, show='headings', height=20)
        self.tree.heading(column[0], text='Description')
        self.tree.column(column[0], minwidth=70, width=155, stretch=NO)
        self.tree.heading(column[1], text='Earnings/Expenses')
        self.tree.column(column[1], minwidth=80, width=125, stretch=NO)
        # self.tree.heading(column[2], text='Total')
        # self.tree.column(column[2], minwidth=50, width=55, stretch=NO)
        self.tree.pack()

        listOfRows = csvFileParsed.generateRows()

        print(listOfRows)
        for i in listOfRows:
            self.tree.insert('', END, values=i)

    def temp_text(self, *args):
        self.budgetCategoryEntry.delete(0, "end")

    def linkCategoriesToActual(self):
        selectedItems = self.tree.selection()
        listOfKeys = self.listOfActualExpEarn.keys()
        if self.dropDownOptions.get() in listOfKeys:
            for i in selectedItems:
                currentAmount = self.listOfActualExpEarn.get(self.dropDownOptions.get())
                print(currentAmount)
                listOf = list(self.tree.item(i)['values'])
                currentAmount += float(listOf[1]) * -1
                print(currentAmount)
                self.listOfActualExpEarn[self.dropDownOptions.get()] = currentAmount
        else:
            self.listOfActualExpEarn[self.dropDownOptions.get()] = 0
            total = 0
            for i in selectedItems:
                listOf = list(self.tree.item(i)['values'])
                total = float(listOf[1]) * -1
            self.listOfActualExpEarn[self.dropDownOptions.get()] = total
        self.updateListOfActual()
        print(self.listOfActualExpEarn)

    def computeIt(self):
        print(self.listOfActual)
        total = 0
        for x in self.listOfActual.keys():
            num = float(self.listOfActual.get(x).get())
            total += num
        total = str(total)
        self.PAndLEntry.config(state='normal')
        self.PAndLEntry.delete(0, "end")
        self.PAndLEntry.insert(0, total)
        self.PAndLEntry.configure(state='disabled')

    def addCategory(self):
        self.currentBudgetPositionY += 30
        texts = self.budgetCategoryEntry.get().title()
        self.categories.append(texts)
        self.dropDownOptions.configure(values=self.categories)
        budgetCategoryLabel = Label(mainWindow, text=texts)
        budgetCategoryLabel.place(x=350, y=self.currentBudgetPositionY)

        budgetCategoryEntry = Entry(mainWindow, width=8)
        budgetCategoryEntry.place(x=430, y=self.currentBudgetPositionY)

        actualEntry = Entry(mainWindow, width=8)
        actualEntry.insert(0, 0)
        actualEntry.place(x=545, y=self.currentBudgetPositionY)

        self.listOfActual[budgetCategoryLabel.cget("text")] = actualEntry

    def callReportToGenerate(self):
        reportPath = self.ReportEntry.get()
        return reportPath

    def updateListOfActual(self):
        listsOfActualObjectEntryBox = self.listOfActual.keys()
        for category in self.listOfActualExpEarn.keys():
            if category in listsOfActualObjectEntryBox:
                self.listOfActual.get(category).delete(0, "end")
                self.listOfActual.get(category).insert(0, self.listOfActualExpEarn[category])




budgetGui = BudgetGUI(mainWindow)
mainWindow.mainloop()
