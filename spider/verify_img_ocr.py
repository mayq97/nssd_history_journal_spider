#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PIL import Image  # 用于打开图片和对图片处理
from aip import AipOcr
from spider.CONFIG import API_KEY,APP_ID,SECRET_KEY

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def picture_process(img):
    page_snap_obj = Image.open('./temp/pictures.png')
    location = img.location
    size = img.size  # 获取验证码的大小参数
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']
    image_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
    img = image_obj.convert("L")  # 转灰度
    pixdata = img.load()
    w, h = img.size
    threshold = 160
    # 遍历所有像素，大于阈值的为黑色
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    img.save("./temp/code.png")

def ocr(img=None):
    picture_process(img)
    image = get_file_content('./temp/code.png')
    try:
        """ 调用通用文字识别, 图片参数为本地图片 """
        res =  client.basicGeneral(image)
        code = res["words_result"][0]["words"]
        code = code.replace(" ","").replace(" ","")
        return code.strip()
    except Exception:
        return "n"
if __name__ == "__main__":
    ocr()