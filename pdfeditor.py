import sys
from pathlib import Path
from pdf2image import convert_from_path
import os

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

pdf_dir = Path('/Users/ceciliabarnard/Desktop//8510/TopicModeling/pdfstoedit')
output_dir = Path('/Users/ceciliabarnard/Desktop/8510/TopicModeling/pdfstoedit/editedpdfimages')
output_dir.mkdir(exist_ok=True)

for pdf_path in pdf_dir.glob('*.pdf'):
    try:
        print(f'Processing: {pdf_path.name}')
        images = convert_from_path(pdf_path, output_folder=output_dir, fmt='png')
        print(f'  Converted {len(images)} pages from {pdf_path.name}')
    except Exception as e:
        print(f'  ❌ Error processing {pdf_path.name}: {e}')

# Script only converts PDFs to images in converted_images and then stops.
