import os
import json
import re
import time
from requests import get,post
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

class Extract_OCR():
    """
        This class handles various functions related to extracting data using OCR
    """
    def get_azure_ocr(self,filename):
        """
            This method returns ocr data using azure form recognizer
            input:base_64_file
            output: list of strings
        """
        endpoint = "https://quixyocr.cognitiveservices.azure.com/"
        apim_key = "03462e450efa4e338d200900d30d8c7b"
        post_url = endpoint +"/formrecognizer/v2.1/prebuilt/invoice/analyze"
        text_lst = []
    
        
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': apim_key,
        }

        params = {
            "includeTextDetails": True
        }
        
        
        # with open(filename, "rb") as f:
        #     data_bytes = f.read()

        try:
            resp = post(url=post_url, data=filename,
                        headers=headers, params=params)
            if resp.status_code != 202:
                #print("POST analyze failed:\n%s" % resp.text)
                return None
            #print("POST analyze succeeded: %s" %
                #resp.headers["operation-location"])
            get_url = resp.headers["operation-location"]
        except Exception as e:
            print("POST analyze failed:\n%s" % str(e))
            return None

        n_tries = 50
        n_try = 0
        wait_sec = 6
        while n_try < n_tries:
            try:
                resp = get(url=get_url, headers={
                        "Ocp-Apim-Subscription-Key": apim_key})
                resp_json = json.loads(resp.text)
                if resp.status_code != 200:
                    #print("GET Invoice results failed:\n%s" % resp_json)
                    return None
                status = resp_json["status"]
                if status == "succeeded":
                    print("Analysis succeeded.")
                    res = resp_json['analyzeResult']['readResults']
                    text_lst = []
                    for i in range(len(res[0]['lines'])):
                        #print('==== ',res[0]['lines'][i]['text'])
                        text_lst.append(res[0]['lines'][i]['text'])
                        regex = re.compile(r'([A-Z][a-z]+(?: [A-Z][a-z]\.)? [A-Z][a-z]+)')
                
                    return text_lst
                if status == "failed":
                    print("Analysis failed:\n%s" % resp_json)
                    return None
                # Analysis still running. Wait and retry.
                time.sleep(wait_sec)
                n_try += 1
                
            except Exception as e:
                print("GET analyze results failed:\n%s" % str(e))
                return None

        
    