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
    
    def kShingling(self, file: str, csvFile : bool = False ) -> list[str]:
        if(csvFile):
            oneShingle = []
            with open(file, newline='') as f:
                reader = csv.reader(f)
                row = next(reader)
                oneShingle = list(row)
                #print(oneShingle)
            text = oneShingle[0]
        else:
            with open(file, "r", encoding="utf-8") as file:
                text = file.read()
                text = text.replace("\n"," ")

        kShingle = []
        text = text.lower()
        
        for i in range(len(self.removeCaracter)):
            text = text.replace(self.removeCaracter[i],"")

        if(self.word):
            wordList = text.split(" ")
            for i in range(len(wordList)):
                if(i+self.k+1>=len(wordList)):
                    self.shingle = kShingle
                    #print(kShingle)
                    return kShingle
                key = ''
                for j in range(self.k):
                    key += wordList[i+j] + ' '
                key = key[:len(key)-1]
                kShingle.append(key)
        else:
            for i in range(len(text)):
                if(i+self.k+1>=len(text)):
                    self.shingle = kShingle
                    #print(kShingle)
                    return kShingle
                key = ''
                for j in range(self.k):
                    key += text[i+j]
                kShingle.append(key)
        
        
    def hashShingling(self, csvFile: str) -> list[int]:
        hashShingle = []
        kShingle = self.kShingling(csvFile)
        for word in kShingle:
            res = h.md5(word.encode())
            hashShingle.append(h.md5(word.encode()))
        self.hashShingle = hashShingle
        return hashShingle
    
    def uniqueHashShingling(self, csvFile: str) -> list[int]:
        hashShingle = []
        kShingle = self.kShingling(csvFile)
        #print(kShingle)
        kShingle = np.unique(kShingle)
        for word in kShingle:
            hashShingle.append(h.md5(word.encode()).hexdigest())
        self.hashShingle = hashShingle
        return hashShingle
    
class CompareSets:
    def __init__(self) -> None:
        print('Compare Sets class')
        
    def getJaccardSim(self,set1,set2) -> float:
        inter = 0
        union = 1
        for hash1 in set1:
            for hash2 in set2:
                if(hash1==hash2):
                    inter += 1
        union = len(np.unique(set1 + set2))
        return inter/union
    
class MinHashing:
    def __init__(self) -> None:
        print('MinHashing class')
        
    def buildSignature(self,set1,set2,nbPermut) -> float:
        
        union = np.unique(set1 + set2)
        mask1 = np.isin(union, set1)
        mask2 = np.isin(union, set2)
        
        signatureMatrix = np.empty((0, 2), int)
        for _ in range(nbPermut):
            permutedIndexes = np.random.permutation(len(union))
            lineSignatureMatrix = np.zeros((1,2))
            for i in range(len(permutedIndexes)):
                if(mask1[permutedIndexes[i]]):
                    lineSignatureMatrix[0][0]=i
                    break
            for j in range(len(permutedIndexes)):
                if(mask2[permutedIndexes[j]]):
                    lineSignatureMatrix[0][1]=j
                    break
            signatureMatrix = np.vstack((signatureMatrix, lineSignatureMatrix))

        return signatureMatrix

class CompareSignatures:
    def __init__(self) -> None:
        print('Compare Signatures class')
        
    def computeEstimateSimilarity(self,signature) -> float:
        
        signature = signature.T

        y = signature[0]-signature[1]
        y = np.where(y==0,1,0)
        
        return np.sum(y)/len(y)
    
class LocalSensitiveHash:
    band: int
    r: int
    threshold: int

    def __init__(self, band : int, threshold : int) -> None:
        self.band = band
        self.threshold = threshold

    def lookForCandidates(self,signature,col1 : int = 0,col2 : int = 1) -> float:
        
        self.r = int(len(signature)/self.band)
        similarities = 0
        if(self.r * self.band == len(signature)):
            signature = signature.T
            for i in range(self.band):
                band1 = str(signature[col1][i:i+self.r])
                band2 = str(signature[col2][i:i+self.r])
                
                if(h.md5(band1.encode()).hexdigest()==h.md5(band2.encode()).hexdigest()):
                    similarities += 1
                    print("similarity found")
            print(f"similarities = {similarities/self.band}")
            if(similarities/self.band >= self.threshold):
                return 1
            else:
                return 0
            
        else:
            print("Wrong size")
            return -1

LSHasher = LocalSensitiveHash(25,0.8) 
estimator = CompareSignatures()
miniHasher = MinHashing()
comparator = CompareSets()

fiveShingler = Shingling(10,False)
shingled = fiveShingler.kShingling('1.txt',False)
hashShingle = fiveShingler.uniqueHashShingling('1.txt')
test3 = fiveShingler.uniqueHashShingling('2.txt')

