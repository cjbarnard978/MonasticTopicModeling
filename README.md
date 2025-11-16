## Activating the Virtual Environment

    python3 -m venv topicmodel_env
    source topicmodel_env/bin/activate

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



## Repositories for Stanza and CLTK

CLTK: https://github.com/cltk/cltk

Stanza: https://stanfordnlp.github.io/stanza/ 