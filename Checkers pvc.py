import turtle
from math import *
from random import randint
from time import sleep

COIN_LOSS_PENALTY = 30
COIN_KILL_BONUS = 40
MOVE_AHEAD_REWARD = 10
IMMOBILITY = 100

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
CompLock = 0

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

#window.onscreenclick(Point,1)


def Comp_move():
    global P
    global G

    '''global COIN_LOSS_PENALTY 
    global COIN_KILL_BONUS
    global MOVE_AHEAD_REWARD 
    global IMMOBILITY''' 
    
    print("Computer has made it's move")

    Dirs = [[-1,-1],[-1,1],[1,-1],[1,1]]

    Point_table = [[0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0]]

    Max_pt = -100
    move_no = -1
    move_coin = -1

    jmp = [[0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0]]
    #Jumps = []
    MaxJumps = []

    mj = 0
    while(mj < len(Grays)):
        
        i = Grays[mj].i
        j = Grays[mj].j

        
        
        mi = 0
        while(mi < 2):
            Jumps = []
            Dirtuple = Dirs[mi]
            if(i+ Dirtuple[0] > 7 or i+ Dirtuple[0] < 0 or j+ Dirtuple[1] > 7 or j+ Dirtuple[1] < 0):
                Point_table[mi][mj]-=IMMOBILITY
            else:    
                if(Arr[ i+ Dirtuple[0] ][ j+ Dirtuple[1] ] == "_"):
                    
                    if(((i+ 2*Dirtuple[0]>=0)and(i+ 2*Dirtuple[0]<=7)and(j+ 2*Dirtuple[1]<=7)and(j+ 2*Dirtuple[1]>=0))and (Arr[ i+ 2*Dirtuple[0] ][ j+ 2*Dirtuple[1] ] != "_") and (Arr[ i+ 2*Dirtuple[0] ][ j+ 2*Dirtuple[1] ].color == "red" )):
                        Point_table[mi][mj]-=COIN_LOSS_PENALTY                         #Minus points for bringing coin to risk
                    
                    elif(((i+ 2*Dirtuple[0]>=0)and(i+ 2*Dirtuple[0]<=7)and(j+ 2*Dirtuple[1]<=7)and(j+ 2*Dirtuple[1]>=0))and (Arr[ i+ 2*Dirtuple[0] ][ j ] != "_") and (Arr[ i ][ j+ 2*Dirtuple[1] ] == " ")):
                        if(Arr[ i+ 2*Dirtuple[0] ][ j ].color == "red"):
                            Point_table[mi][mj]-=COIN_LOSS_PENALTY                     #Minus points for bringing coin to risk
                        else:
                            Point_table[mi][mj]+=MOVE_AHEAD_REWARD                     #A Safe but not necessarily Beneficial move

                    elif(((i+ 2*Dirtuple[0]>=0)and(i+ 2*Dirtuple[0]<=7)and(j+ 2*Dirtuple[1]<=7)and(j+ 2*Dirtuple[1]>=0))and(Arr[ i+ 2*Dirtuple[0] ][ j ] == "_") and (Arr[ i ][ j+ 2*Dirtuple[1] ] != "_")):
                        if(Arr[ i ][ j+ 2*Dirtuple[1] ].color == "red" and Arr[ i ][ j+ 2*Dirtuple[1] ].Type == "king"):
                            Point_table[mi][mj]-=COIN_LOSS_PENALTY                     #Minus points for bringing coin to risk
                        else:
                            Point_table[mi][mj]+=MOVE_AHEAD_REWARD                     #A Safe but not necessarily Beneficial move
                    else:
                        Point_table[mi][mj]+=MOVE_AHEAD_REWARD
                    
                    if(Point_table[mi][mj] > Max_pt):
                        Max_pt = Point_table[mi][mj]
                        move_no = mi
                        move_coin = mj

                else:                                                       #in case of possibility of a jump
                    if(Arr[ i+ Dirtuple[0] ][ j+ Dirtuple[1] ].color != "red"):
                        Point_table[mi][mj]-=IMMOBILITY
                    else:
                        J = 1
                        jump_i = i
                        jump_j = j
                        UD = Dirtuple[0]
                        LR = Dirtuple[1]
                        
                        if(Arr[jump_i][jump_j].Type == "norm"):
                            while(J == 1):

                                if(UD == -1 and jump_i-2>=0 and jump_j+ 2*LR>=0 and jump_j+ 2*LR<=7 and Arr[ jump_i+ 2*(-1) ][ jump_j+ 2*LR ] == "_"):
                                    jmp[mi][mj] = 1
                                    Jumps.append([jump_i+ 2*(-1),jump_j+ 2*LR])
                                    
                                    Point_table[mi][mj]+=COIN_KILL_BONUS
                                    
                                    jump_i = jump_i+ 2*(-1)
                                    jump_j = jump_j+ 2*LR

                                    if(jump_i+ 2*(-1)>=0):
                                        
                                        if(jump_j+2<=7 and Arr[jump_i-1][jump_j+1]!="_" and Arr[jump_i-1][jump_j+1].color == "red" and Arr[ jump_i+ 2*(-1) ][ jump_j+2 ] == "_"):
                                            LR = 1
                                        elif(jump_j-2 >=0 and Arr[jump_i-1][jump_j-1]!="_" and Arr[jump_i-1][jump_j-1].color == "red"):
                                            LR = -1
                                        else:
                                            J = 0
                                    else:
                                        J = 0
                                else:
                                    J = 0
                            if(jmp[mi][mj] == 0):
                                Point_table[mi][mj]-=IMMOBILITY
                            else:
                                if(Point_table[mi][mj] >= Max_pt):
                                    Max_pt = Point_table[mi][mj]
                                    MaxJumps = Jumps
                                    move_no = mi
                                    move_coin = mj
                                    
                        else:
                            while(J==1):
                                if(jump_i+2*UD>=0 and jump_i+2*UD<=7 and jump_j+2*LR>=0 and jump_j+2*LR<=7 and Arr[ jump_i+2*UD ][ jump_j+2*LR ] == "_"):
                                    jmp[mi][mj] = 1
                                    Jumps.append([jump_i+ 2*UD,jump_j+ 2*LR])
                                    Point_table[mi][mj]+=COIN_KILL_BONUS
                                    jump_i = jump_i+ 2*UD
                                    jump_j = jump_j+ 2*LR

                                    
                                    if(UD!=1 and LR!=-1 and jump_i-2 >=0 and jump_j+2<=7 and Arr[jump_i-1][jump_j+1]!="_" and Arr[jump_i-1][jump_j+1].color == "red" and Arr[ jump_i-2 ][ jump_j+2 ] == "_" and ([jump_i-2,jump_j+2] not in Jumps)):
                                        UD = -1; LR = 1;            #jumping towards top-right
                                    elif(UD!=1 and LR!=1 and jump_i-2 >=0 and jump_j-2>=0 and Arr[jump_i-1][jump_j-1]!="_" and Arr[jump_i-1][jump_j-1].color == "red" and Arr[ jump_i-2 ][ jump_j-2 ] == "_" and ([jump_i-2,jump_j-2] not in Jumps)):
                                        UD = -1; LR = -1;           #jumping towards top-left
                                    elif(UD!=-1 and LR!=-1 and jump_i+2<=7 and jump_j+2<=7 and Arr[jump_i+1][jump_j+1]!="_" and Arr[jump_i+1][jump_j+1].color == "red" and Arr[ jump_i+2 ][ jump_j+2 ] == "_" and ([jump_i+2,jump_j+2] not in Jumps)):    
                                        UD = 1;LR = 1;              #jumping towards bottom right
                                    elif(UD!=-1 and LR!=1 and jump_i+2<7 and jump_j-2>=0 and Arr[jump_i+1][jump_j-1]!="_" and Arr[jump_i+1][jump_j-1].color == "red" and Arr[ jump_i+2 ][ jump_j-2 ] == "_" and ([jump_i+2,jump_j-2] not in Jumps)):
                                        UD = 1;LR = -1;             #jumping towards bottom left
                                    else:
                                        J=0
                                else:
                                    J=0
                            if(jmp[mi][mj] == 0):
                                Point_table[mi][mj]-=IMMOBILITY
                            else:
                                if(Point_table[mi][mj] >= Max_pt):
                                    Max_pt = Point_table[mi][mj]
                                    MaxJumps = Jumps
                                    move_no = mi
                                    move_coin = mj        
            mi += 1

        while(mi < 4):
            Dirtuple = Dirs[mi]
            Jumps = []

            if(Arr[i][j].Type != "king"):
                    Point_table[mi][mj]-=IMMOBILITY
            else:

                if(i+ Dirtuple[0] > 7 or i+ Dirtuple[0] < 0 or j+ Dirtuple[1] > 7 or j+ Dirtuple[1] < 0):
                    Point_table[mi][mj]-=IMMOBILITY    
                
                else:

                    Dirtuple = Dirs[mi]
                    if(Arr[ i+ Dirtuple[0] ][ j+ Dirtuple[1] ] == "_"):
                
                        if((i+ 2*Dirtuple[0]>=0)and(i+ 2*Dirtuple[0]<=7)and(j+ 2*Dirtuple[1]<=7)and(j+ 2*Dirtuple[1]>=0)and(Arr[ i+ 2*Dirtuple[0] ][ j ] == "_") and (Arr[ i ][ j+ 2*Dirtuple[1] ] != "_") and (Arr[ i ][ j+ 2*Dirtuple[1] ].color == "red" )):
                            Point_table[mi][mj]-=COIN_LOSS_PENALTY                         #Minus points for bringing coin to risk
                    
                        elif((i+ 2*Dirtuple[0]>=0)and(i+ 2*Dirtuple[0]<=7)and(j+ 2*Dirtuple[1]<=7)and(j+ 2*Dirtuple[1]>=0)and(Arr[ i+ 2*Dirtuple[0] ][ j ] != "_") and (Arr[ i ][ j+ 2*Dirtuple[1] ] == "_") ):
                            if(Arr[ i+ 2*Dirtuple[0] ][ j ].color == "red" and (Arr[ i+ 2*Dirtuple[0] ][ j ].Type == "king")):
                                Point_table[mi][mj]-=COIN_LOSS_PENALTY                     #Minus points for bringing coin to risk
                            else:
                                Point_table[mi][mj]+=MOVE_AHEAD_REWARD                     #A Safe but not necessarily Beneficial move

                        elif((i+ 2*Dirtuple[0]>=0)and(i+ 2*Dirtuple[0]<=7)and(j+ 2*Dirtuple[1]<=7)and(j+ 2*Dirtuple[1]>=0)and Arr[ i+ 2*Dirtuple[0] ][ j+ 2*Dirtuple[1] ] != "_"):
                            if(Arr[ i+ 2*Dirtuple[0] ][ j+ 2*Dirtuple[1] ].color == "red" and Arr[ i+ 2*Dirtuple[0] ][ j+ 2*Dirtuple[1] ].Type == "king"):
                                Point_table[mi][mj]-=COIN_LOSS_PENALTY                     #Minus points for bringing coin to risk
                            else:
                                Point_table[mi][mj]+=MOVE_AHEAD_REWARD                     #A Safe but not necessarily Beneficial move
                        else:
                            Point_table[mi][mj]+=MOVE_AHEAD_REWARD

                        if(Point_table[mi][mj] > Max_pt):
                            Max_pt = Point_table[mi][mj]
                            move_no = mi
                            move_coin = mj    
                    else:                                                   #in case of possibility of a jump
                        J = 1
                        jump_i = i
                        jump_j = j
                        UD = Dirtuple[0]
                        LR = Dirtuple[1]
                        while(J==1):
                                if(Arr[ jump_i+2*UD ][ jump_j+2*LR ] == "_"):
                                    jmp[mi][mj] = 1
                                    Jumps.append([jump_i+ 2*UD,jump_j+ 2*LR])
                                    Point_table[mi][mj]+=COIN_KILL_BONUS
                                    jump_i = jump_i+ 2*UD
                                    jump_j = jump_j+ 2*LR

                                    
                                    if(UD!=1 and LR!=-1 and jump_i-2 >=0 and jump_j+2<=7 and Arr[jump_i-1][jump_j+1]!="_" and Arr[jump_i-1][jump_j+1].color == "red" and Arr[ jump_i-2 ][ jump_j+2 ] == "_" and ([jump_i-2,jump_j+2] not in Jumps)):
                                        UD = -1; LR = 1;            #jumping towards top-right
                                    elif(UD!=1 and LR!=1 and jump_i-2 >=0 and jump_j-2>=0 and Arr[jump_i-1][jump_j-1]!="_" and Arr[jump_i-1][jump_j-1].color == "red" and Arr[ jump_i-2 ][ jump_j-2 ] == "_" and ([jump_i-2,jump_j-2] not in Jumps)):
                                        UD = -1; LR = -1;           #jumping towards top-left
                                    elif(UD!=-1 and LR!=-1 and jump_i+2<=7 and jump_j+2<=7 and Arr[jump_i+1][jump_j+1]!="_" and Arr[jump_i+1][jump_j+1].color == "red" and Arr[ jump_i+2 ][ jump_j+2 ] == "_" and ([jump_i+2,jump_j+2] not in Jumps)):    
                                        UD = 1;LR = 1;              #jumping towards bottom right
                                    elif(UD!=-1 and LR!=1 and jump_i+2<7 and jump_j-2>=0 and Arr[jump_i+1][jump_j-1]!="_" and Arr[jump_i+1][jump_j-1].color == "red" and Arr[ jump_i+2 ][ jump_j-2 ] == "_" and ([jump_i+2,jump_j-2] not in Jumps)):
                                        UD = 1;LR = -1;             #jumping towards bottom left
                                    else:
                                        J=0
                                else:
                                    J=0
                        if(jmp[mi][mj] == 0):
                            Point_table[mi][mj]-=IMMOBILITY
                        else:
                            if(Point_table[mi][mj] >= Max_pt):
                                Max_pt = Point_table[mi][mj]
                                MaxJumps = Jumps
                                move_no = mi
                                move_coin = mj
            mi+=1
        mj+=1

    #Display here
    for i in range(0,4):
        for j in range(0,len(Reds)):
            print(Point_table[i][j],"\t",end=' ')
        print()

    print(move_no, move_coin)

    if(Max_pt == -100):
        print("Player Wins\n")
        G=1
    elif(jmp[move_no][move_coin] == 1):
        Pointer.clearstamps()
        Pointer.setposition(Map[Grays[move_coin].j],Map[7-Grays[move_coin].i])
        Grays[move_coin].setPos(Grays[move_coin].i,Grays[move_coin].j)

        pi = Grays[move_coin].i; pj = Grays[move_coin].j;
        di = 0; dj = 0;
        
        for JP in MaxJumps:
            Pointer.clearstamps()
            Pointer.setposition(Map[JP[1]],Map[7-JP[0]])
            Grays[move_coin].setPos(JP[0],JP[1])
            Arr[pi][pj] = "_"
            if(JP[0]==0):
                if(Grays[move_coin].Type!="king"):
                    Grays[move_coin].upgrade()

            di = (pi + JP[0])//2
            dj = (pj + JP[1])//2

            d_ind = Arr[di][dj].ai
            Arr[di][dj] = "_"
            del Reds[d_ind]
            RedT[d_ind].hideturtle()
            del RedT[d_ind]
            
            while(d_ind<len(Reds)):
                Reds[d_ind].ai-=1
                Arr[Reds[d_ind].i][Reds[d_ind].j] = Reds[d_ind]
                d_ind+=1

            
            if(len(Reds)==0):
                print("Computer Wins!!\n")
                window.bgcolor("green")
                G = 1
            else:
                pi = JP[0]
                pj = JP[1]
                
    else:
        '''Point(Map[Grays[move_coin].j],Map[7-Grays[move_coin].i])
        Point(Map[j+(Dirs[move_no])[1]],Map[7-(i+Dirs[move_no][0])])'''
        Pointer.clearstamps()
        Pointer.setposition(Map[Grays[move_coin].j+(Dirs[move_no])[1]],Map[7-(Grays[move_coin].i+Dirs[move_no][0])])
        Pointer.stamp()

        Arr[Grays[move_coin].i][Grays[move_coin].j] = "_"
        Grays[move_coin].setPos(Grays[move_coin].i+Dirs[move_no][0],Grays[move_coin].j+(Dirs[move_no])[1])
        if(Grays[move_coin].i+Dirs[move_no][0] == 0):
            Grays[move_coin].upgrade()
        
    P = 1-P
    window.bgcolor(Colors[P])

def Click_Act(x,y):
    global CompLock
    global P
    global G

    if(CompLock == 0 and G==0):
        Point(x,y)
        print("-----------------------------------------------------------------------------------")
        for i in range(8):
            for j in range(8):
                if(Arr[i][j]=="_"):
                    print("_","\t",end = "")
                else:    
                    print(Arr[i][j].Type,Arr[i][j].color,Arr[i][j].ai,"\t",end = "")
            print("\n")
        print("-----------------------------------------------------------------------------------")    
        if(P==1):
            CompLock = 1
            sleep(1)
            Comp_move()
            CompLock = 0
            print("-----------------------------------------------------------------------------------")
            for i in range(8):
                for j in range(8):
                    if(Arr[i][j]=="_"):
                        print("_","\t",end = "")
                    else:    
                        print(Arr[i][j].Type,Arr[i][j].color,Arr[i][j].ai,"\t",end = "")
                print("\n")
            print("-----------------------------------------------------------------------------------")
    else:
        print("Please Wait for your turn")

window.onscreenclick(Click_Act,1)        
'''def Unpoint(x,y):                                   #Unhighlights a highlighted square
    Pointer.clearstamps()
    
window.onscreenclick(Unpoint,3)'''
