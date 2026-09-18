import pygame, sys
from pygame.locals import *
from simulation import *

class Viewer:
    def __init__(self, sim:Simulation):
        # Set up display
        pygame.init()
        self.__running = True
        self.__WIDTH, self.__HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        pygame.display.set_caption('2D viewer for simulation')
        self.__fps = 60
        self.__fpsClock = pygame.time.Clock()
        self.simulation = sim
        
        self.simulation.addMass(Mass(Vector3(10,10,10),pow(10,1),Vector3(0,0,0)))
        self.simulation.addMass(Mass(Vector3(50,10,10),pow(10,15),Vector3(0,0,0)))
        
        
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
        pass
    
    def drawScreen(self):
        self.screen.fill((0, 0, 0)) # Fill the screen with black
        for mass in self.simulation.getMasses():
            pygame.draw.circle(self.screen, (200,200,200), (mass.pos.x,mass.pos.z), 15)