import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageColor
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
from sklearn.cluster import KMeans
import argparse
import imutils
import math 
import io
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab as pl
from PIL import Image
import numpy as np
import pylab
from colorsys import rgb_to_hsv


#Image Paths on my computer
WESE_Path='/Users/rohitganti/Desktop/Research/Luis Research/WSe2/'
Monolayer_Path='/Users/rohitganti/Desktop/Research/Luis Research/WSe2/Potential Monolayers'
Samples_Path='/Users/rohitganti/Desktop/Research/Luis Research/WSe2/Usable Samples'



#Creating the path directories for accessing these images easily for automation
WESE_Array=[]
for items in os.listdir(WESE_Path):
    if items[-4:-1]=='.jp':
        WESE_Array.append(WESE_Path+items)
    
Monolayer_Array=[]
for items in os.listdir(Monolayer_Path):
    Monolayer_Array.append(Monolayer_Path+ items)

Sample_Array=[]
for items in os.listdir(Samples_Path):
    Sample_Array.append(Samples_Path+items)

def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def fig2data(fig):
    fig.canvas.draw()
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w,h,4)
    buf = np.roll(buf,3,axis=2)
    return buf

def fig2img2(fig):
    buf = fig2data(fig )
    w, h, d = buf.shape
    return Image.frombytes("RGBA", (w,h), buf.tostring( ) )
    
#PIXEL BY PIXEL FUNCTIONS
def count_pixels(filename):
    """
    This function counts all the pixels in the RGB value and returns the color count in an integers format
    and the color tuple in color array
    """
    color_count = {}
    with Image.open(filename) as image:
        width, height = image.size
        rgb_image = image.convert('RGB')
        for x in range(width):
            for y in range(height):
                rgb = rgb_image.getpixel((x, y))
                if rgb in color_count:
                    color_count[rgb] += 1
                else:
                    color_count[rgb] = 1
    color_array=[]
    for colors in color_count:
        color_array.append(colors)
    return color_count, color_array

def get_max(color_dict,color_array):
    """Returns the color value with the most number of pixes or the set background """
    new_max= color_dict[color_array[0]]
    color=color_array[0]
    for colors in color_dict:
        if int(color_dict[colors])> int(new_max):
            new_max= color_dict[colors]
            color= colors
    return color

def average_tuple(nums):
    """Gets an average value for the tuple colors"""
    result = [sum(x) / len(x) for x in zip(*nums)]
    tup_down= (math.floor(result[0]), math.floor(result[1]), math.floor(result[2]))
    tup_up= (math.ceil(result[0]), math.ceil(result[1]), math.ceil(result[2]))
    return tup_down, tup_up

def get_possible_backgrounds(color_dict, color_array):
    """Returns the top five abundant backgrounds in an image"""
    new_dict= color_dict.copy()
    first_back= get_max(new_dict, color_array)
    new_dict.pop(first_back)
    color_array.remove(first_back)
    second_back= get_max(new_dict, color_array)
    new_dict.pop(second_back)
    color_array.remove(second_back)
    third_back= get_max(new_dict, color_array)
    new_dict.pop(third_back)
    color_array.remove(third_back)
    fourth_back= get_max(new_dict,color_array)
    new_dict.pop(fourth_back)
    color_array.remove(fourth_back)
    fifth_back= get_max(new_dict, color_array)
    new_dict.pop(fifth_back)
    color_array.remove(fifth_back)
    all_tuples= first_back, second_back, third_back, fourth_back, fifth_back
    #total_similar_pixels= color_dict[first_back]+color_dict[second_back]+color_dict[third_back]+color_dict[fourth_back]+color_dict[fifth_back]
    return first_back,second_back,third_back,fourth_back,fifth_back


image_number=WESE_Array[4]
color_dict, color_array= count_pixels(image_number)
print(color_dict)


print()
print()
print(color_array)



def generate_heatmap(image_number):
    """
    This function is used to create and save 
    """
    img= Image.open(image_number).convert('L')
    z= np.asarray(img)
    mydata= z[::1,::1]
    fig= pl.figure(facecolor='w')
    ax1= fig.add_subplot(1,2,1)
    im= ax1.imshow(mydata, interpolation='nearest', cmap=pl.cm.jet)
    pl.xticks([])
    pl.yticks([])
    #pl.show()
    b= fig2img(fig)
    c=b.resize(img.size)
    d= c.convert('RGB')
    im= image_number.strip('.jpg')
    string= im+'heatmap.jpg'
    d.save(string)
    return d


image_number= WESE_Array[4]
image_number_stripped= image_number.strip('.jpg')
generate_heatmap(image_number_stripped+'heatmap.jpg')
ab=Image.open(image_number_stripped+'heatmap.jpg')
print(ab)




