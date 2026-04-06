import spacy
import pandas as pd
import argparse
import sys
from pathlib import Path

def load_spacy_model(model_name="en_core_web_sm"):
    try:
        nlp = spacy.load(model_name)
        nlp.max_length = 2000000
        print(f"model loaded: {model_name}")
        return nlp
    except Exception as e:  
        print(f"spaCy model '{model_name}' not found or failed to load: {e}")
        nlp = spacy.blank("en")
        print("Loaded blank English pipeline instead.")
        return nlp

def setup_custom_entities(nlp):
    Scottish_place_names = [
        "Scotland",
        "Scots",
        "Kelso",
        "Passelet",
        "Aberbroth",
        "Dryburgh",
        "Dunfermline",
        "Dunfermlyn",
        "Inchaffrey",
        "Scotch",
        "Newbattle",
        "Edinburgh",
        "Glasgow",
        "Inverness"
    ]

    if "ner" in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    else:
        ruler = nlp.add_pipe("entity_ruler")
    patterns = [{"label": "Scottish_place_names", "pattern": placename} for placename in Scottish_place_names]
    ruler.add_patterns(patterns)

    print("ruler added")
    for placename in Scottish_place_names:
        print(f"{placename}")
    return nlp

def extract_entities(text, nlp):
    doc = nlp(text)
    entities = []

    Scottish_place_names = {"Scottish Place Names"}
    for ent in doc.ents:
        if ent.label_ not in Scottish_place_names:
            continue
        entities.append({
            'text': ent.text,
            'label': ent.label_,
            'label_description': 'Place name',
            'start': ent.start_char,
            'end': ent.end_char,
            'confidence': ent._.prob if hasattr(ent._, 'prob') else None,
        })

    return entities

Scottish_place_names = [
        "Scotland",
        "Scots",
        "Kelso",
        "Passelet",
        "Aberbroth",
        "Dryburgh",
        "Dunfermline",
        "Dunfermlyn",
        "Inchaffrey",
        "Newbattle",
        "Edinburgh",
        "Glasgow",
        "Inverness"
]

def save_entities_to_csv(entities, output_file):
    if not entities:
        print("no entities found")
        return
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    output_path = results_dir / output_file
    entities_df = pd.DataFrame(entities)
    entities_df.to_csv(output_path, index=False)
    print(f"Saved {len(entities)} entities to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Scottish place name identifications using SpaCy')
    parser.add_argument('input_file', help='Path to the text file to analyze')
    parser.add_argument('--output', default='scottish_places', help='Base name for output files (default: scottish_places)')
    parser.add_argument('--max-chars', type=int, default=None, help='Maximum characters to process (useful for large files)')
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)

    print(f"Reading file: {args.input_file}")

    try:
        nlp = load_spacy_model()
        nlp = setup_custom_entities(nlp)
        print('spaCy pipeline initialized')
    except Exception as e:
        print('Failed to initialize spaCy pipeline:', e)
        sys.exit(1)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

    if args.max_chars and len(text) > args.max_chars:
        text = text[:args.max_chars]
        print(f"⚠️  Limited processing to first {args.max_chars} characters")

    print(f"📝 Processing {len(text):,} characters of text...")

    print("🔍 Extracting place name entities...")
    entities = extract_entities(text, nlp)

    if not entities:
        print("no mentions of Scotland.")
        return

    print(f"Found {len(entities)} place name entities")
    print("\n entities found:")
    noun_declensions = list(set([ent['text'] for ent in entities]))
    for noun in sorted(noun_declensions):
        count = sum(1 for ent in entities if ent['text'] == noun)
        print(f"   • {noun}: {count} occurrence{'s' if count > 1 else ''}")

    output_file = f"{args.output}.csv"
    save_entities_to_csv(entities, output_file)
    print(f"\nExtraction complete! Results saved to: {output_file}")

if __name__ == "__main__":
    main()
