import base64
from base64 import b64decode
import imghdr
from io import BytesIO
from datetime import datetime



def is_invalid_extension(encoded_string):  #DP_02
    """
        User is trying to upload 1 or more non-PDF or Image file
        error_code: DP_02 (Front End)
    """
    try:
        is_invalid_extension=False
        if encoded_string!="":
            decoded_string = b64decode(encoded_string)
            extension = imghdr.what(None, h=decoded_string)
            is_pdf = decoded_string[1:4] == b'PDF'
            is_invalid_extension=False if (extension in ["jpeg","jpg","png"] or is_pdf==True) else True
        return is_invalid_extension
    except Exception as e:
        print("Exception as is_invalid_extension",str(e))
        return False

def is_file_encrypted(encoded_string):  #DP_03
    """
        User has uploaded password protected file
        error code: DP_03 (Front End)
    """
    try:
        is_encrypted=False
        if encoded_string!="":
            decoded_string = base64.b64decode(encoded_string)
            is_pdf = decoded_string[1:4] == b'PDF'
            if is_pdf:
                is_encrypted = PyPDF2.PdfFileReader(BytesIO(decoded_string) ).isEncrypted
        return is_encrypted
    except Exception as e:
        print("Exception as is_file_encrypted",str(e))
        return False

def is_invalid_file_size(encoded_string):   #DP_04
    """
        User is trying to upload a file that is more than 1 MB in size
        error code: DP_04 (Front End) 
    """
    try:
        is_invalid_size=False
        if encoded_string!="":
            file_size_in_bytes = (len(str(encoded_string)) - 814) / 1.37
            file_size_in_mb=(file_size_in_bytes//1000)
            is_invalid_size=False if file_size_in_mb>0 and file_size_in_mb<4024 else True
        return is_invalid_size
    except Exception as e:
        print("Exception as is_invalid_file_size",str(e))
        return False
    
##DP_05 ==> technical error in code
##DP_06 ==> unclear pdf/image==> mode=-1



def populate_error_json(error_code,error_code_2,result_dict,request_data_dict):
    """
        populates the response json in specified format
        input: error code
        output: error message related to given error code + result dict with specified fields
    """
    try:
        error_msgs={
                        "DP_01":"Please choose only 2 or less than 2 files to upload",#FrontEnd
                        "DP_02":"Please choose only Image or PDF file to upload", #FrontEnd
                        "DP_03":"Unable to process the file please check the file that is uploaded", #FrontEnd
                        "DP_04":"File size cannot exceed 1 MB. Please choose a different file to upload", #FrontEnd
                        "DP_05":"Unable to process the file now. Please try again later.",
                        "DP_06":"An unsupported image(s) is detected in the file. Please try again with different file.",
                        "DP_07":"One of the files is of un-supported format. Please upload a different file", #FrontEnd
                        "DP_08":"Unable to detect the data you are trying to process. Please upload a different file.",
                        "DP_09":"Duplicate files detected. Processed the first file.",
                        "DP_10":"Processed successfully!",
                        "DP_11":"Detected files of more than one user. Processed only the first one.",
                        "DP_12":"Detected different document types. Successfully processed the expected document",
                        "DP_13":"Unable to detect the data you are trying to process. Please upload a different file.",
                        "DP_14":"Partial Success! Only few fields detected from the uploaded files.",
                        "DP_15":"Partial Success!",
                    }
        error_status={
                "DP_01":"Error",
                "DP_02":"Error",
                "DP_03":"Error",
                "DP_04":"Error",
                "DP_05":"Error",
                "DP_06":"Error",
                "DP_07":"Error",
                "DP_08":"Error",
                "DP_09":"Success",
                "DP_10":"Success",
                "DP_11":"Success",
                "DP_12":"Success",
                "DP_13":"Error",
                "DP_14":"Success",
                "DP_15":"Success"
                }
        last_updated_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        results = {
                    'ReferenceID':request_data_dict['ReferenceID'],
                    'status':error_status[error_code],
                    "statusCode": error_code,
                    'error_code_2':error_code_2,
                    'createdDateTime':request_data_dict['createdDateTime'], #
                    'lastUpdatedDateTime':last_updated_time,  
                    'Modelversion':request_data_dict['Modelversion'],
                    "DocumentType": request_data_dict["DocumentType"],
                    "Document":request_data_dict["Document"],      
                    'api_version' :request_data_dict['api_version'],      
                    'error_message':error_msgs[error_code],
                    'FormData' : [result_dict]
                    }
        
        error_code_2_msg="" if error_code_2=="00" else error_msgs[error_code_2]
        results["error_message"]=results["error_message"] if error_code_2=="00" else results["error_message"]+error_code_2_msg
        return results
    except Exception as e:
        print("Exception as populate_error_json",str(e))
        return {}
    

