
import asyncio
from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import numpy as np
from typing import Dict
import cv2

from scipy import signal
import random


import openai





app = FastAPI()
frame_queue = asyncio.Queue()


templates = Jinja2Templates(directory="templates")


class ResultData(BaseModel):
    HR: int
    stiffnessIndex: float
    reflectionIndex: float
    augmentationIndex: float
    crestTime: float
    crestTimeRatio: float
    E_A: float
    vascularAging: float
    perfusionIndex: float


class ProcessingResult(BaseModel):
    status: str
    data: ResultData


class VitalSignsData(BaseModel):
    data: Dict[str, object]


class HeightData(BaseModel):
    height: float


async def process_frames():

    while True:
        # print("hehehe")
        frame_bytes = await frame_queue.get()
        # print('processing from queue')
        

        return JSONResponse(content={'status': 'ok'})


@app.get('/')
async def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.post('/store_height')
async def store_height(height_data: HeightData):
    app.state.user_height = height_data.height
    return {"status": "success"}


@app.get('/home')
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get('/result')
async def result(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})


@app.post('/process_video', response_model=ProcessingResult)
async def process_video(background_tasks: BackgroundTasks, frame: UploadFile = File(...)):
    if not hasattr(app.state, 'frameCount'):
        app.state.frameCount = 0
    frame_bytes = await frame.read()
    await frame_queue.put(frame_bytes)
    app.state.frameCount += 1

    if not hasattr(app.state, 'processing_task'):
        background_tasks.add_task(process_frames)

    return JSONResponse(content={'status': 'ok'})


@app.post('/processing_complete')
async def processing_complete():
    sec=30
    

   
    del app.state.frameCount

    # Calculating rPPG
    height=app.state.user_height
    del app.state.user_height
    
    # print(HRV)
    data = {
        'height':height

    }
    return {"status": "success", "data": data}
