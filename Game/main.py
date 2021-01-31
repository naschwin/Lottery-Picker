"""
Fiverr Project for ryancox642
Raffle Game
"""

import pygame, sys, random
from tkinter import messagebox, Tk
import tkinter as tk 
from PIL import ImageTk, Image
from copy import deepcopy

def show_text(Text,X,Y,Spacing,WidthLimit,Font,surface,double=1,overflow='normal'):
    Text += ' '
    if double == 2:
        X = int(X/2)
        Y = int(Y/2)
    OriginalX = X
    OriginalY = Y
    CurrentWord = ''
    if overflow == 'normal':
        for char in Text:
            if char not in [' ','\n']:
                try:
                    Image = Font[str(char)][1]
                    CurrentWord += str(char)
                except KeyError:
                    pass
            else:
                WordTotal = 0
                for char2 in CurrentWord:
                    WordTotal += Font[char2][0]
                    WordTotal += Spacing
                if WordTotal+X-OriginalX > WidthLimit:
                    X = OriginalX
                    Y += Font['Height']
                for char2 in CurrentWord:
                    Image = Font[str(char2)][1]
                    surface.blit(pygame.transform.scale(Image,(Image.get_width()*double,Image.get_height()*double)),(X*double,Y*double))
                    X += Font[char2][0]
                    X += Spacing
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                else:
                    X = OriginalX
                    Y += Font['Height']
                CurrentWord = ''
            if X-OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
        return X,Y
    if overflow == 'cut all':
        for char in Text:
            if char not in [' ','\n']:
                try:
                    Image = Font[str(char)][1]
                    surface.blit(pygame.transform.scale(Image,(Image.get_width()*double,Image.get_height()*double)),(X*double,Y*double))
                    X += Font[str(char)][0]
                    X += Spacing
                except KeyError:
                    pass
            else:
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                if char == '\n':
                    X = OriginalX
                    Y += Font['Height']
                CurrentWord = ''
            if X-OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
        return X,Y

def generate_font(FontImage,FontSpacingMain,TileSize,TileSizeY,color):
    FontSpacing = deepcopy(FontSpacingMain)
    FontOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
    FontImage = pygame.image.load(FontImage).convert()
    NewSurf = pygame.Surface((FontImage.get_width(),FontImage.get_height())).convert()
    NewSurf.fill(color)
    FontImage.set_colorkey((255,0,0))
    NewSurf.blit(FontImage,(0,0))
    FontImage = NewSurf.copy()
    FontImage.set_colorkey((0,0,0))
    num = 0
    for char in FontOrder:
        FontImage.set_clip(pygame.Rect(((TileSize+1)*num),0,TileSize,TileSizeY))
        CharacterImage = FontImage.subsurface(FontImage.get_clip())
        CharacterImage = CharacterImage.convert()
        CharacterImage.set_colorkey((0,0,0))
        try:
            FontSpacing[char].append(CharacterImage)
        except KeyError:
            break
        num += 1
    FontSpacing['Height'] = TileSizeY
    return FontSpacing


class Data(object):
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("300x100+500+200")   
        self.root.title("Raffle Game")

        self.x_var = tk.StringVar() 
        self.y_var = tk.StringVar()
        self.bombs = tk.StringVar() 

        self.x_label = tk.Label(self.root, text = 'No of Columns: ', 
                        font=('courier', 
                                10, ))

        self.y_label = tk.Label(self.root, text = 'No of Rows: ', 
                            font=('courier', 
                                    10, )) 
        
        self.bomb_label = tk.Label(self.root, text = 'No of Bomb: ', 
                            font=('courier', 
                                    10, )) 
        
        self.x_entry = tk.Entry(self.root, textvariable = self.x_var, font=('courier',10,'normal')) 
        
        self.y_entry = tk.Entry(self.root, textvariable = self.y_var, font=('courier',10,'normal')) 

        self.bomb_entry = tk.Entry(self.root, textvariable = self.bombs, font=('courier',10,'normal')) 

        self.sub_btn=tk.Button(self.root,text = 'Submit', command = self.submit) 
        
        self.x_label.grid(row=0,column=0) 
        self.x_entry.grid(row=0,column=1) 
        self.y_label.grid(row=1,column=0) 
        self.y_entry.grid(row=1,column=1) 
        self.bomb_label.grid(row=2,column=0) 
        self.bomb_entry.grid(row=2,column=1) 
        self.sub_btn.grid(row=3,column=1) 
        
        self.root.mainloop() 
    
    
    def submit(self): 
        x = self.x_var.get() 
        y = self.y_var.get() 
        bomb = self.bombs.get() 
        self.x_var.set("") 
        self.y_var.set("") 
        self.root.destroy()
        self.start = Raffle(int(x), int(y), int(bomb))
        




class Grid(object):
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.bomb = False
        self.notbomb = False
        self.col = (0, 0, 0)
        self.image = pygame.image.load("images/bomb.png")
        self.clicked = False
        
    def _id(self):
        self.clicked = True
        if self.bomb:
            self.notbomb = True
            self.bomb = False
            self.clicked = False


    def show(self, win):
        if self.clicked and not self.notbomb:
            self.col = (231, 0, 150)
        pygame.draw.rect(win, self.col, (self.x*self.w, self.y*self.h, self.w-1, self.h-1))
        if self.notbomb:
            win.blit(pygame.transform.scale(self.image, (self.w-1, self.h-1)), (self.x*self.w, self.y*self.h))
            


class Raffle(object):
    def __init__(self, cols, rows, bombs):
        self.cols = cols
        self.rows = rows
        
        self.size = (width, height) = cols*30, rows*30
        pygame.init()

        self.win = pygame.display.set_mode(self.size)
        self.icon = pygame.image.load("images/2.png")
        pygame.display.set_caption("Raffle Game")
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()


        self.w = width//cols
        self.h = height//rows

        self.grid = []


        # Font ------------------------------------------------------- #
        self.font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
                'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
                '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
                '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
                '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],';':[1]}

        self.font = generate_font('font/small_font.png', self.font_dat, 5, 8, (255, 255, 255))  

        #Initialize Grids
        for i in range(self.cols):
            arr = []
            for j in range(self.rows):
                arr.append(Grid(i, j, self.w, self.h))
            self.grid.append(arr)

        for i in range(bombs):
            a, b = random.randint(0, cols-1), random.randint(0, rows-1)
            while self.grid[a][b].bomb:
                a, b = random.randint(0, cols-1), random.randint(0, rows-1)
            self.grid[a][b].bomb = True


        self.main()

    # Put or remove walls
    def clickWall(self, pos, state):
        tile = self.grid[pos[0] // self.w][pos[1] // self.h]
        tile._id();

    def main(self):
        while True:
            for event in pygame.event.get():  # All events (mouse moving, button clicks, mouse clicks etc)
                if event.type == pygame.QUIT:  # If they try to close the window
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # If they press the mouse (any button)
                    if event.button in (1, 3):  # And it's a left or right click
                        self.clickWall(pygame.mouse.get_pos(), event.button==1)  # Click a wall with either (True as a left click or False as not a left click (a right click)


            self.win.fill((236,240,241))

            for i in range(self.cols):
                for j in range(self.rows):
                    spot = self.grid[i][j]
                    spot.show(self.win)
                    show_text(str(i+j*self.cols+1), i*self.w+self.w//3+2, j*self.h+self.h//3+10, 1, 9999, self.font, self.win)        
                    
            pygame.display.flip()


intro = Data()







