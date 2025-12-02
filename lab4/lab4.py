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
    eigenValues : list
    eigenVectors : np.matrix
    k : int
    laplacien : np.matrix

    def __init__(self, data, sigma, dataIsGRaph, maxNode) -> None:
        self.k = None
        self.data = np.array(data)
        self.sigma = sigma
        if(dataIsGRaph):
            self.N = maxNode
            self.affinity=np.zeros((self.N,self.N))
            for edge in data:
                self.affinity[edge[0]-1,edge[1]-1]=1
                self.affinity[edge[1]-1,edge[0]-1]=1
        else:
            self.N = len(data)
            self.affinity=np.empty((self.N,self.N))
            for i in range(self.N):
                for j in range(self.N):
                    if(i==j):
                        self.affinity[i,j]=0
                    else:
                        self.affinity[i,j] = np.exp(-np.linalg.norm(self.data[i] - self.data[j])**2/(2*sigma**2))

    def buildDandL(self) -> None:
        D = np.zeros((self.N, self.N))
        diagValues = np.sum(self.affinity,axis=1) #sum rows of A
        for i, value in enumerate(diagValues):
            D[i][i] = value 
        self.D = D
        invertedsqrtD = np.where(D==0,0,D**(-1/2))
        self.laplacien = D-self.affinity
        self.L = invertedsqrtD @ self.affinity @ invertedsqrtD
        #np.linalg.eigh already normalize eigenvectors
        eigenvalues, eigenvectors = np.linalg.eigh(self.laplacien) #eigenvectors are column wise eigenvectors[:, i] <-> eigenvalues[i]
        self.eigenValues = eigenvalues
        self.eigenVectors = eigenvectors
        
        #k = self.unicite(eigenvalues,1e-6) 
        # u = np.unique(eigenvalues) #remove any multiplicity
        # k = len(u)
        #print(f'k = {k}')
        #self.Y = eigenvectors[:,self.N-k:]


    """
    np.unique and unicite do the same thing, just gave a threshold value 
    """
    def unicite(self,eigenvalues:list,threshold: float)->int:
        unique = [eigenvalues[0]]
        for i in range(1,len(eigenvalues)):
            if(not(self.inUnique(threshold,unique,eigenvalues[i]))):
                unique.append(eigenvalues[i])
        print(f'unique lambdas ={unique}')
        return unique

    def inUnique(self,threshold,unique,eigenvalue)->bool:
        for u in unique:
            if(np.abs(eigenvalue-u)<threshold):
                return True
        return False

    #useless
    def buildY(self )->None:
        
        Y = [self.X[i]/np.linalg.norm(self.X[i]) for i in range(self.N)]
        self.Y = np.array(Y)
    
    #clustering technique K-mean
    def kMeans(self) -> list:
        Y = self.eigenVectors[:,:self.k]
        kmeans = km(n_clusters=self.k).fit(Y)
        return kmeans.labels_

    def plotDifsEigen(self,maxClusters)->None:
        xAxis = [i for i in range(1,self.N+1)]
        plt.plot(xAxis,self.eigenValues)
        plt.ylabel("eigenValues")
        plt.show()
        print(f'lambdas ={self.eigenValues}')
        difs = []
        max = 0
        index = 1
        #dif = np.abs(self.eigenValues[:self.N-1] - self.eigenValues[1:])
        for i in range(maxClusters):
            if np.abs(self.eigenValues[i]-self.eigenValues[i+1])>max :
                max = np.abs(self.eigenValues[i]-self.eigenValues[i+1])
                index = i+1
            difs.append(np.abs(self.eigenValues[i]-self.eigenValues[i+1]))
        plt.plot(xAxis[:maxClusters],difs)
        plt.ylabel("lambda[i]-lambda[i+1]")
        plt.show()
        print(f'k = {index}')
        self.k = index
        
def getData(file : str, splitterChar: str):
    output = []
    maxNode = 0
    with open(file, "r") as f:
        for line in f:
            row = list(map(int, line.split(splitterChar)))
            row[:2]
            if(maxNode<row[0]):
                maxNode=row[0]
            if(maxNode<row[1]):
                maxNode=row[1]
            output.append(row)
    return output, maxNode

e1, maxNode1 = getData("example1.dat",",")
e2, maxNode2 = getData("example2.dat",",")

sigma = 0.03
data = [[1,2],[1,3],[2,3],[2,4],[4,5],[5,6],[6,4]]
customGraph = [[1,2],[1,3],[2,4],[4,5],[1,5],[2,6],[1,6],[5,7],[5,8],[2,8],[2,9],[3,9],[3,10],[9,10],
               [9,8],[9,5],[9,6],[9,7],[10,8],[10,7],[10,6],
               [4,11],[11,12],[11,13],[12,13],[12,14],[12,15],[12,16],[12,17],[13,16],[13,18],[13,19],
               [14,15],[14,16],[15,13],[15,17],[15,20],[16,20],[16,17],[16,19],[16,18],[17,19],[17,20],
               [19,20],[20,21],[21,22],[21,23],[21,24],[21,25],[22,23],[22,24],[22,25],[23,24],[23,25],
               [24,25]]

test = SpectralClustering(data,None,True,6)
course = SpectralClustering(customGraph,None,True,25)

"""
test.buildDandL()
test.plotDifsEigen(5)
fit = test.kMeans()
print(fit)

course.buildDandL()
course.plotDifsEigen(20)
fit = course.kMeans()
print(fit)

fix, axes = plt.subplots(nrows=1, ncols=2)
axes[0].imshow(course.affinity)
axes[1].imshow(test.affinity)
plt.show()
"""

e=t.time()
clusterE1 = SpectralClustering(e1,None,True,maxNode1)
clusterE1.buildDandL()
clusterE1.plotDifsEigen(int(maxNode1/2))
labels = clusterE1.kMeans()
s = (t.time()-e)*1000
print(f'calculation time = {s}')
print(f'classification = {labels}')

e=t.time()
clusterE2 = SpectralClustering(e2,None,True,maxNode2)
clusterE2.buildDandL()
clusterE2.plotDifsEigen(int(maxNode2/2))
labels = clusterE2.kMeans()
s = (t.time()-e)*1000
print(f'calculation time = {s}')
print(f'classification = {labels}')

fix, axes = plt.subplots(nrows=1, ncols=2)
fix.suptitle('Affinity Matrix')
axes[0].imshow(clusterE1.affinity)
axes[0].set_title('example1.dat')
axes[1].imshow(clusterE2.affinity)
axes[1].set_title('example2.dat')
plt.show()
