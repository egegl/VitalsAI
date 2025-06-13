# VitalsAI

A tool for extracting structured clinical data from PDF discharge summaries and transcribing audio using OCR and speech-to-text models.

## Features

- **PDF OCR Extraction**: Extracts patient name, date of birth, and key lab results with their warnings from scanned discharge notes.
- **Audio Transcription**: Records audio from your microphone and transcribes it using OpenAI's Whisper model.
- **Outputs**: Structured JSON for clinical data, raw OCR text, audio WAV files, and transcript text files.

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

Developed by Ege Gursel for WinFully On Technologies' Summer 2025 AI/ML Internship Application.
