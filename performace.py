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
                  ("109.jpg","เรื่อง การเตรียมความพร้อม เฝ้าระวัง ป้องกันควบคุมการระบาดของโรคติดเชื้อต่าง ๆ ตามข้อสั่งการนายกรัฐมนตรี"),
            ("110.jpg","อ้างถึง หนังสือกรมการปกครองที่ มท ๐๓๑๙ /ว ๑๘๗๗")
            
            
            
            
    ]
    df = pd.DataFrame(columns=['Sentences','T-OCR Nectec','Tesseract (tha)','Lenght str sentences','Lenght str T-OCR','Lenght str Tesseract'])
    for t in listfile:
        url = "https://api.aiforthai.in.th/ocr"
        files = {'uploadfile':open('testset/{}'.format(t[0]), 'rb')}
        
        headers = {
            'Apikey': "OwuduyXiJiAWrSWg9nskGBdfcJwNYYsL",
        }
        
        response = requests.post(url, files=files, headers=headers)
        
        textjson = response.json()

        c2 = json.loads(json.dumps(textjson))

        tocr  = c2["Original"]
        lentocr = len(tocr)

        lensentences = len(t[1])
        img  = Image.open('testset/{}'.format(t[0]),)
        result = pytesseract.image_to_string(img, lang='tha', config='--psm 11')
        char = '\n'
        char2  = '\n\n'
        word = syllable_tokenize(result)
        word = [wo.replace(char, '') for wo in word]
        word = [wo2.replace(char2, '') for wo2 in word]

        tesserractocr = ''.join(word)

        tesserractocr.replace(' ', '')

        lentesseract = len(tesserractocr)

        cer = fastwer.score_sent(tocr, t[1], char_level=True)
        round(cer,2)

        cer2 = fastwer.score_sent(tesserractocr, t[1], char_level=True)
        round(cer2,2)


        df = df.append({ 'Sentences' : t[1],
        'T-OCR Nectec' :tocr ,
        'Tesseract (tha)' : tesserractocr,
        'Lenght str sentences' : lensentences ,
        'Lenght str T-OCR' : lentocr,
        'Lenght str Tesseract' : lentesseract,
        'CER 1' : cer,
        'CER 2' : cer2,
        }
        ,ignore_index=True
        )

    #df_compare = compare_diff(df, 'T-OCR Nectec' ,'Sentences' , 'Tesseract (tha)' , lensentences , lentocr , lentesseract)

    file = 'report_performace_01.csv'
    df.to_csv(file, encoding='utf-8-sig')
