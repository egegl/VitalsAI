import logging
import sounddevice as sd
import soundfile as sf
import whisper
from pathlib import Path

total_duration = 30

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ensure_output_dir():
    # Check if the output directory exists
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def record_audio(duration=total_duration, sample_rate=44100):
    # Record audio from microphone
    logger.info(f"Recording {duration} seconds of audio...")
    try:
        # Record audio in one go
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='float32'
        )

        # Wait until recording is finished
        sd.wait()
        logger.info(f"Finished recording {duration} seconds of audio")
        return recording, sample_rate
    except Exception as e:
        logger.error(f"Error recording audio: {e}")
        raise

def save_audio(recording, sample_rate, output_path):
    # Save recorded audio to WAV file
    logger.info(f"Saving audio to {output_path}")
    try:
        sf.write(output_path, recording, sample_rate)
    except Exception as e:
        logger.error(f"Error saving audio: {e}")
        raise

def transcribe_audio(audio_path):
    # Transcribe audio using Whisper
    logger.info("Loading Whisper model")
    try:
        # Load Whisper model
        model = whisper.load_model("base")

        # Transcribe audio
        logger.info("Transcribing audio")
        result = model.transcribe(str(audio_path))
        
        return result["text"]
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        raise

def save_transcript(text, output_path):
    # Save transcription to text file
    logger.info(f"Saving transcript to {output_path}")
    try:
        with open(output_path, 'w') as f:
            f.write(text)
    except Exception as e:
        logger.error(f"Error saving transcript: {e}")
        raise

# Main method to record and transcribe audio
def main():
    try:
        # Check if output directory exists
        output_dir = ensure_output_dir()
        
        # Record and save audio
        recording, sample_rate = record_audio()
        audio_path = output_dir / "audio.wav"
        save_audio(recording, sample_rate, audio_path)
        
        # Transcribe audio and save transcript
        transcript = transcribe_audio(audio_path)
        transcript_path = output_dir / "transcript.txt"
        save_transcript(transcript, transcript_path)
        
        logger.info("Audio recording and transcription completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in process: {e}")
        raise

if __name__ == "__main__":
    main() 