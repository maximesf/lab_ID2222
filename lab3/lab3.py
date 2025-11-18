import numpy as np
import time as t
import matplotlib.pyplot as plt

class Reservoir:
    s: int
    samples: np.matrix[int]
    n: int

    def __init__(self, s) -> None:
        self.s = s
        self.samples = -1*np.ones(s) #initialize with minus one
        self.n = 0

    def resampleFromIncomingData(self,incomingData: np.matrix[int] ) -> None:
        for elem in incomingData:
            if(self.n < self.s):
                self.samples[self.n] = elem
            else:
                rdm= np.random.randint(1, self.n + 2)
                if(rdm <= self.s): #skewed coin flip to interchange samples (or not)
                    index = np.random.randint(0, self.s)
                    self.samples[index] = elem
            self.n = self.n + 1

reservoirTesteur = Reservoir(4)
firstStream = [1,5,6,2]
reservoirTesteur.resampleFromIncomingData(firstStream)
print(reservoirTesteur.samples)
secondStream = [1,3,4,5,6,7,8,9]
reservoirTesteur.resampleFromIncomingData(secondStream)
print(f'samples = {reservoirTesteur.samples}, n = {reservoirTesteur.n}')


