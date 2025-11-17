import numpy as np
import time as t
import matplotlib.pyplot as plt
import copy


class FrequentItem:
    itemFound: np.matrix

    def __init__(self) -> None:
        print("Frequent Item Finder")
    
    def findSingletons(self, set: np.matrix,threshold: int) -> list[any]:
        temp = []
        for subset in set:
            temp = np.hstack((temp,np.unique(subset)))
        uniqueItems = np.unique(temp)
        items = []
        for i,item in enumerate(uniqueItems):
            sum = 0
            for j,subset in enumerate(set):
                idx = (subset == item)
                sum += np.sum(idx)
                if(sum/len(set)>=threshold):
                        items.append(item)
                        break
        return items
    
    def buildCandidates(self, singletons: list[any], multiplons: np.matrix) -> list[any]:
        candidates = []
        for set in multiplons:
            for single in singletons:
                if(np.isin(single,set,invert=True)):
                    if isinstance(set, np.integer):
                        temp = [set, single]
                        temp.sort()
                        candidates.append(temp)
                    else:
                        temp = set
                        temp = np.hstack((temp,single))
                        temp.sort()
                        candidates.append(temp)
      
        return np.unique(candidates,axis=0)
    
    #initialize frequentItem with singletons
    #each subset of the initial working set should be a set and not a bag meaning that every subset contain an element exactly once
    def getFrequentItemFinder(self,threshold:int,set: np.matrix,frequentItem : list , singletons : list[any], depth: int = 0) -> list[any]:
        candidates = self.buildCandidates(singletons,frequentItem[depth])
        #print(f"candidates= {candidates}")
        depth +=1
        items = []
        for i,item in enumerate(candidates):
            sum = 0
            for j,subset in enumerate(set):
                mask = np.isin(subset,item)
                if(np.sum(mask)==depth+1):
                    sum += 1
            if(sum/len(set)>=threshold):
                items.append(item)
        #print(f"items that are frequent= {items}")
        if(len(items)==0):
            #print("exting recursive loop")
            #print(frequentItem)
            self.itemFound = frequentItem
            return frequentItem
        else:
            frequentItem.append(items)
            #print(f"resulting matrix= {frequentItem}")
            self.getFrequentItemFinder(threshold,set,frequentItem,singletons,depth)

    def computeSupport(self, set: np.matrix , kFrequent: list[float]) -> float:
        support = 0
        for j,subset in enumerate(set):
            mask = np.isin(subset,kFrequent)
            if(np.sum(mask)==len(kFrequent)):
                    support += 1
        return support

    """
    X->Y is stored as followed
    [[[X1],[Y1]],
     [[X2],[Y2]],
        ...
     [[Xn],[Yn]]]
    
    """

    def findSimpleAssociationRules(self, set : np.matrix ,confidence : float) -> np.matrix:
        simpleAssociationRules = []
        for kFrequents in self.itemFound[1:]: #no need to investigate singletons
            for i,kFrequent in enumerate(kFrequents):
                supportN = self.computeSupport(set,kFrequent)
                for j in range(len(kFrequent)-1,-1,-1):
                    temp = np.delete(kFrequent,j)
                    #print(temp)
                    supportD = self.computeSupport(set,temp)
                    if(supportN/supportD >= confidence):
                        simpleAssociationRules.append([temp,[kFrequent[j]]])
                        #print([temp,[kFrequent[j]]])
                        self.mineAssociationRules(set,temp,[kFrequent[j]],simpleAssociationRules,supportN,confidence)
                        #print(f"building association rules = {simpleAssociationRules}")
        return simpleAssociationRules
                    
    def mineAssociationRules(self,set: np.matrix , X : list[float], Y : list[float], rules : list[any], supportN : int, confidence : float)-> np.matrix:
        if(len(X)<=1):
            return rules
        else:
            for i in range(len(X)):
                temp = np.delete(X,i)
                #print(Y)
                supportD = self.computeSupport(set,temp)
                if(supportN/supportD >= confidence):
                    rules.append([temp,Y+[X[i]]])
                    #print([temp,Y+[X[i]]])
                    self.mineAssociationRules(set,temp,Y+[X[i]],rules,supportN,confidence)

# with open("T10I4D100K.dat", "r") as f:
#     for line in f:
#         row = list(map(int, line.split()))
#         matrix.append(row)

def saveFrequentItemsResults(file,matrix):
    with open(file, "w") as f:
        for row in matrix:
            line = " ".join(map(str, row))
            f.write(line + "\n")

def saveAssociationRulesResults(file,matrix):
    with open(file, "w") as f:
        for row in matrix:
            line = f"{row[0]} -> {np.array(row[1]).astype(float)}"
            f.write(line + "\n")

