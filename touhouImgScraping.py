from urllib import request
import os
import io

from selenium import webdriver
from PIL import Image

while True:
    url = input("東方画像まとめブログのURLを入力してください")
    html = webdriver.Chrome("chromedriver.exe")
    html.get(url)

    elem_2d = html.find_element_by_class_name("article-body-inner")

    folder_name = html.title.replace("\u3000", "").replace(":", "")
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        print("このURLの画像はすでに取得しています")
        html.quit()
        continue

    elem_imgs = elem_2d.find_elements_by_tag_name("img")
    urlList = []
    for i,elem_img in enumerate(elem_imgs):
        alt_img = elem_img.get_attribute("alt")
        img_url = elem_img.get_attribute("src")
        urlList.append(img_url)
        

    for i, url in enumerate(urlList):
        f = io.BytesIO(request.urlopen(url).read())
        img = Image.open(f)
        if img.mode != "RGB":
            img = img.convert("RGB")

        img.save(f"{folder_name}/image{i}.jpg")

    html.quit()

    continue_program=input("他の記事の画像も取得しますか？(Yes or No)\n")
    if continue_program.upper()=="NO":
        break