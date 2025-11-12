import numpy as np
import csv
import hashlib as h
import mmap

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
    def getFrequentItemFinder(self,threshold:int,set: np.matrix,frequentItem : list , singletons : list[any], depth: int = 0) -> np.matrix:
        candidates = self.buildCandidates(singletons,frequentItem[depth])
        print(f"candidates= {candidates}")
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
        print(f"items that are frequent= {items}")
        if(len(items)==0):
            print("exting recursive loop")
            print(frequentItem)
            self.itemFound = frequentItem
            return frequentItem
        else:
            frequentItem.append(items)
            print(f"resulting matrix= {frequentItem}")
            self.getFrequentItemFinder(threshold,set,frequentItem,singletons,depth)

    def findAssociationRules(self, set : np.matrix ,confidence : float ,interest:float) -> np.matrix:
        for kFrequent in self.itemFound[1:]: #no need to investigate singletons
            for j,subset in enumerate(set):
                if()


itemFinder = FrequentItem()
mySet = [[1],[3,1,2],[2,1],[1],[2,3,4],[1,4],[5,3],[1,2,3],[4,2],[1,2,3],[1,2]]
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