import librosa
import numpy as np

def extract_mfcc_features(wav_path: str):
    """
    Load WAV file and extract MFCC features.
    Returns mean MFCC vector.
    """
    # Load audio
    y, sr = librosa.load(wav_path, sr=16000, mono=True)

    # Extract MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Take mean across time axis
    mfcc_mean = np.mean(mfccs, axis=1)

    return mfcc_mean
