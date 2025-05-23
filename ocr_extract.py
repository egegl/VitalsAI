import os
import json
import re
import logging
from pathlib import Path
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ensure_output_dir():
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def convert_pdf_to_images(pdf_path):
    # Convert all pages of PDF to images
    logger.info(f"Converting PDF to images: {pdf_path}")
    try:
        images = convert_from_path(pdf_path)
        if not images:
            raise ValueError("No pages found in PDF")
        return [np.array(img) for img in images]
    except Exception as e:
        logger.error(f"Error converting PDF to images: {e}")
        raise

def preprocess_image(image):
    # Preprocess image for better OCR
    logger.info("Preprocessing image...")
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise

def extract_text_from_image(image):
    # Extract text from image using Tesseract OCR
    logger.info("Extracting text using Tesseract OCR...")
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        raise

def parse_clinical_data(text):
    # Parse clinical data from extracted text using regex
    logger.info("Parsing clinical data...")
    
    data = {
        "patient_name": None,
        "dob": None,
        "hemoglobin": {
            "test_name": None,
            "value": None,
            "units": None,
            "warning": None
        },
        "creatinine": {
            "test_name": None,
            "value": None,
            "units": None,
            "warning": None
        },
        "bun": {
            "test_name": None,
            "value": None,
            "units": None,
            "warning": None
        }
    }
    
    try:
        # Patient name pattern - match until the end of the line
        name_pattern = r"Name:\s*([A-Z\s,]+)(?:\n|$)"
        name_match = re.search(name_pattern, text)
        if name_match:
            data["patient_name"] = name_match.group(1).strip()
        
        # DOB pattern - match until the end of the line
        dob_pattern = r"DOB:\s*(\d{1,2}/\d{1,2}/\d{4})(?:\n|$)"
        dob_match = re.search(dob_pattern, text)
        if dob_match:
            # Convert date format from MM/DD/YYYY to YYYY-MM-DD
            dob = dob_match.group(1)
            month, day, year = dob.split('/')
            data["dob"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        # Hemoglobin
        hgb_match = re.search(r"[\{\(\|]?\s*Hgb\s*([0-9.]+)\s*([a-zA-Z/%]+)(?:\s*\((High|Low|Critical)\))?", text)
        if hgb_match:
            data["hemoglobin"]["test_name"] = "Hemoglobin"
            data["hemoglobin"]["value"] = hgb_match.group(1)
            data["hemoglobin"]["units"] = hgb_match.group(2)
            data["hemoglobin"]["warning"] = hgb_match.group(3) if hgb_match.group(3) else None
        
        # Creatinine
        creat_match = re.search(r"[\{\(\|]?\s*Creatinine Level\s*[\{\(\|]?\s*([0-9.]+)\s*([a-zA-Z0-9/%]+)(?:\s*\((High|Low|Critical)\))?", text)
        if creat_match:
            data["creatinine"]["test_name"] = "Creatinine Level"
            data["creatinine"]["value"] = creat_match.group(1)
            data["creatinine"]["units"] = creat_match.group(2)
            data["creatinine"]["warning"] = creat_match.group(3) if creat_match.group(3) else None
        
        # BUN
        bun_match = re.search(r"[\{\(\|]?\s*BUN\s*([0-9.]+)\s*([a-zA-Z0-9/%]+)(?:\s*\((High|Low|Critical)\))?", text)
        if bun_match:
            data["bun"]["test_name"] = "BUN"
            data["bun"]["value"] = bun_match.group(1)
            data["bun"]["units"] = bun_match.group(2)
            data["bun"]["warning"] = bun_match.group(3) if bun_match.group(3) else None
        
        return data
    except Exception as e:
        logger.error(f"Error parsing clinical data: {e}")
        raise

def save_json(data, output_path):
    # Save extracted data to JSON file
    logger.info(f"Saving data to {output_path}")
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving JSON: {e}")
        raise

def process_file(input_path):
    # Main method to process input file
    try:
        output_dir = ensure_output_dir()
        if input_path.lower().endswith('.pdf'):
            images = convert_pdf_to_images(input_path)
        else:
            image = cv2.imread(input_path)
            if image is None:
                raise ValueError(f"Could not read image file: {input_path}")
            images = [image]

        # OCR all pages
        all_text = ""
        for image in images:
            processed_image = preprocess_image(image)
            extracted_text = extract_text_from_image(processed_image)
            all_text += extracted_text + "\n"
        logger.info("Extracted text sample: " + all_text[:100] + "...")
        clinical_data = parse_clinical_data(all_text)
        output_path = output_dir / "extracted_data.json"
        save_json(clinical_data, output_path)

        # Save full OCR text to outputs/ocr_output.txt
        ocr_txt_path = output_dir / "ocr_output.txt"
        with open(ocr_txt_path, 'w') as f:
            f.write(all_text)
        logger.info(f"Full OCR text saved to {ocr_txt_path}")
        logger.info("Processing completed successfully!")
        return clinical_data
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise

if __name__ == "__main__":
    input_file = "sample_inputs/discharge_note.pdf"
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
    else:
        process_file(input_file) 