similarity = comparator.getJaccardSim(hashShingle,test3)
signature = miniHasher.buildSignature(hashShingle,test3,100)
estimate = estimator.computeEstimateSimilarity(signature)
#print(f"longueur de la signature {len(signature)}")
retour = LSHasher.lookForCandidates(signature)
print(f"r = {LSHasher.r}, retour de LSH {retour}")

#print(signature)
print(similarity)
print(estimate)

"""docs = ['00'+str(i)+'.txt' for i in range(1,10)]
print(docs)
comparedHash = fiveShingler.uniqueHashShingling('data/politics/010.txt')

e = time.time()
for doc in docs:
    hash = fiveShingler.uniqueHashShingling('data/politics/'+doc)
    signature = miniHasher.buildSignature(comparedHash,hash,100)
    estimate = estimator.computeEstimateSimilarity(signature)
    if(estimate>=0.2):
        print(doc)
print((time.time()-e)*1000)"""


"""permuts = [10**i for i in range(1,6)]
permuts = [10, 100, 1000, 10000, 40000, 70000, 100000]
docs = ['10.txt','200.txt','1000.txt','5000.txt']
numberWords = [10,200,1000,5000]
fiveShingler = Shingling(10,False)
for i in range(1,10,3):
    computeEstimate=[]
    for doc in docs:
        shingler = Shingling(i,True)
        e = time.time()
        comparedHash = shingler.uniqueHashShingling('data/lenght/'+doc)
        computeEstimate.append((time.time()-e)*1000)
    plt.plot(numberWords,computeEstimate,label=f"k = {i}")

plt.xlabel("Number of word")
plt.legend()
plt.ylabel("time in ms")
plt.show()"""

"""
docs = ['10.txt','200.txt','1000.txt','2500.txt','5000.txt']
numberWords = [10,200,1000,2500,5000]
fiveShingler = Shingling(10,False)

computeEstimate=[]
for doc in docs:
    e = time.time()

    for i in range(10):
        comparedHash = fiveShingler.uniqueHashShingling('data/lenght/'+doc)
        sim = comparator.getJaccardSim(hashShingle,comparedHash)
        # signature = miniHasher.buildSignature(hashShingle,comparedHash,100)
        # estimate = estimator.computeEstimateSimilarity(signature)

    computeEstimate.append((time.time()-e)*100)
print(computeEstimate)
plt.scatter(numberWords,computeEstimate)

plt.xlabel("Number of words")
plt.legend()
plt.ylabel("time in ms")
plt.show()
"""

permuts = [10, 100, 1000, 10000, 40000, 70000, 100000,150000,300000]
computeEstimate=[]
estimates = []

for i in permuts:
    e = time.time()
    signature = miniHasher.buildSignature(hashShingle,test3,i)
    estimate = estimator.computeEstimateSimilarity(signature)
    computeEstimate.append((time.time()-e)*1000)
    estimates.append(estimate)

jac = comparator.getJaccardSim(hashShingle,test3)
errorVector = np.abs(np.array(estimates)-jac)/jac*100
# fig = plt.figure()
# ax = plt.gca()
# ax.scatter(permuts ,compute , c='blue', alpha=0.05, edgecolors='none')
# ax.set_yscale('log')
# ax.set_xscale('log')
plt.scatter(permuts,computeEstimate,colorizer='blue')
plt.xlabel("number of permutation")
plt.ylabel("time in ms")
plt.show()

plt.scatter(permuts,errorVector,colorizer='blue')
plt.xlabel("number of permutation")
plt.ylabel("Relative error")
plt.show()

"""
computeEstimate=[]
computeLSH=[]
docs = ['10.txt','200.txt','1000.txt']
for doci in docs:
    e = time.time()
    comparedHash = fiveShingler.uniqueHashShingling('data/lenght/'+doci)
    temp = []
    tempLSH = []
    for docj in docs:
        hash = fiveShingler.uniqueHashShingling('data/lenght/'+docj)
        signature = miniHasher.buildSignature(comparedHash,hash,100000)
        
        estimate = estimator.computeEstimateSimilarity(signature)
        temp.append((time.time()-e)*1000)
        e = time.time()
        candidates = LSHasher.lookForCandidates(signature)
        tempLSH.append((time.time()-e)*1000)
    computeEstimate.append(temp)
    computeLSH.append(tempLSH)

sns.heatmap(computeLSH, annot=True, xticklabels=docs, yticklabels=docs, cmap="viridis")
plt.title("Computation time LSH")
plt.show()

sns.heatmap(computeEstimate, annot=True, xticklabels=docs, yticklabels=docs, cmap="viridis")
plt.title("Computation time LSH")
plt.show()"""