def getData(file):
    output = []
    with open(file, "r") as f:
        for line in f:
            row = list(map(int, line.split()))
            output.append(row)
    return output

matrix =[]

with open("dataSaves/test.dat", "r") as f:
    for line in f:
        row = list(map(int, line.split()))
        matrix.append(row)

#print(matrix)

#exampleSet = getData("data/10.dat")
print("=====")
#print(exampleSet)

#print(matrix)

itemFinder = FrequentItem()
mySet = [[1],[3,1,2],[2,1],[1],[2,3,4],[1,4],[5,3],[1,2,3],[4,2],[1,2,3],[1,2]]
otherSet = [[1,2,3],[2,3],[1,2,3],[3],[2]]

singletons = itemFinder.findSingletons(matrix,0.03)
kFrequents = itemFinder.getFrequentItemFinder(0.03,matrix,[singletons],singletons)
simpleAsso = itemFinder.findSimpleAssociationRules(matrix,0.5)

saveFrequentItemsResults(f"kfrequentssave.dat",itemFinder.itemFound)
saveAssociationRulesResults(f"associationrulessave.dat",simpleAsso)

print("=======")
"""
print(len(matrix))
e1 = t.time()
singletons = itemFinder.findSingletons(matrix,0.04)
itemFinder.getFrequentItemFinder(0.04,matrix,[singletons],singletons)
s1 = (t.time()-e1)*1000
e2 = t.time()
simpleAsso = itemFinder.findSimpleAssociationRules(matrix,0.5)
s2 = (t.time()-e2)*1000
with open("time.dat", "a") as f:
    f.write(f"{len(matrix)} {s1} {s2}\n")

saveFrequentItemsResults(f"kfrequents{len(matrix)}.dat",itemFinder.itemFound)
saveAssociationRulesResults(f"associationrules{len(matrix)}.dat",simpleAsso)


timeScales = np.genfromtxt("time.dat")
print(timeScales.T)

nbLines= [10**i for i in range(3,6)]
plt.scatter(timeScales.T[0],timeScales.T[1],label='kFrequent')
#plt.scatter(nbLines,timeScales.T[0],label='Association')
plt.xlabel("number of lines")
plt.ylabel("time in ms")
plt.show()"""

"""
timekFrequent = []
timeAssociation = []

thresholds = [4,5,7,10]
for i in thresholds:
    print(f'finding frequent items t={i/100}')
    e = t.time()
    singletons = itemFinder.findSingletons(matrix,i/100)
    kFrequents = itemFinder.getFrequentItemFinder(i/100,matrix,[singletons],singletons)
    timekFrequent.append((t.time()-e)*1000)
    print(f'finding associations rules')
    e = t.time()
    simpleAsso = itemFinder.findSimpleAssociationRules(matrix,0.5)
    timeAssociation.append((t.time()-e)*1000)

plt.scatter(thresholds,timekFrequent,label='kFrequent')
plt.xlabel("threshold (%)")
plt.ylabel("time in ms")
plt.show()

plt.scatter(thresholds,timeAssociation,label='Association')
plt.xlabel("threshold (%)")
plt.ylabel("time in ms")
plt.show()
"""
"""
timekFrequent = []
timeAssociation = []

confidence = [40,50,70,90]
singletons = itemFinder.findSingletons(matrix,0.03)
kFrequents = itemFinder.getFrequentItemFinder(0.03,matrix,[singletons],singletons)
saveFrequentItemsResults(f"kfrequentsT0.03.dat",itemFinder.itemFound)

for i in confidence:
    print(f'finding associations rules c={i/100}')
    e = t.time()
    simpleAsso = itemFinder.findSimpleAssociationRules(matrix,i/100)
    timeAssociation.append((t.time()-e)*1000)
    saveAssociationRulesResults(f"associationrulesC{i/100}.dat",simpleAsso)

plt.scatter(confidence,timeAssociation,label='Association')
plt.xlabel("confidence (%)")
plt.ylabel("time in ms")
plt.show()

"""
quit()
testMatrix = [[1,2,1,1],[3,1,4],[4,4,9,1,5,7]]
myCharSet =['a','b','ab']
myFrequentItems =[]
# singletonsMatrix = itemFinder.findSingletons(testMatrix,0.1)
# print(f"testMatrix singletons {singletonsMatrix}")
singletons = itemFinder.findSingletons(mySet,0.1)
print(singletons)
candidates = itemFinder.buildCandidates(singletons,singletons)
print(f"candidates {candidates}")
itemFinder.getFrequentItemFinder(0.1,mySet,[singletons],singletons)
print("found")
print(itemFinder.itemFound)