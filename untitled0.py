# -*- coding: utf-8 -*-
import requests
from PIL import Image
n=15
im1 = Image.open(r'C:\Users\augu\.spyder-py3\frame5.png')
im1.save(r'test.jpg')
pic2="test.jpg"

def ai_run(pic1, pic2):
    r = requests.post(
        "https://api.deepai.org/api/image-similarity",
        files={
            'image1': open(pic1, 'rb'),
            'image2': open(pic2, 'rb'),
        },
        headers={'api-key': '66f8d598-83cb-4e00-bf75-dd62827e5016'}
    )
    dist=r.json()["output"]["distance"]
    print(dist)
    return dist

rlist = []
for i in range(n):
    pic1="image{}.jpg".format(i+1)
    res=ai_run(pic1, pic2)
    rlist.append(res)
out=sum(rlist) / n
print(out)