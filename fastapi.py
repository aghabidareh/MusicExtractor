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


@app.post("/extract-vocals/", response_class=FileResponse)
async def extract_vocals_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.mp3', '.wav')):
        raise HTTPException(status_code=400, detail="Only MP3 or WAV files are supported.")

    temp_dir = Path(f"temp_{uuid.uuid4()}")
    output_dir = temp_dir / "output_vocals"
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        temp_audio_path = temp_dir / file.filename
        with temp_audio_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        output_vocal_path = await extract_vocals(str(temp_audio_path), str(output_dir))

        if not os.path.exists(output_vocal_path):
            raise HTTPException(status_code=500, detail="Vocal extraction failed.")

        return FileResponse(
            path=output_vocal_path,
            filename=f"{Path(file.filename).stem}_vocals.wav",
            media_type="audio/wav"
        )

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


@app.get("/")
async def root():
    return {"message": "Welcome to Vocal Extraction API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
