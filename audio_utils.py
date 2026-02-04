import subprocess
import os

def convert_mp3_to_wav(mp3_path: str) -> str:
    """
    Convert MP3 to WAV using ffmpeg (mono, 16kHz).
    Returns the WAV file path.
    """
    wav_path = mp3_path.replace(".mp3", ".wav")

    command = [
        "ffmpeg",
        "-y",
        "-i", mp3_path,
        "-ac", "1",
        "-ar", "16000",
        wav_path
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    return wav_path
