import numpy as np
import csv
import hashlib as h
import time
import matplotlib.pyplot as plt
import seaborn as sns

class Shingling:
    k: int
    shingle: list[str]
    hashShingle: list[str]
    removeCaracter: list[str]
    word: bool

    def __init__(self, k: int = 1, word = False) -> None:
        self.k = k
        self.word = word
        self.removeCaracter = '()+=-_!,;.:/?"'
    
class CompareSets:
    def __init__(self) -> None:
        print('Compare Sets class')

    def preProcess(self,set1,set2):
        temp1, temp2 = [],[]
        for i in range(len(set1)):
            if not (set1[i] == 0 or set1[i] == 4 or set2[i] == 0 or set2[i]==4):
                temp1.append(set1[i])
                temp2.append(set2[i])
            
        return temp1, temp2
    
    def jaccardSim(self,set1,set2) -> float:
        y = np.array(set1)-np.array(set2)
        y = np.where(y==0,1,0)
        
        return np.sum(y)/len(y)
        
    def getJaccardSim(self,set1,set2) -> float:
        inter = 0
        union = 1
        for hash1 in set1:
            for hash2 in set2:
                if(hash1==hash2):
                    inter += 1
        union = len(np.unique(set1 + set2))
        return inter/union


import pandas as pd
import polars as pl

comparator = CompareSets()

df = pl.read_excel('data/EP7.xlsx')

"""
n =  df.height
sclicing = 9

simMat = np.zeros((n,n))

for i in range(n):
    subseti = df[i, 9:]

    rowi = list(subseti.rows()[0])
    print(f'{i} done over, {n} total')
    for j in range(i+1,n):
        subsetj = df[j, 9:]
        rowj = list(subsetj.rows()[0])
        tempi, tempj = comparator.preProcess(rowi,rowj)
        simMat[i,j] = comparator.jaccardSim(tempi,tempj)

print(simMat)
np.save('simMatrix.npy', simMat)

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

docs = df[:,0]

sns.heatmap(simMat, annot=True, xticklabels=docs, yticklabels=docs, cmap="viridis")
plt.title("Exact Jaccard Similarity Matrix")
plt.show()
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

countries = df[:, 4]
epgs = df[:, 6]

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_mep_clusters(coords, countries, epgs):
    
    df = pd.DataFrame({
        'MDS1': coords[:, 0],
        'MDS2': coords[:, 1],
        'Country': countries,
        'EPG': epgs
    })

    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='MDS1', y='MDS2', hue='EPG', 
                    palette='tab10', s=80, alpha=0.8, edgecolor='w')
    
    plt.title('MEP Clusters by Political Group (EPG)', fontsize=15, pad=20)
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')

    plt.legend(title='Political Group', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='MDS1', y='MDS2', hue='Country', 
                    palette='husl', s=80, alpha=0.8, edgecolor='w')
    
    plt.title('MEP Clusters by Country', fontsize=15, pad=20)
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2, borderaxespad=0.)
    plt.tight_layout()
    plt.show()


def mds(S, k=2):

    n = S.shape[0]
    diag = np.zeros((n, n)) 
    np.fill_diagonal(diag, 1)

    S = S+S.T + diag
    S = np.nan_to_num(S, nan=0.0)  

    D_sq = 2 - 2 * S

    I = np.eye(n)
    ones = np.ones((n, n))
    J = I - (ones / n)
    B = -0.5 * J @ D_sq @ J
    eigenvalues, eigenvectors = np.linalg.eigh(B)

    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    L_k = np.diag(np.maximum(eigenvalues[:k], 0))
    V_k = eigenvectors[:, :k]
    X = V_k @ np.sqrt(L_k)

    return X

data = np.load('simMatrix.npy')
X = mds(data)

plot_mep_clusters(X,countries,epgs)

#print(row1)
#print(row2)
quit()