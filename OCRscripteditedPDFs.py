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


import pytesseract
from collections import defaultdict
from PIL import Image

results_dir = Path('/Users/ceciliabarnard/Desktop/8510/TopicModeling/results')
results_dir.mkdir(exist_ok=True)


# Step 1: Convert images in 'editedpfimages' to grayscale, then OCR and save results
edited_images_dir = Path('/Users/ceciliabarnard/Desktop/8510/TopicModeling/pdfstoedit/editedpdfimages')
grayscale_dir = Path('/Users/ceciliabarnard/Desktop/8510/TopicModeling/pdfstoedit/editedpdfimages/grayscale_images')
grayscale_dir.mkdir(exist_ok=True)

for img_path in edited_images_dir.glob('*.png'):
    try:
        # Convert to grayscale
        with Image.open(img_path) as img:
            gray_img = img.convert('L')
            gray_img_path = grayscale_dir / img_path.name
            gray_img.save(gray_img_path)
            print(f'Converted {img_path.name} to grayscale.')

        # OCR
        text = pytesseract.image_to_string(gray_img)
        print(f'Processed {img_path.name}:')
        print(text[:200])
        print('-' * 40)

        # Save OCR result
        pdf_base = img_path.stem.split('_page')[0] if '_page' in img_path.stem else img_path.stem
        result_file = results_dir / (pdf_base + '.txt')
        with open(result_file, 'a', encoding='utf-8') as f:
            f.write(f'--- {img_path.name} ---\n{text}\n')

    except Exception as e:
        print(f'  ❌ Error processing {img_path.name}: {e}')

# Integrate all .txt files in results_dir into one file
all_txt_files = sorted(results_dir.glob('*.txt'))
with open(results_dir / 'all_results.txt', 'w', encoding='utf-8') as outfile:
    for txt_file in all_txt_files:
        with open(txt_file, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
