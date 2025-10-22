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
def setup_custom_entities(nlp)
    hibernia_declensions = [
        "Hibernia",
        "Hiberniae",
        "Hiberniam",
        "Hiberniarum",
        "Hiberniis",
        "Hibernias"
    ]

    ruler = nlp.add_pipe("entity_ruler", before ="ner")
    patterns = [{"label": "NOUN_DECLENSION", "pattern": declension} for declension in hibernia_declensions]
    ruler.add_patterns(patterns)

    print("ruler added")
    for declension in hibernia_declensions:
        print(f"{declension}")
def extract_entities(text, nlp):

    doc = nlp(text):
    entities = []

    noun_declensions = {"NOUN_DECLENSION"}
    for ent in doc.ents: 
        if ent.label_ not in noun_declensions:
            continue
        entities_append({
            'text': ent.text,
            'label': ent.label_,
            'label_description':'custom noun declension',
            'start': ent.start_char,
            'end': ent.end_char,
            'confidence': ent._.prob if hasattr(ent._, 'prob') else None
        })
    
    return entities

def save_entities_to_csv(entities, output_file): 
    if not entities : 
        print("no entities found")
        return 
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    output_path = results_dir / output_file
    entities_df = pd.DataFrame(entities)
    entities_df.to_csv(output_path, index=False)
    print(f"Saved {len(entities)} entities to: {output_path}")

def main():
   
    parser = argparse.ArgumentParser(description='Hibernia Noun Declension Identification using LatinCy)
    parser.add_argument('input_file', help='Path to the text file to analyze')
    parser.add_argument('--model', default='la_core_web_sm', 
                       help='spaCy model to use (default: la_core_web_sm)')
    parser.add_argument('--output', default='ireland_mentions', 
                       help='Base name for output files (default: ireland_mentions)')
    parser.add_argument('--max-chars', type=int, default=None,
                       help='Maximum characters to process (useful for large files)')
    
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print ("Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    
    print(f"Reading file: {args.input_file}")
    
    nlp = load_spacy_model(args.model)
    
    
    nlp = setup_custom_entities(nlp)
    
  
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        
        with open(input_path, 'r', encoding='latin-1') as f:
            text = f.read()
    
    
    
    if args.max_chars and len(text) > args.max_chars:
        text = text[:args.max_chars]
        print(f"⚠️  Limited processing to first {args.max_chars} characters")
    
    print(f"📝 Processing {len(text):,} characters of text...")
    
    # Extract entities
    print("🔍 Extracting noun declension entities...")
    entities = extract_entities(text, nlp)
    
    if not entities:
        print("no mentions of Hibernia.")
        return
    
  
    print(f"Found {len(entities)} noun declensions")
    
    # Show found sports
    if entities:
        print("\n entities found:")
        noun_declensions = list(set([ent['text'] for ent in entities]))
        for noun in sorted(noun_declensions)):
            count = sum(1 for ent in entities if ent['text'] == noun)
            print(f"   • {noun}: {count} occurrence{'s' if count > 1 else ''}")
    

    output_file = f"{args.output}.csv"
    save_entities_to_csv(entities, output_file)
    
    print(f"\nExtraction complete! Results saved to: {output_file}")

if __name__ == "__main__":
    main()
