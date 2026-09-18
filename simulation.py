import math

SPEED_MULTIPLIER = 1000000000000000000000

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
            forceMagnitude = SPEED_MULTIPLIER * simulation.G * ((self.mass * mass.mass) / pow(distance / 2, 2))
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

        print(self.velocity)
        # add velocity per time to displacement
        self.pos = Vector3.add(self.pos, self.velocity)
        
class Vector3:
    def __init__(self, x,y,z):
        self.x, self.y, self.z = (x,y,z)
        
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