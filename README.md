# Overview 
This python script helps small businesses create compressed jpeg images of the receipts, indexed with transaction dates, for bookkeeping purpose.
1. The script takes in a pdf of one or more receipt pictures. (Tips: I use the Scan Documents feature in the iOS stock Notes app to capture pictures and convert to pdf)
1. The pdf is exploded into jpeg images at reduced sizes
1. The jpeg images go through OCR to capture the date of the transaction
1. The jpeg images are renamed to the date of the transaction and a random UUID
1. All images are saved in the output/ directory

This script for now works with date text in English and Japanese.

# Quick Start
1. Clone the project and go to the project directory
1. Set up venv: `$python3 -m venv .env`
1. Activate venv: `$source .env/bin/activate`
1. Install dependencies: `$pip3 install -r requirements.txt`
1. Run script: `$python3 receipt-archive.py -i sample-receipt.pdf`

