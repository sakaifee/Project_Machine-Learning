import turtle
from math import *
from random import randint
from time import sleep

Arr=[['_','_','_','_','_','_','_','_'],              #2D array for background processes of Game board
    ['_','_','_','_','_','_','_','_'],
    ['_','_','_','_','_','_','_','_'],
    ['_','_','_','_','_','_','_','_'],
    ['_','_','_','_','_','_','_','_'],
    ['_','_','_','_','_','_','_','_'],
    ['_','_','_','_','_','_','_','_'],
    ['_','_','_','_','_','_','_','_']]

Reds=['_','_','_','_','_','_','_','_','_','_','_','_'];
Grays=['_','_','_','_','_','_','_','_','_','_','_','_'];

RedT=['_','_','_','_','_','_','_','_','_','_','_','_'];     #Arrays for storing turtles corresponding to coins
GrayT=['_','_','_','_','_','_','_','_','_','_','_','_'];

ColArrays=[Reds,Grays]
TurtArrays=[RedT,GrayT]

Map = [40+n*80 for n in range(-4,4)]                #for mapping array indices to co-ordinates
Bcolors = ["black","white"]
Colors = ["red","gray"]

turtle.setup(1500,700)                               #setting up game window
window = turtle.Screen()
window.title('Checkers')
window.bgcolor("blue")
            
DrawBot = turtle.getturtle()                        #setting up a turtle for drawing
DrawBot.speed(0)

DrawBot.begin_poly()                                #creating a square shape for turtle
DrawBot.penup()
DrawBot.setposition(40,40)
DrawBot.setheading(180)
DrawBot.pendown()
i=0
while(i<4):
    DrawBot.forward(80)
    DrawBot.left(90)
    i+=1
DrawBot.penup()
DrawBot.setposition(0,0)
DrawBot.end_poly()
turtle.register_shape('Block',DrawBot.get_poly())

DrawBot.begin_poly()                                #creating a circle shape for coins
DrawBot.pensize(5)
DrawBot.penup()
DrawBot.setheading(90)
DrawBot.forward(30)
DrawBot.left(90)
DrawBot.pendown()
DrawBot.circle(30)
DrawBot.penup()
DrawBot.setposition(0,0)
DrawBot.setheading(90)
DrawBot.end_poly()
turtle.register_shape('Coin',DrawBot.get_poly())

DrawBot.begin_poly()                                #creating a King circle shape for coins
DrawBot.fillcolor("yellow")
DrawBot.pensize(5)
DrawBot.penup()
DrawBot.setheading(90)
DrawBot.forward(20)
DrawBot.left(90)
DrawBot.pendown()
DrawBot.begin_fill()
DrawBot.circle(20)
DrawBot.end_fill()

DrawBot.penup()
DrawBot.setheading(90)
DrawBot.forward(10)
DrawBot.left(90)
DrawBot.pendown()
DrawBot.circle(30)

DrawBot.penup()
DrawBot.setposition(0,0)
DrawBot.setheading(90)
DrawBot.end_poly()
turtle.register_shape('King_Coin',DrawBot.get_poly())

class Coin(object):
    def _init_(self,i,j,color,Type,ai):
        self.i = i
        self.j = j
        self.color = color
        self.Type = Type
        self.ai = ai
    def setup_coin(self,i,j,color,Type,ai):
        self.i = i
        self.j = j
        self.color = color
        self.Type = Type
        self.ai = ai

    def setTurtPos(self,i,j):
        if(self.color=="red"):
            RedT[self.ai].setposition(Map[j],Map[7-i])
        else:
            GrayT[self.ai].setposition(Map[j],Map[7-i])

    def setPos(self,i,j):
        self.i = i
        self.j = j
        Arr[i][j] = self
        self.setTurtPos(i,j)

    def upgrade(self):
        self.Type = "king"
        if(self.color=="red"):
            RedT[self.ai].shape("King_Coin")
        else:
            GrayT[self.ai].shape("King_Coin")



