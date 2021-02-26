# -*- coding: utf-8 -*-
import requests
from PIL import Image
n= #insert the number of frames in the reference 
im1 = Image.open(r'insert the location of your test frame')
im1.save(r'test.jpg')
pic2="test.jpg"

def ai_run(pic1, pic2):
    r = requests.post(
        "https://api.deepai.org/api/image-similarity",
        files={
            'image1': open(pic1, 'rb'),
            'image2': open(pic2, 'rb'),
        },
        headers={'api-key': 'insert your own api key'}
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
