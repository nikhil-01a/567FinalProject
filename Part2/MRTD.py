class HardwareScanner():
    pass
    
def decode():
    x=HardwareScanner()
    string_1 = x.string1
    string_2 = x.string2
    line1_list = list(string_1)
    line2_list = list(string_2)
    line1_dict = {}
    line2_dict = {}
    ################################################## Decoding line 1

    #decoding document type    
    document_type = ''.join(line1_list[0:2])
    if document_type.find("<"):
        document_type = document_type[:-1]

    #decoding country code
    country_code = ''.join(line1_list[2:5])

    #decoding full name
    name = line1_list[5:]
    i=0
    primary_name = []
    f_name = []
    for a in name:
        if a=='<':
            if(name[i+1]=='<'):
                secondary_name = name[i+2:]
                j=0
                for b in secondary_name:
                    if b=='<':
                        m_name = secondary_name[j+1:]
                        c=0
                        for d in m_name:
                            if d=='<':
                                m_name = m_name[0:c]
                            c=c+1
                        break
                    else:    
                        f_name.append(b)
                    j=j+1
                break
            else:
                primary_name.append(a)
        else:
            primary_name.append(a)
        i = i+1
    
    last_name= ''.join(primary_name)
    middle_name = ''.join(m_name)
    first_name = ''.join(f_name)
    given_name = first_name+' '+middle_name

    #creating line2 dictionary
    line1_dict['issuing_country'] = country_code
    line1_dict['last_name'] = last_name
    line1_dict['given_name'] = given_name

    ################################################## Decoding line 2

    #decoding passport number
    passport_no = ''.join(line2_list[0:9])

    #decoding and storing check digit for passport number in a list
    fields_decode = []
    fields_decode.append(str(line2_list[9]))

    #decoding country code
    nationality = ''.join(line2_list[10:13])

    #decoding date of birth 
    dob = ''.join(line2_list[13:19])

    #decoding and storing check digit for date of birth
    fields_decode.append(str(line2_list[19]))

    #decoding sex
    sex=str(line2_list[20])

    #decoding date of expiration
    doe = ''.join(line2_list[21:27])

    #decoding and storing check digit for date of expiration 
    fields_decode.append(str(line2_list[27]))

    #decoding personal number
    personal_number= ''.join(line2_list[28:41])
    if personal_number.find("<"):
        i = personal_number.find("<")
        personal_number = personal_number[:i]

    #decoding and storing check digit for personal number 
    fields_decode.append(str(line2_list[43]))

    #storing the check digit's list as a string to return
    res_dec = ''.join(fields_decode)

    #creating line2 dictionary
    line2_dict['passport_number']=passport_no
    line2_dict['country_code']=nationality
    line2_dict['birth_date']= dob
    line2_dict['sex']=sex
    line2_dict['expiration_date']=doe
    line2_dict['personal_number']=personal_number

    #joining line1 and line2 dictionaries
    records_decoded = {
        "line1":line1_dict,
        "line2": line2_dict
    }

    return res_dec,records_decoded

class dummydatabase():
    pass

