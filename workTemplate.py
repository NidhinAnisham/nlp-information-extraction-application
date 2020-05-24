# -*- coding: utf-8 -*-
"""
Filename: workTemplate.py
Authors: Nidhin Anisham, Divya Machenahalli Lokesh

Use command "python workTemplate.py" to run
 
This program does the following: 
 1. Creates a SpaCy NLP pipeline on the input 'filename'
 2. Extracts (person,organization,position,location)
 3. Outputs a dictionary of filled templates
 
"""

import spacy

import numpy as np
import neuralcoref

nlp = spacy.load("en_core_web_sm")
neuralcoref.add_to_pipe(nlp)

jobs=['chief executive officer','cheif','executive','officer','vice','teacher','software engineer','software','engineer','developer','mechanic','ceo','cheif operating officer','coo','president','clerk','vice prsident','chairman','chairwoman','chairperson','owner','manager','dean','partner','professor','cfo','director','board','member','board member','bookseller','homeowner','publisher','analyst','scientist','hr','human resources','architect','employee','actor','actress','technician','clerk']
buy = ['buy','acquire','purchase','acquisition']

def get_work_data(article):
    work_data=[]
    
    for s in article.sents:
       illegal_sent=0
       doc=nlp(str(s))
       for word in doc:
           if word.lemma_ in buy:
            illegal_sent=1
            break;
       if illegal_sent==0:
           for ent in doc.ents:
               if ent.label_=='PERSON':
                   work_data.append(str(s).replace(';',' '))
                   break
    return work_data



def get_work_separated_data(work_data):
    person_tain_data=[]
    per_org_train_data=[]
    per_org_loc=[]           
    for person_text in work_data:
        count_org=0
        count_loc=0
       
        doc=nlp(person_text)
        for ent in doc.ents:
            if ent.label_=='ORG':
                count_org+=1
            elif ent.label_=='GPE':
                count_loc+=1
            
        if count_loc==0 and count_org==0 :
            person_tain_data.append(person_text)
        elif count_org!=0 and count_loc==0:
            per_org_train_data.append(person_text)
        elif count_loc!=0 :
            per_org_loc.append(person_text)
    return person_tain_data,per_org_train_data,per_org_loc

def get_person_template(person_tain_data,paragraph):
    pw_template=[]
    for per in person_tain_data:
        each_template={}
        pw={}
        p=[]
        doc=nlp(per)
        founder=0
        other_jobs=0
        for word in doc:
            if word.lemma_=='found':
               founder=1
            if word.text in jobs:
               other_jobs=1 
        
        for ent in doc.ents:
            if ent.label_=='PERSON':
                p.append(ent.text)
        if founder==1:
            for i in p:
                each_template={}
                pw={}
                each_template['template']='WORK'
                
                each_template['sentence']=paragraph
                
                pw['1']=i
                pw['2']=''
                for tok in doc:
                    if tok.dep_=='nsubj':
                        pw['2']=tok.text
                        break
                pw['3']='Founder'
                pw['4']=''
                each_template['arguments']=pw
                pw_template.append(each_template)
            
        elif founder==0 or other_jobs!=0:
            for i in p:
                each_template={}
                pw={}
                t=''
                child_dep={}
                for tok in doc:
                    if tok.dep_=='appos' or tok.text.lower() in jobs :
                        
                        child_dep={child.text:child.dep_ for child in tok.children}
                        break
                    else:
                        t=''
                for key,values in child_dep.items():
                    if(values=='conj'):
                        t+=','+key
                            
                if t!='':
                        each_template['template']='WORK'
                        each_template['sentence']=paragraph
                        pw['1']=i
                        pw['2']=''
                        pw['3']=t
                        pw['4']=''
                        each_template['arguments']=pw
                        pw_template.append(each_template)
                        t=''
    return pw_template

