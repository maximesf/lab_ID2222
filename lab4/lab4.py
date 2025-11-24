import numpy as np
import time as t
import matplotlib.pyplot as plt

class SpectralClustering:
    sigma: float
    affinity : np.matrix
    data: list
    D : np.matrix
    L : np.matrix
    N: int
    X: np.matrix

    def __init__(self, data, sigma) -> None:
        self.data = data
        self.N = len(data)
        hstack = [data for i in range(self.N)]
        vstack = np.array(hstack).T
        self.sigma = sigma
        self.affinity = np.exp(-np.abs(vstack - np.array(hstack))**2/(2*sigma**2)) - np.identity(self.N)

    def buildDandL(self) -> None:
        D = np.zeros((self.N, self.N))
        diagValues = np.sum(self.affinity,axis=1) #sum rows of A
        for i, value in enumerate(diagValues):
            D[i][i] = value 
        self.D = D
        invertedsqrtD = np.where(D==0,0,D**(-1/2))
        self.L = invertedsqrtD @ self.affinity @ invertedsqrtD
        #np.linalg.eigh already normalize eigenvectors
        eigenvalues, eigenvectors = np.linalg.eigh(self.L) #eigenvectors are column wise eigenvectors[:, i] <-> eigenvalues[i]
        # u, indices = np.unique(eigenvalues, return_index=True) #remove any multiplicity
        # self.X = [eigenvectors[:,i] for i in indices]
        self.Y = eigenvectors
        print(eigenvectors)

    #useless
    def buildY(self)->None:
        print()
        Y = [self.X[i]/np.linalg.norm(self.X[i]) for i in range(self.N)]
        self.Y = np.array(Y)
    
    #clustering technique
    def kMeans(self) -> None:
        return


sigma = 1
data = [0,2,3]

test = SpectralClustering(data,sigma)
test.buildDandL()
#test.buildY()
#print(test.Y)


    
