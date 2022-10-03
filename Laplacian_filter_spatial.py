import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
from matplotlib.widgets import Slider,RadioButtons
from pic2str import blurry_moon,skeleton_orig
import base64

def LaplacianSharpen(img,mode=0):
    height,width=img.shape
    new_img=np.zeros((height,width),dtype=np.float)
    padded_img=np.pad(img,((1,1),(1,1)),'reflect')
    core=np.array([[1,1,1],[1,-8,1],[1,1,1]])
    if mode==1:
        core=np.array([[0,1,0],[1,-4,1],[0,1,0]])
    for y in range(0,height):
        for x in range(0,width):
            new_img[y][x]=np.sum(padded_img[y:y+3,x:x+3]*core)
    result_img=np.clip(img-new_img,0,255).astype(np.uint8)
    return result_img

def ReadByteImg(func):
    byte_data = base64.b64decode(func)
    img_buffer_numpy = np.frombuffer(byte_data, dtype=np.uint8) 
    return cv2.imdecode(img_buffer_numpy, cv2.IMREAD_GRAYSCALE)

def PlotHisto(fig,data,pos_num):
    ax = axisartist.Subplot(fig, 3,2,pos_num)
    fig.add_subplot(ax)
    ax.imshow(data,cmap='gray')
    ax.axis["bottom"].set_visible(False)
    ax.axis["left"].set_visible(False)
    ax.axis["top"].set_visible(False)
    ax.axis["right"].set_visible(False)
    plt.tight_layout()

def PlotBackground(i,title):
    ax = axisartist.Subplot(fig, 3,2,i)
    fig.add_subplot(ax)
    ax.axis["bottom"].set_visible(False)
    ax.axis["left"].set_visible(False)
    ax.axis["top"].set_visible(False)
    ax.axis["right"].set_visible(False)
    ax.annotate(title, xy=(0,0.5))
    plt.tight_layout()

moon=cv2.imread('./blurry_moon.tif',cv2.IMREAD_GRAYSCALE)
if type(moon)==type(None):
    moon=ReadByteImg(blurry_moon)
bone=cv2.imread('./skeleton_orig.bmp',cv2.IMREAD_GRAYSCALE)
if type(bone)==type(None):
    bone=ReadByteImg(skeleton_orig)

fig = plt.figure()
img_lt=[moon,bone]
# PlotBackground(1,'original images')
# PlotBackground(4,'mask without diagonal')
# PlotBackground(7,'mask with diagonal')
for i,(img) in enumerate(img_lt):
    diagonal_img=LaplacianSharpen(img,mode=0)
    w_diagonal_img=LaplacianSharpen(img,mode=1)
    PlotHisto(fig,img,i+1)
    PlotHisto(fig,w_diagonal_img,i+3)
    PlotHisto(fig,diagonal_img,i+5)

plt.tight_layout()
plt.show()