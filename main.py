import librosa
import soundfile as sf
from spleeter.separator import Separator
import os


def extract_vocals(input_audio_path, output_directory):
    separator = Separator('spleeter:2stems')

    os.makedirs(output_directory, exist_ok=True)

    separator.separate_to_file(
        input_audio_path,
        output_directory,
        codec='wav',
        filename_format='{filename}_vocals.{codec}'
    )

    filename = os.path.splitext(os.path.basename(input_audio_path))[0]
    output_vocal_path = os.path.join(output_directory, f"{filename}_vocals.wav")

    print(f"Vocals extracted and saved to: {output_vocal_path}")

def main():
    input_audio = "music-with-beat.mp3"
    output_dir = "output_vocals"

    if not os.path.exists(input_audio):
        print(f"Error: Input file {input_audio} not found.")
        return

    extract_vocals(input_audio, output_dir)

if __name__ == "__main__":
    main()