DrawBot.penup()                                     #Drawing the game board using stamps
DrawBot.shape('Block')
c=0;i=0;                                            
while(i<8):                                         
    j=0
    while(j<8):
        DrawBot.setposition(Map[i],Map[j])
        DrawBot.pendown()
        DrawBot.pencolor(Bcolors[c])
        DrawBot.fillcolor(Bcolors[c])
        DrawBot.stamp()
        DrawBot.penup()
        j+=1
        c=1-c
    c=1-c
    i+=1
        
        
i=1;j=0;t=0;                                            #Creating and Arranging Red Coins
while(j<8):
    Reds[t] = Coin()
    Reds[t].setup_coin(i,j,"red","norm",t)
    RedT[t] = turtle.Turtle()
    RedT[t].shape('Coin')
    RedT[t].speed(10)
    RedT[t].fillcolor("red")
    RedT[t].penup()
    Arr[i][j] = Reds[t]
    Arr[i][j].setTurtPos(i,j)
    t+=1    
    i+=2
    if(i>2):
        j+=1
        i%=3

i=0;j=0;t=0;                                            #Creating and Arranging Gray Coins
while(j<8):
    Grays[t] = Coin()
    Grays[t].setup_coin(i+5,j,"gray","norm",t)
    GrayT[t] = turtle.Turtle()
    GrayT[t].shape('Coin')
    GrayT[t].speed(10)
    GrayT[t].fillcolor("gray")
    GrayT[t].penup()
    Arr[i+5][j] = Grays[t]
    Arr[i+5][j].setTurtPos(i+5,j)
    t+=1
    i+=2
    if(i>2):
        j+=1
        i%=3


Pointer=turtle.Turtle()                             #Creating a Pointer for the Game Board
Pointer.hideturtle()
Pointer.speed(0)
Pointer.setheading(90)
Pointer.penup()
Pointer.shape("Block")
Pointer.fillcolor("yellow")
Pointer.pencolor("yellow")

All_step = [1,-1]
All_jump = [2,-2]
P=0
G=0
pi=(-1)
pj=(-1)
SLock = 0

def ClickTrack(x,y):                                #returns coordinates of the centre of any clicked square
    
    if(x<320 and x>(-320)):
        X=int(fabs(x))
        Y=int(fabs(y))
        
        a=floor(X/80)
        A=ceil(X/80)
        xi=(x/X)*((a*80+A*80)/2)
    elif(x>320):
        xi=280
    else:
        xi=(-280)
        
    if(y<320 and y>(-320)):
        b=floor(Y/80)
        B=ceil(Y/80)
        yj=(y/Y)*((b*80+B*80)/2)
    elif(y>320):
        yj=280
    else:
        yj=(-280)    

    return [xi,yj]

