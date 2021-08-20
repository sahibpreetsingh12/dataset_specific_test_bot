# Levenshtein distance https://www.youtube.com/watch?v=MiqoA-yF-0M

# or  https://medium.com/@ethannam/understanding-the-levenshtein-distance-equation-for-beginners-c4285a5604f0

# source http://norvig.com/spell-correct.html

# instead of big.txt we will will have a text file that contains all our glosaary

import re


from collections import Counter


master_dic_dataset_name = {
        'agricultural data' : 'agcensus_crop',
        'agricluture' : 'agcensus_crop', 
        'agri data' : 'agcensus_crop',
        'agricuture data':'agcensus_crop',
        'agriculture':'agcensus_crop',
        'agriculture census': 'agcensus_crop',
        'agcensus':'agcensus_crop',
        'rainfall':'rainfall',
        'rain data':'rainfall',
        'rainfall data':'rainfall',
        'agricultural census':'agcensus_crop',
        'rain figures':'rainfall',
        'sales of fertiliser':'fertiliser_sales',
        'sales of fertilisers':'fertiliser_sales',
        'fertiliser sales':'fertiliser_sales',
        'fertilizer sales data':'fertiliser_sales',
        'fertilizers sales data':'fertiliser_sales',
         'sales regarding fertlisers':'fertiliser_sales',
         'rbi_deposit':'rbi_deposit',
         'deposits of rbi':'rbi_deposit',
         'rbi-deposit':'rbi_deposit',
         'rbi deposit': 'rbi_deposit',
         'deposits by rbi':'rbi_deposit',
         'investments of rbi':'rbi_deposit',
         'investments by rbi':'rbi_deposit',
         'mnrega employment':'nrga_emp',
         'credit by bank':'rbi_credit',
         'Soil':'soil'
         ,'soil':'soil',
         'pmfby':'pmfby'
         }

template_names_variations =['granularity']
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(list(master_dic_dataset_name.keys()) + template_names_variations)

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    #Most probable spelling correction for word.

    # key : key function where the iterables are passed and comparsion is performed
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]

    # Deletes words one by one
    deletes    = [L + R[1:]               for L, R in splits if R]

    # transposes are done on first and second place
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))