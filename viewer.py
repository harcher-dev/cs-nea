import pygame, sys
from pygame.locals import *

from simulation import Simulation

PAN_SPEED_MULTIPLIER = 1
ZOOM_SPEED_MULTIPLIER = 1
START_ZOOM_MULTIPLIER = 2

class Viewer:
    def __init__(self, sim:Simulation, frameRateLimit):
        # Set up display
        pygame.init()
        self.__running = True
        self.__WIDTH, self.__HEIGHT = 1920//2, 1080//2
        self.screen = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        self.__fps = frameRateLimit
        self.__deltaTime = self.__fps
        self.__fpsClock = pygame.time.Clock()
        self.simulation = sim
        self.__zoomMultiplier = START_ZOOM_MULTIPLIER
        self.font = pygame.font.Font('noto_sans.ttf', 12)

        self.__viewerOffset = [0, 0]
        self.__centre = (self.__WIDTH/2, self.__HEIGHT/2)
        
        pygame.display.set_caption('2D viewer for simulation')



        # self.simulation.addMass(Mass(Vector3(200.0,10.0,10.0),pow(10,15),Vector3(0.0,0,0.0)))
        # self.simulation.addMass(Mass(Vector3(200.0,10.0,210.0),pow(10,8),Vector3(5.0,0,0.0), tag="a"))
        # self.simulation.addMass(Mass(Vector3(200.0,10.0,-190.0),pow(10,8),Vector3(-5.0,0,0.0), tag="b"))
        # self.simulation.addMass(Mass(Vector3(0,10.0,10.0),pow(10,8),Vector3(0,0,5.0), tag="c"))
        # self.simulation.addMass(Mass(Vector3(400.0,10.0,10.0),pow(10,8),Vector3(0.0,0,-5.0), tag="d"))

        # self.simulation.addMass(Mass(Vector3(0.0,0.0,1000.0),pow(10,17),Vector3(0.0,0,0.0)))
        # self.simulation.addMass(Mass(Vector3(0.0,0.0,0.0),pow(10,18),Vector3(0.0,0,0.0)))

        # self.simulation.addMass(Mass(Vector3(200.0,10.0,10.0),pow(10,8),Vector3(0.0,0,0.0)))


        # self.simulation.addMass(Mass(Vector3(0.0,10.0,0.0),pow(10,14),Vector3(15,0,0.0)))
        # self.simulation.addMass(Mass(Vector3(randint(0,self.__WIDTH),10,randint(0,self.__HEIGHT)),pow(10,randint(10,18)),Vector3(0.0,0.0,0.0)))
        # self.simulation.addMass(Mass(Vector3(randint(0,self.__WIDTH),10,randint(0,self.__HEIGHT)),pow(10,randint(10,18)),Vector3(0.0,0.0,0.0)))
        # self.simulation.addMass(Mass(Vector3(randint(0,self.__WIDTH),10,randint(0,self.__HEIGHT)),pow(10,randint(10,18)),Vector3(0.0,0.0,0.0)))
        
        
        self.mainloop()

    def mainloop(self):
        # Main game loop
        while self.__running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            # handle user input
            self.handleInput()
            
            # update simulation
            self.simulation.propagate(self.__deltaTime)

            # draw simulation
            self.drawScreen()
            
            # flip the display to show the new frame
            pygame.display.flip()
            self.__deltaTime = self.__fpsClock.tick(self.__fps) / 1000
            
    def handleInput(self):
        # -- keyboard --
        keys = pygame.key.get_pressed()
        
        # zooming in and out (Q E)
        zoomAmount = (self.__deltaTime) * ZOOM_SPEED_MULTIPLIER
        if keys[pygame.K_q]:
            # increase view area
            self.__zoomMultiplier += zoomAmount
        elif keys[pygame.K_e]:
            # decrease view area
            if zoomAmount > 0.0:
                self.__zoomMultiplier -= zoomAmount
    
        # panning around (W A S D)
        panAmount = PAN_SPEED_MULTIPLIER * self.__deltaTime
        if keys[pygame.K_w]:
            self.__viewerOffset[1] += panAmount
        elif keys[pygame.K_s]:
            self.__viewerOffset[1] -= panAmount
        if keys[pygame.K_a]:
            self.__viewerOffset[0] += panAmount
        if keys[pygame.K_d]:
            self.__viewerOffset[0] -= panAmount
            
        # -- mouse --
        if not pygame.mouse.get_focused(): return
        
        # panning around (mouse pos)
        mouseDelta = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0]:
            self.__viewerOffset[0] += mouseDelta[0]
            self.__viewerOffset[1] += mouseDelta[1]
        
        
        
    def drawScreen(self):
        self.screen.fill((0, 0, 0)) # clear the screen
        self.drawGridAndAxis()
        self.drawMasses()
        self.drawCoordinates()
    
    def drawGridAndAxis(self):
        # grid
        lineGap = int( (1 / self.__zoomMultiplier) * 100 )
        while lineGap < self.__WIDTH / 10:
            lineGap *= 2 # help performance by culling unneccesary grids
            
        lineOffset = ( (self.__centre[0] + self.__viewerOffset[0]) % lineGap, (self.__centre[1] + self.__viewerOffset[1]) % lineGap )

        for i in range(self.__WIDTH % lineGap):
            pygame.draw.line(self.screen, (25,25,25), (i*lineGap + lineOffset[0],0), (i*lineGap + lineOffset[0],self.__HEIGHT), width=2)
        
        for i in range(self.__HEIGHT % lineGap):
            pygame.draw.line(self.screen, (25,25,25), (0, i*lineGap + lineOffset[1]), (self.__WIDTH, i*lineGap + lineOffset[1]), width=2)
            
        # axis
        for axis in range(2):
            if self.__viewerOffset[axis] > self.__centre[axis]: # if off screen, no need to draw
                continue
            
            offset = self.__centre[axis] + self.__viewerOffset[axis]
            startPos = (offset, 0) if axis == 0 else (0, offset)
            endPos = (offset, self.__HEIGHT) if axis == 0 else (self.__WIDTH, offset)
            
            pygame.draw.line(
                self.screen, # surface
                (100,25,25) if axis == 0 else (25,25,100), # colour
                (startPos), # start
                (endPos), # end
                width=2
            )

    def drawCoordinates(self):
        self.drawText((f"{-self.__viewerOffset[0]}, {self.__viewerOffset[1]}"), (self.__WIDTH-100, self.__HEIGHT-100))
            
    def drawMasses(self):
        for mass in self.simulation.getMasses():

            pos = (self.__centre[0] + self.__viewerOffset[0] + (mass.pos.x / self.__zoomMultiplier), self.__centre[1] + self.__viewerOffset[1] + mass.pos.z / self.__zoomMultiplier)
            pygame.draw.circle(
                self.screen, # surface
                (200,200,200), # colour
                pos, # screen position
                10 * (1 / self.__zoomMultiplier) # radius
            )

            if mass.tag != "none":
                self.drawText(mass.tag, pos)

    def drawText(self, text:str, pos:tuple):
        text = self.font.render(text, True, (0, 0, 0), pygame.Color(200,200,200))
        text.set_alpha(255)
        textRect = text.get_rect()

        textRect.center = (pos[0], pos[1])
        self.screen.blit(text, textRect)