def Point(x,y):                                     #Highlights the recently clicked square
    Coords = ClickTrack(x,y)
    Pointer.clearstamps()
    Pointer.setposition(Coords[0],Coords[1])
    Pointer.stamp()

    global P
    global pi
    global pj
    global G
    global SLock
    window.bgcolor(Colors[P])

    if(G==0):
        
        j=Map.index(Coords[0])
        i=7-Map.index(Coords[1])

        if(Arr[i][j]!='_'):                         #if a coin was recently clicked
            if(SLock == 0):
                Arr[i][j].setTurtPos(i,j)
                if(Arr[i][j].color == Colors[P]):
                    pi = i;pj = j;
                else:
                    pi = (-1);pj = (-1);
        else:                                       #if a free block was recently clicked
            if(pi!=(-1)):                               #if a coin was already selected
                di = i - pi
                dj = j - pj
                if(fabs(di) > 2):                   #if the recently clicked block cant be reached by selected coin #change this to >2 when enabling jump move
                    if(SLock == 0):
                        pi = (-1);pj = (-1);
                else:
                    if(fabs(di)==1 and fabs(dj)==1 and SLock==0):
                        
                        if(Arr[pi][pj].Type=="norm" and di!=All_step[P]):
                                pi = (-1);pj = (-1);
                        else:
                            t = Arr[pi][pj].ai
                            c = Arr[pi][pj].color
                            Arr[pi][pj] = '_'

                            if(c=="red"):
                                Reds[t].setPos(i,j)
                                if(Reds[t].Type=="norm" and i==7):
                                    Reds[t].upgrade()
                            else:
                                Grays[t].setPos(i,j)
                                if(Grays[t].Type=="norm" and i==0):
                                    Grays[t].upgrade()
                                    
                            pi = (-1);pj = (-1);        
                            P = 1-P
                            window.bgcolor(Colors[P])
                            
                    elif(fabs(di)==2 and fabs(dj)==2):
                        dei = int((pi+i)/2); dej = int((pj+j)/2);
                        print("dei=",dei,"\n")
                        print("dej=",dej,"\n")
                        if((Arr[pi][pj].Type=="norm" and di!=All_jump[P]) or Arr[dei][dej]=='_'):
                            if(SLock == 0):
                                pi = (-1);pj = (-1);
                        else:
                            
                            if(Arr[dei][dej].color==Colors[P]):
                                if(SLock == 0):
                                    pi = (-1);pj = (-1);
                            else:
                                t = Arr[pi][pj].ai
                                c = Arr[pi][pj].color
                                Arr[pi][pj] = '_'

                                if(c=="red"):
                                    Reds[t].setPos(i,j)
                                    if(Reds[t].Type=="norm" and i==7):
                                        Reds[t].upgrade()
                                else:
                                    Grays[t].setPos(i,j)
                                    if(Grays[t].Type=="norm" and i==0):
                                        Grays[t].upgrade()
                                        
                                td = Arr[dei][dej].ai
                                tc = Arr[dei][dej].color
                                Arr[dei][dej] = '_'

                                
                                
                                if(tc=="red"):
                                    del Reds[td]
                                    RedT[td].hideturtle()
                                    del RedT[td]
                                    R=len(Reds)
                                    if(R>td):
                                        ind = td
                                        while(ind<R):
                                            Reds[ind].ai-=1
                                            Arr[Reds[ind].i][Reds[ind].j] = Reds[ind]
                                            ind+=1
                                else:
                                    del Grays[td]
                                    GrayT[td].hideturtle()
                                    del GrayT[td]
                                    R=len(Grays)
                                    if(R>td):
                                        ind = td
                                        while(ind<R):
                                            Grays[ind].ai-=1
                                            Arr[Grays[ind].i][Grays[ind].j] = Grays[ind]
                                            ind+=1
                                

                                
                                print(Colors[1-P],":",R)
                                if(R==0):
                                    G=1
                                    window.bgcolor("green")
                                    print("Player",P+1,"Wins!!")
                                else:
                                    
                                    Jumps = []

                                    for qi in [1,-1]:
                                        if((ColArrays[P])[t].Type == "norm" and qi != All_step[P]):
                                            Jumps.append(False)
                                        else:
                                            if(i+2*qi>7 or i+2*qi<0):
                                                Jumps.append(False)
                                            else:
                                                for qj in [1,-1]:
                                                    if(j+2*qj>7 or j+2*qj<0):
                                                        Jumps.append(False)
                                                    elif(Arr[i+2*qi][j+2*qj]=='_' and Arr[i+qi][j+qj]!='_'):
                                                        if(Arr[i+qi][j+qj].color==Colors[1-P]):
                                                            Jumps.append(True)
                                                        else:
                                                            Jumps.append(False)
                                                    else:
                                                        Jumps.append(False)
                                                        
                                    if(True in Jumps):
                                        pi = i;pj = j;
                                        SLock = 1
                                        
                                    else:
                                        SLock = 0
                                        pi =(-1);pj =(-1);
                                        P = 1-P
                                        window.bgcolor(Colors[P])
                                    '''pi =(-1);pj =(-1);
                                    P = 1-P
                                    window.bgcolor(Colors[P])'''
                    else:
                        if(SLock == 0):
                            pi = (-1);pj = (-1);

window.onscreenclick(Point,1)

def Unpoint(x,y):                                   #Unhighlights a highlighted square
    global P
    Pointer.clearstamps()
    P = 1-P
    window.bgcolor(Colors[P])
window.onscreenclick(Unpoint,3)
