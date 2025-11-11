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


import pytesseract
from collections import defaultdict

results_dir = Path('/Users/ceciliabarnard/Desktop/8510/TopicModeling/results')
results_dir.mkdir(exist_ok=True)

for pdf_path in pdf_dir.glob('*.pdf'):
    try:
        print(f'Processing: {pdf_path.name}')
        # Step 1: Convert PDF to images
        images = convert_from_path(pdf_path, output_folder=output_dir, fmt='png')
        print(f'  Converted {len(images)} pages from {pdf_path.name}')

        # Step 2: Convert images to grayscale
        pdf_base = pdf_path.stem
        grayscale_dir = Path('/Users/ceciliabarnard/Desktop/8510/TopicModeling/grayscale_images')
        grayscale_dir.mkdir(exist_ok=True)
        page_texts = []
        for i, img in enumerate(images):
            gray_img = img.convert('L')
            img_name = f'{pdf_base}_page{i+1}.png'
            gray_img_path = grayscale_dir / img_name
            gray_img.save(gray_img_path)
            print(f'Converted {img_name} to grayscale.')

            # Step 3: OCR
            text = pytesseract.image_to_string(gray_img)
            print(f'Processed {img_name}:')
            print(text[:200])
            print('-' * 40)
            page_texts.append(f'--- {img_name} ---\n{text}\n')

        # Step 4: Save combined OCR result for this PDF
        result_file = results_dir / (pdf_base + '.txt')
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f'OCR results for {pdf_base}.pdf\n\n')
            f.write('\n'.join(page_texts))
        print(f'Saved combined OCR result to {result_file}')
    except Exception as e:
        print(f'  ❌ Error processing {pdf_path.name}: {e}')


