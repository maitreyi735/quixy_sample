import re



class Extract_Pan_Data():
    """
        This class handles various functions related to extracting data from PAN Card
    """
    def findPanCardNo(self,text_tag):  
        """ 
            uses regex to check valid PAN Card number
            input:list of strings
            output:string 
        """
        try:
            regex = "^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
            pan_card_num=""
            
            if text_tag != None:
                p = re.compile(regex)
                for i in range(len(text_tag)):
                    if(re.search(p, text_tag[i]) and len(text_tag[i]) == 10):
                        pan_card_num= text_tag[i]
                        break
            return pan_card_num
        except Exception as e:
            print("Exception as findPanCardNo",str(e))
            return ""
    
    
    def find_names(self,text_tag):
        """
            finds name from the given text 
            input:list of strings
            output:string
        """
        try:
            names=[]
            for i in range(len(text_tag)):
                if i<2 or re.search('(INCOMETAXDEPARWENT|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', text_tag[i]):
                    continue
                if(re.search('(^[A-Z]+.+\D[A-Z]+$)', text_tag[i])):
                    print(text_tag[i])
                    names.append(text_tag[i])
            if len(names) == 3:
                name = names[0]+' '+names[1]
                father_name = names[2]
            elif len(names) == 4:
                name = names[0]+' '+names[1]
                father_name = names[2]+' '+names[3]
            else:
                name = names[0]
                father_name = names[1]     
            return name, father_name
        except Exception as e:
            print("Exception as find_name",str(e))
            return ""

    def get_date_of_birth(self,text_tag):
        """
            extracts date of birth from pan_card data
            input:list of strings
            output:string
        """
        try:
            regex = "[0-9]{2}/[0-9]{2}/[0-9]{4}" # Regex to searching date
            p = re.compile(regex)
            birth_date=""                         
            for i in range(len(text_tag)):
                if(re.search(p, text_tag[i])):
                    x=re.findall(p, text_tag[i])
                    birth_date= x[0]
                    break
            return birth_date
        except Exception as e:
            print("Exception as find_name",str(e))
            return ""

    def get_pan_data(self,text_tag):  
        """
            calls all functions to extract required fields from given text
            input:list of strings
            output:dictionary of required fields
        """
        
        try:
            required_fields=["Name","PAN no.","DoB","Father Name"]
            result_dict={}
            for field in required_fields:
                result_dict[field]=""
            if text_tag:
                names = self.find_names(text_tag)
                first_name=names[0] if names!=[] else ""
                father_name=names[1] if len(names)==2 else ""
                pan_card_num= self.findPanCardNo(text_tag)
                date_of_birth = self.get_date_of_birth(text_tag)
                
                result_dict["Name"]=first_name
                result_dict["PAN no."]=pan_card_num
                result_dict["DoB"]=date_of_birth
                result_dict["Father Name"]=father_name
            return result_dict
        except Exception as e:
            print("Exception as find_name",str(e))
            return None 

