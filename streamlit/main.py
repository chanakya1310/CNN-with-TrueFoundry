import base64
import pickle
import tempfile
from io import BytesIO, StringIO
import io
import json
from json import JSONEncoder

import numpy as np
import requests
from PIL import Image
import numpy as np
import streamlit as st

def predict(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img = img_byte_arr.getvalue()

    img = base64.b64encode(img)

    obj = {"data": img.decode("utf-8")}

    x = requests.post(request_url, json=obj)
    return "Image is of a " + str(x.text)


st.title("Dog or Cat Classifier")
st.write(
    """
Upload an image to get to know whether it's a dog or a cat!!
"""
)


request_url = "https://cat-dog-classifier-chanakya-beta-ws.tfy-ctl-euwe1-develop.develop.truefoundry.tech/predict/image"

st.header("Sample Image")
img = Image.open("sample_image1.jpg")
img = img.resize((300, 300))
st.image(img)

cap_button = st.button("Predict") # Give button a variable name
if cap_button: # Make button a condition.
    ptext = predict(img)
    st.text(ptext)

st.header("Upload an image")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    bytes_data = uploaded_file.getvalue()

    stream = BytesIO(bytes_data)
    image = Image.open(stream)
    image = image.resize((300, 300))
    st.image(image, caption="Selected Picture")

    url = "https://cat-dog-classifier-chanakya-beta-ws.tfy-ctl-euwe1-develop.develop.truefoundry.tech/predict/image"
    ## URL returned by deploying the service

    img = base64.b64encode(bytes_data)
    obj = {"data": img.decode("utf-8"), "convert": True}

    x = requests.post(url, json=obj)

    st.write("Image is of a" + str(x.text))
