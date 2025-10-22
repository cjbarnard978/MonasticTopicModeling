#Hibernia 
#Hiberniae
#Hiberniam
#Hiberniarum 
#Hiberniis
#Hibernias

#python3 -m venv TM_env
#source TM_env/bin/activate

import spacy
import pandas as pd
import argparse
import sys
from pathlib import Path 



def load_spacy_model(model_name="la_core_web_sm")
    try: 
        nlp = spacy.load("la_core_web_sm")
        print("model loaded")
    except OSError:
        print("latin model not found")
        sys.exit(1)
    

