from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from spleeter.separator import Separator
import os
import shutil
import uuid
from pathlib import Path

app = FastAPI(title="Vocal Extraction API", description="API to extract vocals from audio files", version="1.0")


async def extract_vocals(input_audio_path: str, output_directory: str) -> str:
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

    return output_vocal_path

@app.get("/")
async def root():
    return {"message": "Welcome to Vocal Extraction API!"}
