from dateutil.parser import parse
import re



class Extract_Aadhar_Data():
    """
        This class handles various functions related to extracting data from Aadhar
    """
    def preprocess_text_tag(self,text_tag):
        """
            preprocess aadhaar text 
        """
        try:
            reg="[a-zA-Z\S\s]+/\s"
            p = re.compile(reg)
            for i in range(len(text_tag)):
                if(re.search(p, text_tag[i])):
                    x=re.sub(p,'',text_tag[i])
                    text_tag[i]=x
            print('====Preprocessed text ===== ', text_tag)
            return text_tag
        except Exception as e:
            print("Exception as preprocess_text_tag in Extract_Aadhaar_Data",str(e))
            return None
    
    def extract_gender(self,text_tag):
        """
            Extracts gender data from text tag
            input:list of strings
            output:string
        """
        try:
            ind = [i for i in range(len(text_tag)) if (text_tag[i].lower().strip() == 'male') | (text_tag[i].lower().strip() == 'female' )]
            gender=""
            if ind==[]:
                # print('ind is empty-------------------------------------')
                for i in range(len(text_tag)):
                    if (re.findall('Female|FEMALE', text_tag[i])):
                        gender= 'Female'
                        break
                    elif (re.findall('Male|MALE', text_tag[i])):
                        gender= 'Male'
                        break
                    
            else:
                gender= text_tag[ind[0]]
            print("gender is-------------------------------",gender)
            return gender        
        except Exception as e:
            print("Exception as extract_gender in Extract_Aadhaar_Data",str(e))
            return ""
            
        
    
    def extract_enrolment(self,text_tag):
        """
            extracts enrollment number from adhaar text
            input:list of strings
            output:string
        """
        try:
            num=""
            reg="[0-9]{4}/[0-9]{5}/[0-9]{5}"
            p = re.compile(reg)
            for i in range(len(text_tag)):
                if(re.search(p, text_tag[i])): 
                    x=re.findall(p,text_tag[i])
                    if x:
                        num=x[0]
            return num
        except Exception as e:
            print("Exception as extract_enrolment in Extract_Aadhaar_Data",str(e))
            return ""
    
    def find_father(self,text_tag,name,is_long):
        """
            returns the name of the father in aadhaar card using S/O to identify father name
            input:list of strings
            output:string
        """
        try:
            father_name=""
            for i in range(len(text_tag)):
                if (re.search('/O|Address',text_tag[i])) and is_long == False:
                    s1 = text_tag[i]
                    s2 = "/O"
                    father_sub1 = s1[s1.index(s2) + len(s2):] if s2 in s1 else ""
                    father_sub2 = text_tag[i+1]
                    father_name = father_sub1+' '+father_sub2
                    father_name=father_name.replace("S/O","")
                    print("father name is--------------",father_name)
                    break
                elif (re.search('/O',text_tag[i])):
                    text=text_tag[i].replace("S/O","")
                    r=re.findall('[A-Za-z\s]+',text)
                    if r!=[]:
                        txt=[x for x in r if len(x)>1]
                        father_name= txt[0]
                    break
                    
            if father_name=="" and is_long==True:
                for i in range(0,len(text_tag)-1):
                    text=text_tag[i]
                    name_exists=name in text
                    if name_exists:
                        r=re.findall('[A-Za-z\s]+',text_tag[i+1])
                        father_name=r[0]
                        break

            if father_name!="" and (re.search(',|:',text_tag[i])):
                father_name = father_name.split(',')[0]
                return father_name
            else:
                return father_name
        except Exception as e:
            print("Exception as find_father in Extract_Aadhaar_Data",str(e))
            return ""
        
    def extract_address(self,text_tags,father_name,is_long):
        """
            Extract address data from Aadhaar using regex 
            input:list of strings
            output:string
        """
        try:
            pin_regex=re.compile("^[1-9]{1}[0-9]{2}[0-9]{3}$")  #TODO match for optional space b/n 3 digits
            start_ind=-1
            address_str=""

            for i in range(len(text_tags)):
                if (re.search('/O',text_tags[i])):
                    start_ind=i 
                    break
            if start_ind==-1 and father_name!="" and is_long==True:
                for i in range(0,len(text_tags)-1):
                    text=text_tags[i]
                    father_name_exists=father_name in text
                    if father_name_exists:
                        start_ind=i
                        break
            
            if start_ind!=-1:
                address_list=[]
                pin_exists=False
                end_name_index=-1
                father_name_line=text_tags[start_ind]
                if "," in father_name_line:
                    end_name_index=father_name_line.index(",")
                    if end_name_index<len(father_name_line)-1:
                        remaining_str=father_name_line[end_name_index+1:len(father_name_line)]
                        address_list.append(remaining_str)     
                        
                for i in range(start_ind+1,len(text_tags)):
                    address_list.append(text_tags[i])
                    tag_digits=re.findall(r'\d+', text_tags[i])
                    if tag_digits !=[]:
                        for digit in tag_digits:
                            pin_match=re.match(pin_regex, digit)
                            if pin_match is not None:
                                pin_exists=True
                                break
                        if pin_exists==True:
                            break

                address_str=" ".join(address_list)
            
            return address_str
        except Exception as e:
            print("Exception as extract_address in Extract_Aadhaar_Data",str(e))
            return ""

    def find_aadhar_number(self,text):
        """
            extracts aadhaar id based on regex pattern
            input:list of strings
            output:string
        """
        try:
            Aadhar_regex = "[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}"
            aadhaar_number=""
            min_aadhar_length=12
            for element in text:
                if len(element) >= min_aadhar_length:
                    match = re.findall(Aadhar_regex, element)
                    if match:
                        aadhaar_number= match[0]
            return aadhaar_number                  
        except Exception as e:
            print("Exception as find_aadhar_number in Extract_Aadhaar_Data",str(e))
            return ""


   

    def find_birthday(self,text):
        """
            extracts birthday date based on regex pattern
            input:list of strings
            output:string
        """
        try:
            DOB_regex1 ="[0-9]{2}[-/.][0-9]{2}[-/.][0-9]{4}" 
            DOB_regex2 ="(?:19\d{2}|20[01][0-9]|)"
            matched_pattern=""
            for i in range(len(text)):
                if(re.search('DOB|Year of Birth|YoB', text[i])): 
                    start_ind=i
                    for i in range(start_ind,len(text)):
                        z = re.findall(DOB_regex1, text[i])
                        y=re.findall(DOB_regex2, text[i])
                        if z:
                            matched_pattern= z[0]
                            break
                        if y:
                            t=[x for x in y if x!=""]
                            matched_pattern= t[0]
                            break
            return matched_pattern
        except Exception as e:
            print("Exception as find_birthday in Extract_Aadhaar_Data",str(e))
            return ""
    

    def is_aadhar_back(self,text):
        """
            checks if "uidai.gov.in" string exists in the extracted text based on regex pattern
            input:list of strings
            output:boolean
        """
        is_back=False
        match_text_list=["www.uldal.gov.in","www.uidai.gov.in","uidai.gov","uidal.gov","uldal.gov"]
        if any(s in text for s in match_text_list):
            is_back=True
            print('--------111111-------is back----------- ', is_back)
        return is_back
    
    def is_long_format_aadhaar(self,text):
        """
            checks if the input file is long or short aadhar, 
            returns true if the input file is long format aadhar
            input: list of strings
            output: boolean value 
        """
        try:
            
            is_long_format=False
            o_exists=any("/O" in s for s in text)     
            if o_exists:
                is_long_format= True if (self.is_aadhar_back(text) == False) else False
            else:
                for i in range(len(text)):
                    if 'To' in text[i]:
                        is_long_format=True
                        break
            return is_long_format
        except Exception as e:
            print("Exception in is_long_format_aadhaar in Extract_Aadhaar_Data",str(e))
            return False    

    
    def extract_name(self,text,is_long_format):
        """ 
            extracts all names from aadhaar data
            input:list of strings
            output:string and boolean value 
        """
        try:
            print("INSIDE GET NAME METHOD-------------------")
            name=""
            o_exists=any("/O" in s for s in text)
            is_back=self.is_aadhar_back(text)
            for i in range(len(text)):
                if (re.search('/O',text[i])):
                    j=i-1
                    print("j is---------------AAA-----------------",j)
                    break
                elif 'To' in text[i] and o_exists==False:
                    j=i+1
                    print("j is--------------BBB------------------",j)
                    break
                
            if is_long_format==True:
                print("----------------2222-------------------------")
                nm = text[j]
                if self.is_date(nm, fuzzy=True) == True:
                    nm = text[j-1]
                if text.count(nm) == 1:
                    names_lst = [i for i in text if i in nm]
                    nm = min(names_lst, key=len)
                name=nm
                print("name-------------222---------------------",name)
            elif is_long_format==False and is_back==True:
                print("----------------3333--------------------------")
                name = ""

            elif is_back==False: #short format
                print("------------------------444---------------")               
                names_list=[]
                prev_str=("GOVERNMENT OF INDIA")
                for i in range(len(text)-1):
                    if prev_str.lower() in text[i].lower():
                        for j in range(i+1,len(text)):
                            word=text[j].split(",")[0]   # take only first word before comma in the sentence
                            print("word is-------------",word)
                            if not any(char.isdigit() for char in word):
                                names_list.append(word)
                                print("nm is---------------",word)
                print("names list is-----------------------",names_list)
                name=max(names_list,key=len)         
                print("final name is------------",name)
                # regex = re.compile('[A-Za-z]')
                # t = []
                # for txt in text: #TODO
                #     match_str=regex.findall(txt)
                #     print("match str-----txt---------------------",match_str,"----------",txt)
                #     len_match = len(match_str)
                #     if len_match == len(txt.replace(' ', '')):
                #         t.append(txt)
                # print("t is--------1111-----------",t)
                # if len(t)>1:
                #     if len(t)>2 and len(t[1]) < len(t[2]):
                #         nm = t[2]
                #     else:
                #         nm = t[1]
                
            return name
        except Exception as e:
            print("Exception as extract_name in Extract_Aadhaar_Data",str(e))
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

    def proc_text(self, text_tag):
        try:
            proc_text = []
            # reg = re.compile('[^a-zA-Z]+[0-9]')
            reg = re.compile('[^a-zA-Z]')
            num_reg = re.compile('^[0-9\s]*$')
            for i in range(len(text_tag)):
                # if(re.search("([a-z][A-Z][0-9]\_\-)*", text_tag[i])):
                if reg.match(text_tag[i]):
                    print(text_tag[i])
                    if num_reg.match(text_tag[i]):
                        # print('---in if------ ', text_tag[i])
                        proc_text.append(text_tag[i])
                else:
                    proc_text.append(text_tag[i])
            return proc_text
        except Exception as e:
            print("Exception in proc_text in Extract_Aadhaar_Data",str(e))
            return None

    def get_aadhar_data(self,text):  
        """
            extracts all the required fields from aadhar data and returns a dict
            input:list of strings
            output:dictionary of required fields
        """
        try:
            required_fields=["Name","Aadhar ID","DoB","Gender","Enrollment No.","Father Name","Address"]
            
            result_dict={}
            for field in required_fields:
                result_dict[field]=""
            

            Aadhar_ID = self.find_aadhar_number(text)
            date_of_birth = self.find_birthday(text)
            is_long_format=self.is_long_format_aadhaar(text)
            print('=-=-=-=-=- is long final-=-=-=-=-=== ', is_long_format)
            name=self.extract_name(text,is_long_format)
            enroll_num=self.extract_enrolment(text)
            preprocessed_text=self.preprocess_text_tag(text) 
            proc_text = self.proc_text(text)       
            
            if preprocessed_text:
                gender=self.extract_gender(preprocessed_text)
                father_name=self.find_father(proc_text,name,is_long_format)
                address=self.extract_address(proc_text,father_name,is_long_format)
            
            # ["Name","Aadhar ID","DoB","Gender","Enrollment No.","Father Name","Address"]
            
            result_dict["Name"]=name
            result_dict["Aadhar ID"]=Aadhar_ID
            result_dict["DoB"]=date_of_birth
            result_dict["Gender"]=gender
            result_dict["Enrollment No."]=enroll_num
            result_dict["Father Name"]=father_name
            result_dict["Address"]=address

            return result_dict
        except Exception as e:
            print("Exception in get_aadhar_data in Extract_Aadhaar_Data",str(e))
            return None

    def merge_both_pages(self,first_page_data,second_page_data):
        """
            used for merging both sides of the passport data
            input: front and back dictionaries
            output: merged dictionary
        """
        try:
            all_fields=["Name","Aadhar ID","DoB","Gender","Enrollment No.","Father Name","Address"]
            merged_dict={}
            print("first page is----------------",first_page_data)
            print("second page is----------------",second_page_data)
            for field in all_fields:
                if first_page_data!={} and field in first_page_data and first_page_data[field]!="":
                    merged_dict[field]=first_page_data[field]
                elif second_page_data!={} and field in second_page_data and second_page_data[field]!="":
                    merged_dict[field]=second_page_data[field]
                else:
                    merged_dict[field]=""     
            return merged_dict
        except Exception as e:
            print("Exception in merge_both_pages method in Extract_Passport_Data class",str(e))
            return {}    
