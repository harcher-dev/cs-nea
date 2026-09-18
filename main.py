from simulation import *
from viewer import *

class Main:
    def __init__(self):
        sim = Simulation()
        Viewer(sim)

if __name__ == "__main__":
    Main()