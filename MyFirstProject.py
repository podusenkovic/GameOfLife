import tkinter
import random

from tkinter import *


btnHeight = 40;

WIDTH = 1280    
HEIGHT = 700
cell_size = 30

field_height = HEIGHT // cell_size
field_width = WIDTH // cell_size



class Segment(object):
    def __init__(self,game, x, y, alive):
        self.instance = game.c.create_rectangle(x*cell_size, y*cell_size, 
                                          x*cell_size + cell_size, y*cell_size + cell_size,
                                          fill = "green" if alive else "white")
        self.x = x
        self.y = y
        self.alive = alive
        self.becomeAlive = alive
        self.needReDr = True

    def ReDraw(self):
        game.c.delete(self.instance)
        self.instance = game.c.create_rectangle(self.x * cell_size, self.y * cell_size, 
                                          self.x * cell_size + cell_size, self.y * cell_size + cell_size,
                                          fill = "green" if self.alive else "white")

    def CheckAlive(self):
        if self.Nb == 3 and self.alive == False:
            self.becomeAlive = True
            self.needReDr = True
        elif self.alive == True and (self.Nb < 2 or self.Nb > 3):
            self.becomeAlive = False
            self.needReDr = True
        else:
           self.needReDr = False

    def SetAlive(self):
        self.alive = self.becomeAlive

    def CountNeightbors(self, BigCell):
        self.Nb = 0
        for x in range(-1,2):
            for y in range(-1,2):
                if (not x == 0) or (not y == 0):
                    ix = (self.x + x) % field_width
                    iy = (self.y + y) % field_height
                    if BigCell.cells[iy][ix].alive == True:
                        self.Nb = self.Nb + 1

class Grid(object):
    def __init__(self, game, H, W):
        self.cells = []
        for line in range(H):
            a = []
            for cell in range(W):
                a.append(Segment(game, cell, line, False))
            self.cells.append(a)

    def RandomIt(self):
        for line in range(len(self.cells)):
            for cell in range(len(self.cells[line])):
                self.cells[line][cell].becomeAlive = random.choice([True, False, False, False, False, False])

    def Draw(self):
        for line in range(len(self.cells)):
            for cell in range(len(self.cells[line])):
                if (self.cells[line][cell].needReDr == True):
                    self.cells[line][cell].ReDraw()
    
    def UpdateCells(self):
        for line in range(len(self.cells)):
            for cell in range(len(self.cells[line])):
                self.cells[line][cell].CountNeightbors(self)
                self.cells[line][cell].CheckAlive()
    
    def SetAliveInside(self):
        for line in range(len(self.cells)):
            for cell in range(len(self.cells[line])):
                if self.cells[line][cell].needReDr == True:
                    self.cells[line][cell].SetAlive()




class Game(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Life simulator")
        
        self.c = Canvas(self.root, width = WIDTH + 75, height = HEIGHT, bg = "black")
        self.c.pack()
        
        self.btnStart = Button(self.root, text = 'Start', height = 2, width = 10 + (WIDTH % cell_size)//10, command = self.StartTheGame)
        self.btnStart.place(x = WIDTH - WIDTH % cell_size, y = 0)

        self.btnPause = Button(self.root, text = 'Pause', height = 2, width = 10 + (WIDTH % cell_size)//10, command = self.PauseGame)
        self.btnPause.place(x = WIDTH - WIDTH % cell_size, y = btnHeight)
        
        self.btnClear = Button(self.root, text = 'Clear', height = 2, width = 10 + (WIDTH % cell_size)//10, command = self.ClearGrid)
        self.btnClear.place(x = WIDTH - WIDTH % cell_size, y = btnHeight * 2)

        self.btnRandom = Button(self.root, text = 'Random', height = 2, width = 10 + (WIDTH % cell_size)//10, command = self.RandomGrid)
        self.btnRandom.place(x = WIDTH - WIDTH % cell_size, y = btnHeight * 3)

        self.btnGlider = Button(self.root, text = 'Glider', height = 2, width = 10 + (WIDTH % cell_size)//10, command = self.PuttingGlider)
        self.btnGlider.place(x = WIDTH - WIDTH % cell_size, y = btnHeight * 4)
        
        self.btnExit = Button(self.root, text = 'Exit', height = 2, width = 10 + (WIDTH % cell_size)//10, command = self.ExitFromProgram)
        self.btnExit.place(x = WIDTH - WIDTH % cell_size, y = btnHeight * 5)

        self.MainCells = Grid(self, field_height,field_width)

        self.c.bind("<Button 1>", self.FillCell)
        self.c.bind("<Button 3>", self.ClearCell)
        self.loop = None


    def main(self):
        self.MainCells.SetAliveInside()
        self.MainCells.Draw()
        self.MainCells.UpdateCells()
        self.loop = self.root.after(10, self.main)

    def StartTheGame(self):
        self.main()

    def PauseGame(self):
        try:
            if self.loop is not None:
                self.root.after_cancel(self.loop)
                self.loop = None
        except BaseException:
            print("Can't pause game if its not started")

    def ClearGrid(self):
        self.PauseGame()
        for line in range(len(self.MainCells.cells)):
            for cell in range(len(self.MainCells.cells[line])):
                self.MainCells.cells[line][cell].becomeAlive = False;
                self.MainCells.cells[line][cell].needReDr = True;
        self.MainCells.SetAliveInside()
        self.MainCells.Draw()

    def RandomGrid(self):
        self.PauseGame()
        self.ClearGrid()
        self.MainCells.RandomIt()
        self.MainCells.SetAliveInside()
        self.MainCells.Draw()

    def ExitFromProgram(self):
        self.root.destroy()

    def PuttingGlider(self):
        self.PauseGame()
        self.c.bind("<Button 1>", self.CreateAGlider)


    def CreateAGlider(self, event):
        x = event.x // cell_size
        y = event.y // cell_size
        print("x = {} y = {}".format(x, y))
        Px = [x, x + 1, x + 1, x, x - 1]
        Py = [y, y + 1, y + 2, y + 2, y + 2]
        for i in range((len(Px))):
            self.MainCells.cells[Py[i]][Px[i]].becomeAlive = True
            self.MainCells.cells[Py[i]][Px[i]].SetAlive()
            self.MainCells.cells[Py[i]][Px[i]].ReDraw()            
        self.c.bind("<Button 1>", self.FillCell)

    def FillCell(self, event):
        x = event.x // cell_size
        y = event.y // cell_size
        print("x = {}; y = {}".format(x, y))
        self.MainCells.cells[y][x].becomeAlive = True
        self.MainCells.cells[y][x].SetAlive()
        self.MainCells.cells[y][x].ReDraw()

    def ClearCell(self, event):
        x = event.x // cell_size
        y = event.y // cell_size
        print("x = {}; y = {}".format(x, y))
        self.MainCells.cells[y][x].becomeAlive = False
        self.MainCells.cells[y][x].SetAlive()
        self.MainCells.cells[y][x].ReDraw()

    

game = Game()

game.root.mainloop()