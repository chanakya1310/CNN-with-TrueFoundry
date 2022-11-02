import base64
import pickle
import tempfile
from io import BytesIO, StringIO

import numpy as np
import requests
from PIL import Image

import streamlit as st

st.title("Dog or Cat Classifier")
st.write(
    """
Upload an image to get to know whether it's a dog or a cat!!
"""
)

request_url = ""

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    bytes_data = uploaded_file.getvalue()

    stream = BytesIO(bytes_data)
    image = Image.open(stream)
    st.image(image, caption="Selected Picture")

    url = "https://cat-dog-classifier-chanakya-beta-ws.tfy-ctl-euwe1-develop.develop.truefoundry.tech/predict/image"
    ## URL returned by deploying the service

    img = base64.b64encode(bytes_data)
    obj = {"data": img.decode("utf-8"), "convert": True}

    x = requests.post(url, json=obj)

    st.write("Image is of a" + x.text)
