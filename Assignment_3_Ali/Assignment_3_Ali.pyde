import os,random

path = os.getcwd() + "/"
G_WIDTH=600
G_HEIGHT=600
TILE_WIDTH = 30
TILE_HEIGHT = 30
dir=RIGHT         # dir refers to direction of snake.   By default, it is right
dirVert = [UP,DOWN]     # Pair of vertical directions that cannot be pressed together
dirHorz = [LEFT,RIGHT]     # Pair of horizontal directions that cannot be pressed together
NUM_COLS=G_WIDTH//TILE_WIDTH     
NUM_ROWS=G_HEIGHT//TILE_HEIGHT
j=0

class Tile:      #Class for tiles
    def __init__(self,c,r,tw,th):       #c is column number     r is row number     tw is tile width   th is tile height
        self.r=r
        self.c=c
        self.tw=tw
        self.th=th
    def showTile(self):                     # show tile as rectangles
        noFill()
        stroke(125)
        strokeWeight(0.5)
        rect(self.c*self.tw,self.r*self.th,self.tw,self.th)

class Board:        #Game Board
    def __init__(self,w,h,tw,th):     # w is width    h is height     tw is tile width      th is tile height
        self.w=w
        self.h=h
        self.th=th
        self.tw=tw
        self.tiles=[]        # collection of tiles within board
        self.num_cols=self.w//self.tw        
        self.num_rows=self.h//self.th
        #Adding tiles to the list "tiles"
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.tiles.append(Tile(col,row,self.tw,self.th))
        
    def showBoard(self):      #Showing tiles
        for tile in self.tiles:
            tile.showTile()

class snakeElement():     # Class for the snake parts (including head)
    def __init__(self,head,x,y,dir,colour):
        self.posX=x
        self.posY=y
        self.dir=dir            # Direction that the current snake element is moving in
        self.head=head          # Boolean variable to check if the element is the head
        self.colour = colour    # Color of the snake part
        if self.head:
            self.imgup=loadImage(path+"images/head_up.png")        #image in the up direction
            self.imgl=loadImage(path+"images/head_left.png")       #image in the left direction
        
    
    def move(self):    
        global TILE_WIDTH, TILE_HEIGHT  
        
        if self.dir==UP:
            self.posY-=TILE_HEIGHT
            
        elif self.dir==DOWN:
            self.posY+=TILE_HEIGHT
        elif self.dir==LEFT:
            self.posX-=TILE_WIDTH
        elif self.dir==RIGHT:
            self.posX+=TILE_WIDTH
    
    def setDir(self,dir):    # Change direction
        self.dir=dir
    
    def getDir(self):        # get direction
        return self.dir
    
    def display(self):
        global TILE_WIDTH, TILE_HEIGHT
        if not self.head:             #Fill according to color if the element is not the head
                if self.colour=="G":
                    fill(80,153,32)     #Green Fill
                elif self.colour=="R":
                    fill(173,48,32)     #Red Fill
                elif self.colour=="Y":
                    fill(251,226,76)     #Yellow Fill
                    
                ellipse(self.posX,self.posY,TILE_WIDTH,TILE_HEIGHT)     #Print circle if it is not the head
        #Code for printing image according to the direction the snake's head is facing    
        elif self.dir==UP:
            image(self.imgup, self.posX-TILE_WIDTH/2,self.posY-TILE_HEIGHT/2,TILE_WIDTH,TILE_HEIGHT)  
        elif self.dir==DOWN:
            image(self.imgup, self.posX-TILE_WIDTH/2,self.posY-TILE_HEIGHT/2,TILE_WIDTH,TILE_HEIGHT,self.imgup.height,self.imgup.width,0,0)  
        elif self.dir==LEFT:
            image(self.imgl, self.posX-TILE_WIDTH/2,self.posY-TILE_HEIGHT/2,TILE_WIDTH,TILE_HEIGHT)  
        elif self.dir==RIGHT:
            image(self.imgl, self.posX-TILE_WIDTH/2,self.posY-TILE_HEIGHT/2,TILE_WIDTH,TILE_HEIGHT,self.imgl.height,self.imgl.width,0,0)  
    
                    
            
        
    
    

