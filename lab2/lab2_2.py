import numpy as np
from collections import Counter

class A_priori():
    def __init__(self,s:int):
        self.s = s
        self.transactions =[]

    def transactions_table(self,file):
        transactions =[]
        with open(file, "r") as f:
            for line in f:
                items = list(map(int,line.strip().split()))
                transactions.append(items)
        self.transactions = transactions
        return transactions
    
    def first_scan(self,transactions):  
        single_items = [item for transaction in transactions for item in transaction]
        L_1 ={}
        #---- First Scan -----
        C_1 = Counter(single_items)  #we've counted the occurences of all elements in all transactions
        # L_1 = C_1.copy()
        # for key in C_1.keys():
        #     if C_1[key] <s:
        #         del C_1[key]
        L_1 = {item:count for item,count in C_1.items()if count>=self.s}
        return L_1
        

    # def generate_candidates(self,prev_items,k): #prev_items is a list of items size k-1
    #     #k = 2
    #     candidates = []
    #     for i in range(len(prev_items)):
    #         for j in range(i+1,len(prev_items)):
    #             item1 = prev_items[i]
    #             item2 = prev_items[j]
    #             candidate = list(set(item1) | set(item2))

    #             if len(candidate) == k:
    #                 candidates.append(tuple(sorted(candidate)))
    #     return list(set(candidates))


##testing with 2-items
# a_priori = A_priori(s=3)
# transactions = a_priori.transactions_table("lab2/transactions.txt")
# L_1 = a_priori.first_scan(transactions)
# print("Frequent 1-itemsets:", L_1)

# prev_items =[(item,)for item in L_1.keys()]
# C2 = a_priori.generate_candidates(prev_items, 2)
# print("Candidate 2-itemsets:", C2)

    def generate_candidates(self,prev_items,transactions):
        k =2
        prev_items =[(item,)for item in prev_items.keys()]
        final_frequent ={} #all frequents
        while prev_items:
            candidates =[]
            for i in range(len(prev_items)):
                for j in range(i+1,len(prev_items)):
                    item1 = prev_items[i]
                    item2 = prev_items[j]
                    candidate = list(set(item1) | set(item2))

                    if len(candidate) == k:
                        candidates.append(tuple(sorted(candidate)))
           # print(f"Candidate {k}-itemsets:", candidates)
            candidates = list(set(candidates))
            if not candidates:
                break
            frequent_candidates ={}   #frequent only from the current iteration
            for cand in candidates:
                count = sum(1 for t in transactions if set(cand).issubset(t))
                if count >= self.s:
                    frequent_candidates[cand] = count
            
            if not frequent_candidates:
                break
            print(f"Frequent {k}-itemsets:", frequent_candidates)

            final_frequent.update(frequent_candidates)
            # moving to the next iteration/ k+1 itemsets
            prev_items = list(frequent_candidates.keys())
            k += 1
        return final_frequent

a_priori = A_priori(s=2)
transactions = a_priori.transactions_table("lab2/transactions.txt")
L_1 = a_priori.first_scan(transactions)
print("Frequent 1-itemsets:", L_1)

#prev_items =[(item,)for item in L_1.keys()]
final_candidates = a_priori.generate_candidates(L_1 , transactions)



