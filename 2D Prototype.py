import pygame
import sys
import math

from pygame.locals import *

# Initialize Pygame

class Main:
    def __init__(self):
        sim = Simulation()
        Viewer(sim)

class Viewer:
    def __init__(self, sim):
        # Set up display
        pygame.init()
        self.running = True
        self.WIDTH, self.HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('')
        self.__fps = 60
        self.__fpsClock = pygame.time.Clock()
        self.simulation = sim
        self.mainloop()

    def mainloop(self):
        # Main game loop
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.simulation.addMass(Mass(Vector3(0,0,0),pow(10,6),Vector3(1,1,1)))

            # Update game state
            # Draw everything
            
            self.simulation.propagate(1/self.__fps)

            self.draw_screen()
            # Flip the display to show the new frame
            pygame.display.flip()
            # Cap the frame rate
            self.__fpsClock.tick(self.__fps)
    
    def draw_screen(self):
        self.screen.fill((0, 0, 0)) # Fill the screen with black
        for mass in self.simulation.getMasses():
            print(mass.pos.x)
            pygame.draw.circle(self.screen, (200,200,200), (mass.pos.x,mass.pos.z), 15)

class Simulation:
    def __init__(self):
        self.G = 0.000000000066743 # big G constant
        self.bodies = []

    def addMass(self, mass):
        self.bodies.append(mass)

    def getMasses(self):
        return self.bodies
    
    def propagate(self, deltaTime):
        for mass in self.bodies:
            mass.propagate(self, self.bodies, deltaTime)

class Vector3:
    def __init__(self, x,y,z):
        self.x, self.y, self.z = (x,y,z)
    
    def magnitude(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))

    def normalized(self):
        mag = self.magnitude()
        return Vector3(self.x/mag, self.y/mag, self.z/mag)

    def multiply(self, a):
        return Vector3(self.x*a,self.y*a,self.z*a)

    @staticmethod
    def subtract(l, m):
        return Vector3(l.x-m.x, l.y-m.y, l.z-m.z)

    @staticmethod
    def add(l, m):
        return Vector3(l.x+m.x, l.y+m.y, l.z+m.z)

class Mass:
    def __init__(self, posVector, mass, velocity):
        self.pos = posVector
        self.mass = 1
        self.velocity = velocity


    def propagate(self, simulation:Simulation, bodies, deltaTime):
        forces = []

        for mass in bodies:
            # calculate the distance between masses
            directionVector = Vector3.subtract(mass.pos, self.pos)
            distance = directionVector.magnitude()
            if distance == 0.0: continue

            # calculate individual force
            forceMagnitude = simulation.G * ((self.mass * mass.mass) / pow(distance / 2, 2))
            forceDirection = directionVector.normalized()

            forceVector = forceDirection.multiply(forceMagnitude)

            forces.append(forceVector)

        # sum forces
        netForce = Vector3(0,0,0)
        for force in forces:
            Vector3.add(force, netForce)
        
        # calculate acceleration per time
        acceleration = netForce.multiply(deltaTime / self.mass)

        # add acceleration per time to velocity
        self.velocity = Vector3.add(self.velocity, acceleration)

        # add velocity per time to displacement
        self.pos = Vector3.add(self.pos, self.velocity)

if __name__ == "__main__":
    Main()