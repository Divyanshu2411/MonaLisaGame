import pygame, sys, os, random
from pygame.font import Font

from pygame.time import delay

''' 
This will need 3 arguments
- the grid size
- the size of the tiles
- the size of the margin
'''
class SlidePuzzle:
    Xdistance=150
    Ydistance=100

    def __init__ (self, gs, ts, ms): #grid size, tile size, margin size
        self.gs, self.ts, self.ms = gs,ts, ms #tupple bante hai phir assignment hota hai ek sath

        Xdistance=150
        Ydistance=100

        self.tiles_len= gs[0]*gs[1]-1 #cause the tiles is mXn and we need one less for blank

        self.tiles= [(x,y) for y in range (gs[1]) for x in range (gs[0])] #grid based on arr of coordinates, as in (0,0), (0,1) (0,2) types
        
        self.tilepos= {(x,y) : (x*(ts+ms) +ms+Xdistance, y*(ts+ms)+ms+Ydistance) for y in range (gs[1]) for x in range (gs[0])} #coordinates on screen ka dictionary, ye wala actual location se deal kar rha, as in (110,210), (210,210)

        self.prev=None

        numMoves=0
        
       
        self.rect= pygame.Rect(0,0,gs[0]*(ts+ms) +ms, gs[1]*(ts+ms)+ms)
        # print(self.rect.size)

        pic=pygame.transform.smoothscale(pygame.image.load('image.jpg'),self.rect.size)
        font=pygame.font.Font(None,120)

        self.images=[]     
        for i in range (self.tiles_len):
            x,y=self.tilepos[self.tiles[i]]
            image= pic.subsurface(x-Xdistance,y-Ydistance,ts,ts)
            text= font.render(str(i+1),2,(0,0,0))
            w,h= text.get_size()
            image.blit(text,((ts-w)/2, (ts-h)/2)) #center text
            self.images+=[image]

    def getBlank(self): return self.tiles[-1]
    def setBlank(self,pos): self.tiles[-1]=pos
    opentile= property(getBlank,setBlank)

    def switch(self,tile): 
        self.tiles[self.tiles.index(tile)], self.opentile,self.prev=self.opentile,tile,self.opentile

    def in_grid(self,tile): 
        return tile[0]>=0 and tile[0]<self.gs[0] and tile[1]>=0 and tile[1]<self.gs[1]

    def adjacent(self): 
        x,y= self.opentile; 
        return (x-1,y),(x+1,y),(x,y-1),(x,y+1)

    def random(self): 
        adj=self.adjacent() 
        self.switch(random.choice([pos for pos in adj if self.in_grid(pos) and pos!=self.prev]))

       
    def update(self, dt,original): #mouse event
        Xdistance=150
        Ydistance=100
        flag=1
        mouse= pygame.mouse.get_pressed() #if mouse is clicked
        mpos= pygame.mouse.get_pos()# position of cursor
        if mouse[0] :
            x,y= (mpos[0]-Xdistance)%(self.ts +self.ms), (mpos[1]-Ydistance)%(self.ts+self.ms)
            if x> self.ms and y> self.ms:
                tile=(mpos[0]-Xdistance)//self.ts, (mpos[1]-Ydistance)//self.ts
                if self.in_grid(tile) and tile in self.adjacent() : 
                    self.switch(tile)
                    flag=0

        if flag==0 and self.tiles==original: flag=3
        
        return flag

    
    def draw(self, screen):
        for i in range (self.tiles_len):
            x,y= self.tilepos[self.tiles[i]]
            screen.blit(self.images[i],(x,y))

    def events(self,event,original): #keyboard
        flag=-1
        if event.type==pygame.KEYDOWN:
            flag=1
            for key, dx, dy in ((pygame.K_w,0,-1),(pygame.K_s,0,1), (pygame.K_a,-1,0),(pygame.K_d,1,0)): #wasd contorls
                if event.key== key:
                    x,y= self.opentile; tile=x+dx, y+dy
                    if self.in_grid(tile): 
                        self.switch(tile)
                        flag=0


            for key, dx, dy in ((pygame.K_UP,0,-1),(pygame.K_DOWN,0,1), (pygame.K_LEFT,-1,0),(pygame.K_RIGHT,1,0)): #keyboard controls
                if event.key== key:
                    x,y= self.opentile; tile=x+dx, y+dy
                    if self.in_grid(tile): 
                        self.switch(tile)
                        flag=0
                        # for x,y in self.tiles:
                        #     print(x,y)
                        # print("___________________________________________")

            if event.key== pygame.K_SPACE:
                for i in range(100): self.random()
                flag=2

        if flag==0 and self.tiles==original: flag=3
            
        return flag
            # if flag : 
            #     font = pygame.font.Font(None,120)
            #     errortxt = font.render('INVALID MOVE!!', True, (255, 255, 255))
            #     screen.blit(errortxt, (195, 475))
            

    




def main():
    pygame.init() #initialise the pygame
    os.environ['SDL_VIDEO_CENTERED']='1' ###To center things
    pygame.display.set_caption('Slide Puzzle') #display the caption above
    screen=pygame.display.set_mode((800,800)) #size of game window, argument should be two item sequence, 
    fpsclock=pygame.time.Clock() #framepersecond, refresh rate

   
    numMoves=0
    font = pygame.font.Font(None,60)
    heading=pygame.font.Font(None,100)
    heading.set_underline(True)
    def printCount() :
        screen.blit(font.render('Moves Made : '+str(numMoves), True, (255, 90, 255)), (50, 670))

   
    program = SlidePuzzle((3,3), 150, 4)

    original= [(x,y) for y in range (3) for x in range (3)]
    
    flag=0
    while True:
        dt= fpsclock.tick()/1000 #small time interval

        screen.fill((0,0,0)) #black color se bhar do
        # pygame.font.Font
        screen.blit(heading.render('Mona Lisa Puzzle', False, (125, 90, 255)), (100, 25))
        program.draw(screen) 
        printCount()
        if flag==1:
            screen.blit(font.render('You WIN!!', True, (0, 255, 0)), (300, 300))
            pygame.display.flip() #display
            delay(5000)
            numMoves=0
        pygame.display.flip() #display
        flag=0
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit() #agar quit aaye to quit
            flagKey=program.events(event,original)
            flagMouse= program.update(dt,original) #update every dt second
            
            if flagKey==0 or flagMouse==0: numMoves=numMoves+1

            if flagKey==1:
                screen.blit(font.render('Wrong Move!!!!', False, (255, 0, 0)), (300, 300))
                pygame.display.flip() #display
                delay(1000)
            
            if flagKey==3 or flagMouse==3:
                flag=1
        
        




if __name__=='__main__':
    main()