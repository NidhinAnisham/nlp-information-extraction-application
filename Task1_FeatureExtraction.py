# -*- coding: utf-8 -*-
"""
Filename: Task1_FeatureExtraction.py
Authors: Nidhin Anisham, Divya Machenahalli Lokesh

Use command "python Task1_FeatureExtraction.py" to run
 
This program does the following: 
 1. Creates a SpaCy NLP pipeline on the input 'filename'
 2. Splits Sentences, Tokenizes, Lemmatizes, POS Tags,creates dependency trees and gets synsets of the word.
 3. The output is stored in the 'features' folder
 
"""

import spacy
import os 
from nltk.corpus import wordnet as wn

nlp = spacy.load("en_core_web_sm")

def getRelations(word):
    relations = {'hypernym':'','hyponym':'','meronym':'','holonym':''}
    for ss in wn.synsets(word):
        
        for hyper in ss.hypernyms():
            for lemma in hyper.lemma_names():
                relations['hypernym'] += lemma + ','
        
        for hypo in ss.hyponyms():
            for lemma in hypo.lemma_names():
                relations['hyponym'] += lemma + ','
        
        for mero in ss.part_meronyms():
            for lemma in mero.lemma_names():
                relations['meronym'] += lemma + ','
                
        for holo in ss.part_holonyms():
            for lemma in holo.lemma_names():
                relations['holonym'] += lemma + ','
                
    return relations
    

if __name__ == "__main__":
        
    filename = input("Enter document name: ")   
    
    print("Running...")
    if not os.path.exists(filename):
        print("File does not exist")
    else:
        with open(filename, 'r', encoding='utf-8') as f:
            datalines = f.readlines()
        
        clean_lines = ""
        for line in datalines:
            line = line.strip()
            clean_lines += line+"\n"
        
        article = nlp(clean_lines)
        sentences = []
        words = []
        lemmas = []
        posTags = []  
        dependency = []
        synset = []
        
        for sentence in article.sents:
            
            tokens = []
            pos = ""
            lemma = ""
            parse = {}
            syn = {}
            for word in sentence:
                tokens.append(word.text)
                lemma += word.text+"_"+word.lemma_+" "
                pos += word.text+"_"+word.pos_+" "
                parse[word.text] = {"dependency":word.dep_,
                                    "head_pos":word.head.text+"_"+word.head.pos_,
                                    "children":[[child.text,child.dep_] for child in word.children]}
                syn[word.text] = getRelations(word.text) 
            
            sentences.append(sentence.text)
            words.append(tokens)
            lemmas.append(lemma)
            posTags.append(pos)
            dependency.append(parse)
            synset.append(syn)
        
        if not os.path.exists('features'):
            os.mkdir('features')
            
        with open('features/sentences.txt', 'w', encoding='utf-8') as f:
            f.writelines("%s\n" % i for i in sentences)
        
        with open('features/tokenized.txt', 'w', encoding='utf-8') as f:
            f.writelines("%s\n" % i for i in words)
        
        with open('features/lemmatized.txt', 'w', encoding='utf-8') as f:
            f.writelines("%s\n" % i for i in lemmas)
        
        with open('features/pos_tagged.txt', 'w', encoding='utf-8') as f:
            f.writelines("%s\n" % i for i in posTags)
        
        with open('features/dependencies.txt', 'w', encoding='utf-8') as f:
            f.writelines("%s\n" % i for i in dependency)
        
        with open('features/relations.txt', 'w', encoding='utf-8') as f:
            f.writelines("%s\n" % i for i in synset)
        
        print("NLP Pipeline run. Results in 'features' folder.")
        