# -*- coding: utf-8 -*-
"""
This is a prototype script.
"""
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from scipy.ndimage import gaussian_filter
import cv2
from skimage import io as ip


frame_rate = 24 #output frame rate


vidcap = cv2.VideoCapture('video9.mov')
success,image = vidcap.read()
count = 1
print('Demuxing video')
while success:
  cv2.imwrite("frame%d.png" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  count += 1

def initial_processing(iminit, low_val, max_val):
    img = Image.open(iminit)
    converter = ImageEnhance.Contrast(img)
    print(low_val)
    print(max_val)
    cont = (1/(max_val/low_val))*2.0
    img = converter.enhance(cont)
    array = np.array(img)
    ip.imsave('temp1.png', array)

def calc_val(im1):
    img = Image.open(im1)
    array = np.array(img)
    low_val = np.mean(array)
    max_val = np.amax(array)
    return low_val, max_val
    
def imadd(I, K):

    import numbers
    if isinstance(K, numbers.Number):
        J = I.astype('int32')
        J += K
    elif isinstance(K, np.ndarray):
        assert K.shape == I.shape, f'Cannot add images with sizes {I.shape} and {K.shape}.'
        J = I.astype('int32') + K.astype('int32')
    else:
        raise TypeError('K must be a number or an array.')
    
    np.clip(J, 0, 255, out=J)
    J = J.astype('uint8')
    return J

def gaussian_filt(I, sigma, pad=0):

    import numbers
    assert isinstance(pad, numbers.Number) or pad in ['reflect', 'nearest', 'wrap'], \
            'Choose a correct value for pad: a number (0-255), ''reflect'', ''nearest'', or ''wrap''.'

    if isinstance(pad, numbers.Number):
        md = 'constant'
        c = pad
    else:
        md = pad
        c = 0
    return gaussian_filter(I, sigma, mode=md, cval=c)

def final_processing(finalim, k):
    I = ip.imread(finalim)
   
    
    R = np.logical_and(I[:, :, 0] > 254, I[:, :, 1] < 255)
    
    new_R = gaussian_filt(255 * R, 5)
    
    J = I.copy()
    J[:, :, 0] = imadd(new_R, J[:, :, 0])
    
    ip.imsave('temp.png', J)
    img2 = Image.open('temp.png')
    converter = ImageEnhance.Color(img2)
    img2 = converter.enhance(1.4)
    im = np.array(img2)
    ip.imsave('final{}.png'.format(k), im)
    
def process_loop(): 
    for i in range(count):
        low_val, max_val=calc_val('frame{}.png'.format(i+1))
        print('Processing image {}'.format(i+1))  
        initial_processing('frame{}.png'.format(i+1), low_val, max_val)
        final_processing('temp1.png', i+1)
        
def video_mux():
    print("Remuxing Files")
    pathOut = 'video_out.mp4'
    fps = frame_rate
    frame_array = []
    files = ['final{}.png'.format(i+1) for i in range(count)]
    for i in range(len(files)):
        #filename=pathIn + files[i]
        filename=files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        #inserting the frames into an image array
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'H264'), fps, size) 
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
count = count-1      
process_loop()
video_mux()

