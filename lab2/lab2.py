import numpy as np
import csv
import hashlib as h
import mmap

class FrequentItem:

    def __init__(self) -> None:
        print("Frequent Item Finder")
    
    #set is a matrix not a list rework this function
    def findSingletons(self, set: list[any],threshorld: int) -> list[any]:
        uniqueItems = np.unique(set)
        items = []
        for i,item in enumerate(uniqueItems):
            idx = (set == item)
            if(np.sum(idx)/len(set)>threshorld):
                items.append(item)
        return items
    
    def buildCandidates(self, singletons: list[any], multiplons: np.matrix) -> list[any]:
        candidates = []
        for set in multiplons:
            for single in singletons:
                if(np.isin(single,set)):
                    print("do nothing")
                    print(f" set = {set}, single = {single}")
                else:
                    print(f" set = {set}, single = {single}, isList ? = {isinstance(set, list)}")

                    if isinstance(set, np.integer):
                        temp = [set, single]
                        temp.sort()
                        candidates.append(temp)
                    else:
                        temp = set
                        temp = np.hstack((temp,single))
                        temp.sort()
                        print(temp)
                        candidates.append(temp)
                
        return np.unique(candidates,axis=0)
    
    def frequentItemFinder(self,threshold:int,set:list[any],frequentItem : np.matrix, depth: int , singletons : list[any]):
        candidates = self.buildCandidates(singletons,frequentItem[depth])
        if(len(candidates)==0):
            return frequentItem
        else:
            for i,item in enumerate(candidates):
            idx = (set == item)
            if(np.sum(idx)/len(set)>threshorld):
                items.append(item)

itemFinder = FrequentItem()
mySet = [1,3,1,3,2,2,2,1,2,1,4,4,4,4,5,5,5,3,3]
myCharSet =['a','b','ab']
myFrequentItems =[]
singletons = itemFinder.findSingletons(mySet,0.1)
print(singletons)
candidates = itemFinder.buildCandidates(singletons,singletons)
print(f"candidates {candidates}")