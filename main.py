from simulation import *
from viewer import *

class Main:
    def __init__(self):
        sim = Simulation()
        Viewer(sim, frameRateLimit=60)

if __name__ == "__main__":
    Main()