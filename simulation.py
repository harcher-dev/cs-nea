import math
G = 0.000000000066743 # big G constant

from csv_data_manager import *

class Simulation:
    def __init__(self, fileToLoad="none"):
        self.__bodies = []
        if fileToLoad != "none": 
            self.addMassesFromFile(CSVDataManager().readDataFromFile(fileToLoad))

    def addMass(self, mass):
        self.__bodies.append(mass)
    
    def addMassesFromFile(self, data):
        for row in data:
            posVector = Vector3(row['posX'], row['posY'], row['posZ'])
            velocityVector = Vector3(row['velX'], row['velY'], row['velZ'])

            mass = int(row['mass'])
            tag = row['tag']

            self.addMass(Mass(posVector, mass, velocityVector, tag))

    def getMasses(self):
        return self.__bodies
    
    def propagate(self, deltaTime):
        for mass in self.__bodies:
            mass.propagate(self.__bodies, deltaTime)
            
class Mass:
    def __init__(self, posVector, mass, velocity, tag="none"):
        self.pos = posVector
        self.mass = mass
        self.velocity = velocity
        self.tag = tag

    def propagate(self, bodies, deltaTime):
        forces = []

        for mass in bodies:
            if mass == self: continue
            # calculate the distance between masses
            directionVector = Vector3.subtract(mass.pos, self.pos)
            distance = directionVector.magnitude()

            # calculate individual force
            forceMagnitude = G * ((self.mass * mass.mass) / pow(distance / 2, 2))
            forceDirection = directionVector.normalized()

            forceVector = forceDirection.multiply(forceMagnitude)

            forces.append(forceVector)

        # sum forces
        netForce = Vector3(0.0,0.0,0.0)
        for force in forces:
            netForce = Vector3.add(force, netForce)
            # print(netForce)
        # calculate acceleration per time
        acceleration = netForce.multiply(deltaTime / self.mass)

        # add acceleration per time to velocity
        self.velocity = Vector3.add(self.velocity, acceleration)

        # print(self.velocity)

        # add the velocity multplied by deltatime to displacement
        self.pos = Vector3.add(self.pos, self.velocity).multiply(deltaTime)
        
class Vector3:
    def __init__(self, x,y,z):
        self.x, self.y, self.z = (float(x),float(y),float(z))
        
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
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
    