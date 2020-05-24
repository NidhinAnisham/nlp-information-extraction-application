# -*- coding: utf-8 -*-
"""
Filename: Task3_InformationExtraction.py
Authors: Nidhin Anisham, Divya Machenahalli Lokesh

Use command "python Task3_InformationExtraction.py" to run
 
This program does the following: 
 1. Extracts templates buy, work and part
 2. Ouputs the extracted templates as a json
 
"""

import os
import json
from buyTemplate import getBuy
from workTemplate import getWork
from partTemplate import getPart

if __name__ == "__main__":
    filename = input("Enter document name: ")
    if not os.path.exists(filename):
        print("File does not exist")
    else:
        print("Extracting templates...")
        
        buyTemplates = getBuy(filename)
        workTemplates = getWork(filename)
        partTemplates = getPart(filename)
        
        templates = buyTemplates + workTemplates + partTemplates
        output = {"document":filename,
                  "extraction":templates}
        
        if not os.path.exists('output'):
            os.mkdir('output')
            
        with open("output/"+filename[:-3]+"json", 'w') as f:
            json.dump(output,f)
        
        print("Templates Extracted. Output in 'output' folder.")  