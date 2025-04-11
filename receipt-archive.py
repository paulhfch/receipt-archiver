import os, argparse, uuid, re, unicodedata
from datetime import datetime
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import pytesseract

def main():
    args = parse_args()

    # create output directory if it doesn't exist
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Convert each pdf page to jpeg: https://github.com/Belval/pdf2image
    # Reduce jpeg size by adjusting dpi setting
    try: 
        images = convert_from_path(args.input, dpi=100, fmt='jpeg')
        print(f"Converted {args.input} to JPEG images.")

        for image in images: # PIL Image representing each page of the PDF document
            image_filename = None
            filename_suffix = str(uuid.uuid4()) + '.jpeg'

            # Extract date from image
            date = date_from_image_en(image)
            if not date:
                date = date_from_image_jp(image)

            # Creates filename from date
            if date:
                date_str = date.strftime('%Y-%m-%d')
                image_filename = f'{date_str}-{filename_suffix}'
            else:
                # If date not found, use a default name
                image_filename = f'unknown-{filename_suffix}'
                print(f"Date not found in image, using default name: {image_filename}")

            # Save the image 
            image.save(os.path.join(output_dir, image_filename), 'JPEG')
    except (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError) as e:
        print(f"Error processing PDF: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description='Receipt Archiver')
    parser.add_argument('-i', '--input', type=str, help='Path to the input PDF file')

    return parser.parse_args()

def match_date(text, pattern, date_format):
    match = re.search(pattern, text)
    if match:
        original_date_str = match.group(0)
        print(f"Extracted date: {original_date_str}")

        try:
            return datetime.strptime(original_date_str, date_format).date()
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None
        
    return None

def date_from_image_en(image):
    text = pytesseract.image_to_string(image)
    # print(text)
    
    date = None

    # Extract date: match mm/dd/yyyy
    date = match_date(text, r'\d{1,2}/\d{1,2}/\d{4}', '%m/%d/%Y')
    
    if not date:
        # Extract date: match yyyy/mm/dd
        date = match_date(text, r'\d{4}/\d{1,2}/\d{1,2}', '%Y/%m/%d')

    if not date:
        # Extract date: match yy/mm/dd, mm/dd/yy
        date_match = re.search(r'\d{2}/\d{2}/\d{2}', text)
        
        if date_match:
            original_date_str = date_match.group(0)
            print(f"Extracted date: {original_date_str}")

            date_components = original_date_str.split('/')
            try:
                if int(date_components[0]) > 12:
                    date = datetime.strptime(original_date_str, '%y/%m/%d').date()
                else:
                    date = datetime.strptime(original_date_str, '%m/%d/%y').date()
            except ValueError as e:
                print(f"Error parsing date: {e}")

    return date

def date_from_image_jp(image):
    tessdata_dir = os.path.join(os.getcwd(), 'tessdata')
    tessdata_dir_config = f'--tessdata-dir {tessdata_dir}'
    text = pytesseract.image_to_string(image, lang='jpn', config=tessdata_dir_config)

    # Replaces the circled numbers
    text = unicodedata.normalize("NFKC", text).replace(" ", "")
    #print(text)
    
    date = None

     # Extract date: match yyyy-mm-dd
    date = match_date(text, r'\d{4}-\d{1,2}-\d{1,2}', '%Y-%m-%d')
    
    if not date:
        # Extract date: match yyyy/mm/dd
        date = match_date(text, r'\d{4}/\d{1,2}/\d{1,2}', '%Y/%m/%d')

    if not date:
        # Extract date: match yy年mm月dd日
        date = match_date(text, r'\d{2}年\d{1,2}月\d{1,2}', '%y年%m月%d')

    if not date:
        # Extract date: match yyyy年mm月dd日
        date = match_date(text, r'\d{4}年\d{1,2}月\d{1,2}', '%Y年%m月%d')

    return date

main()