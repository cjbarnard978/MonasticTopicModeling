import cltk
import pandas as pd
import argparse
import sys
from pathlib import Path

HIBERNIA_DECLENSIONS = [
    "Hibernia",
    "Hiberniae",
    "Hiberniam",
    "Hiberniarum",
    "Hiberniis",
    "Hibernias",
    "Ibernia",
    "Iberniae",
    "Iberniam",
    "Iberniarum",
    "Iberniis",
    "Ibernias",
    "Insula Sacra",
    "Archmachia",
    ""
]

def extract_entities_with_cltk(text, cltk_nlp):
    entities = []
    for declension in HIBERNIA_DECLENSIONS:
        start = 0
        while True:
            idx = text.find(declension, start)
            if idx == -1:
                break
            # Lemmatize using CLTK
            lemma = None
            try:
                doc = cltk_nlp.analyze(text=declension)
                lemmas = [word.lemma for word in doc.words]
                lemma = ' '.join(lemmas) if lemmas else None
            except Exception:
                lemma = None
            entities.append({
                'text': declension,
                'label': 'HIBERNIA_DECLENSION',
                'label_description': 'custom noun declension',
                'start': idx,
                'end': idx + len(declension),
                'confidence': None,
                'lemma': lemma,
            })
            start = idx + len(declension)
    return entities

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
    parser = argparse.ArgumentParser(description='Hibernia Noun Declension Identification using CLTK NLP')
    parser.add_argument('input_file', help='Path to the text file to analyze')
    parser.add_argument('--output', default='ireland_mentions', help='Base name for output files (default: ireland_mentions)')
    parser.add_argument('--max-chars', type=int, default=None, help='Maximum characters to process (useful for large files)')
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)

    print(f"Reading file: {args.input_file}")

    try:
        from cltk import NLP
        cltk_nlp = NLP("lat")
        print('CLTK pipeline initialized for Latin')
    except Exception as e:
        print('Failed to initialize CLTK pipeline:', e)
        sys.exit(1)

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

    print("🔍 Extracting noun declension entities...")
    entities = extract_entities_with_cltk(text, cltk_nlp)

    if not entities:
        print("no mentions of Hibernia.")
        return

    print(f"Found {len(entities)} noun declensions")
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
