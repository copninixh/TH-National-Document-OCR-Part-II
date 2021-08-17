# coding: utf-8
#This process is a performance testing and calculate character error rate (CER Value) T-OCR from AI for Thai and Tesseract (tha model) without finetune and train
#Result report export (.csv) file 
import requests
import pytesseract
import numpy as np
import pandas as pd
import difflib
import fastwer
import json
from PIL import Image
from ssg import syllable_tokenize

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


if __name__ == "__main__":
    listfile = [
            ("testing.png","ถึง สํานักงานส่งเสริมการปกครองท้องถิ่นจังหวัด ทุกจังหวัด ด้วยกรมบัญชีกลางได้ปรับปรุงประกาศข้อมูลสาระสําคัญในสัญญาในระบบการจัดซื้อจัดจ้าง ภาครัฐด้วยอิเล็กทรอนิกส์ (Electronic Government Procurement : e-GP) ให้มีข้อมูลการจัดซื้อจัดจ้าง สอดคล้องกับสรุปผลการดําเนินการจัดซื้อจัดจ้างของหน่วยงานของรัฐตามแบบ สขร. ๑ ตามแบบประกาศ ข้อมูลสาระสําคัญในสัญญา โดยหน่วยงานของรัฐสามารถนําประกาศดังกล่าวมาจัดไว้ในศูนย์ข้อมูลข่าวสารสําคัญ ในสัญญาได้ รายละเอียดตามสําเนาหนังสือกรมบัญชีกลาง ที่ กค ๐๔๓๓.๔/ว ๕๖๘ ลงวันที่ ๓๐ พฤศจิกายน ๒๕๖๓ ที่แนบมาพร้อมนี้ และสามารถเปิดดูได้ที่เว็บไซต์กรมส่งเสริมการปกครองท้องถิ่น www.dla.go.th จึงเรียนมาเพื่อทราบ และแจ้งเจ้าหน้าที่ที่เกี่ยวข้องถือปฏิบัติต่อไป")
            
            
            
            
            
    ]
    df = pd.DataFrame(columns=['Sentences','T-OCR Nectec','Tesseract (tha)','Lenght str sentences','Lenght str T-OCR','Lenght str Tesseract'])
    for t in listfile:
        url = "https://api.aiforthai.in.th/ocr"
        files = {'uploadfile':open('{}'.format(t[0]), 'rb')}
        
        headers = {
            'Apikey': "OwuduyXiJiAWrSWg9nskGBdfcJwNYYsL",
        }
        
        response = requests.post(url, files=files, headers=headers)
        
        textjson = response.json()

        c2 = json.loads(json.dumps(textjson))

        tocr  = c2["Original"]
        lentocr = len(tocr)

        lensentences = len(t[1])

        img  = Image.open('{}'.format(t[0]),)
        result = pytesseract.image_to_string(img, lang='tha', config='--psm 11')
        char = '\n'
        char2  = '\n\n'
        word = syllable_tokenize(result)
        word = [wo.replace(char, '') for wo in word]
        word = [wo2.replace(char2, '') for wo2 in word]

        tesserractocr = ''.join(word)

        tesserractocr.replace(' ', '')

        lentesseract = len(tesserractocr)

        resultthnd = pytesseract.image_to_string(img, lang='thnd', config='--psm 11')
        charthnd = '\n'
        char2thnd  = '\n\n'
        wordthnd = syllable_tokenize(resultthnd)
        wordthnd = [wothnd.replace(charthnd , '') for wothnd in wordthnd]
        wordthnd = [wo2thnd.replace(char2thnd , '') for wo2thnd in wordthnd]

        tesserracthnd = ''.join(wordthnd)

        tesserracthnd.replace(' ', '')

        lentesseractthnd = len(tesserracthnd)

        cer = fastwer.score_sent(tocr, t[1], char_level=True)
        round(cer,2)

        cer2 = fastwer.score_sent(tesserractocr, t[1], char_level=True)
        round(cer2,2)

        cer3 = fastwer.score_sent(tesserracthnd, t[1], char_level=True)
        round(cer3,2)


        df = df.append({ 
        'Sentences' : t[1],
        'T-OCR Nectec' :tocr ,
        'Tesseract (tha)' : tesserractocr,
        'Tesseract (thnd)' : tesserracthnd,
        'Lenght str sentences' : lensentences ,
        'Lenght str T-OCR' : lentocr,
        'Lenght str Tesseract THA' : lentesseract,
        'Lenght str Tesseract THND' : lentesseractthnd,
        'CER T-OCR' : cer,
        'CER Tesseract THA' : cer2,
        'CER Tesseract THND' : cer3,
        }
        ,ignore_index=True
        )

    #df_compare = compare_diff(df, 'T-OCR Nectec' ,'Sentences' , 'Tesseract (tha)' , lensentences , lentocr , lentesseract)

    file = 'performace.csv'
    df.to_csv(file, encoding='utf-8-sig')
