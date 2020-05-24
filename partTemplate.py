# -*- coding: utf-8 -*-
"""
Filename: partTemplate.py
Authors: Nidhin Anisham, Divya Machenahalli Lokesh

Use command "python partTemplate.py" to run
 
This program does the following: 
 1. Creates a SpaCy NLP pipeline on the input 'filename'
 2. Extracts (location,location)
 3. Outputs a dictionary of filled templates
 
"""


import spacy

import numpy as np
import neuralcoref

nlp = spacy.load("en_core_web_sm")
neuralcoref.add_to_pipe(nlp)

def get_part_data(article):
    part_data=[]
   
    for s in article.sents:
       doc=nlp(str(s))
       count=0
       for ent in doc.ents:
           if ent.label_=='GPE':
               count+=1
           if count>=2:
               part_data.append(str(s))
               break
    return part_data


def get_part_template(part_data,paragraph):
    part_template=[]
    for part in part_data:
        each_template={}
        doc=nlp(part)
        location=[]
        each_loc_value=[]
        part1=[]
        part2=[]
        ep={}
        flag=0
        for ent in doc.ents:
            if ent.label_=='GPE':
                location.append(ent.text)
                t=ent.text.split(" ")
                each_loc_value=np.hstack((each_loc_value,t))
        #print(len(each_loc_value))
        for tok in doc:
            if tok.dep_=='pobj' and tok.text in location:
                part1=[]
                part2=[]
                flag=0
                p2=''
                part1.append(tok.text)
                child_dep={}
                child_dep={child:child.dep_ for child in tok.children}
                for key,values in child_dep.items():
                    if values=='appos' or  key.text in each_loc_value:
                        part2_child={}
                        p2=''
                        part2_child={c.text:c.dep_ for c in key.children}
                        for k,v in part2_child.items():
                            if v=='compound' or v=='det':
                                p2+=k+' '
                        p2+=key.text
                        if p2 in location :
                            part2.append(p2)
                    elif values=='conj' and key.text in location:
                        part1.append(key.text)
                    if part2:
                        flag=1
                        for i in part1:
                            each_template={}
                            ep={}
                            each_template['template']='PART'
                            each_template['sentence']=paragraph
                            ep["1"]=i
                            ep["2"]=part2[0]
                            each_template['arguments']=ep
                            part_template.append(each_template)
                        part2=[]
                        part1=[]
                if flag==0 and part1:
                    if tok.head.text.lower()=='of':
                        child_dep={}
                        p2=''
                        child_dep={child:child.dep_ for child in tok.head.children}
                        for k,v in child_dep.items():
                            if v=='compound' or v=='det':
                                p2+=k.text+' '
                        p2+=tok.head.text
                        if p2 in location:
                            part2.append(p2)
                    if part2:
                        flag=1
                        for i in part1:
                            each_template={}
                            ep={}
                            each_template['template']='PART'
                            each_template['sentence']=paragraph
                            ep["1"]=i
                            ep["2"]=part2[0]
                            each_template['arguments']=ep
                            part_template.append(each_template)
                        part2=[]
                        part1=[]
                    
            elif tok.dep_=='pobj' and tok.text in each_loc_value:
                  p1=' '
                  child_dep={}
                  part1=[]
                  part2=[]
                  flag=0
                  p2=''
                  child_dep={child:child.dep_ for child in tok.children}
                  for key,values in child_dep.items():
                      if values=='compound' or values=='det':
                          p1+=key.text+' '
                  p1+=tok.text
                  part1.append(p1)
                  for key,values in child_dep.items():
                      if values=='conj' and key.text in location:
                            part1.append(key.text)
                  
                      elif values=='appos' or  key.text in each_loc_value:
                            part2_child={}
                            p2=''
                            part2_child={c.text:c.dep_ for c in key.children}
                            for k,v in part2_child.items():
                                if v=='compound' or k in each_loc_value:
                                    p2+=k+' '
                            p2+=key.text
                            if p2 in location:
                                part2.append(p2)
                            
                  if part2:
                      flag=1
                      for i in part1:
                          each_template={}
                          ep={}
                          each_template['template']='PART'
                          each_template['sentence']=paragraph
                          ep["1"]=i
                          ep["2"]=part2[0]
                          each_template['arguments']=ep
                          part_template.append(each_template)
                      part2=[]
                      part1=[]
                  if flag==0 and part1:
                    if tok.head.text.lower()=='of':
                        child_dep={}
                        p2=''
                        child_dep={child:child.dep_ for child in tok.head.children}
                        for k,v in child_dep.items():
                            if v=='compound' or v=='det':
                                p2+=k.text+' '
                        p2+=tok.head.text
                        if p2 in location:
                            part2.append(p2)
                    if part2:
                        flag=1
                        for i in part1:
                            each_template={}
                            ep={}
                            each_template['template']='PART'
                            each_template['sentence']=paragraph
                            ep["1"]=i
                            ep["2"]=part2[0]
                            each_template['arguments']=ep
                            part_template.append(each_template)
                        part2=[]
                        part1=[]
                        
            elif tok.dep_=='pobj' or tok.text in each_loc_value:
                  p1=' '
                  child_dep={}
                  part1=[]
                  part2=[]
                  flag=0
                  p2=''
                  child_dep={child:child.dep_ for child in tok.children}
                  for key,values in child_dep.items():
                      if values=='compound' or values=='det':
                          p1+=key.text+' '
                  p1+=tok.text
                  part1.append(p1)
                  for key,values in child_dep.items():
                      if values=='conj' and key.text in location:
                            part1.append(key.text)
                  
                      elif values=='appos' or  key.text in each_loc_value:
                            part2_child={}
                            p2=''
                            part2_child={c.text:c.dep_ for c in key.children}
                            for k,v in part2_child.items():
                                if v=='compound' :
                                    p2+=k+' '
                            p2+=key.text
                            if p2 in location:
                                part2.append(p2)
                            
                  if part2:
                        for i in part1:
                            each_template={}
                            ep={}
                            each_template['template']='PART'
                            each_template['sentence']=paragraph
                            ep["1"]=i
                            ep["2"]=part2[0]
                            each_template['arguments']=ep
                            part_template.append(each_template)
                        part2=[]
                        part1=[]   
                  
                      
                    
                        
    return part_template                        
    
def getPart(filename):
    with open(filename, 'r',encoding='UTF-8') as file:
        #data = file.read().replace('\n', '')
        datalines = file.readlines()
        
    clean_lines = []
    for line in datalines:
        line = line.strip()
        if(len(line)>0):
            clean_lines.append(line)
    
    part_template=[]
    for line in clean_lines:
        sentences = nlp(line)
        paragraph = []
        for sent in sentences.sents:
            paragraph.append(sent.text)
            
        article = nlp(sentences._.coref_resolved)  
        part_data=get_part_data(article)
        part_template=list(np.hstack((part_template,get_part_template(part_data,paragraph))))
        
    return part_template