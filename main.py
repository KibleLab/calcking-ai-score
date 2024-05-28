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

@app.post("/v1/ocr-number")
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
    img = cv2.imread(file)
    text = reader.readtext(img, detail=0, allowlist="0123456789x")
    return {"result" : text}