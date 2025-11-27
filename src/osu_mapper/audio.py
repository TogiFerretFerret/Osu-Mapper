import librosa
import numpy as np

def extract_features(audio_path: str) -> np.ndarray:
    """
    Loads an audio file and extracts features (e.g., a spectrogram).

    Args:
        audio_path: Path to the audio file.

    Returns:
        A numpy array containing the audio features.
    """
    # TODO: Experiment with different audio features (MFCCs, Chroma, etc.)
    print(f"Extracting features from {audio_path}...")
    
    try:
        y, sr = librosa.load(audio_path, sr=None)
        
        # As a starting point, let's use a Mel-spectrogram
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        
        # Convert to log scale (dB)
        log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
        
        return log_mel_spectrogram

    except Exception as e:
        print(f"Error processing audio file {audio_path}: {e}")
        return np.array([])
