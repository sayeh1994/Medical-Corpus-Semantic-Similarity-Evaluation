import spacy
import numpy as np
nlp = spacy.load("en_core_web_md")
# nlp = spacy.load("en_ner_bionlp13cg_md")

def check_negation(entity):
    negations = ['not', 'never', 'no', 'neither', 'none', 'nobody', 'nowhere', 'nothing', 'without', "don't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't", "shouldn't", "wouldn't", "couldn't", "doesn't", "didn't", "may not", "might not", "need not", "mustn't", "shall not", "will not", "ought not to", "nevermore", "rarely", "scarcely"]
    for neg in negations:
        if neg in entity:
            return True
    return False

def sim_score(ref,gen):
    a = nlp(ref).similarity(nlp(gen))
    weight = 0.5
    if check_negation(ref) ^ check_negation(gen): #if one of them hase negation in text
        return a*weight
    else:
        return a

def calculate_ratio(table):
    ratios = []
    maximum = []
    for column in table.T:  # Iterate over the columns of the table
        max_value = np.max(column)
        average_value = np.mean(column)
        if max_value + average_value != 0:
            ratio = max_value / (max_value + average_value)
        else:
            ratio=0
        ratios.append(ratio)
        
    return ratios
 
def similarity_score(ref_term, gen_term):
    # Calculate the similarity scores between each pair of terms
    similarity_scores = [[sim_score(ref, gen) for gen in gen_term] for ref in ref_term]
    # print(similarity_scores)
    ratio = calculate_ratio(np.array(similarity_scores))

    # Determine the length of the longest term in each list
    # avg_score = sum(sum(similarity_scores, [])) / (len(ref_term) * len(gen_term))
    return ratio