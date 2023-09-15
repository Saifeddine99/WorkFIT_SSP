import streamlit as st
import json

import datetime

import data_dictionary

import uuid

import fillpdf
from fillpdf import fillpdfs

import pymongo as py

myclient=py.MongoClient("mongodb://localhost:27017")

#Relating data to "clinical_data_ssp"
clinical_data_db=myclient["clinical_data_ssp"]
clinical_data_collection=clinical_data_db["clinical_data"]

#Relating data to "demographic_data_ssp"
demographic_data_db=myclient["demographic_data_ssp"]
demographic_data_collection=demographic_data_db["demographic_data"]

#----------------------------------------------------------------------------------------------------------------
def self_certif(uid):
    st.markdown("<h1 style='text-align: center; color: #0d325c;'>SELF CERTIFICATION FORM (SSP)</h1>", unsafe_allow_html = True)
    st.write('#')
    st.write('#')


    downloaded_well="undone"
    if (clinical_data_collection.find_one({"_id": uid}) and demographic_data_collection.find_one({"_id": uid})):

        clinical_data = clinical_data_collection.find_one({"_id": uid},{"clinical_data": 1})

        problem_diagnosis_name,clinical_description,date_of_sickness_beginning,last_date_of_work,time_of_finishing_work,sickness,date_of_resolution=clinical_data_extractor(clinical_data)

        demographic_data = demographic_data_collection.find_one({"_id": uid},{"demographic_data": 1})
        phone_number,country_code,first_name,surname,title,birthday,national_insurance,clock_payroll=demographical_data_extractor(demographic_data)


        # Define field values
        field_values = fill_form_with_data(phone_number,first_name,surname,title,birthday,national_insurance,clock_payroll,problem_diagnosis_name,clinical_description,date_of_sickness_beginning,last_date_of_work,time_of_finishing_work,sickness,date_of_resolution)

        # Input PDF file and output flattened PDF file
        input_pdf_path = 'self-certificate-form-editable.pdf'
        non_flattened_pdf='non_flattened_pdf.pdf'
        output_pdf_path ='filled_form_flattened.pdf'

        fillpdfs.write_fillable_pdf(input_pdf_path, non_flattened_pdf, field_values,flatten=False)
        fillpdfs.flatten_pdf(non_flattened_pdf, output_pdf_path)
        
        #convert_pdf_to_images(output_pdf_path)

        with open(output_pdf_path, "rb") as file:
            pdf_contents = file.read()

        st.markdown(
        "<h1 style='font-size: 170%; text-align: center; color: #0B5345;'>Your pdf form is filled successfully! Click on the 'Download' button below to get it </h1>", 
        unsafe_allow_html = True
        )
        col1, col2, col3 = st.columns([4,2,3])
        with col2:
            
            #This is a download button that allows to download the created new treatment file 
            st.write("#")
            download_button = st.download_button('Download', data=pdf_contents, file_name="filled_form_flattened.pdf")
        
        if (download_button):
            st.write("#")
            st.success(": File saved well" ,icon="✅")
            downloaded_well="done"


    else:
        if clinical_data_collection.find_one({"_id": uid})==None :
            st.warning(": fill your clinical data form",icon="⚠️")
        if demographic_data_collection.find_one({"_id": uid})==None :
            st.warning(": fill your demographical data form",icon="⚠️")


    return(downloaded_well)
#---------------------------------------------------------------------------------------------------------------

