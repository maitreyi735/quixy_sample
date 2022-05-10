import re



class Extract_Driving_License():
    """
        This class handles various functions related to extracting data from Driving License
    """

    def match_pattern_drive(self,regx,typ,text):  #matching for driving license
        try:
            # print("INSIDE MATCH PATTERN DRIVE")
            a = 14
            if typ == "ID":
                a = 16
            elif typ == "Issued":
                a = 10
            for element in text:
                l = len(element)
                if l > a:
                    for i in range(l-(a-1)):
                        z = re.match(regx, element[i:i+a])
                        if z:
                            return z[0]
            return ""
        except Exception as e:
            print("Exception in match_pattern_aadhaar",str(e))
            return None

    def get_DrivingLicence_data(self,text):   #extraction for driving data

        names = get_Names(text)        
        
        Driving_ID_Regex = "^(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}"+"|([a-zA-Z]{2}[0-9]{2}[\\/][a-zA-Z]{3}[\\/][0-9]{2}[\\/][0-9]{5})"+"|([a-zA-Z]{2}[0-9]{2}(N)[\\-]{1}((19|20)[0-9][0-9])[\\-][0-9]{7})"+"|([a-zA-Z]{2}[0-9]{14})"+"|([a-zA-Z]{2}[\\-][0-9]{13})$"
        Issued_Date_Regex = "[0-9]{2}-[0-9]{2}-[0-9]{4}"
        
        driving_id = self.match_pattern_drive(Driving_ID_Regex,"ID",text)
        issued_date = self.match_pattern_drive(Issued_Date_Regex,"Issued",text)
        
        name=names[0] if names!=[] else ""
        rta=names[1] if len(names)>1 else ""
        required_field=["Name","Unique ID","Issue Date","RTA Division"]
        
        result_dict = {"Name": name, "Unique ID": driving_id, "Issue Date": issued_date, "RTA Division": rta}
        
        return result_dict
    
    