def encode():
    db = dummydatabase()
    l1 = db.line1
    l2 = db.line2
    ################################## CREATING MRZ LINE 1 #####################
    ARR_L = []

    #Accessing countrycode,lastname and given name from database
    icountry = l1['issuing_country']
    lname = l1['last_name']
    gname = l1['given_name']

    #forming a part of the first line till lastname
    mline1 = f"P<{icountry+lname}<<"

    #checking if given name has a first name and middle name both, and if yes then setting flag to '1'
    flag = 0
    for a in gname:
        if a==' ':
            flag=1

    #if flag '1' then calculating the number of arrows we'll have to append after first name & middle name ELSE flag '0' then calculating the number of arrows to append after given name alone
    len1 = len(lname)
    if flag == 1:
        gnamelist = gname.split()
        firstname = gnamelist[0]
        middlename = gnamelist[1]
        mline1 = mline1 + f"{firstname}<{middlename}" #adding second part of mline1
        len2 = len(firstname)
        len3 = len(middlename)
        total_len = len1+len2+len3
        arr_length = 36 - total_len
        z=0
        while(z<arr_length):
            ARR_L.append('<')
            z=z+1  
    else:
        len2 = len(gname)
        mline1 = mline1 + f"{gname}" #adding second part of mline1
        total_len = len1+len2
        arr_length = 37 - total_len
        z=0
        while(z<arr_length):
            ARR_L.append('<')
            z=z+1
    
    Arrows_string = ''.join(ARR_L)


    #adding third part of mline1 to get the final first line of MRZ
    finalline1 = mline1 + f"{Arrows_string}"
    
    ################################## CREATING CHECK Digits #####################
    pass_number = l2['passport_number']
    c_code = l2['country_code']
    dob = l2['birth_date']
    sex = l2['sex']
    doe = l2['expiration_date']
    pers_number = l2['personal_number']
    fields_encode = []
    fields_encode.append(str(getCheckCode(pass_number)))
    fields_encode.append(str(getCheckCode(dob)))
    fields_encode.append(str(getCheckCode(doe)))
    fields_encode.append(str(getCheckCode(pers_number)))
    res_enc = ''.join(fields_encode)

    ################################## CREATING MRZ LINE 2 #####################

    #forming first part of mline2
    mline2 = f"{pass_number+fields_encode[0]+c_code+dob+fields_encode[1]+sex+doe+fields_encode[2]+pers_number}"

    #Calculating the number of arrows to append after first part of mline2
    lenmline2 = len(mline2)
    arr_len = 43-lenmline2
    j=0
    arr_list = []
    while j<arr_len:
        arr_list.append('<')
        j=j+1
    arr_str = ''.join(arr_list)

    #forming second part of mline2
    finalline2 = mline2+f"{arr_str+fields_encode[3]}"

    #joining MRZ LINE 1 AND MRZ LINE 2 and dividing them by ';'
    finalMRZ = f"{finalline1};{finalline2}"

    return res_enc,finalMRZ
    
def getCheckCode(inputString: str) -> int:
    numeric = []
    for char in inputString:
        if char.isdigit():
            # append to list if character is a number
            numeric.append(int(char))
        elif char.isalpha():
            # convert to number if character is a letter
            # A:10, B:11 ...
            asci_value = ord(char)
            asci_differnce = asci_value - ord('A')
            numeric.append(10 + asci_differnce)
        else:
            if char == '<':
                numeric.append(0)
            else:
                # error
                return 'Illegal character found.'
    weights = [7,3,1] * len(inputString)
    products = [ weights[i] * numeric[i] for i in range(len(inputString))]
    return sum(products) % 10

def compare_EncDec(res_decode,res_encode):
    #print("=====================Comparing encode and decode===================") 

    dec_list = list(res_decode)
    enc_list = list(res_encode)

    check_num = []
    k=0
    for i in dec_list:
        if dec_list[k] != enc_list[k]:
            k = k+1
            check_num.append(str(k))
        else:
            k=k+1

    #Creating list to store mismatch fields
    mismatch_col = []

    if len(check_num)==0:
        return "No mismatch"
    else:
        for x in check_num:
            if x == '1':
                mismatch_col.append("Passport Number")
            if x == '2':
                mismatch_col.append("DOB")
            if x == '3':
                mismatch_col.append("DOE")
            if x == '4':
                mismatch_col.append("Personal Number")
        
        if len(check_num)!=0:
            mismatchSTR = ','.join(mismatch_col)
            mismatchSTR = ''.join("Mismatch in "+ mismatchSTR)
            return mismatchSTR
        
if __name__ == '__main__':
    res_decode = decode()[0]
    res_encode = encode()[0]
    compare_EncDec(res_decode,res_encode)
