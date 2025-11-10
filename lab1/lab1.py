import numpy as np
import csv
import hashlib as h
import matplotlib.pyplot as plt
import time

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
    
    def kShingling(self, csvFile: str) -> list[str]:
        oneShingle = []
        with open(csvFile, newline='') as f:
            reader = csv.reader(f)
            row = next(reader)
            oneShingle = list(row)
            #print(oneShingle)
        text = oneShingle[0]
        kShingle = []

        text = text.lower()
        
        for i in range(len(self.removeCaracter)):
            text = text.replace(self.removeCaracter[i],"")

        if(self.word):
            wordList = text.split(" ")
            for i in range(len(wordList)):
                if(i+self.k>len(wordList)):
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
                if(i+self.k>len(text)):
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
#kShingle = fiveShingler.kShingling('test.csv')
#hashList = fiveShingler.uniqueHashShingling('test.csv')
#print(f"len = {len(hashList)}")
hashShingle = fiveShingler.uniqueHashShingling('1.csv')
test3 = fiveShingler.uniqueHashShingling('2.csv')
#print(kShingle)
#print(hashShingle)

similarity = comparator.getJaccardSim(hashShingle,test3)
for i in range(2,8):
    e = time.time()
    signature = miniHasher.buildSignature(hashShingle,test3,10**i)
    estimate = estimator.computeEstimateSimilarity(signature)
#print(f"longueur de la signature {len(signature)}")
retour = LSHasher.lookForCandidates(signature)
print(f"r = {LSHasher.r}, retour de LSH {retour}")

similarity = comparator.getJaccardSim(hashShingle,test3)
compute = []
permuts = [10**i for i in range(2,4)]
for i in permuts:
    e = time.time()
    signature = miniHasher.buildSignature(hashShingle,test3,i)
    estimate = estimator.computeEstimateSimilarity(signature)
    compute.append((e-time.time())*1000)

plt.scatter(i,compute)
plt.xlabel("number of permutation")
plt.ylabel("time in ms")
plt.show()

#print(signature)
print(similarity)
print(estimate)
"""
word = 'test'
word2 = 'test'
hash = h.md5(word.encode())
hash2 = h.md5(word2.encode())
print(hash.hexdigest())
print(hash2.hexdigest())


if(hash.hexdigest() == hash2.hexdigest()):
    print('le meme hash')
"""
