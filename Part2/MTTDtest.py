import unittest
from unittest.mock import patch
from MRTD import decode
from MRTD import encode
from MRTD import getCheckCode
from MRTD import compare_EncDec

#Mock function 1
class MockResponse():
    
    string1 = "P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<"  
    string2 = "W620126G54CIV5910106F9707302AJ010215I<<<<<<6"

    line1 = {'issuing_country':"CIV",'last_name' : "LYNN",'given_name':"NEVEAH BRAM"}
    line2 = {'passport_number':"W620126G5",'country_code' : "CIV",'birth_date':"591010",'sex':"F",'expiration_date':"970730",'personal_number':"AJ010215I"}

#Mock function 2
class MockResponse1():
    string1 = "P<ABWMALDONADO<<CAMILLA<<<<<<<<<<<<<<<<<<<<<"  
    string2 = "V008493B64ABW7809095M0909088QZ181922T<<<<<<5"

    line1 = {'issuing_country':"ABW",'last_name' : "MALDONADO",'given_name':"CAMILLA"}
    line2 = {'passport_number':"V008493B6",'country_code' : "ABW",'birth_date':"780909",'sex':"M",'expiration_date':"090908",'personal_number':"QZ181922T"}
    

class TestMRTD(unittest.TestCase):
    # define multiple sets of tests as functions 

    #Mocking HardwareScanner() and giving two strings as input to the decode function. This string contains a given name with first and middle names inside it.
    @patch('MRTD.HardwareScanner',side_effect=MockResponse)
    def test_decode_firstmiddle_name(self,mock_obj): 
        self.assertEqual(decode(),('4626', {'line1': {'issuing_country': 'CIV', 'last_name': 'LYNN', 'given_name': 'NEVEAH BRAM'}, 'line2': {'passport_number': 'W620126G5', 'country_code': 'CIV', 'birth_date': '591010', 'sex': 'F', 'expiration_date': '970730', 'personal_number': 'AJ010215I'}}),'The check digits should be identified correctly')

    #Mocking the dummydatabase() and givng two dictionary lines containing all the information fields of a person. Here again the given name of the person includes first and middle name in it. 
    @patch('MRTD.dummydatabase',side_effect=MockResponse)
    def test_encode_firstmiddle_name(self,mock_obj): 
        self.assertEqual(encode(),('4626', 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'),'The check digits should be calculated correctly')

    #Mocking HardwareScanner() and giving two strings as input to the decode function. This string contains a single given name.
    @patch('MRTD.HardwareScanner',side_effect=MockResponse1)
    def test_decode_givenname(self,mock_obj): 
        self.assertEqual(decode(),('4585', {'line1': {'issuing_country': 'ABW', 'last_name': 'MALDONADO', 'given_name': 'CAMILLA '}, 'line2': {'passport_number': 'V008493B6', 'country_code': 'ABW', 'birth_date': '780909', 'sex': 'M', 'expiration_date': '090908', 'personal_number': 'QZ181922T'}}),'The check digits should be identified correctly')

    #Mocking the dummydatabase() and givng two dictionary lines containing all the information fields of a person. This person has a single given name. 
    @patch('MRTD.dummydatabase',side_effect=MockResponse1)
    def test_encode_givenname(self,mock_obj): 
        self.assertEqual(encode(),('4585', 'P<ABWMALDONADO<<CAMILLA<<<<<<<<<<<<<<<<<<<<<;V008493B64ABW7809095M0909088QZ181922T<<<<<<5'),'The check digits should be calculated correctly')

    #Testing the check digit generator function by giving a passport number as an input
    def test_getCheckCode(self): 
        self.assertEqual(getCheckCode('W620126G5'),4,'The Checkcode is not calculated properly')

    #Testing the check digit generator function by giving an '<' symbol as an input
    def test_getCheckCode_arrow(self): 
        self.assertEqual(getCheckCode('<'),0,'The character entered should be illegal for this test case')

    #Testing the check digit generator function by giving a '$' symbol as an input
    def test_getCheckCode_illegalcharacter(self): 
        self.assertEqual(getCheckCode('$'),'Illegal character found.','The character entered should be illegal for this test case')

    #Testing the 'encoder-decoder check digits comparing' function with both equal check digits
    def test_NoMismatch(self): 
        self.assertEqual(compare_EncDec('4646','4646'),'No mismatch','The check-digits are supposed to be equal')

    #Testing the 'encoder-decoder check digits comparing' function with 'passport number' not matching (the first digit)
    def test_MismatchPassNo(self): 
        self.assertEqual(compare_EncDec('4646','5646'),'Mismatch in Passport Number','The check-digits are supposed to be equal')

    #Testing the 'encoder-decoder check digits comparing' function with 'Date of Birth' not matching (the second digit)
    def test_MismatchDOB(self): 
        self.assertEqual(compare_EncDec('4646','4746'),'Mismatch in DOB','The check-digits are supposed to be equal')

    #Testing the 'encoder-decoder check digits comparing' function with 'Date of Expiration' not matching (the third digit)
    def test_MismatchDOE(self): 
        self.assertEqual(compare_EncDec('4646','4656'),'Mismatch in DOE','The check-digits are supposed to be equal')

    #Testing the 'encoder-decoder check digits comparing' function with 'Personal Number' not matching (the fourth digit)
    def test_MismatchPersNo(self): 
        self.assertEqual(compare_EncDec('4646','4648'),'Mismatch in Personal Number','The check-digits are supposed to be equal')
    
    #Testing the 'encoder-decoder check digits comparing' function with 'DOE' and 'Personal Number'  
    def test_MismatchPersNoDoe(self): 
        self.assertEqual(compare_EncDec('4646','4638'),'Mismatch in DOE,Personal Number','The check-digits are supposed to be equal')

    #Testing the 'encoder-decoder check digits comparing' function with 'DOB', 'DOE' and 'Personal Number'
    def test_MismatchDobPersNoDoe(self): 
        self.assertEqual(compare_EncDec('4646','4738'),'Mismatch in DOB,DOE,Personal Number','The check-digits are supposed to be equal')

    #Testing the 'encoder-decoder check digits comparing' function with 'Passport number','DOB', 'DOE' and 'Personal Number'
    def test_MismatchPassDobPersNoDoe(self): 
        self.assertEqual(compare_EncDec('4646','5738'),'Mismatch in Passport Number,DOB,DOE,Personal Number','The check-digits are supposed to be equal')


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
 