def get_per_org_loc_data(per_org_loc,paragraph):
    pw_temp=[]
    for per in per_org_loc:
       each_template={}
       p=[]
       l=[]
       o=[]
       doc=nlp(per)
       founder=0
       other_jobs=0
       for ent in doc.ents:
            if ent.label_=='PERSON':
                p.append(ent.text)
                
            if ent.label_=='GPE':
                l.append(ent.text)
            if ent.label_=='ORG':
                o.append(ent.text)
       for word in doc:
           if word.lemma_ == 'found':
               founder=1
           if word.text in jobs:
               other_jobs=1 
       if founder==1:
           for i in p:
                each_template={}
                each_template['template']='WORK'
                each_template['sentence']=paragraph
                pw={}
                pw['1']=i
                org=''
                for tok in doc:
                    if tok.dep_.startswith('nsubj') or tok.text in o:
                        child_dep={}
                   
                        org=''
                        child_dep={child.text:child.dep_ for child in tok.children}
                        for key,values in child_dep.items():
                                if(values=='compound'):
                                    org+=key+' '
                        org+=tok.text
                        for key,values in child_dep.items():
                            if(values=='conj'):
                                org+=','+key
                        
                    
                    t=''
                    child_dep={}
                    if tok.dep_=='appos':
                        if tok.text in l:
                            child_dep={child.text:child.dep_ for child in tok.head.children}
                            
                        for key,values in child_dep.items():
                            if(values=='compound'):
                                t+=key+' '
                        t+=tok.head.text+','+tok.text
                    if org!='' and t!='':
                        pw['2']=org
                        pw['3']='founder'
                        pw['4']=t
                        each_template['arguments']=pw
                        pw_temp.append(each_template)
                        org=''
                        t=''
                
       elif other_jobs!=0 or founder==0:
           for i in p:  
                each_template={}
                each_template['template']='WORK'
                each_template['sentence']=paragraph
                t=""
                child_dep={}
                pw={}
                for tok in doc:
                    if tok.dep_=='appos' or tok.text in o:
                        child_dep={}
                       
                        org=''
                        child_dep={child.text:child.dep_ for child in tok.children}
                        for key,values in child_dep.items():
                                if(values=='compound'):
                                    org+=key+' '
                        org+=tok.text
                        for key,values in child_dep.items():
                            if(values=='conj'):
                                org+=','+key
                         
                    if tok.text.lower() in jobs:
                        child_dep={}
                        child_dep={child.text:child.dep_ for child in tok.children}
                        for key,values in child_dep.items():
                                if(values=='compound'):
                                    t+=key+' '
                        t+=tok.text
                        for key,values in child_dep.items():
                            if(values=='conj'):
                                t+=','+key
                    else:
                        t=''
                    loc=''
                    child_dep={}
                    if tok.dep_=='appos' and tok.text in l:
                        child_dep={child.text:child.dep_ for child in tok.head.children}
                        
                        for key,values in child_dep.items():
                            if(values=='compound'):
                                loc+=key+' '
                        loc+=tok.head.text+','+tok.text
                              
                    if t!='' and loc!='':
                        
                        pw['1']=i
                        pw['2']=org
                        pw['3']=t
                        pw['4']=loc
                        each_template['arguments']=pw
                        pw_temp.append(each_template)
                        t=''
                        loc=''
               
    return pw_temp
        
    
