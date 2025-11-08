import sys
from pathlib import Path
from pdf2image import convert_from_path
import os
import re


required_packages = ['numpy', 'pandas', 'pytesseract', 'Pillow', 'opencv-python', 'pdf2image']
missing = []

for pkg in required_packages:
    try:
        if pkg == 'Pillow':
            import PIL
        elif pkg == 'opencv-python':
            import cv2
        else:
            __import__(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print("missing packages")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)

pdf_dir = Path('/Users/ceciliabarnard/Desktop//8510/TopicModeling/pdfs')

output_dir = Path('/Users/ceciliabarnard/Desktop/8510/TopicModeling/pdfs/converted_images')
output_dir.mkdir(exist_ok=True)

for pdf_path in pdf_dir.glob('*.pdf'):
    try:
        print(f'Processing: {pdf_path.name}')
        images = convert_from_path(pdf_path, output_folder=output_dir, fmt='png')
        print(f'  Converted {len(images)} pages from {pdf_path.name}')
    except Exception as e:
        print(f'  ❌ Error processing {pdf_path.name}: {e}')

quality_settings = {
            'high': {'dpi': 300, 'format': 'PNG'},
            'medium': {'dpi': 200, 'format': 'PNG'},
            'low': {'dpi': 150, 'format': 'JPEG'}
        }
settings = quality_settings.get('high', quality_settings['high'])


from pathlib import Path
from PIL import Image

input_dir = Path('/Users/ceciliabarnard/Desktop/8510/ocrtesseract/ocrai/pdf/converted_images')
output_dir = Path('/Users/ceciliabarnard/Desktop/8510/ocrtesseract/ocrai/pdf/grayscale_images')
output_dir.mkdir(exist_ok=True)

for img_path in input_dir.glob('*.png'):
    with Image.open(img_path) as img:
        gray_img = img.convert('L')
        gray_img.save(output_dir / img_path.name)
        print(f'Converted {img_path.name} to grayscale.')

def ocr_conversion(image_path, lang='eng'):
    # Simple wrapper around pytesseract for future reuse
    import pytesseract
    from PIL import Image
    image = Image.open(image_path)
    config = f'--psm 3 -l {lang}'
    text = pytesseract.image_to_string(image, config=config)
    data = {}
    try:
        data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DICT)
    except Exception:
        data = {'conf': []}
    return text, data


input_dir = Path('/Users/ceciliabarnard/Desktop/8510/ocrtesseract/ocrai/pdf/grayscale_images')
results_dir = Path('/Users/ceciliabarnard/Desktop/8510/ocrtesseract/ocrai/pdf/results')
results_dir.mkdir(exist_ok=True)

import pytesseract

from collections import defaultdict

# Group images by their source PDF (assumes naming convention: <pdfname>_pageN.png)
pdf_texts = defaultdict(list)

for img_path in input_dir.glob('*.png'):
    try:
        image = Image.open(img_path)
        text = pytesseract.image_to_string(image)
        print(f'Processed {img_path.name}:')
        print(text[:200])
        print('-' * 40)

        # Extract PDF base name from image filename
        # Example: 'mydoc_page1.png' -> 'mydoc'
        base = img_path.stem
        pdf_base = base.split('_page')[0] if '_page' in base else base
        pdf_texts[pdf_base].append(f'--- {img_path.name} ---\n{text}\n')
    except Exception as e:
        print(f'❌ Error processing {img_path.name}: {e}')

# Write one .txt file per PDF
for pdf_base, texts in pdf_texts.items():
    result_file = results_dir / (pdf_base + '.txt')
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(f'OCR results for {pdf_base}.pdf\n\n')
        f.write('\n'.join(texts))
    print(f'Saved combined OCR result to {result_file}')


