import base64
from PIL import Image
from io import BytesIO

# image를 base64로 전환
def image_to_base64(image_path):
    # 이미지 파일 열기
    with Image.open(image_path) as image:
        # 이미지를 바이트 스트림으로 변환
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        
        # 바이트 스트림을 base64로 인코딩
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return img_str

# base64를 image로 전환
def base64_to_image(base64_string):
    # Base64 디코딩
    decoded_data = base64.b64decode(base64_string)
    
    # 이진 데이터를 이미지로 변환
    image = Image.open(BytesIO(decoded_data))
    return image

# 이미지를 파일로 저장
def save_base64_image(base64_string, filename):
    try:        
        # Base64 디코딩
        decoded_data = base64.b64decode(base64_string)
        
        # 이미지 파일로 저장
        with open(filename, 'wb') as file:
            file.write(decoded_data)
        
        print(f"이미지가 {filename}에 성공적으로 저장되었습니다.")
    except Exception as e:
        print("이미지 저장 중 오류가 발생했습니다:", e)