def get_per_org_data(per_org_train_data,paragraph):
    
    pw_temp=[]
    for per in per_org_train_data:
       p=[]
       o=[]
       each_template={}
       doc=nlp(per)
       founder=0
       other_jobs=0
       for ent in doc.ents:
            if ent.label_=='PERSON':
                p.append(ent.text)
            if ent.label_=='ORG':
                o.append(ent.text)
       for word in doc:
           if word.lemma_ == 'found':
               founder=1
           if word.text in jobs:
               other_jobs=1
       if founder==1:
           for i in p:
                #print(i)
                pw={}
                each_template={}
                each_template['template']='WORK'
                each_template['sentence']=paragraph
                org=''
                for tok in doc:
                    if tok.dep_.startswith('nsubj') or tok.text in o:
                        child_dep={}
                        #print(1)
                        org=''
                        child_dep={child.text:child.dep_ for child in tok.children}
                        
                        for key,values in child_dep.items():
                                if(values=='compound'):
                                    org+=key+' '
                        org+=tok.text
                        for key,values in child_dep.items():
                            if(values=='conj'):
                                org+=','+key
                    if org!='':
                        #print(2)
                        pw['1']=i
                        pw['2']=org
                        pw['3']='founder'
                        pw['4']=''
                        each_template['arguments']=pw
                        pw_temp.append(each_template)
                        org=''
                        
       elif founder==0 or other_jobs!=0:
           
           each_template={}
           pw={}
           sentence_parsed=0
           t=''
           company=''

           for tok in doc:
               
               child_dep={}
               
               if (tok.dep_.startswith('nsubj') or tok.dep_=='appos') and tok.text in jobs:
                   child_dep={child.text:child.dep_ for child in tok.children}
                   
                   for key,values in child_dep.items():
                       if(values=='compound'):
                           t+=key+' '
                   t+=tok.text
                   for key,values in child_dep.items():
                       if(values=='conj'):
                           t+=','+key
                   
               if tok.dep_=='pobj' or tok.text in o:
                   child_dep={}
                   child_dep={child:child.dep_ for child in tok.children}
                   

                   for key,values in child_dep.items():
                       if(values=='compound' or values=='poss'):
                           company+=key.text+' '
                           
                   company+=tok.text  
                   
                   if t!='' and company !='':
                       for i in p:
                           pw={}
                           each_template={}
                           each_template['template']='WORK'
                           each_template['sentence']=paragraph
                           pw['1']=i
                           pw['2']=company
                           pw['3']=t
                           pw['4']=''
                           sentence_parsed=1
                           each_template['arguments']=pw
                           pw_temp.append(each_template)
                           
                           t=''
                           company=''
                           
           if sentence_parsed!=1:
               
                t=""
                child_dep={}
                for tok in doc:
                    if tok.dep_=='appos' or tok.text.lower() in jobs:
                        t=tok.text
                        if t.lower() in jobs:
                            child_dep={child.text:child.dep_ for child in tok.children}
                            break
                        else:
                            t=''
                for key,values in child_dep.items():
                    if(values=='conj'):
                        t+=','+key
                company=''
                for org in o:
                    val= org.split(" ")[-1]
                    for tok in doc:
                        if val==tok.text:
                            child_dep={}
                            child_dep={child.text:child.dep_ for child in tok.children}
                            for k,v in child_dep.items():
                                if (v=='conj' ):
                                    if k in o:
                                        org+=','+k
                    company=org 
                    break
                    
                if t!='' and company!='':
                    pw={}
                    each_template={}
                    each_template['template']='WORK'
                    each_template['sentence']=paragraph
                    pw['1']=p[0]
                    pw['2']=company
                    pw['3']=t
                    pw['4']=''
                    each_template['arguments']=pw
                    pw_temp.append(each_template)
                    t=''
                    company=''
    return pw_temp
                


def getWork(filename):


    with open(filename, 'r',encoding='UTF-8') as file:
        #data = file.read().replace('\n', '')
        datalines = file.readlines()
        
    clean_lines = []
    for line in datalines:
        line = line.strip()
        if(len(line)>0):
            clean_lines.append(line)
    pw_template=[]

    for line in clean_lines:
        sentences = nlp(line)
        paragraph = []
        for sent in sentences.sents:
            paragraph.append(sent.text)
            
        article = nlp(sentences._.coref_resolved)        
    
        work_data=get_work_data(article)
            
        person_tain_data,per_org_train_data,per_org_loc=get_work_separated_data(work_data)          
        
                
        pw_template=list(np.hstack((pw_template,get_person_template(person_tain_data,paragraph))))

        pw_template=list(np.hstack((pw_template,get_per_org_loc_data(per_org_loc,paragraph))))               
   
        pw_template=list(np.hstack((pw_template,get_per_org_data(per_org_train_data,paragraph))))   
        
        
    return   pw_template           
                