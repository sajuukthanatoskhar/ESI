from tkinter import *
import math
from MarketWatcher import market_and_fleet


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Moon Reaction Planner")
        self.label = Label(master, text="Reaction Calculator").grid(row=0, column=0)
        maximum = 10000
        BasicMoonOre = Label(master, text="Basic Moon Ore").grid(row=1, column=0)
        BasicMoonOreUse = Label(master, text="Want to use").grid(row=1, column=1)
        BasicMoonOreInvent = Label(master, text="Inventory").grid(row=1, column=2)
        AdvReactions = Label(master, text="Advanced Reactions").grid(row=1, column=3)
        AdvancedReactionUse = Label(master, text="Want to use").grid(row=1, column=4)
        AdvancedReactionInvent = Label(master, text="Inventory").grid(row=1, column=5)

        basicorenames = ['Atmospheric Gases', 'Cadmium', 'Caesium', 'Chromium', 'Cobalt', 'Dysprosium',
                         'Evaporite Deposits', 'Hafnium', 'Hydrocarbons', 'Mercury', 'Neodymium', 'Platinum',
                         'Promethium', 'Scandium', 'Silicates', 'Technetium', 'Thulium', 'Titanium', 'Tungsten',
                         'Vanadium']
        advancedreactions = ['Caesarium Cadmide', 'Carbon Polymers', 'Ceramic Powder', 'Crystallite Alloy', 'Dysporite',
                             'Fernite Alloy', 'Ferrofluid', 'Fluxed Condensates', 'Hexite', 'Hyperflurite',
                             'Neo Mercurite'
            , 'Platinum Technite', 'Promethium Mercurite', 'Prometium', 'Rolled Tungsten Alloy', 'Silicon Diborite',
                             'Solerium', 'Sulfuric Acid', 'Thulium Hafnite', 'Titanium Chromide', 'Vanadium Hafnite']
        compositereactions = ['Crystalline Carbonide', 'Fermionic Condensates', 'Fernite Carbide', 'Ferrogel',
                              'Fullerides', 'Hypersynaptic Fibers', 'Nanotransistors', 'Nonlinear Metamaterials',
                              'Phenolic Composites', 'Photonic Metamaterials', 'Plasmonic Metamaterials',
                              'Sylramic Fibers', 'Terahertz Metamaterials', 'Titanium Carbide', 'Tungsten Carbide']
        BasicOreWantToUse = []
        BasicOreLabels = []
        BasicOreInventory = []

        AdvancedReactionsWantToUse = []
        AdvancedReactionsLabels = []
        AdvancedReactionsInventory = []

        CompositeWantToUse = []
        CompositeLabels = []
        CompositeInventory = []
        CompositeIncrements = [10000, 400, 10000, 400, 3000, 750, 1500,
                               300, 2200, 300, 300, 6000, 300, 10000, 10000]

        complexmatsreqs = [[0, 2], [-1, 3, 6, 12], [1, 4],
                           [5, 7, 8, 12], [0, 10], [3, 15, 19],
                           [9, 10, 16], [6, 18], [-1, 14, 19],
                           [17, 2], [4, 9], [1, 7], [11, 13],
                           [14, 18], [16, 13]]
        advancedreqs = [
            [0, 1], [7, 13], [5, 13],
            [0, 3], [4, 8], [12, 18],
            [4, 6], [9, 15], [2, 10],
            [11, 18], [9, 8], [10, 14],
            [8, 11], [0, 11], [10, 17],
            [5, 13], [1, 2], [-1, 5],
            [6, 15], [2, 16], [6, 18]]

        for i in range(0, len(basicorenames)):
            BasicOreLabels.append(Label(master, text=basicorenames[i]))
            BasicOreLabels[i].grid(row=2 + i, column=0)
            BasicOreWantToUse.append(Spinbox(master, from_=0, increment=100, to=maximum))
            BasicOreWantToUse[i].grid(row=2 + i, column=1)
            BasicOreInventory.append(Entry(master))
            BasicOreInventory[i].grid(row=2 + i, column=2)
            BasicOreInventory[i].insert(0, "0")
        # Gases = Label(master, text="Atmospheric Gases").grid(row=2,column=0)
        # EntryVanadium = Spinbox(master, from_=0,increment=100,to=maximum).grid(row=22, column=1)

        for j in range(0, len(advancedreactions)):
            AdvancedReactionsLabels.append(Label(master, text=advancedreactions[j]))
            AdvancedReactionsLabels[j].grid(row=2 + j, column=3)
            AdvancedReactionsWantToUse.append(Spinbox(master, from_=0, increment=200, to=maximum))
            AdvancedReactionsWantToUse[j].grid(row=2 + j, column=4)
            AdvancedReactionsInventory.append(Entry(master))
            AdvancedReactionsInventory[j].grid(row=2 + j, column=5)
            AdvancedReactionsInventory[j].insert(0, "0")

        for k in range(0, len(compositereactions)):
            CompositeLabels.append(Label(master, text=compositereactions[k]))
            CompositeLabels[k].grid(row=2 + k, column=6)
            CompositeWantToUse.append(
                Spinbox(master, from_=0, increment=CompositeIncrements[k], to=maximum * CompositeIncrements[k]))
            CompositeWantToUse[k].grid(row=2 + k, column=7)
            CompositeInventory.append(Entry(master))
            CompositeInventory[k].grid(row=2 + k, column=8)
            CompositeInventory[k].insert(0, "0")
        # CaesariumCadmide = Label(master,text = "Caesarium Cadmide").grid(row=2,column=3)
        # EntryCaesariumCadmide = Entry(master).grid(row=2, column=4)
        self.update_button = Button(master, text="Update",
                                    command=lambda: self.update(BasicOreInventory, BasicOreWantToUse)).grid(row=23,
                                                                                                            column=1)
        self.update_button = Button(master, text="Update Basic Reactions",
                                    command=lambda: self.update(BasicOreInventory, BasicOreWantToUse,
                                                                AdvancedReactionsInventory, AdvancedReactionsWantToUse,
                                                                CompositeIncrements, CompositeWantToUse)).grid(row=23,
                                                                                                               column=4)
        self.update_button = Button(master, text="Update Basic Reactions",
                                    command=lambda: self.updatebasic(BasicOreInventory, BasicOreWantToUse,
                                                                     AdvancedReactionsInventory,
                                                                     AdvancedReactionsWantToUse, CompositeIncrements,
                                                                     CompositeWantToUse)).grid(row=23, column=4)
        self.update_button = Button(master, text="Update Complex",
                                    command=lambda: self.updatecomplexupwards(AdvancedReactionsInventory,
                                                                              CompositeInventory, complexmatsreqs,
                                                                              CompositeIncrements)).grid(row=23,
                                                                                                         column=7)
        self.update_button = Button(master, text="Update Basic",
                                    command=lambda: self.updatecomplexupwards(BasicOreInventory,
                                                                              AdvancedReactionsInventory, advancedreqs,
                                                                              [200])).grid(row=23, column=3)
        self.update_button = Button(master, text="Print to Console",
                                    command=lambda: self.printvalue(BasicOreLabels, BasicOreWantToUse)).grid(row=23,
                                                                                                             column=6)
        # self.updatecomplexupwards
        self.close_button = Button(master, text="Close", command=master.quit).grid(row=23, column=0)
        # self.close_button.pack()

    # label_1 = Entry(master,state='disabled').grid(row=0,column=1)

    def printvalue(self, BasicOreLabels, BasicOreWantToUse):
        offset = 1
        totalcost = 0
        for i in range(0, len(BasicOreWantToUse)):
            if int(BasicOreWantToUse[i].get()) > 0:
                print(BasicOreLabels[i]["text"] + " " + str(int(BasicOreWantToUse[i].get())))
                totalcost = market_and_fleet.get_market_price("The Forge", BasicOreLabels[i]["text"]) * int(
                    BasicOreWantToUse[i].get()) + totalcost

            else:
                continue
        print("{:,}".format(totalcost))
        # self.label_1.pack()

    def updatecomplexupwards(self, AdvancedReactionsInventory, CompositeInventory, complexreqs, CompositeIncrements):
        for i in range(0, len(CompositeInventory)):
            complexcyclereqs = []
            offset = 1
            complexnumberofcycles = []
            for j in range(0, len(complexreqs[i])):
                # print(complexreqs[i])
                complexcyclereqs.append(int(int(AdvancedReactionsInventory[complexreqs[i][j] + offset].get()) / 100))
            value = complexcyclereqs[0]
            for k in range(0, len(complexcyclereqs)):
                value = min(value, complexcyclereqs[k])

            for j in range(0, len(complexreqs[i])):
                # print(complexreqs[i])
                # complexcyclereqs.append(int(AdvancedReactionsInventory[complexreqs[i][j]+offset].get())/100)
                storage = int(AdvancedReactionsInventory[complexreqs[i][j] + offset].get())
                AdvancedReactionsInventory[complexreqs[i][j] + offset].delete(0, END)
                AdvancedReactionsInventory[complexreqs[i][j] + offset].insert(0, (storage - value * 100))
            if CompositeIncrements[0] == 200:
                output = value * 200
            else:
                output = value * CompositeIncrements[i]
            print(output)

            CompositeInventory[i].delete(0, END)
            CompositeInventory[i].insert(0, output)
            # if value >= 100:
            #     print(value)
            #
            #     complexnumberofcycles.append(int(AdvancedReactionsInventory[j].get())/)

            del complexcyclereqs[:]

    def update(self, BasicOreInventory, BasicOreWantToUse):
        print("Updating...")
        for j in range(len(BasicOreInventory)):
            BasicOreInventory[j]['state'] = 'disabled'
            if int(BasicOreWantToUse[j].get()) > 0:
                if int(BasicOreWantToUse[j].get()) <= int(BasicOreInventory[j].get()):
                    BasicOreInventory[j]['state'] = 'normal'
                    newvalue = int(BasicOreInventory[j].get()) - int(BasicOreWantToUse[j].get())
                    BasicOreInventory[j].delete(0, END)
                    BasicOreInventory[j].insert(0, int(newvalue))
                    print(BasicOreInventory[j].get())
                    BasicOreInventory[j]['state'] = 'disabled'
                else:
                    print("Error - can't want more than you have")

    def updatebasic(self, BasicOreInventory, BasicOreWantToUse, AdvancedReactionsInventory, AdvancedReactionsWantToUse,
                    CompIncrement, CompositeWant):
        print("Updating Basic Reactions")
        offset = 1
        before1 = 0
        before2 = 0
        before = [0, 0, 0, 0]

        for i in range(0, len(AdvancedReactionsWantToUse)):
            AdvancedReactionsWantToUse[i].delete(0, END)
            AdvancedReactionsWantToUse[i].insert(0, int(int(0)))
        for i in range(0, len(CompositeWant)):

            numberofcycles = 2 * math.ceil(float(CompositeWant[i].get()) / (CompIncrement[i]))

            print(numberofcycles)
            if numberofcycles > 0:
                if i == 0:  # Crysta Carbonide
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [0, 2])
                if i == 1:  # Ferm Con
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [-1, 3, 6, 12])
                if i == 2:  # Fern Carb
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [1, 4])
                if i == 3:  # Ferrogel
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [5, 7, 8, 12])
                if i == 4:  # Fuller
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [0, 10])
                if i == 5:  # Hyper
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [3, 15, 19])
                if i == 6:  # Nano
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [9, 10, 16])
                if i == 7:  # PNonlinear
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [6, 18])
                if i == 8:  # Phenolic
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [-1, 14, 19])
                if i == 9:  # Photonic
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [17, 2])
                if i == 10:  # Plasmonic
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [4, 9])
                if i == 11:  # Sylramics
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [1, 7])
                if i == 12:  # Terahert
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [11, 13])
                if i == 13:  # titanium carb
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [14, 18])
                if i == 14:  # Tungsten
                    basicoreupdate(AdvancedReactionsWantToUse, offset, numberofcycles, [16, 13])

        for i in range(0, len(BasicOreWantToUse)):
            BasicOreWantToUse[i].delete(0, END)
            BasicOreWantToUse[i].insert(0, str(int(0)))
        for i in range(len(AdvancedReactionsWantToUse)):
            numberofcycles = 2 * math.ceil(float(AdvancedReactionsWantToUse[i].get()) / 100)  # Needs to
            if numberofcycles > 0:
                if i == 0:  # Caesarium            Cadmide
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [0, 1])
                if i == 1 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Carbon Polymers
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [7, 13])
                if i == 2 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # CeramicPowder
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [5, 13])
                if i == 3 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # CrystalCarbide
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [0, 3])
                if i == 4 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Dysporite
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [4, 8])
                if i == 5 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Fernite Alloy
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [12, 18])
                if i == 6 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Ferrofluid
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [4, 6])
                if i == 7 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Fluxed Condensates
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [9, 15])
                if i == 8 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Hexite
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [2, 10])
                if i == 9 and int(AdvancedReactionsWantToUse[i].get()) > 0:  ##Hyperflurite
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [11, 18])
                if i == 10 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Neo Mercurite
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [9, 8])
                if i == 11 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Platinum Technite
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [10, 14])
                if i == 12 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Promethium Mercurite
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [8, 11])
                if i == 13 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Prometium
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [0, 11])
                if i == 14 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Rolled Tungsten Alloy
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [10, 17])
                if i == 15 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Silicon Diborite
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [5, 13])
                if i == 16 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Solerium
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [1, 2])
                if i == 17 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # SulfuricAcid
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [-1, 5])
                if i == 18 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # Thulium Hafnite
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [6, 15])
                if i == 19 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # TitaniumChromide
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [2, 16])
                if i == 20 and int(AdvancedReactionsWantToUse[i].get()) > 0:  # VanadiumHafnite
                    basicoreupdate(BasicOreWantToUse, offset, numberofcycles, [6, 18])

    def greet(self):
        print("Greetings!")

    # def


def basicoreupdate(BasicOreWantToUse, offset, numberofcycles, minreqs):
    before = [0, 0, 0, 0]
    for i in range(0, len(minreqs)):
        before[i] = int(BasicOreWantToUse[minreqs[i] + offset].get())
    for i in range(0, len(minreqs)):
        BasicOreWantToUse[minreqs[i] + offset].delete(0, END)
    for i in range(0, len(minreqs)):
        BasicOreWantToUse[minreqs[i] + offset].insert(0, int(int(before[i] + numberofcycles * 100 / 2)))


if __name__ == "__main__":
    root = Tk()
    my_gui = MyFirstGUI(root)
    root.mainloop()
