import pygame, sys
from pygame.locals import *


from simulation import *

from random import randint

PAN_SPEED_MULTIPLIER = 1
ZOOM_SPEED_MULTIPLIER = 1

class Viewer:
    def __init__(self, sim:Simulation, frameRateLimit):
        # Set up display
        pygame.init()
        self.__running = True
        self.__WIDTH, self.__HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        self.__fps = frameRateLimit
        self.__deltaTime = self.__fps
        self.__fpsClock = pygame.time.Clock()
        self.simulation = sim
        self.__zoomMultiplier = 1

        self.__viewerOffset = [0, 0]
        self.__centre = (self.__WIDTH/2, self.__HEIGHT/2)
        
        pygame.display.set_caption('2D viewer for simulation')
        
        self.simulation.addMass(Mass(Vector3(110,10,10),pow(10,13),Vector3(0,0,0)))
        self.simulation.addMass(Mass(Vector3(50,10,10),pow(10,15),Vector3(0,0,0.1)))
        self.simulation.addMass(Mass(Vector3(200,10,70),pow(10,12),Vector3(0,0,0.1)))
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
            self.simulation.propagate(1/self.__deltaTime)

            # draw simulation
            self.drawScreen()
            
            # flip the display to show the new frame
            pygame.display.flip()
            self.__deltaTime = self.__fpsClock.tick(self.__fps)
            
    def handleInput(self):
        # -- keyboard --
        keys = pygame.key.get_pressed()
        
        # zooming in and out (Q E)
        zoomAmount = (1/self.__fps) * ZOOM_SPEED_MULTIPLIER
        if keys[pygame.K_q]:
            # increase view area
            self.__zoomMultiplier += zoomAmount
        elif keys[pygame.K_e]:
            # decrease view area
            if self.__zoomMultiplier - zoomAmount > 0.0:
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
            
    def drawMasses(self):
        for mass in self.simulation.getMasses():
            pygame.draw.circle(
                self.screen, # surface
                (200,200,200), # colour
                ( self.__centre[0] + self.__viewerOffset[0] + (mass.pos.x / self.__zoomMultiplier), self.__centre[1] + self.__viewerOffset[1] + mass.pos.z / self.__zoomMultiplier ), # screen position
                10 * (1 / self.__zoomMultiplier) # radius
            )