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