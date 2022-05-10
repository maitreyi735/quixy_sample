import re
from dateutil.parser import parse
from .country_code_mapping import *

class Extract_Passport_Data():
    """
        This class handles various functions related to extracting data from Passport
    """

    def preprocess_text_tag(self,text_tag):   # removing spaces and text before slash
        """ 
            preprocess pan text 
            input: list of strings
            output: list of strings 
        """
        try:
            reg="[a-zA-Z\S\s]+/\s"
            p = re.compile(reg)
            for i in range(len(text_tag)):
                if(re.search(p, text_tag[i])):
                    x=re.sub(p,'',text_tag[i])
                    text_tag[i]=x
            return text_tag
        except Exception as e:
            print("Exception in preprocess_text_tag in Extract_Passport_Data class",str(e))
            return None

    def find_passport_no(self,text_tag):        
        """
            returns passport number from ocr text using regex
            input:list of strings
            output:string 
        """
        try:
            passport_num=""
            if text_tag != None:
                reg_1="(^[A-Z₱][0-9]+)"
                # reg_1= "^[A-PR-WYa-pr-wy][1-9]\\d" + "\\s?\\d{4}[1-9]$"
                p = re.compile(reg_1)
                
                # q = re.compile(reg_2)
                for i in range(len(text_tag)):
                    if(re.search(p, text_tag[i])):
                        match=re.findall(p,text_tag[i])
                        if match:
                            passport_num=match[0]
                            break
            # print("--------------------------passport number--------final------",passport_num)
            return passport_num
        except Exception as e:
            print("Exception in find passport_num",str(e))
            return ""    
    
    def passport_keyword_exists(self,text_tag):         
        """
            checks if passport keyword exists at the back or front of the passport
            input: list of strings
            output: boolean
        """
        try:
            passport_keyword_exists=False
            if text_tag != None:
                passport_str="passport"
                for i in range(len(text_tag)):
                    if(passport_str in text_tag[i].lower()):
                        passport_keyword_exists=True
                        break                       
            
            return passport_keyword_exists
        except Exception as e:
            print("Exception in find passport keyword exists method",str(e))
            return False    
    
    
    
    def get_gender(self,text_tag):
        """
            returns the gender from the given text
            input:list of strings
            output: string=> male/female/""
        """
        try:
            gender_reg='^[A-Z]$'
            q= re.compile(gender_reg)
            gender=""
            for i in range(len(text_tag)):
                # if(re.search('D[a-z]+e of B[a-z]+h|[A-Za-z]+te of B[a-z]+|D[a-z]+ of [A-Za-z]+h', text_tag[i])):
                if(re.search('D[a-z]+e of B[a-z]+h|[A-Za-z]+te of B[a-z]+|D[a-z]+ of [A-Za-z]+h', text_tag[i])) or (re.search('I[A-Z]N$|I[A-Z]D$', text_tag[i])):
                    for j in range(i+1,len(text_tag)):
                        match=re.findall(q,text_tag[j])
                        if match:
                            gender_match=match[0]
                            gender="Male" if gender_match=="M" else "Female"
                            break
                    if gender!="":
                        break
            return gender
        except Exception as e:
            print("Exception in get_gender method in Extract_Passport_Data class",str(e))
            return ""

    def extract_code_and_type(self,text_tag):
        """
            returns the code and type of the passport using regex
            input: list of strings
            output: tuple =>(passport_type,code)
        """
        try:
            reg_type="^P|S|D$"
            reg_code='^[A-Z]{3}$'
            p = re.compile(reg_type)
            c= re.compile(reg_code)
            for i in range(len(text_tag)):
                if(re.search(p, text_tag[i])): 
                    type_list=re.findall(p,text_tag[i])    
                if(re.search(c, text_tag[i])): 
                    code_list=re.findall(c,text_tag[i]) 
            passport_type=type_list[0] if type_list!=[] else ""
            code=code_list[0] if code_list!=[] else ""
            return passport_type,code
        except Exception as e:
            print("Exception in extract_code_and_type method in Extract_Passport_Data class",str(e))
            return None
    


    def check_surname_match(self,first_page_data,second_page_data):
        """
        check if surname in passport front side matches with any name in second_page_data
        ouput:boolean
        """
        try:
            surname_match=False
            surname=first_page_data["Surname"] if first_page_data!={} else ""
            second_page_name_fields=["father","mother","spouse"]
            if second_page_data:
                for field in second_page_data.keys():
                    if field in second_page_name_fields and surname in second_page_data[field]:
                        surname_match=True
                        break

            return surname_match

        except Exception as e:
            print("Exception in check_surname_match method in Extract_Passport_Data class",str(e))
            return False 
    def find_surname(self,text_tag):
        """
            finds surname from the given text by searching for surname keyword
            input:list of strings
            output:string
        """
        try:
            extra_text=["MISCELLANEOUS SERVICE","OBSERVATION"]
            reg="(^[A-Z]+\s[A-Z\s]*\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)|(^[A-Z]+$)"
            p = re.compile(reg)
            surname=""
            if text_tag != None:
                j=-1
                for i in range(len(text_tag)):
                    if(re.search('Surname', text_tag[i])):
                        j=i
                j = 7 if j==-1 else j
                for i in range(j,len(text_tag)):
                    if (re.findall(p,text_tag[i])) and (text_tag[i].upper() not in extra_text):
                        surname= text_tag[i]
                        break
            return surname
        except Exception as e:
            print("Exception in extract_code_and_type method in Extract_Passport_Data class",str(e))
            return ""
        
     
    def get_nationality(self,text_tag,country_code): 
        """
            extracts nationality from the given text
            input:list of strings
            output:string
        """
        try:
            reg='^[A-Z0-9/s]+'
            p = re.compile(reg)
            nationality=""
            for i in range(len(text_tag)):
                if(re.search('D[a-z]+e of B[a-z]+h|[A-Za-z]+te of B[a-z]+|D[a-z]+ of [A-Za-z]+h', text_tag[i])): 
                    for k in range(i+1,len(text_tag)):
                        if (re.search(p,text_tag[k])):
                            text_tag[k]=re.sub('[A-Z]+/','',text_tag[k])
                            nationality= text_tag[k]
                            break
                    if nationality:
                        break
            if nationality=="":
                nationality=return_country_name(country_code)
            return nationality
        except Exception as e:
            print("Exception in get_nationality method in Extract_Passport_Data class",str(e))
            return ""

    def find_given_name(self,text):
        """
            finds givenname from the given text by searching for given keyword
            input:list of strings
            output:string
        """
        try:
            reg="(^[A-Z]+\s[A-Z]+\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)|(^[A-Z]+$)"
            p = re.compile(reg)
            given_name=""
            j=-1
            for i in range(len(text)):
                if(re.search('Given Name', text[i])):
                    j=i
                    for i in range(j,len(text)):
                        if (re.findall(p,text[i])):
                            given_name= text[i]
                            break
            return given_name
        except Exception as e:
            print("Exception in find_given_name method in Extract_Passport_Data class",str(e))
            return ""
     
    def get_place_of_issue(self,text):
        """
            finds place of issue from the given text using regex for the words place of issue
            input:list of strings
            output:string
        """
        try:
            p= re.compile('^[A-Z0-9/s]+')
            place_of_issue=""
            j=-1
            for i in range(len(text)):
                if(re.search('P[a-z]+e of I[a-z]+e|[A-Za-z]+ce of I[a-z]+|P[a-z]+ of [A-Za-z]+e', text[i])):
                    j=i
                    for i in range(j+1,len(text)):
                        if (re.findall(p,text[i])):
                            place_of_issue= text[i]
                            break
            return place_of_issue
        except Exception as e:
            print("Exception in get_place_of_issue method in Extract_Passport_Data class",str(e))
            return ""


    def is_date(self,string, fuzzy=False):
        """
         Checks whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try: 
            parse(string, fuzzy=fuzzy)
            return True

        except Exception as e:
            print("Exception in is_date in Extract_Aadhaar_Data",str(e))
            return False
    def find_all_dates(self,text_tag):
        """
            extracts all dates from the given text using regex 
            input:list of strings
            output:list of dates
        """
        try:
            reg="[0-9]{2}/[0-9]{2}/[0-9]{4}"
            all_years={}
            for i in range(len(text_tag)):
                match = re.match(reg, text_tag[i])
                if match:
                    date_val=match.group(0)
                    date_year=int(date_val[-4:])
                    all_years[date_year]=date_val
                    
            print('===DATE=== ',all_years)
            sorted_years_list=list(all_years.keys())
            sorted_years_list.sort()
            birth_date=""
            issue_date=""
            expiry_date=""
            
            birth_date=all_years[sorted_years_list[0]] if len(sorted_years_list)>0 else "" 
            issue_date=all_years[sorted_years_list[1]] if len(sorted_years_list)>1 else ""
            expiry_date=all_years[sorted_years_list[2]] if len(sorted_years_list)>2 else ""
            return [birth_date,issue_date,expiry_date]
        except Exception as e:
            print("Exception in find_all_dates method in Extract_Passport_Data class",str(e))
            return []

    def get_place_of_birth(self,text):
        """
            finds place of birth from the given text using regex for the words place of birth
            input:list of strings
            output:string
        """
        try:
            birth_place=""
            p= re.compile('^[A-Z0-9/s]+')
            for i in range(len(text)):
                if(re.search('P[a-z]+e of B[a-z]+h|[A-Za-z]+ce of B[a-z]+|P[a-z]+ of [A-Za-z]+h', text[i])):
                    for k in range(i+1,len(text)):
                        if (re.findall(p,text[k])):
                            birth_place=text[k]
                            break
                    if birth_place!=None:
                        break
            return birth_place
        except Exception as e:
            print("Exception in get_place_of_birth method in Extract_Passport_Data class",str(e))
            return ""

    def get_passport_data(self,text):
        """
            calls all functions to extract required fields from given text
            input:list of strings
            output:dictionary of required fields
        """
        try:
            print("INSIDE GET PASSPORT DATA")
            text_tag=self.preprocess_text_tag(text)
            print("preprocessed text is----------------------------",text_tag)
            result_dict={}
            required_fields=["Surname","Name","Passport_num","DoB","Issue Date","Expiry Date","Type","Country code","Gender","Birth Location","Resident","Nation"]
            for field in required_fields:
                result_dict[field]=""
            gender=self.get_gender(text_tag)
            place_of_issue=self.get_place_of_issue(text_tag)
            place_of_birth=self.get_place_of_birth(text_tag)
            passport_type_and_code=self.extract_code_and_type(text_tag)
            country_code=""
            passport_type=""
            if passport_type_and_code:
                passport_type,country_code=passport_type_and_code
            passport_num = self.find_passport_no(text_tag)
            surname = self.find_surname(text_tag)
            given_name = self.find_given_name(text_tag)
            all_dates_result=self.find_all_dates(text_tag)
            birth_date=""
            issue_date=""
            expiry_date=""
            if all_dates_result:
                birth_date,issue_date,expiry_date=all_dates_result
            nationality=self.get_nationality(text_tag,country_code)
            result_dict["Surname"]=surname
            result_dict["Name"]= given_name
            result_dict["Passport_num"]= passport_num
            result_dict["DoB"]=birth_date
            result_dict["Issue Date"]=issue_date
            result_dict["Expiry Date"]=expiry_date
            result_dict["PassportType"]=passport_type
            result_dict["Country code"]= country_code
            result_dict["Gender"]=gender
            result_dict["Birth Location"]= place_of_birth
            result_dict["Nationality"]= nationality 
            result_dict["Place_Of_Issue"]=place_of_issue 
            return result_dict
        except Exception as e:
            print("Exception in get_passport_data method in Extract_Passport_Data class",str(e))
            return None




    def extract_pass_back(self,text_tag):
        """
            extracts the name of father, mother and spouse from the given data using regex
            input:list of strings
            output:dictionary of required fields for backside of the passport
        """
        try:
            reg="([A-Z]+\s[A-Z]+\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)|(^[A-Z]+$)"
            q = re.compile(reg)
            z,j,s,r,t,y=0,0,0,0,0,0
            for i in range(len(text_tag)):
                # if(re.search('^L[a-z]+l G[a-z]+n$|^[A-Za-z]+l [A-Za-z]+n$|^L[a-z]+ G[a-z]+$', text_tag[i])):
                if(re.search('Father|Name of Father|Legal Guardian', text_tag[i])): 
                    z=i 
                # if(re.search('^N[a-z]+e of M[a-z]+r$|^[A-Za-z]+e of [A-Za-z]+r$|^N[a-z]+ of M[a-z]+$', text_tag[i])):
                if(re.search('Mother|Name of Mother', text_tag[i])): 
                    j=i
                # if(re.search('^N[a-z]+e of S[a-z]+e$|^[A-Za-z]+e of [A-Za-z]+e$|^N[a-z]+ of S[a-z]+$', text_tag[i])): 
                if(re.search('Spouse|Name of Spouse', text_tag[i])): 
                    s=i
                # if(re.search('^Address$|^A[a-z]+s$|^[A-Za-z]+ss$|^Ad[a-z]+$', text_tag[i])):
                if(re.search('Address$|^Ad[a-z]+$', text_tag[i])):  
                    r=i
                if(re.search('O[a-z]+ P[a-z]+t No|P[a-z]+e of I[a-z]+e', text_tag[i])): 
                    t=i
                if(re.search('F[a-z]+e No|[A-Za-z]+le No', text_tag[i])): 
                    y=i 
        
            father=""
            for i in range(z+1,len(text_tag)):

                if (re.search(q,text_tag[i])):
                    father=text_tag[i]
                    break 
            mother=""
            for i in range(j+1,len(text_tag)):
                if (re.search(q,text_tag[i])):
                    mother=text_tag[i]
                    break
            spouse=""
            for i in range(s+1,r+1):
                if (re.search(q,text_tag[i])):
                    spouse=text_tag[i]
                    break
            address=[]
            for i in range(r+1,t):
                address.append(text_tag[i])
            
            address=" ".join(address) if address!=[] else ""
            file=""
            for i in range(y+1,len(text_tag)):
                file=text_tag[i]
                break
            passport_num=self.find_passport_no(text_tag)
            passport_backside_details={}
            # ["father","mother","spouse","address","file"]
            passport_backside_details["father"]=father
            passport_backside_details["mother"]=mother
            passport_backside_details["spouse"]=spouse
            passport_backside_details["address"]=address
            passport_backside_details["file"]=file
            passport_backside_details["Passport_num"]= passport_num
            return passport_backside_details
        except Exception as e:
            print("Exception in extract_pass_back method in Extract_Passport_Data class",str(e))
            return {}


    def decide_side(self,text_tag):    
        """
            used for checking the side of passport
            input: list of strings
            output: boolean
        """
        try:
            y=-1
            for i in range(len(text_tag)):
                if(re.search('F[a-z]+e No|[A-Za-z]+le No', text_tag[i])): 
                    y=i 
            front=True if y==-1 else False 
            return front
        except Exception as e:
            print("Exception in decide_side method in Extract_Passport_Data class",str(e))
            return {}


    def populate_front_and_back(self,front_side_data,back_side_data,text):
        """
            used for merging both sides of the passport data
            input: front and back dictionaries
            output: merged dictionary
        """
        try:
            front_fields= ["Surname","Name","Passport_num","DoB","Issue Date","Expiry Date","PassportType","Country code","Gender","Birth Location","Nationality","Place_Of_Issue"]
            back_fields= ["father","mother","spouse","address","file","Passport_num"]
            all_fields=["Surname","Name","Passport_num","DoB","Issue Date","Expiry Date","PassportType","Country code","Gender","Birth Location","Nationality","Place_Of_Issue","father","mother","spouse","address","file"]
            merged_dict={}
            print("front is----------------",front_side_data)
            print("back is----------------",back_side_data)
            if back_side_data=={}:
                if self.is_rotated_image(text):
                    back_side_data=self.get_rotated_image_fields(text)
            for field in all_fields:
                if field in front_fields:
                    merged_dict[field]=front_side_data[field] if front_side_data!={} else "" 
                elif field in back_fields:
                    merged_dict[field]=back_side_data[field] if back_side_data!={} else ""
                if field in back_fields and field in front_fields:
                    merged_dict[field]=front_side_data[field] if front_side_data!={} else back_side_data[field] if back_side_data!={} else ""

            print("merged dict is-----------------------------------",merged_dict)
            return merged_dict
        except Exception as e:
            print("Exception in populate_front_and_back method in Extract_Passport_Data class",str(e))
            return {}

        
    def is_rotated_image(self,text_tag):    
        """
            used for checking if one side of the passport is rotated 
            input: list of strings
            output: boolean
        """
        try:
            pin_regex=re.compile("^[1-9][0-9][0-9]$")
            is_rotated_image=False
            address_keyword_index=-1
            pin_code_index=-1
            address_keyword_found=False
            pin_code_found=False
            for i in range(len(text_tag)):
                tag_digits=re.findall(r'\d+', text_tag[i])
                if re.findall(r'\d+', text_tag[i]) !=[] and pin_code_found==False:
                    for digit in tag_digits:
                        pin_match=re.match(pin_regex, digit)
                        if pin_match is not None:
                            pin_code_index=i
                            pin_code_found=True
                if(re.search('Address$|^Ad[a-z]+$', text_tag[i])) and address_keyword_found==False:  
                    address_keyword_index=i
                    address_keyword_found=True
                    
                if address_keyword_found and pin_code_found:
                    break
            if pin_code_found==True and pin_code_index<address_keyword_index:
                is_rotated_image=True
            print("pincode uindex is------------------------",pin_code_index,is_rotated_image)
            return is_rotated_image

        except Exception as e:
            print("Exception in decide_side method in Extract_Passport_Data class",str(e))
            return False
        

    def get_rotated_image_fields(self,text_tag):
        """
            returns the fields of the back of the passport 
            when back of the passport image is upside down
        """
        try:
            print("INSIDE GETROTATED FIELDS-----------------------")
            pin_regex=re.compile("^[1-9]{1}[0-9]{2}[0-9]{3}$")
            reg="([A-Z]+\s[A-Z]+\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)|(^[A-Z]+$)"
            q = re.compile(reg)
            z,j,s,r,t,y,p=0,0,0,0,0,0,0
            pin_found=False
            for i in range(len(text_tag)):
                if(re.search('Father|Name of Father|Legal Guardian', text_tag[i])): 
                    z=i 
                if(re.search('Mother|Name of Mother', text_tag[i])): 
                    j=i
                if(re.search('Spouse|Name of Spouse', text_tag[i])): 
                    s=i
                if(re.search('Address$|^Ad[a-z]+$', text_tag[i])):  
                    r=i
                if(re.search('O[a-z]+ P[a-z]+t No|P[a-z]+e of I[a-z]+e', text_tag[i])): 
                    t=i
                if(re.search('F[a-z]+e No|[A-Za-z]+le No', text_tag[i])): 
                    y=i
                tag_digits=re.findall(r'\d+', text_tag[i])
                if re.findall(r'\d+', text_tag[i]) !=[] and pin_found==False:
                    for digit in tag_digits:
                        pin_match=re.match(pin_regex, digit)
                        if pin_match is not None:
                            p=i
                            pin_found=True        
            father=""
            for i in range(z,-1,-1):
                if (re.search(q,text_tag[i])):
                    father=text_tag[i]
                    break 
            mother=""
            for i in range(j,-1,-1):
                if (re.search(q,text_tag[i])):
                    mother=text_tag[i]
                    break
            spouse=""
            for i in range(s,j-1,-1):
                if (re.search(q,text_tag[i])):
                    spouse=text_tag[i]
                    break
            address=[]
            for i in range(r-1,p-1,-1):
                address.append(text_tag[i])
            
            
            address=" ".join(address) if address!=[] else ""
            file=""
            for i in range(y,-1,-1):
                file=text_tag[i]
                break

            rotated_results_dict={}
            rotated_results_dict["father"]=father
            rotated_results_dict["mother"]=mother
            rotated_results_dict["spouse"]=spouse
            rotated_results_dict["address"]=address
            rotated_results_dict["file"]=file
            print("rotated-----------------------",rotated_results_dict)
            return rotated_results_dict

        except Exception as e:
            print("Exception in decide_side method in Extract_Passport_Data class",str(e))
            return {}