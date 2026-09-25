import pygame, sys
from pygame.locals import *


from simulation import *

from random import randint

class Viewer:
    def __init__(self, sim:Simulation):
        # Set up display
        pygame.init()
        self.__running = True
        self.__WIDTH, self.__HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        self.__fps = 60
        self.__fpsClock = pygame.time.Clock()
        self.simulation = sim
        self.__zoomMultiplier = 1

        self.__viewerOffset = (0,0)
        
        pygame.display.set_caption('2D viewer for simulation')
        # self.simulation.addMass(Mass(Vector3(110,10,10),pow(10,13),Vector3(0,0,0)))
        # self.simulation.addMass(Mass(Vector3(50,10,10),pow(10,15),Vector3(0,0,0.1)))
        # self.simulation.addMass(Mass(Vector3(200,10,70),pow(10,12),Vector3(0,0,0.1)))
        self.simulation.addMass(Mass(Vector3(randint(0,self.__WIDTH),10,randint(0,self.__HEIGHT)),pow(10,randint(10,18)),Vector3(0.0,0.0,0.0)))
        self.simulation.addMass(Mass(Vector3(randint(0,self.__WIDTH),10,randint(0,self.__HEIGHT)),pow(10,randint(10,18)),Vector3(0.0,0.0,0.0)))
        self.simulation.addMass(Mass(Vector3(randint(0,self.__WIDTH),10,randint(0,self.__HEIGHT)),pow(10,randint(10,18)),Vector3(0.0,0.0,0.0)))
        
        
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
            self.simulation.propagate(1/self.__fps)

            # draw simulation
            self.drawScreen()
            
            # flip the display to show the new frame
            pygame.display.flip()
            self.__fpsClock.tick(self.__fps)
            
    def handleInput(self):
        if pygame.key.get_pressed()[pygame.K_e]:
            # increase view area
            self.__zoomMultiplier += 1/self.__fps
        elif pygame.key.get_pressed()[pygame.K_q]:
            # decrease view area
            if self.__zoomMultiplier - 1/self.__fps == 0.0: return
            self.__zoomMultiplier -= 1/self.__fps
    
    def drawScreen(self):
        self.screen.fill((0, 0, 0)) # clear the screen
        self.drawGrid()

        for mass in self.simulation.getMasses():
            pygame.draw.circle(self.screen, (200,200,200), (mass.pos.x/self.__zoomMultiplier,mass.pos.z/self.__zoomMultiplier), 10*(1/self.__zoomMultiplier))
    
    def drawGrid(self):
        lineGap = int((1/self.__zoomMultiplier)*100)
        lineOffset = (self.__viewerOffset[0] % lineGap, self.__viewerOffset[1] % lineGap)

        for i in range(self.__WIDTH % lineGap):
            pygame.draw.line(self.screen, (25,25,25), (i*lineGap,0), (i*lineGap,self.__HEIGHT), width=2)
        
        for i in range(self.__HEIGHT % lineGap):
            pygame.draw.line(self.screen, (25,25,25), (0, i*lineGap), (self.__WIDTH, i*lineGap), width=2)