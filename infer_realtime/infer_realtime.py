import base64
import io
import os
import pickle
from io import BytesIO, StringIO
from typing import List

import mlfoundry
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, Request, UploadFile
from PIL import Image
from pydantic import BaseModel, Field
from tensorflow.keras.preprocessing import image

MODEL_VERSION_FQN = os.getenv("MLF_MODEL_VERSION_FQN")


class Data(BaseModel):
    data: bytes


client = mlfoundry.get_client(
    tracking_uri="https://app.develop.truefoundry.tech/",
    api_key="<YOUR API KEY HERE>",
)
model_version = client.get_model(MODEL_VERSION_FQN)
model = model_version.load()

app = FastAPI(docs_url="/")


async def parse_input(request: Request):
    data: bytes = await request.body()
    return data


@app.get("/test")
async def testing():
    return "Hello World"


@app.post("/predict/image")
async def predict_api(data: Data):

    classifier = model

    img = base64.b64decode((data.data))
    stream = BytesIO(img)
    img = Image.open(stream)
    
    test_img = img.resize((200, 200))

    test_img = image.img_to_array(test_img)
    test_img = np.expand_dims(test_img, axis=0)
    result = classifier.predict(test_img)

    if result[0][0] == 1:
        prediction = "dog"
    else:
        prediction = "cat"

    return prediction
