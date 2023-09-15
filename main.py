import streamlit as st 
import PIL as pillow
from PIL import Image
import json
import os
import datetime

from clinical_data import clinical, add_clinical_data 
from demographics_extraction import demographical_data_extractor,demographical_document_extractor
from display_pdf import convert_pdf_to_images
from self_certification import fill_form_with_data

import fillpdf
from fillpdf import fillpdfs

#------------------------------------------------------------------------------------------------------------------
import pymongo as py
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data_ssp"
clinical_data_db=myclient["clinical_data_ssp"]
clinical_data_collection=clinical_data_db["clinical_data"]

page_icon_img=Image.open(os.path.join("images","Sick-employees.jpeg"))

#this function allows to add the page title and icon
st.set_page_config(page_title="Self Certification Form", page_icon=page_icon_img, layout="centered", initial_sidebar_state="expanded")

home_image=Image.open(os.path.join("images","My project.png"))
st.image(home_image)
st.write('#')

phone_number="+21655303276"

demographic_doc=demographical_document_extractor(phone_number)
if (len(demographic_doc)!=0):
    #demographic data extraction function:

    uuid=demographic_doc["uuid"]
    phone_number=demographic_doc["phone_number"]
    json_object_demographic_data=demographic_doc["demographic_data"]
    first_name,surname,title,birthday,national_insurance,clock_payroll=demographical_data_extractor(json_object_demographic_data)

    #Receiving clinical data from filled form
    clinical_description,problem_diagnosis_name,last_date_of_work,sickness,time_of_finishing_work,date_of_resolution,date_of_sickness_beginning=clinical()

    #Here we will check if we should move forward or there are missing values: 
    if(len(clinical_description)>0 and len(problem_diagnosis_name)>0):
        
        #This is a json file containing standard clinical data in the OpenEHR standards form
        full_path_clinical_data = 'diagnosis-workfit.v0_20230808104544_000001_1.json'
        #Demographic data file:
        with open(full_path_clinical_data, 'r') as openfile:
            # Reading from json file
            json_object_clinical_data = json.load(openfile)
        
        #Here we add the clinical data to "json_object_clinical_data", which is a dict that will be saved in database 
        json_object_clinical_data=add_clinical_data(json_object_clinical_data,clinical_description,problem_diagnosis_name,last_date_of_work,sickness,time_of_finishing_work,date_of_resolution,date_of_sickness_beginning)
        
        # Define field values
        field_values = fill_form_with_data(phone_number,first_name,surname,title,birthday,national_insurance,clock_payroll,problem_diagnosis_name,clinical_description,date_of_sickness_beginning,last_date_of_work,time_of_finishing_work,sickness,date_of_resolution)
        
        #Here we will generate the pdf:
        
            # Input PDF file and output flattened PDF file
        input_pdf_path = 'self-certificate-form-editable.pdf'
        non_flattened_pdf='non_flattened_pdf.pdf'
        output_pdf_path ='filled_form_flattened.pdf'

        #adding data to pdf
        fillpdfs.write_fillable_pdf(input_pdf_path, non_flattened_pdf, field_values,flatten=False)
        #flattening the pdf
        fillpdfs.flatten_pdf(non_flattened_pdf, output_pdf_path)

        #Here we will display the pdf as images:
        convert_pdf_to_images(output_pdf_path)
        st.write("#")

        with open(output_pdf_path, "rb") as file:
            pdf_contents = file.read()

        st.markdown(
        "<h1 style='font-size: 170%;text-align: center; color: #0B5345;'>You can save this patient's clinical data from here:  </h1>", 
        unsafe_allow_html = True
        )
        st.write("#")

        col1, col2, col3 = st.columns([4,2,3])
        with col2:    
            #This is a download button that allows to download the created new treatment file 
            download_button = st.download_button('Download', data=pdf_contents, file_name="filled_form_flattened.pdf")
        if (download_button):
            
            my_doc={"uuid":uuid,
                    "phone_number":phone_number,
                    "date":"<"+str(datetime.date.today())+">",
                    "clinical_data":json_object_clinical_data
                    }

            clinical_data_collection.insert_one(my_doc)

            st.write("#")
            st.success(": File saved well" ,icon="✅")
            
    else:
        st.write("#")
        st.error(": One of the values you entered is invalid, Please check them carefully!",icon="⛔")

else:
    st.write("#")
    st.error(": There is no user with this phone number in the demographic database!",icon="⛔")

#---------------------------------------------------------------------------------------------------------------
def decryption(encrypted_value):
    from nacl.secret import SecretBox
    import base64

    # Generate a random key
    key = b'\x009Rt\x8d\x93\x1a\xb23\xcdz\xe6\xea8f\xeb\xc3e\xd2-\xeaG\xb0\x92\x04\xc6\x85p\xeb&\xe7\xf0'
    box = SecretBox(key)

    ciphertext=base64.b64decode(encrypted_value)

    original_value = box.decrypt(ciphertext).decode('ascii')

    print("decryption done successfully!\n")
    return(original_value)