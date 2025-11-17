import os
from collections import defaultdict
from itertools import combinations
class Apriori:
    def __init__(self, min_support, min_confidence):
        self.min_support = min_support
        self.transactions = []
        self.frequent_itemsets = {}
        self.min_confidence = min_confidence
        self.rules =[]

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

    
    def generate_rules(self):
        #rules = []
        for itemset in self.frequent_itemsets:
            if len(itemset)<2:
                continue #rule made of 2 items at least
            subsets = [set(x) for i in range(1, len(itemset)) for x in combinations(itemset, i)]
            for sub in subsets:
                res = set(itemset) - sub
                if not res:
                    continue
                
                support_itemset = self.frequent_itemsets[itemset]
                #support_sub = frequent_itemsets[tuple(sorted(sub))]
                support_sub = self.frequent_itemsets.get(tuple(sorted(sub)), 0)#because sub is a set and the keys of the dictionary are tuples e.g ('32',)
                if support_sub == 0:
                    continue
                confidence = support_itemset / support_sub

                if confidence >= self.min_confidence:
                    self.rules.append((sub,res, confidence)) #each rule is a tuple + its associated confidence
        #return rules




    


# ------------------Prog principal------------------

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'T10I4D100K.dat')

    min_support = 1000
    min_confidence = 0.7
    apriori = Apriori(min_support,min_confidence)
    apriori.load_transactions(file_path)
    apriori.find_frequent_itemsets()

    print("\nFrequent Itemsets:")
    for itemset, support in apriori.frequent_itemsets.items():
        print(f"{itemset}: {support}")

    print("\nGenerating associated rules to the frequent Itemsets found:")
    apriori.generate_rules()
    for antecedent, consequent, confidence in apriori.rules:
        print(f"{antecedent} -> {consequent}, confidence = {confidence:.2f}")


if __name__ == "__main__":
    main()
