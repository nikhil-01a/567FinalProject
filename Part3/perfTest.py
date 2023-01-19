
# test encode
import json
import unittest
from unittest.mock import patch
import time
from MRTD import decode
from MRTD import encode
import csv
file1 = open('PART3/records_encoded.json')
encodedLines = json.load(file1)['records_encoded']

file2 = open ('PART3/records_decoded.json')
decodedLines = json.load(file2)['records_decoded']
class TestMRTD(unittest.TestCase):
    @patch('MRTD.dummydatabase')
    @patch('MRTD.HardwareScanner')
    def test_decode(self,mock_hardware, mock_db):
        lineNumber = 0
        fields = ['NumOfLines', 'RawExecuteTime', 'TimeWithAssert'] 
        with open('PART3/output.csv', 'w') as csvfile: 
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            startTime = time.perf_counter()
            for encodedline, decodedline in zip(encodedLines,decodedLines):
                lineNumber += 1
                s1,s2 = encodedline.split(';')
                mock_hardware.return_value.string1 = s1
                mock_hardware.return_value.string2 = s2
                decode()
                l1,l2 = decodedline['line1'], decodedline['line2']
                mock_db.return_value.line1 = l1
                mock_db.return_value.line2 = l2
                encode()
                executeTime = time.perf_counter()
                self.assertEqual(decode()[0], encode()[0],'the result of encode and decode should be match')
                assertTime = time.perf_counter()
                if lineNumber == 100 or lineNumber % 1000 == 0:
                    csvwriter.writerow([lineNumber,(executeTime-startTime) * 1000, (assertTime-startTime) * 1000])
            
            

if __name__ == '__main__':
    print('Running performance test')
    unittest.main()