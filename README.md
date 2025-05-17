# VitalsAI

A toolkit for extracting structured clinical data from PDF discharge summaries and transcribing audio using OCR and speech-to-text models.

## Features

- **PDF OCR Extraction**: Extracts patient name, date of birth, and key lab results with their warnings from scanned discharge notes.
- **Audio Transcription**: Records audio from your microphone and transcribes it using OpenAI's Whisper model.
- **Outputs**: Structured JSON for clinical data, raw OCR text, audio WAV files, and transcript text files.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd VitalsAI
   ```

2. **Set up a Python virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   **Required packages:**
   - opencv-python
   - numpy
   - pytesseract
   - pdf2image
   - pillow
   - sounddevice
   - soundfile
   - openai-whisper
   - torch

4. **Install Tesseract OCR and FFmpeg**
   - **macOS:**
     ```bash
     brew install tesseract ffmpeg
     ```
   - **Linux:**
     ```bash
     sudo apt-get install tesseract-ocr ffmpeg
     ```
   - **Windows:**
     - [Tesseract installer](https://github.com/tesseract-ocr/tesseract)
     - [FFmpeg installer](https://ffmpeg.org/download.html)
     - Add both to your PATH

---

## Usage

### 1. OCR Extraction from Discharge Note PDF

Place your PDF file in the `sample_inputs` directory.

Run:
```bash
python ocr_extract.py
```

**Outputs:**
- `outputs/extracted_data.json` — structured clinical data
- `outputs/ocr_output.txt` — full OCR text from the PDF

### 2. Audio Transcription

Run:
```bash
python transcribe.py
```

- Records 30 seconds of audio from your microphone
- Outputs:
  - `outputs/audio.wav` — the recorded audio
  - `outputs/transcript.txt` — the transcribed text

---

## Output Example (OCR)
```json
{
  "patient_name": "ASHBY, ANNIE LAURIE",
  "dob": "1932-04-04",
  "hemoglobin": {
    "test_name": "Hemoglobin",
    "value": "13.8",
    "units": "gm/dL",
    "warning": null
  },
  "creatinine": {
    "test_name": "Creatinine Level",
    "value": "0.7",
    "units": "mg/dL",
    "warning": null
  },
  "bun": {
    "test_name": "BUN",
    "value": "23",
    "units": "mg/dL",
    "warning": "High"
  }
}
```
