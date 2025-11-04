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
            print(oneShingle)
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
        print(kShingle)
        kShingle = np.unique(kShingle)
        for word in kShingle:
            res = h.md5(word.encode())
            hashShingle.append(h.md5(word.encode()).hexdigest())
        self.hashShingle = hashShingle
        return hashShingle
    
class CompareSets:
    def __init__(self) -> None:
        print('Done')
        
    def getJaccardSim(self,set1,set2) -> float:
        inter = 0
        union = 1
        for hash1 in set1:
            for hash2 in set2:
                if(hash1==hash2):
                    inter += 1
        union = len(np.unique(set1 + set2))

        print(inter/union)
        return inter/union

comparator = CompareSets()

fiveShingler = Shingling(5)
#kShingle = fiveShingler.kShingling('test.csv')
hashShingle = fiveShingler.uniqueHashShingling('test.csv')
email2Hash = fiveShingler.uniqueHashShingling('test.csv')
#print(kShingle)
#print(hashShingle)

similarity = comparator.getJaccardSim(hashShingle,email2Hash)
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
