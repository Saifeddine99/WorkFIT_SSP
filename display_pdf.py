import streamlit as st
import numpy as np
from PIL import Image

def convert_pdf_to_images(output_pdf_path):
    from pdf2image import convert_from_path 
    images=convert_from_path(output_pdf_path, poppler_path=r"C:\Program Files (x86)\poppler-23.08.0\Library\bin")
    x=1
    for image in images:
        img_name=f"image_{x}.jpeg"
        image.save(img_name,"JPEG")
        x+=1

    image1=Image.open("image_1.jpeg")
    image2=Image.open("image_2.jpeg")

    cola,colb,colc=st.columns([4,.25,4])
    with cola:
        st.image(image1, caption='First page', use_column_width=True)
    
    with colc:
        st.image(image2, caption='Second page', use_column_width=True)
    
    st.write("#")