import os
from collections import defaultdict
from itertools import combinations
class Apriori:
    def __init__(self, min_support, min_confidence):
        # Minimum support count required for an itemset to be considered frequent
        self.min_support = min_support
        # List to store all transactions (each transaction is a set of items)
        self.transactions = []
        self.frequent_itemsets = {} #storing all found itemsets with the format {itemset_tuple: support_count}
        # Minimum confidence required for an association rule to be considered valid
        self.min_confidence = min_confidence
        #storing generated association rules 
        self.rules =[] # Format [(sub_set, res, confidence), ...] e.g: {704} -> {825}, Confidence = 0.6143

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
        """Filters the candidate itemsets based on the minimum support count."""
        return {itemset: count for itemset, count in itemset_support.items() if count >= self.min_support}

    def find_frequent_itemsets(self):
        """Main Apriori algorithm."""
        print(f"Running Apriori with min_support = {self.min_support}")
        # Single-item candidates
        items = {item for t in self.transactions for item in t}
        # (C1)
        current_itemsets = [tuple([item]) for item in sorted(items)]
        k = 1

        while current_itemsets:
            #1. (Ck)
            support_counts = self.get_itemset_support(current_itemsets)
            #2. Filtering : (Lk)
            frequent_itemsets_k = self.filter_itemsets_by_support(support_counts)
            print(f"Found {len(frequent_itemsets_k)} frequent itemsets of size {k}")
            # 3. Storing the frequent itemsets
            self.frequent_itemsets.update(frequent_itemsets_k)

            # next iteration (k+1)
            k += 1
            # 4. Generate candidates for the next size (Ck+1)
            current_itemsets = self.generate_candidates(frequent_itemsets_k, k-1)

            if k > 2 and current_itemsets:
                self.transactions = [t for t in self.transactions if any(set(c) <= t for c in current_itemsets)]
    def write_results_to_file(self, output_file_path, rule_count):
        """Writes frequent itemsets (with support) and association rules to a file."""
        print(f"\nWriting results to {output_file_path}")
        
        # Grouping frequent itemsets by size (k)
        itemsets_by_k = defaultdict(list)
        for itemset, support in self.frequent_itemsets.items():
            itemsets_by_k[len(itemset)].append((itemset, support))

        with open(output_file_path, 'w') as f:
            f.write("Frequent Itemsets (by size k)\n\n")

            # Write Frequent Itemsets
            sorted_ks = sorted(itemsets_by_k.keys())
            for k in sorted_ks:
                f.write(f"--- k = {k} ---\n")
                sorted_itemsets = sorted(itemsets_by_k[k], key=lambda x: x[0])
                for itemset, support in sorted_itemsets:
                    itemset_str = "{" + ", ".join(itemset) + "}"
                    f.write(f"{itemset_str}: Support Count = {support}\n")
                f.write("\n")

            f.write("=====================================\n\n")
            f.write("=== Association Rules ===\n\n")

            # Writing Association Rules
            f.write(f"Total rules generated (Confidence >= {self.min_confidence}): {rule_count}\n\n")
            if not self.rules:
                f.write("No association rules found that satisfy min_confidence.\n")
            else:
                # Iterate through stored rules (antecedent, consequent, confidence)
                for antecedent, consequent, confidence in self.rules:
                    ante_str = "{" + ", ".join(sorted(list(antecedent))) + "}"
                    cons_str = "{" + ", ".join(sorted(list(consequent))) + "}"
                    f.write(f"{ante_str} -> {cons_str}\n")
            
            f.write("\n=========================\n")
        print("Results successfully written to file.")
    
    def generate_rules(self):
        cmp = 0 # Counter for rules generated
        for itemset in self.frequent_itemsets:
            if len(itemset)<2:
                continue #rule made of 2 items at least
            # Generate all non-empty proper subsets of the current itemset
            subsets = [set(x) for i in range(1, len(itemset)) for x in combinations(itemset, i)]
            for sub in subsets:
                # Consequent is the rest of the itemset
                res = set(itemset) - sub
                if not res:
                    continue
                support_itemset = self.frequent_itemsets[itemset]
                # Look up support for the antecedent (sub). 0 if not found.
                support_sub = self.frequent_itemsets.get(tuple(sorted(sub)), 0)#because sub is a set and the keys of the dictionary are tuples e.g ('32',)
                if support_sub == 0:
                    continue
                confidence = support_itemset / support_sub

                if confidence >= self.min_confidence:
                    self.rules.append((sub,res, confidence)) #each rule is a tuple + its associated confidence
                    cmp +=1
        return cmp



    


# ------------------Prog principal------------------

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'T10I4D100K.dat')
    # Defining the output file path
    output_file_path = os.path.join(current_dir, 'apriori_results.txt')

    #algorithm parameters
    min_support = 800
    min_confidence = 0.5
    # Initializing and running Apriori
    apriori = Apriori(min_support,min_confidence)
    apriori.load_transactions(file_path)
    apriori.find_frequent_itemsets()
    # Generate rules and capture the count
    rule_count = apriori.generate_rules()
    print("\nFrequent Itemsets:")
    for itemset, support in apriori.frequent_itemsets.items():
        print(f"{itemset}: {support}")

    print("\nGenerating associated rules to the frequent Itemsets found:")
    for antecedent, consequent, confidence in apriori.rules:
        print(f"{antecedent} -> {consequent}")

    #  saving results to a file
    apriori.write_results_to_file(output_file_path,rule_count)


if __name__ == "__main__":
    main()
