# Clinical Lab Report OCR and Audio Transcription

This project provides two main functionalities:
1. OCR extraction from clinical lab reports (PDF or image)
2. Audio recording and transcription

## Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system
- Microphone access for audio recording

### Installing Tesseract OCR

#### macOS
```bash
brew install tesseract
```

#### Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr
```

#### Windows
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### OCR Extraction

1. Place your clinical lab report (PDF or image) in the `sample_inputs` directory.
2. Run the OCR script:
```bash
python ocr_extract.py
```

The script will:
- Convert PDF to image if needed
- Preprocess the image
- Extract text using Tesseract OCR
- Parse clinical data
- Save results to `outputs/extracted_data.json`

### Audio Transcription

1. Run the transcription script:
```bash
python transcribe.py
```

The script will:
- Record 30 seconds of audio from your microphone
- Save the recording as `outputs/audio.wav`
- Transcribe the audio using Whisper
- Save the transcript to `outputs/transcript.txt`

## Output Format

### OCR Output (extracted_data.json)
```json
{
  "patient_name": "Jane Doe",
  "dob": "1985-06-12",
  "test_name": "Hemoglobin",
  "value": "13.2",
  "units": "g/dL"
}
```

### Audio Transcription Output (transcript.txt)
The transcript will be saved as plain text.

## Error Handling

Both scripts include comprehensive error handling and logging. Check the console output for any issues during execution.

## Notes

- The OCR script assumes a specific format for the clinical lab report. You may need to adjust the regex patterns in `parse_clinical_data()` to match your specific report format.
- The audio recording is set to 30 seconds by default. You can modify this in the `record_audio()` function.
- Make sure you have sufficient disk space for the Whisper model and audio files. 