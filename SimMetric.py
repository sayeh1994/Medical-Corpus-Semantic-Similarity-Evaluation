from SimilarityScorev2 import similarity_score
import numpy as np

def find_similar_entities(list1, list2):
    similar_strings = []
    list1_copy = list1.copy()  # Create a copy of list1 to avoid modifying it directly
    for string in list1:
        if string in list2:
            similar_strings.append(string)
            list1_copy.remove(string)
            list2.remove(string)
    return similar_strings, list1_copy, list2

def sim_metric(ref, gen):
    if len(ref)==0 or len(gen)==0:
        return 0
    else:
        similar, ref_remain, gen_remain = find_similar_entities(ref, gen)
        # sim_score = similarity_score(ref,gen)
        sim_score = similarity_score(ref_remain, gen_remain)
        # print(sim_score)
        return (len(similar)+np.sum(sim_score))/(len(similar)+len(sim_score))