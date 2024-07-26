import os
from typing import List, Tuple

import torch
import whisper
import torchaudio
from gtts import gTTS


device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)

def load_audio(audio_path: str) -> Tuple[torch.Tensor, int]:
    """
    Load an audio file from the specified path and return the waveform and sample rate.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        waveform (Tensor): Tensor containing the audio waveform.
        sample_rate (int): Sample rate of the audio.
    """
    waveform, sample_rate = torchaudio.load(audio_path)
    return waveform, sample_rate

def create_audio_chunks(waveform: torch.Tensor, total_duration: float, sample_rate: int, 
                        chunk_duration: int = 30) -> Tuple[List[torch.Tensor], int]:
    """
    Divide the audio waveform into chunks of specified duration.

    Args:
        waveform (Tensor): Tensor containing the audio waveform.
        total_duration (float): Total duration of the audio in seconds.
        sample_rate (int): Sample rate of the audio.
        chunk_duration (int, optional): Duration of each chunk in seconds. Default is 30 seconds.

    Returns:
        chunks (list): List of tensors, each containing a chunk of the audio.
        sample_rate (int): Sample rate of the audio.
    """
    chunks = []
    for start in range(0, int(total_duration), chunk_duration):
        end = min(start + chunk_duration, total_duration)
        chunk_waveform = waveform[:, int(start * sample_rate):int(end * sample_rate)]
        chunks.append(chunk_waveform)
    return chunks, sample_rate

def transcribe_with_whisper(audio_path: str) -> str:
    """
    Transcribe the audio file using the Whisper model.

    Args:
        model (Model): Whisper model instance.
        device (str): Device to use for processing ('cpu' or 'cuda').
        audio_path (str): Path to the audio file.

    Returns:
        str: Transcribed text from the audio.
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"The file {audio_path} does not exist.")
    else:
        waveform, sample_rate = load_audio(audio_path)
        total_duration = waveform.size(1) / sample_rate

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available. Please check your CUDA installation.")

    if total_duration <= 45:
        waveform = waveform.to(device)

        # Whisper expects audio to be resampled to 16000 Hz
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000).to(device)
        waveform = resampler(waveform)

        audio_tensor = waveform.squeeze(0).cpu().numpy()  # Whisper expects a 1D numpy array
        options = {"fp16": False, "language": None, "task": "transcribe"}
        result = model.transcribe(audio_tensor, **options)
        
        return result['text']
    else:
        chunks, sample_rate = create_audio_chunks(waveform, total_duration, sample_rate)
    
        # Whisper expects audio to be resampled to 16000 Hz
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000).to(device)
        transcriptions = []
    
        for chunk in chunks:
            chunk = chunk.to(device)
            chunk = resampler(chunk)
            
            with torch.cuda.amp.autocast():
                audio_tensor = chunk.squeeze(0).cpu().numpy()  # Whisper expects a 1D numpy array
                result = model.transcribe(audio_tensor)
                transcriptions.append(result['text'])
    
            torch.cuda.empty_cache()  # Release GPU memory
    
        return " ".join(transcriptions)

def create_audio(text: str, file_path: str = 'data/audio_storage/response.ogg') -> str:
    """
    Convert text to speech and save it as an audio file.

    Args:
        text (str): Text to convert to speech.
        file_path (str, optional): Path to save the audio file. Default is 'data/audio_storage/response.ogg'.

    Returns:
        str: Path to the saved audio file.
    """
    tts = gTTS(text=text, lang='en')
    tts.save(file_path)  # Save the audio file
    return file_path
