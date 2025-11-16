## This script package performs Named Entity Recognition for texts in Latin and English using two Latin NLPs and one English NLP

## Activating the Virtual Environment

    python3 -m venv topicmodel_env
    source topicmodel_env/bin/activate

## To Install Dependencies

    pip install -r requirements.txt

## Loading SpaCy and Running the Scripts

    To download: python -m spacy download en_core_web_smr
    This is only designed to run using the small model since the NLP process is outsourced. 

    To run: python filename.py textfilename.txt 
    Output will appear in a "results" folder under "NERscripts" 

## Files 

- NEREnglishTexts.py: Runs NER on .txt files in English
    -for use with file: MH1and2edited.txt
- NERwithCLTK.py: Runs NER on .txt files in Latin using Classical Language Toolkit
- NERwithStanza.py: Runs NER on .txt files in Latin using Stanza NLP
    - for use with files: Aberbroth.txt, Aberbroth1.txt, DryburghAbbey.txt, Dunfermline.txt, InchaffreyAbbey.txt, Kelso1.txt, Kelso2.txt, Newbattle.txt, and Passelet.txt 

## How it Works 

This is a custom Named Entity Recognition script that allows the user to input specific locations for the model to identify. First, add your custom locations and name it. Then, the function defines the entities you customized and passes it to one of three NLPs: Stanza, CLTK, or SpaCy. Both Latin models lemmatize texts for better analysis, grouping variants together. Make sure to change the "for" loop statements and then the labels to better align with your custom place list. Make sure that the file path structure for the results matches the file path structure you set up in your directory. Then, define the argument based on your custom list. You may have to alter the length allowed. If so, add this code 
     nlp.max_length = 2000000 (this integer can change).
When you are defining the model. If the script finds what you're looking for, results will be printed to a CSV in a "results" folder. If no results are found, make sure to edit the "no results found" statement to correspond with your custom list. 

***Both the Stanza and the English scripts define the model at the beginning of the script, and the CLTK integrates the NLP and defines toward the end

## Repositories for Stanza and CLTK

CLTK: https://github.com/cltk/cltk

Stanza: https://stanfordnlp.github.io/stanza/ 