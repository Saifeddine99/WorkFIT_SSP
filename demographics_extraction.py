def demographical_document_extractor(phone_number):
    import pymongo as py
    myclient=py.MongoClient("mongodb://localhost:27017")
    #Relating data to "demographic_data_ssp"
    demographic_data_collection=myclient["demographic_data_ssp"]["demographic_data"]

    demographic_doc={}
    if demographic_data_collection.find_one({"phone_number": phone_number}):
        demographic_doc=demographic_data_collection.find_one({"phone_number": phone_number})

    return(demographic_doc)

#if this function returns an empty dict, it means this phone number is not found in the demographic data database.
#---------------------------------------------------------------------------------------------------------------
def demographical_data_extractor(json_object_demographic_data):    
    #extracting+decrypting data:
    first_name=json_object_demographic_data["identities"][0]["details"]["items"][0]["value"]["value"]
    surname=json_object_demographic_data["identities"][0]["details"]["items"][1]["value"]["value"]
    title=json_object_demographic_data["identities"][0]["details"]["items"][2]["value"]["value"]
    birthday=json_object_demographic_data["identities"][0]["details"]["items"][3]["value"]["value"]
    national_insurance=str(json_object_demographic_data["identities"][0]["details"]["items"][6]["value"]["value"])
    clock_payroll=str(json_object_demographic_data["identities"][0]["details"]["items"][7]["value"]["value"])

    return(first_name,surname,title,birthday,national_insurance,clock_payroll)

