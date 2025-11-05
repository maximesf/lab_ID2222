import numpy as np
import csv
import hashlib as h

class Shingling:
    k: int
    shingle: list[str]
    hashShingle: list[str]

    def __init__(self, k: int = 1) -> None:
        self.k = k
    
    def kShingling(self, csvFile: str) -> list[str]:
        oneShingle = []
        with open(csvFile, newline='') as f:
            reader = csv.reader(f)
            row = next(reader)
            oneShingle = list(row)
            #print(oneShingle)
        text = oneShingle[0]
        kShingle = []
        for i in range(len(text)):
            if(i+self.k>len(text)):
                self.shingle = kShingle
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
            res = h.md5(word.encode())
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
    
estimator = CompareSignatures()
miniHasher = MinHashing()
comparator = CompareSets()

fiveShingler = Shingling(5)
#kShingle = fiveShingler.kShingling('test.csv')
hashList = fiveShingler.uniqueHashShingling('test.csv')
#print(f"len = {len(hashList)}")
hashShingle = fiveShingler.uniqueHashShingling('test.csv')
test3 = fiveShingler.uniqueHashShingling('test2.csv')
#print(kShingle)
#print(hashShingle)

similarity = comparator.getJaccardSim(hashShingle,test3)
signature = miniHasher.buildSignature(hashShingle,test3,100000)
estimate = estimator.computeEstimateSimilarity(signature)
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
