from .Extract_Aadhar_Data import *
from .Extract_Driving_License import *
from .Extract_Pan_Data import *
from .Extract_Passport_Data import *

import base64
from base64 import b64decode
from io import BytesIO
import datetime
from dateutil import parser
from pprint import pprint

class InputFileHandler():
    
  
    def Extract_Data(self,doc_type,text):
        """
          Extracts the required fields of the given doc type from the list of ocr strings and returns the result dictionary
          input: doctype(int value) and list of ocr strings(text)
          output: dictionary with required fieldnames mapped to their extracted values  
        """
        try:
            extract_aadhar_obj=Extract_Aadhar_Data()
            extract_DrivingLicence_obj=Extract_Driving_License()
            extract_pan_obj=Extract_Pan_Data()
            extract_passport_obj=Extract_Passport_Data()
            
            Extracted_data = {}
            if doc_type == 0:
                Extracted_data = extract_aadhar_obj.get_aadhar_data(text)
            elif doc_type == 1:
                Extracted_data = extract_DrivingLicence_obj.get_DrivingLicence_data(text)
            elif doc_type == 2:
                Extracted_data = extract_pan_obj.get_pan_data(text)
            elif doc_type == 3:
                Extracted_data = extract_passport_obj.get_passport_data(text)
            return Extracted_data
        except Exception as e:
            print("Exception as Extract_Data in InputFileHandler",str(e))
            return ""

    def identify_document_name(self,mode_value):
      """
        returns name of document based on input mode value
      """
      try:
        doc_name_dict={
          0:"Aadhar",
          1:"Driving Licence",
          2:"Pan Card",
          3:"Passport"
        }
        doc_name=doc_name_dict[mode_value] if mode_value in doc_name_dict else "Invalid File"
        return doc_name
      except Exception as e:
          print("Exception in identify_document_name method in InputFileHandler",str(e))
          return "Invalid File"

    def detect_reference_elements(self,reference_elements,result_dict):
      """
        checks if the reference elements exist in the result dict
      """
      try:
        all_elements_exist=True
        reference_elements_list=reference_elements.replace("[","").replace("]","").replace("\"","").split(",")
        for field_name in reference_elements_list:
          if field_name not in result_dict.keys() or (field_name in result_dict.keys() and result_dict[field_name]=="") :
            all_elements_exist=False
            break
        return all_elements_exist

      except Exception as e:
          print("Exception in detect_reference_elements method in InputFileHandler",str(e))
          return True

    def return_only_reference_elements(self,reference_elements,result_dict):
      """
        returns only the selected reference elements from the result dictionary 
        containing all elements
      """
      try:
        
        reference_elements_list=reference_elements.replace("[","").replace("]","").replace("\"","").split(",")
        final_dict={}
        for field_name in reference_elements_list:
          if field_name in result_dict.keys():
            final_dict[field_name]=result_dict[field_name]
        return final_dict

      except Exception as e:
          print("Exception in return_only_reference_elements method in InputFileHandler",str(e))
          return {}

    def decide_card(self,text_tag):
      """
      mode values for each id type are as follows:
        aadhaar=0
        drivers_licence=1
        pan_card=2
        passport=3
      """
      try:
        extract_aadhar_obj=Extract_Aadhar_Data()
        extract_DrivingLicence_obj=Extract_Driving_License()
        extract_pan_obj=Extract_Pan_Data()
        extract_passport_obj=Extract_Passport_Data()
        
        
        Driving_ID_regex = "^(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}"+"|([a-zA-Z]{2}[0-9]{2}[\\/][a-zA-Z]{3}[\\/][0-9]{2}[\\/][0-9]{5})"+"|([a-zA-Z]{2}[0-9]{2}(N)[\\-]{1}((19|20)[0-9][0-9])[\\-][0-9]{7})"+"|([a-zA-Z]{2}[0-9]{14})"+"|([a-zA-Z]{2}[\\-][0-9]{13})$"
        
        drivers_license_data=extract_DrivingLicence_obj.match_pattern_drive(Driving_ID_regex,'ID',text_tag)
        print("driving-------1111----------------",drivers_license_data)
        aadhar_data=extract_aadhar_obj.find_aadhar_number(text_tag)
        print("aadhaar-------2222----------------",aadhar_data)
        pan_data=extract_pan_obj.findPanCardNo(text_tag)
        print("pan_data-------3333----------------",pan_data)
        passport_data=extract_passport_obj.find_passport_no(text_tag)
        print("passport_data-------4444----------------",passport_data)
        passport_keyword_exists= extract_passport_obj.passport_keyword_exists(text_tag)
        print("passport_keyword-------5555----------------",passport_keyword_exists)
        uidai_keyword_exists=extract_aadhar_obj.is_aadhar_back(text_tag) ##in some case aadhaar back has no aadhaar id but can be identified by uidai.gov.in keyword
        mode_value=-1
        if (aadhar_data is not None and aadhar_data!="") or (uidai_keyword_exists==True):
          print("IT IS AN AADHAAR CARD!!!!")
          mode_value=0
        elif drivers_license_data is not None and drivers_license_data!="":
          print("IT IS AN DRIVING LICENSE!!!!")
          mode_value=1
        elif pan_data is not None and pan_data!="":
          print("IT IS AN PAN DATA!!!!")
          mode_value=2
        elif (passport_data is not None and passport_data!="") or (passport_keyword_exists==True):
          print("IT IS AN PASSPORT DATA!!!!")
          mode_value=3
        else:
          mode_value=-1
        
        print("mode value---------------",mode_value)
        return mode_value
      except Exception as e:
            print("Exception as decide_card in InputFileHandler",str(e))
            return ""

    
    # def populate_response(self,result_dict):  ##TODO remove later       #,reference_id,created_date_time):
    #   """
    #   populate json response when status is successful
    #   """
    #   try:
    #     reference_id=""
    #     created_date_time=""
    #     results = {
    #               'ReferenceID':reference_id,
    #               'status':'Success',
    #               "statusCode": "",
    #               'createdDateTime':created_date_time, #
    #               'lastUpdatedDateTime':datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    #               'Modelversion':"",      
    #               'api_version' :"",      
    #               'Data' : [result_dict]
    #               }
    #     return results
    #   except Exception as e:
    #         print("Exception as populate_response in InputFileHandler",str(e))
    #         return ""


    
    def date_parse(self,date_text):
        """
        input:date field of dictionary
        output: Date in parsed format 
        """
        try:
            orig=date_text
            date_text=date_text.replace(".","-")
            date_text=re.sub('[^A-Za-z0-9-/]+', '', date_text)
            dic = {1:"JAN",
                    2:"FEB",
                    3:"MAR",
                    4:"APR",
                    5:"MAY",
                    6:"JUN",
                    7:"JUL",
                    8:"AUG",
                    9:"SEP",
                    10:"OCT",
                    11:"NOV",
                    12:"DEC"}
            date = ""
            if len(date_text)>0:
                try:
                    date = parser.parse(date_text, dayfirst=True)
                    date = str(date.day)+'-'+str(dic[date.month])+'-'+str(date.year)
                except:
                    date = orig
                return date
            else:
                return orig
        except Exception as e:
            print("Error ocurred while parsing InvoiceDate:\n%s" % str(e))
            return orig

    def check_date_field(self,result_dict,mode_value):
      """
        checks if the fields extracted from the uploaded file have valid dates that are less than the current datetime
        output: boolean (true if the extracted datefield is less than currentdatetime else false)
      """
      try:  
        
        has_valid_date_field=True
        date_field_map={
                    0:["DoB"], ##aadhaar dates
                    1:["Issue Date"],##driving license dates
                    2:["DoB"],  ##pan_data dates
                    3:["DoB","Issue Date"] #,"Expiry Date"] #passport_data dates
                  }
        date_fields_list=date_field_map[mode_value]
        present_date_parsed=self.date_parse(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
        present_year=int(present_date_parsed[-4:])
        
        for date_field in date_fields_list:
          if date_field in result_dict and result_dict[date_field]!="":
            date_value_parsed=self.date_parse(result_dict[date_field])
            date_field_year=int(date_value_parsed[-4:]) if (date_value_parsed!="" and len(date_value_parsed)>4) else ""
            if (date_field_year!="" and date_field_year>present_year):  ##if the date on the document is more than the present date then its an invalid date===> and invalid file 
              has_valid_date_field=False
              break
        return has_valid_date_field          
      except Exception as e:
            print("Exception as check_date_field in InputFileHandler",str(e))
            return ""