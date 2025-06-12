from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from spleeter.separator import Separator
import os
import shutil
import uuid
from pathlib import Path


