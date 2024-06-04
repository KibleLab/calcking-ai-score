import easyocr
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
from PIL import ImageDraw, Image

file = './imgs/testImage.png'

reader = easyocr.Reader(['ko', 'en'], gpu = True)
result = reader.readtext(file, allowlist="0123456789+x")

img = cv2.imread(file)
img = Image.fromarray(img)
draw = ImageDraw.Draw(img)
COLORS = np.random.randint(0, 255, size=(255, 3), dtype="uint8")

print("----------------------------")
for i in result :
    # 텍스트 영역의 좌상단 x 좌표
    x = i[0][0][0] 
    # 텍스트 영역의 좌상단 y 좌표
    y = i[0][0][1] 
    # 텍스트 영역의 너비
    w = i[0][1][0] - i[0][0][0]
    # 텍스트 영역의 높이
    h = i[0][2][1] - i[0][1][1]
    print(x,y,w,h)
    print("인식된 값 : ", i[1])
    print("정확도 : ", i[2])
    print("----------------------------")

    color_idx = random.randint(0, 255) 
    color = [int(c) for c in COLORS[color_idx]]

    draw.rectangle(((x, y), (x + w, y + h)), outline=tuple(color), width=2)
    draw.text((int((x + x + w) / 2) , y - 2), str(i[1]), fill=tuple(color))

plt.figure()
plt.imshow(img)
plt.axis('off')  # xy축 숨기기
plt.tight_layout()  # 이미지 크기에 맞게 조정
plt.show()