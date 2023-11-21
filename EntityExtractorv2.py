import spacy
import re
# from Bio_Epidemiology_NER.bio_recognizer import ner_prediction
import nltk

nlp = spacy.load("en_core_sci_md")
nlp2 = spacy.load("en_core_web_sm")

def check_word_in_sentence(word_list, sentence):
    words = nltk.tokenize.word_tokenize(sentence.lower())
    neg = []
    for word in word_list:
        if word in words:
            neg.append(word)
    return neg

def remove_special_characters(string):
    # Define the regular expression pattern
    pattern = r"[^a-zA-Z\s.!?]+"
    
    # Remove special characters except end-of-sentence characters
    try:
        cleaned_string = re.sub(pattern, "", string)
        return cleaned_string
    except:
        pass

def check_negation(sentence, entity, negations):
    tokens = sentence.split()  # Tokenize the sentence
    try:
        entity_index = tokens.index(entity)  # Find the index of the entity
    except:
        return False
    
    for i in range(1, 4):  # Search one, two, and three words behind the entity
        if entity_index - i >= 0 and tokens[entity_index - i] in negations:
            return True
    
    return False

def clean_text(text):
    # text = re.sub(r'[^\w\s]', '', text)
    text = remove_special_characters(text)
    text = text.replace('\n','')
    return text.lower()

def extract_medical_terms(text):
    # Load the spaCy English model
    # nlp = spacy.load("en_core_sci_md")
    
    # text = clean_text(text)

    # Process the text with spaCy
    doc = nlp(text)

    # Extract medical terms from the text
    labels = ["ENTITY"] 
    medical_terms = []
    for ent in doc.ents:
        if ent.label_ in labels:
            medical_terms.append(ent.text)
    
    return medical_terms

def add_negations(medical_terms, text):
    # list of negation words
    negations = ['not', 'never', 'no', 'neither', 'none', 'nobody', 'nowhere', 'nothing', 'without', "don't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't", "shouldn't", "wouldn't", "couldn't", "doesn't", "didn't", "may not", "might not", "need not", "mustn't", "shall not", "will not", "ought not to", "nevermore", "rarely", "scarcely"]
    # negations = ['not', 'never', 'no']
    # iterate over sentences in the report
    sentences = re.split('[.?!]', text.lower())
    for sentence in sentences:
        # check if any negation word is present in the sentence
        neg = check_word_in_sentence(negations, sentence)
        if neg:
            # check if any medical term is present in the same sentence
            for i, term in enumerate(medical_terms):
                if term in sentence:
                    if check_negation(sentence, term.split()[0], negations):
                        # replace the medical term with negation + medical term
                        # neg_term = 'no ' + term
                        neg_term = neg[0] + ' ' + term
                        medical_terms[medical_terms.index(term)] = neg_term
                        if i+1<len(medical_terms):
                            if (' or ' and medical_terms[i+1] in sentence):
                                neg_term = neg[0] + ' ' + medical_terms[i+1]
                                medical_terms[medical_terms.index(medical_terms[i+1])] = neg_term
    
    return medical_terms

def remove_single_adj(medical_terms):
    # nlp = spacy.load("en_core_web_sm")
    for term in medical_terms:
        # Last Check if the term is an single adjective
        idoc = nlp2(term.lower())
        if len(idoc) == 1 and idoc[0].pos_ == "ADJ" :
            medical_terms.remove(term)
        elif len(idoc) == 2 and idoc[0].pos_ == "DET" and idoc[1].pos_ == "ADJ":
            medical_terms.remove(term)
    return medical_terms

def extract_associated_adjectives(text, medical_terms):
    # parse report text with spaCy
    # nlp2 = spacy.load("en_core_web_sm")
    doc = nlp2(text)
    
    assoc_adjs = {}

    for sent in doc.sents:
        # extract adjectives and medical terms in sentence
        tokens = [token for token in sent]
        adjs = [tokens[i-1].text for i in range(1, len(tokens)) if tokens[i].pos_ == 'ADJ']

        # check if any medical term is present in sentence
        for term in medical_terms:
            # check if any associated adjective is present in sentence
            assoc_adjs[term] = [adj.lower() for adj in adjs if adj + ' ' + term in sent.text]
    return assoc_adjs

def replace_medical_terms(medical_terms, assoc_adjs):
    
    for i, term in enumerate(medical_terms):
        if term in assoc_adjs:
            adj = assoc_adjs[term]
            if adj:
                medical_terms[i] = " ".join(adj) + ' ' + term
    return medical_terms

def medical_term(reftext):
    reftext = clean_text(reftext)
    medical_terms = extract_medical_terms(reftext)
    # print("1.\n", medical_terms)
    medical_terms = remove_single_adj(medical_terms)
    # print("single adj\n", medical_terms)
    assoc_adjs = extract_associated_adjectives(reftext, medical_terms)
    medical_terms = replace_medical_terms(medical_terms, assoc_adjs)
    # print("replace\n", medical_terms)
    medical_terms = add_negations(medical_terms, reftext)
    # print("negation\n", medical_terms)
    return medical_terms
