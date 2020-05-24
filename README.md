# Information Extraction Application
Program to extract information from text and fill pre-defined templates using Natural Language Processing.

Requirements:
1. Python 3.7
2. SpaCy 2.2.4
3. nltk 3.4.5
4. neuralcoref 4.0 (Install from source https://github.com/huggingface/neuralcoref)

File Description:
1. buyTemplate.py : Extracts buy event templates from the document
2. workTemplate.py : Extract work event templates from the document
3. partTemplate.py : Extracts location templates from the document

To run the demo:
1. Task 1 : Run "Task1_FeatureExtraction.py"
2. Task 3 : Run "Task3_InformationExtraction.py" 

Objectives:
1. Implement an NLP pipeline to extract features. The features include sentence splitting, tokenization, lemmatization, part-of-speech tagging, dependency parsing and word relation extraction.
2. Implement a machine-learning, statistical, or heuristic (or a combination) based approach to extract filled information templates from the corpus of text articles. The templates are BUY (Buyer, Item, Price, Quantity, Source), WORK (Person, Organization, Position, Location), PART (Location, Location)
3. Implement a program that will accept an input text document and output a JSON file with extracted/filled information templates from the input text document.
