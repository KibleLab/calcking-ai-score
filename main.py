import datetime
import os
from fastapi import FastAPI
from pydantic import BaseModel
import easyocr
import cv2
from utils.preprocessing import save_base64_image

app = FastAPI()

class OcrDto(BaseModel):
    image: str

@app.post("/v1/ocr")
def ocr_number(ocrDto: OcrDto):

    folder = "imgs"

    # 현재 시간을 문자열로 가져오기 (예: '2024-05-27_12-30-45')
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
    # 이미지 파일명 생성
    file = f"imgs/{current_time}.png"

    # If the folder doesn't exist, Create
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save a Base64 string as an image
    save_base64_image(ocrDto.image, file)

    reader = easyocr.Reader(['ko', 'en'], gpu=True)



    # 자를 영역 지정 (x, y, width, height)
    x, y, width, height = 0, 0, 250, 180  # 예시 값, 실제 이미지에 맞게 조정 필요

    # 이미지 자르기
    cropped_image = crop_image(file, x, y, width, height)



    # img = cv2.imread(cropped_image)
    textArr = reader.readtext(cropped_image, detail=0, allowlist="0123456789+-x")
    
    #배열을 문자열로 바꿈
    text = "".join(textArr)

    # 연산을 수행함.
    anwser = calculate(text)

    return {"result" : text + '=' + str(anwser)}


def calculate(text):
    operators = ['+', '-', 'x', '/']
    for op in operators:
        if op in text:
            parts = text.split(op)
            if len(parts) == 2:
                a, b = int(parts[0]), int(parts[1])
                if op == '+':
                    return a + b
                elif op == '-':
                    return a - b
                elif op == 'x':
                    return a * b
                elif op == '/':
                    return a / b
    return "유효한 연산이 아닙니다."

def crop_image(image_path, x, y, width, height):
    # 이미지 읽기
    image = cv2.imread(image_path)
    
    # 지정된 영역 자르기
    cropped_image = image[y:y+height, x:x+width]
    
    return cropped_image