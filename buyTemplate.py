# -*- coding: utf-8 -*-
"""
Filename: buyTemplate.py
Authors: Nidhin Anisham, Divya Machenahalli Lokesh

Use command "python buyTemplate.py" to run
 
This program does the following: 
 1. Creates a SpaCy NLP pipeline on the input 'filename'
 2. Extracts (buyer,item,quantity,price,source)
 3. Outputs a dictionary of filled templates
 
"""

import spacy
import neuralcoref

nlp = spacy.load("en_core_web_sm")
neuralcoref.add_to_pipe(nlp)
buy = ['buy','acquire','purchase','acquisition']

def getTemplate(doc):    
    passive = False
    x = ''
    y = ''
    s = True
    o = True
    fo = True
    fr = True
    reachedRoot = False
    for tok in doc:
        if tok.lemma_ in buy:
            reachedRoot = True
        elif tok.text == 'for' and fo:
            forToken = tok
            fo = False
        elif tok.text == 'from' and fr:
            fromToken = tok
            fr = False
        elif tok.dep_.endswith("subj") and s:
            x = tok
            s = False
        elif tok.dep_.endswith("subjpass") and o:
            y = tok
            passive = True
            o = False
        elif tok.dep_.endswith("obj") and passive and s and reachedRoot:
            x = tok
            s = False
        elif tok.dep_.endswith("obj") and not passive and o and reachedRoot:
            y = tok
            o = False
    
    template = {"buyer":'',"item":[],"quantity":'',"price":'',"source":''}
    
    if not s:
        template["buyer"] = x.text
        tempBuyer = ""        
        for child in x.children:
            if child.dep_.endswith("compound"):
                tempBuyer += child.text+" "
        template["buyer"] = tempBuyer + template["buyer"]
    
    while(not o):
        o = True
        conj = y
        item = conj.text
        template["quantity"] = ''
        tempItem = ""
        for child in conj.children:
            if child.dep_.endswith("compound"):
                tempItem += child.text+" "
            elif child.dep_.endswith("nummod"):
                template["quantity"] = child.text
            elif child.dep_.endswith("conj"):
                y = child
                o = False
        item = tempItem + item
        template["item"].append(item)
    
    if not fo:
        for child in forToken.children:
            if child.dep_.endswith("pobj"):
                template["price"] = child.text
                price = child
                break
        if len(template["price"])>0 :
            tempPrice = ''
            for child in price.children:
                if child.dep_.endswith("quantmod") or child.dep_.endswith("compound"):
                    tempPrice += child.text + " "
            template["price"] = tempPrice + template["price"]
        
    if not fr:
        for child in fromToken.children:
            if child.dep_.endswith("pobj"):
                template["source"] = child.text
                source = child
                break
        if len(template["source"])>0:
            tempSource = ""
            for child in source.children:
                if child.dep_.endswith("compound"):
                    tempSource += child.text+ " "
            template["source"] = tempSource + template["source"]
            
    return template,passive

def getNER(doc1,doc2,passive):
    template = {"buyer":'',"item":[],"quantity":'',"price":'',"source":''}
    doc = nlp(doc1+ " "+ doc2)
    ner = (dict([(str(x), x.label_) for x in doc.ents])) 

    if passive:
        for key,value in ner.items():
            if value == 'ORG' or value == 'PRODUCT' and key in doc1:
                template["item"] = key.split(",")
            elif value == 'QUANTITY' or value == 'CARDINAL':
                template["quantity"] = key
            elif value == 'MONEY' and key in doc1:
                template["price"] = key
            elif value == 'ORG' or value == 'PRODUCT' or value == 'PERSON' and template["buyer"]=='' and key in doc2:
                template["buyer"] = key
            elif value == 'MONEY' and template["price"]=='':
                template["price"] = key
    
    else: 
        for key,value in ner.items():
            
            if (value == 'ORG' or value == 'PRODUCT') and key in doc2 and len(template["item"])==0:
                template["item"] = key.split(",")
            
            elif value == 'QUANTITY':
                template["quantity"] = key
            
            elif value == 'CARDINAL':
                item = template["quantity"]
                if item in ner and ner[item]!='QUANTITY':
                    template["quantity"] = key
            
            elif value == 'MONEY' and key in doc2:
                template["price"] = key
            
            elif (value == 'ORG') and key in doc1:
                template["buyer"] = key
            
            elif (value == 'PERSON') and key in doc1:
                item = template["buyer"]
                if item in ner and ner[item]!='ORG':
                    template["buyer"] = key
            
            elif (value == 'PRODUCT') and key in doc1:
                item = template["buyer"]
                if (item in ner) and (ner[item] not in ['ORG','PERSON']):
                    template["buyer"] = key
                
            elif value == 'MONEY' and template["price"]=='':
                template["price"] = key

    return template

def getFinalTemplate(dep,ner):
    template = {"buyer":'',"item":[],"quantity":'',"price":'',"source":''}
    if(dep["buyer"] == ''):
        template["buyer"] = ner["buyer"]
    else:
        template["buyer"] = dep["buyer"]
    
    if(len(dep["item"]) == 0):
        template["item"] = ner["item"]
    else:
        if(template["buyer"] in dep["item"]):
            template["item"] = ner["item"]
        else:
            template["item"] = dep["item"]
    
    if(dep["quantity"] == ''):
        template["quantity"] = ner["quantity"]
    else:
        template["quantity"] = dep["quantity"]
        
    if(dep["price"] == ''):
        template["price"] = ner["price"]
    else:
        template["price"] = dep["price"]
        
    template["source"] = dep["source"]
    
    
    templates = []
    if len(template["item"]) == 0:
        template["item"] =''
        templates.append(template)
    else:
        for i in range(len(template["item"])):
            templates.append({"buyer":template["buyer"],
                             "item":template["item"][i],
                             "quantity":template["quantity"],
                             "price":template["price"],
                             "source":template["source"]})   
    return templates

def getBuy(filename):
        
    with open(filename, 'r', encoding='utf-8') as file:
        datalines = file.readlines()
    
    clean_lines = []
    for line in datalines:
        line = line.strip()
        if(len(line)>0):
            clean_lines.append(line)
      
    template_data = []
    for line in clean_lines:
        sentences = nlp(line)
        paragraph = []
        for sent in sentences.sents:
            paragraph.append(sent.text)
            
        article = nlp(sentences._.coref_resolved)
        for s in article.sents:
            sent_split = []
            temp = ""
            for word in s:
                if word.lemma_ in buy:
                    sent_split.append(temp)
                    temp = word.text + " "
                else:
                    temp += word.text+" "
            sent_split.append(temp)
            
            if(len(sent_split)>1):
                for i in range(1,len(sent_split)):
                    templateDEP,passive = getTemplate(nlp(sent_split[0]+" "+sent_split[i]))
                    templateNER = getNER(sent_split[0],sent_split[i],passive)
                    template = getFinalTemplate(templateDEP,templateNER)
                    for j in template:
                        temp = {"template":"BUY",
                                "sentences":paragraph,
                                "arguments": {
                                    "1" : j["buyer"],
                                    "2" : j["item"],
                                    "3" : j["price"],
                                    "4" : j["quantity"],
                                    "5" : j["source"]
                                    }
                                }
                        template_data.append(temp)
    
    return template_data