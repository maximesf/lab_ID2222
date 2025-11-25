import numpy as np
import time as t
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans as km

class SpectralClustering:
    sigma: float
    affinity : np.matrix
    data: list
    D : np.matrix
    L : np.matrix
    N: int
    X: np.matrix

    def __init__(self, data, sigma) -> None:
        self.data = np.array(data)
        self.N = len(data)
        self.affinity=np.empty((self.N,self.N))
        self.sigma = sigma
        for i in range(self.N):
            for j in range(self.N):
                if(i==j):
                    self.affinity[i,j]=0
                else:
                    self.affinity[i,j] = np.exp(-np.linalg.norm(self.data[i] - self.data[j])**2/(2*sigma**2))
        print(self.affinity)
        
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
        
        print(f'lambdas ={eigenvalues}')
        k = self.unicite(eigenvalues,1e-6) # u = np.unique(eigenvalues) #remove any multiplicity
        print(f'k = {k}')
        self.Y = eigenvectors[:,self.N-k:]


    """
    np.unique and unicite do the same thing, just gave a threshold value 
    """
    def unicite(self,eigenvalues:list,threshold: float)->int:
        unique = [eigenvalues[0]]
        for i in range(1,len(eigenvalues)):
            if(not(self.inUnique(threshold,unique,eigenvalues[i]))):
                unique.append(eigenvalues[i])
        print(f'unique lambdas ={unique}')
        return len(unique)

    def inUnique(self,threshold,unique,eigenvalue)->bool:
        for u in unique:
            if(np.abs(eigenvalue-u)<threshold):
                return True
        return False

    #useless
    def buildY(self)->None:
        Y = [self.X[i]/np.linalg.norm(self.X[i]) for i in range(self.N)]
        self.Y = np.array(Y)
    
    #clustering technique K-mean
    def kMeans(self) -> list:
        kmeans = km(n_clusters=len(self.Y[0])).fit(self.Y)
        return kmeans.labels_

def getData(file : str, splitterChar: str):
    output = []
    with open(file, "r") as f:
        for line in f:
            row = list(map(int, line.split(splitterChar)))
            output.append(row)
    return output

e1 = getData("example1.dat",",")

sigma = 0.03
data = [[1,2],[1,3],[2,3],[2,4],[4,5],[5,6],[6,4]]

test = SpectralClustering(data,sigma)
test.buildDandL()
fit = test.kMeans()
print(fit)


clusterE1 = SpectralClustering(e1,0.1)
clusterE1.buildDandL()
labels = clusterE1.kMeans()
print(labels)

    
