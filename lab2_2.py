# import numpy as np
# from collections import Counter

# class A_priori():
#     def __init__(self,s:int):
#         self.s = s
#         self.transactions =[]

# #storing the data as a list of lists 
#     def transactions_table(self,file):
#         transactions =[]
#         with open(file, "r") as f:
#             for line in f:
#                 items = list(map(int,line.strip().split()))
#                 transactions.append(items)
#         self.transactions = transactions
#         return transactions
#     #returns a dictionary {item: count}
#     def first_scan(self,transactions):  
#         single_items = [item for transaction in transactions for item in transaction]
#         L_1 ={}
#         #---- First Scan -----
#         C_1 = Counter(single_items)  #we've counted the occurences of all elements in all transactions
#         L_1 = {item:count for item,count in C_1.items()if count>=self.s}
#         return L_1
        

#     # def generate_candidates(self,prev_items,k): #prev_items is a list of items size k-1
#     #     #k = 2
#     #     candidates = []
#     #     for i in range(len(prev_items)):
#     #         for j in range(i+1,len(prev_items)):
#     #             item1 = prev_items[i]
#     #             item2 = prev_items[j]
#     #             candidate = list(set(item1) | set(item2))

#     #             if len(candidate) == k:
#     #                 candidates.append(tuple(sorted(candidate)))
#     #     return list(set(candidates))


# ##testing with 2-items
# # a_priori = A_priori(s=3)
# # transactions = a_priori.transactions_table("lab2/transactions.txt")
# # L_1 = a_priori.first_scan(transactions)
# # print("Frequent 1-itemsets:", L_1)

# # prev_items =[(item,)for item in L_1.keys()]
# # C2 = a_priori.generate_candidates(prev_items, 2)
# # print("Candidate 2-itemsets:", C2)

#     def generate_candidates(self,prev_items,transactions):
#         transactions = [set(t) for t in transactions]  

#         k =2
#         prev_items =[(item,)for item in prev_items.keys()]
#         final_frequent ={} #all frequents
#         while prev_items:
#             candidates =[]
#             for i in range(len(prev_items)):
#                 for j in range(i+1,len(prev_items)):
#                     item1 = prev_items[i]
#                     item2 = prev_items[j]
#                     candidate = list(set(item1) | set(item2))
#                     #candidate = frozenset(set(item1) | set(item2))

#                     if len(candidate) == k:
#                         candidates.append(tuple(sorted(candidate)))
#            # print(f"Candidate {k}-itemsets:", candidates)
#             candidates = list(set(candidates))
#             if not candidates:
#                 break
#             frequent_candidates ={}   #frequent only from the current iteration
#             for cand in candidates:
#                 count = sum(1 for t in transactions if set(cand).issubset(t))
#                 if count >= self.s:
#                     frequent_candidates[cand] = count
            
#             if not frequent_candidates:
#                 break
#             print(f"Frequent {k}-itemsets:", frequent_candidates)

#             final_frequent.update(frequent_candidates)
#             # moving to the next iteration/ k+1 itemsets
#             prev_items = list(frequent_candidates.keys())
#             k += 1
#         return final_frequent

# a_priori = A_priori(s=1000)
# transactions = a_priori.transactions_table("lab2\T10I4D100K.dat")
# L_1 = a_priori.first_scan(transactions)
# print("Frequent 1-itemsets:", L_1)

# #prev_items =[(item,)for item in L_1.keys()]
# final_candidates = a_priori.generate_candidates(L_1 , transactions)



import os
from collections import defaultdict

class Apriori:
    def __init__(self, min_support):
        self.min_support = min_support
        self.transactions = []
        self.frequent_itemsets = {}

    def load_transactions(self, file_path):
        """Read dataset and store as list of sets."""
        with open(file_path, 'r') as f:
            self.transactions = [set(line.strip().split()) for line in f]
        print(f"Loaded {len(self.transactions)} transactions.")

    def get_itemset_support(self, itemsets):
        """returns how many transactions contain each itemset """
        support_counts = defaultdict(int)
        for t in self.transactions:
            for itemset in itemsets:
                if set(itemset) <= t:  # itemset is subset of transaction
                    support_counts[itemset] += 1
        return support_counts

    def generate_candidates(self, frequent_itemsets, k):
        """Generate candidate itemsets of size k+1 from previous itemsets"""
        candidates = set()
        frequent_list = list(frequent_itemsets.keys())
        for i in range(len(frequent_list)):
            for j in range(i+1, len(frequent_list)):
                itemset1, itemset2 = frequent_list[i], frequent_list[j]
                if itemset1[:k-1] == itemset2[:k-1]:
                    candidate = tuple(sorted(set(itemset1) | set(itemset2)))
                    candidates.add(candidate)
        return list(candidates)

    def filter_itemsets_by_support(self, itemset_support):
        return {itemset: count for itemset, count in itemset_support.items() if count >= self.min_support}

    def find_frequent_itemsets(self):
        """Main Apriori algorithm."""
        print(f"Running Apriori with min_support = {self.min_support}")
        # Single-item candidates
        items = {item for t in self.transactions for item in t}
        current_itemsets = [tuple([item]) for item in sorted(items)]
        k = 1

        while current_itemsets:
            support_counts = self.get_itemset_support(current_itemsets)
            frequent_itemsets_k = self.filter_itemsets_by_support(support_counts)
            print(f"Found {len(frequent_itemsets_k)} frequent itemsets of size {k}")
            self.frequent_itemsets.update(frequent_itemsets_k)

            k += 1
            current_itemsets = self.generate_candidates(frequent_itemsets_k, k-1)

            if k > 2 and current_itemsets:
                self.transactions = [t for t in self.transactions if any(set(c) <= t for c in current_itemsets)]

    


# ------------------Prog principal------------------

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'T10I4D100K.dat')

    min_support = 1000
    apriori = Apriori(min_support)
    apriori.load_transactions(file_path)
    apriori.find_frequent_itemsets()

    print("\nFrequent Itemsets:")
    for itemset, support in apriori.frequent_itemsets.items():
        print(f"{itemset}: {support}")


if __name__ == "__main__":
    main()
