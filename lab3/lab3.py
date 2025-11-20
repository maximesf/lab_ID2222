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
    
    def resetSampleSize(self, newS) -> None:
        if(newS!=None):
            print(f"Seting new sample size to {newS}")
            self.s = newS
        print("Reseting samples queue")
        self.samples = -1*np.ones(newS) #initialize with minus one
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

"""
elem = (boolean,[u,v]) # tuple(bool,list) true = +1/ false =-1


"""

class TriestBase:
    M: int
    samples: list[list]
    t: int
    tau: int
    tau_local : dict

    def __init__(self,M) -> None:
        print("TriestBase algorithm")
        self.M = M
        self.samples = []
        self.t = 0
        self.tau = 0
        self.tau_local = {}

    def triestBase(self, stream : list[tuple])->None:
        for elem in stream:
            if(elem[0]):
                UV = elem[1]
                self.t = self.t + 1
                if self.sampleEdge(UV):
                    self.samples.append(UV)
                    self.updateCounters(UV,True)
            
    def sampleEdge(self, UV : list) -> bool:
        if(self.t <= self.M):
            return True
        elif(np.random.randint(1, self.M + 1) <= self.t):
            index = np.random.randint(0, self.M)
            UVprime = self.samples[index]
            self.samples.pop(index)
            self.updateCounters(UVprime , False)
            return True
        return False
    
    def updateCounters(self, UV : list, rule: bool) -> None:
        interNeighbours = self.findNeighbours(UV)

        if rule:
            delta = 1
        else:
            delta = -1

        for c in interNeighbours:
            self.tau = self.tau + delta
            self.tau_local[c] = self.tau_local.get(c, 0) + delta
            self.tau_local[UV[0]] = self.tau_local.get(UV[0], 0) + delta
            self.tau_local[UV[1]] = self.tau_local.get(UV[1], 0) + delta

    def findNeighbours(self, UV : list) -> list:
        neighboorU = []
        neighboorV = []
        for sample in self.samples:
            if(np.isin(UV[0],sample)):
                maskU = np.isin(sample,UV[0],invert=True)
                temp =np.array(sample)
                neighboorU.append(temp[maskU].item())
            if(np.isin(UV[1],sample)):
                maskV = np.isin(sample,UV[1],invert=True)
                temp =np.array(sample)
                neighboorV.append(temp[maskV].item())
        inter = np.isin(neighboorU,neighboorV)
        if(np.sum(inter)==0):
            return []
        else:
            neighboorU = np.array(neighboorU)
            return neighboorU[inter]
    
    def setSamples(self,samplesList) -> None: # testing only
        self.samples = samplesList

countTriangle = TriestBase(6)
streamingEdges = [(True,[1,2]),(True,[2,5]),(True,[5,4]),(True,[4,1]),(True,[1,3]),(True,[3,5]),(True,[4,6]),(True,[3,4])]
fakeSamples = [[1,2],[2,5],[5,4],[4,1],[1,3]]#,[3,2]]#,[1,5]]
#countTriangle.setSamples(fakeSamples)
countTriangle.triestBase(streamingEdges)
print(countTriangle.samples)
print(countTriangle.tau_local)
print(countTriangle.tau)