class Snake():      #Class for whole snake
    def __init__(self):
        self.parts = [snakeElement(True,TILE_WIDTH*(NUM_ROWS)/2-TILE_WIDTH//2,TILE_HEIGHT*(NUM_ROWS)/2-TILE_HEIGHT//2,RIGHT,"G")]   #self.parts is the list of the snake elements
        for i in range(1,3):
            self.parts.append(snakeElement(False,TILE_WIDTH*(NUM_ROWS)/2-TILE_WIDTH//2-TILE_WIDTH*i,TILE_HEIGHT*(NUM_ROWS)//2-TILE_HEIGHT//2,RIGHT,"G"))
            
    def changeDir(self,dir):      #Change direction of the snake
        self.parts[0].setDir(dir)
    
    def display(self):     #Display each element of Snake
        for part in self.parts:
            part.display()
        
    def move(self):     #Move Snake
        i=0
        for part in self.parts:                
            part.move()
            #Making the direction of the nth snake element be the direction of the (n-1)th snake element
            if i==0:
                swap=part.getDir()
                i+=1
                continue
            
            temp=part.getDir()
            part.setDir(swap)
            swap=temp
            
    def growOne(self,fruit):  # Function for increasing the length of the snake after eating fruit
        lastDir=self.parts[-1].dir   #parts[-1] refers to the tail of the snake, where the next snake element will be added
        X=self.parts[-1].posX
        Y=self.parts[-1].posY
        type=fruit.type[1]
        self.parts.append(self.addElem(lastDir,X,Y,type))
            
    

    def addElem(self,dir,X,Y,colour):      # Function for deciding the direction and position of the next snake element
        if dir==UP:
            return snakeElement(False,X,Y+30,UP,colour)
        elif dir==DOWN:
            return snakeElement(False,X,Y-30,DOWN,colour)
        elif dir==LEFT:
            return snakeElement(False,X+30,Y,LEFT,colour)
        elif dir==RIGHT:
            return snakeElement(False,X-30,Y,RIGHT,colour)
    
    
    def bitItself(self):     #Function for checking if the snake has bitten itself
        part1=self.parts[0]      # part1 is the head of the snake
        for part2 in self.parts[1:]:     
            if part1.posX==part2.posX and part1.posY==part2.posY:
                return True
        return False
            

class Fruit():          
    def __init__(self,target):
        global NUM_ROWS, NUM_COLS, TILE_WIDTH, TILE_HEIGHT
        self.axisX=range(TILE_WIDTH//2,TILE_WIDTH*NUM_COLS+TILE_WIDTH//2,TILE_WIDTH)          # Axis referse to possible positions where the fruit can be placed (along the x or y axis)  e.g. range(15,30*20+15,30)
        self.axisY=range(TILE_HEIGHT//2,TILE_HEIGHT*NUM_ROWS+TILE_HEIGHT//2,TILE_HEIGHT)     
        self.posX=random.choice(self.axisX)
        self.posY=random.choice(self.axisY)
        
        while(self.checkSnake(target)):    #Keep recreating the position x and y of the fruit until it is not on the snake
            self.posX=random.choice(self.axisX)
            self.posY=random.choice(self.axisY)
        
        self.apple=[loadImage(path+"images/apple.png"),"R"]
        self.banana=[loadImage(path+"images/banana.png"),"Y"]
        # type=[apple,banana]
        self.type = random.choice([self.apple,self.banana])
        
    def display(self):
        global TILE_WIDTH, TILE_HEIGHT
        fill(132,132,0)
        image(self.type[0],self.posX-TILE_WIDTH/2,self.posY-TILE_HEIGHT/2,TILE_WIDTH,TILE_HEIGHT)         # Display fruit
        # ellipse(self.posX,self.posY,30,30)
    
    def checkSnake(self,target):    # Function to check that the position of the target (the fruit) does not overlap with the Snake 
        for ele in target.parts:      
            if self.posX==ele.posX and self.posY==ele.posY:
                return True
        return False
        
        
        

class Game():
    def __init__(self,w,h,tw,th):
        
        self.snake = Snake()       # Game's snake
        self.fruit = Fruit(self.snake)      # Game's fruit
        self.board = Board(w,h,tw,th)     #Game's board
        self.score = 0     #Game's score
        self.maxSnake=(w//tw)*(h//th)     # Max number of snake elements possible in the game
        self.play = True     # Variable to decide whether the game should keep printing
        self.win = False    # Variable to decide whether the player has won
    
    def changeDir(self,dir):    # Function to change the direction of the snake in the game
        self.snake.changeDir(dir)
    
    def display(self):    #Display game
        self.checkEat()
        self.board.showBoard()
        if self.play:
            self.fruit.display()
            self.snake.display()
       
    
    def checkEat(self):     #Check if the snake has eaten the fruit
        if self.fruit.posX == self.snake.parts[0].posX and self.fruit.posY == self.snake.parts[0].posY:
            self.snake.growOne(self.fruit)     #Increment the length of the snake
            self.fruit=Fruit(self.snake)       # Re-initialize the snake
            self.score+=1     
    
    def checkWin(self):     # Check if the game has been won
        global NUM_COLS, NUM_ROWS, TILE_WIDTH, TILE_HEIGHT
        if self.snake.bitItself() or self.snake.parts[0].posY>=NUM_COLS*TILE_WIDTH or self.snake.parts[0].posX>=NUM_ROWS*TILE_HEIGHT or self.snake.parts[0].posX<=0 or self.snake.parts[0].posY<=0: # Check if the snake has gone out of bounds and if the snake has bitten itself
            self.play = False
        
        if len(self.snake.parts)>=self.maxSnake:      # Check if the number of snake elements is (greater or) equal to the maximum number of snakes possible on the grid.
            self.play = False
            self.win = True
        
            
    
    
        


#Starting the Game
game = Game(G_WIDTH,G_HEIGHT,TILE_WIDTH,TILE_HEIGHT)


def checkOpp(dir):  # Function to make sure the pressed key is not in the opposite direction of the snake's direction
    if (dir in dirVert and keyCode not in dirVert) or (dir in dirHorz and keyCode not in dirHorz):
        return True
    return False


def setup():
    # background(0)
    size(G_WIDTH,G_HEIGHT)



        
def draw():
    global dir,G_WIDTH, G_HEIGHT
    if frameCount % 10 == 0 and game.play:   # Slowing down the speed of the snake and checking if the game should be played
        if checkOpp(dir) and keyCode!=0:  #Making sure that the entered direction is not in the opposite direction and an arrow key is pressed
            dir = keyCode          
            game.changeDir(dir)    #Change direction according to keyCode
            
        game.snake.move()
        game.checkWin()
        background(255)
        stroke(255)
        game.display()
        textSize(20)
        text("Score:"+str(game.score),G_WIDTH*0.8,20)
    elif not game.play:  # If game is finished
        background(0)
        textSize(50)
        if game.win:    # If game has won
            text("YOU WON!",G_WIDTH/2,G_HEIGHT/2)
        else:
            text("GAME OVER",G_WIDTH/2,G_HEIGHT/2)
        textSize(20)
        text("Score: " + str(game.score), G_WIDTH*0.5,G_HEIGHT*0.75)
        


def mouseClicked():  #If mouse is clicked, then restart the game
    game.__init__(G_WIDTH,G_HEIGHT,TILE_WIDTH,TILE_HEIGHT)
    dir = RIGHT
    j = 0