def fill_form_with_data(phone_number,first_name,surname,title,birthday,national_insurance,clock_payroll,problem_diagnosis_name,clinical_description,date_of_sickness_beginning,last_date_of_work,time_of_finishing_work,sickness,date_of_resolution):

    data=data_dictionary.data_dict

    #printing the surname
    data["Surname"]=surname
    #printing the first name
    data["First names"]=first_name
    #printing the title
    data["Title  enter MR MRS MISS MS or other title"]=title

    #printing the national insurance number
    while(len(national_insurance)<9):
        national_insurance='0'+national_insurance
    data["National Insurance number1"]=national_insurance[0]
    data["National Insurance number2"]=national_insurance[1]
    data["National Insurance number3"]=national_insurance[2]
    data["National Insurance number4"]=national_insurance[3]
    data["National Insurance number5"]=national_insurance[4]
    data["National Insurance number6"]=national_insurance[5]
    data["National Insurance number7"]=national_insurance[6]
    data["National Insurance number8"]=national_insurance[7]
    data["National Insurance number9"]=national_insurance[8]

    #printing the birthdate
    data["Date of birth1"]=birthday[8]
    data["Date of birth2"]=birthday[9]
    data["Date of birth3"]=birthday[5]
    data["Date of birth4"]=birthday[6]
    data["Date of birth5"]=birthday[0]
    data["Date of birth6"]=birthday[1]
    data["Date of birth7"]=birthday[2]
    data["Date of birth8"]=birthday[3]
    #printing the Clock or payroll number
    while(len(clock_payroll)<14):
        clock_payroll='0'+clock_payroll
    data["payroll number 1"]=clock_payroll[0]
    data["payroll number 2"]=clock_payroll[1]
    data["payroll number 3"]=clock_payroll[2]
    data["payroll number 4"]=clock_payroll[3]
    data["payroll number 5"]=clock_payroll[4]
    data["payroll number 6"]=clock_payroll[5]
    data["payroll number 7"]=clock_payroll[6]
    data["payroll number 8"]=clock_payroll[7]
    data["payroll number 9"]=clock_payroll[8]
    data["payroll number 10"]=clock_payroll[9]
    data["payroll number 11"]=clock_payroll[10]
    data["payroll number 12"]=clock_payroll[11]
    data["payroll number 13"]=clock_payroll[12]
    data["payroll number 14"]=clock_payroll[13]

    #printing the Problem_diognisis_name
    data['Problem_diognisis_name']=problem_diagnosis_name

    #printing the clinical description
    data["clinical_description"]=clinical_description

    #printing the date of sickness beginning
    data["sickness beginning1"]=date_of_sickness_beginning[8]
    data["sickness beginning2"]=date_of_sickness_beginning[9]
    data["sickness beginning3"]=date_of_sickness_beginning[5]
    data["sickness beginning4"]=date_of_sickness_beginning[6]
    data["sickness beginning5"]=date_of_sickness_beginning[0]
    data["sickness beginning6"]=date_of_sickness_beginning[1]
    data["sickness beginning7"]=date_of_sickness_beginning[2]
    data["sickness beginning8"]=date_of_sickness_beginning[3]

    #printing date of sickness end:
    #printing date of sickness end:
    if(date_of_resolution!="no"):
        data["sickness end1"]=date_of_resolution[8]
        data["sickness end2"]=date_of_resolution[9]
        data["sickness end3"]=date_of_resolution[5]
        data["sickness end4"]=date_of_resolution[6]
        data["sickness end5"]=date_of_resolution[0]
        data["sickness end6"]=date_of_resolution[1]
        data["sickness end7"]=date_of_resolution[2]
        data["sickness end8"]=date_of_resolution[3]
    else:
        data["sickness end1"]=""
        data["sickness end2"]=""
        data["sickness end3"]=""
        data["sickness end4"]=""
        data["sickness end5"]=""
        data["sickness end6"]=""
        data["sickness end7"]=""
        data["sickness end8"]=""

    #printing the date of last work before the sickness began
    data["last_date_of_work_1"]=last_date_of_work[8]
    data["last_date_of_work_2"]=last_date_of_work[9]
    data["last_date_of_work_3"]=last_date_of_work[5]
    data["last_date_of_work_4"]=last_date_of_work[6]
    data["last_date_of_work_5"]=last_date_of_work[0]
    data["last_date_of_work_6"]=last_date_of_work[1]
    data["last_date_of_work_7"]=last_date_of_work[2]
    data["last_date_of_work_8"]=last_date_of_work[3]

    #Printing the time of leaving work on that date
    data["enter time in 24 hours"]=time_of_finishing_work

    #printing info about whether sickness ir related to work or not
    if(sickness=='No'):
        data["Check Box5"]="Yes"
        data["Check Box6"]=""
    else:
        data["Check Box5"]=""
        data["Check Box6"]="Yes"

    #printing the current date
    date=str(datetime.date.today())
    data["date1"]=date[8]
    data["date2"]=date[9]
    data["date3"]=date[5]
    data["date4"]=date[6]
    data["date5"]=date[0]
    data["date6"]=date[1]
    data["date7"]=date[2]
    data["date8"]=date[3]

    #printing the phone number
    data["Phone number"]=phone_number
       
    return(data)

#---------------------------------------------------------------------------------------------------------------

def clinical_data_extractor(json_object_clinical_data):

    problem_diagnosis_name=json_object_clinical_data["clinical_data"]["content"][0]["data"]["items"][0]["value"]["value"]
    clinical_description=json_object_clinical_data["clinical_data"]["content"][0]["data"]["items"][1]["value"]["value"]
    date_of_sickness_beginning=json_object_clinical_data["clinical_data"]["content"][0]["data"]["items"][2]["value"]["value"] #What date did your sickness begin? 
    last_date_of_work=json_object_clinical_data["clinical_data"]["content"][0]["data"]["items"][4]["value"]["value"]
    time_of_finishing_work=json_object_clinical_data["clinical_data"]["content"][0]["data"]["items"][5]["value"]["value"]
    sickness=json_object_clinical_data["clinical_data"]["content"][0]["data"]["items"][6]["value"]["symbol"]["value"]
    date_of_resolution=json_object_clinical_data["clinical_data"]["content"][0]["data"]["items"][11]["value"]["value"]#date of end of sickness

    return(problem_diagnosis_name,clinical_description,date_of_sickness_beginning,last_date_of_work,time_of_finishing_work,sickness,date_of_resolution)

#------------------------------------------------------------------------------------------------------------------

def demographical_data_extractor(json_object_demographic_data):


    phone_number=json_object_demographic_data["demographic_data"]["contacts"][0]["addresses"][2]["details"]["items"][0]["value"]["value"]
    country_code=json_object_demographic_data["demographic_data"]["contacts"][0]["addresses"][2]["details"]["items"][1]["value"]["value"]
    first_name=json_object_demographic_data["demographic_data"]["identities"][0]["details"]["items"][0]["value"]["value"]
    surname=json_object_demographic_data["demographic_data"]["identities"][0]["details"]["items"][1]["value"]["value"]
    title=json_object_demographic_data["demographic_data"]["identities"][0]["details"]["items"][2]["value"]["value"]
    birthday=json_object_demographic_data["demographic_data"]["identities"][0]["details"]["items"][3]["value"]["value"]
    national_insurance=str(json_object_demographic_data["demographic_data"]["identities"][0]["details"]["items"][6]["value"]["value"])
    clock_payroll=str(json_object_demographic_data["demographic_data"]["identities"][0]["details"]["items"][7]["value"]["value"])

    return(phone_number,country_code,first_name,surname,title,birthday,national_insurance,clock_payroll)
