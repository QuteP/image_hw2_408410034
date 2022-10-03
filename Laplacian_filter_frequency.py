import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
from matplotlib.widgets import Slider,RadioButtons
from pic2str import blurry_moon,skeleton_orig
import base64

def GetDis(array,u,v):
    height,width=array.shape
    height=height/2
    width=width/2
    return ((u-height)**2+(v-width)**2)

def Laplacian(four):#H用
    height,width=four.shape
    new_img=np.zeros((height,width),dtype=np.complex128)
    for u in range(0,height):
        for v in range(0,width):
            new_img[u][v]=-4*(np.pi**2)*GetDis(four,u,v)
    return new_img

def FTrans(img):
    height, width =img.shape
    four_x=np.zeros((height,height),dtype=np.complex128)
    four_y=np.zeros((width,width),dtype=np.complex128)
    four=np.zeros((height,width),dtype=np.complex128)
    new_img=np.zeros((height,width),dtype=np.complex128)
    for u in range(0,height):
        for m in range(0,height):
            four_x[u][m]=np.exp(-2j * np.pi *((u*m)/height))
    for v in range(0,width):
        for n in range(0,width):
            four_y[v][n]=np.exp(-2j * np.pi *((v*n)/width))
    for x in range(0,height):
        for y in range(0,width):
            new_img[x][y]=img[x][y]*np.exp(1j * np.pi *(x+y))
    four=four_x.dot(new_img).dot(four_y)
    return four

def IFTrans(img):
    height, width =img.shape
    i_four_x=np.zeros((height,height),dtype=np.complex128)
    i_four_y=np.zeros((width,width),dtype=np.complex128)
    for x in range(0,height):
        for m in range(0,height):
            i_four_x[x][m]=np.exp(2j* np.pi *((x*m)/height))
    for y in range(0,width):
        for n in range(0,width):
            i_four_y[y][n]=np.exp(2j * np.pi *((y*n)/width))

    return i_four_x.dot(img).dot(i_four_y)/(height*width)

def LaplacianTrans(img):
    height, width =img.shape
    fp=np.pad(img,[(0,height),(0,width)],mode="constant")
    four=FTrans(fp)
    Hlp=Laplacian(four)
    flp=IFTrans(four*Hlp)
    max_v=np.max(abs(flp))
    new_flp=abs(flp/max_v*255)
    new_flp=np.clip(img+new_flp[:height,:width],0,255).astype(np.uint8) 

    return new_flp

def ReadByteImg(func):
    byte_data = base64.b64decode(func)
    img_buffer_numpy = np.frombuffer(byte_data, dtype=np.uint8) 
    return cv2.imdecode(img_buffer_numpy, cv2.IMREAD_GRAYSCALE)

def PlotHisto(fig,data,ax_lt,x_pos,y_pos):
    pos_num=x_pos+1+2*(y_pos-1)
    ax = axisartist.Subplot(fig, 2,2,pos_num)
    fig.add_subplot(ax)
    ax_lt.append(ax)
    ax.imshow(data,cmap='gray')
    ax.axis["bottom"].set_visible(False)
    ax.axis["left"].set_visible(False)
    ax.axis["top"].set_visible(False)
    ax.axis["right"].set_visible(False)
    plt.tight_layout()

moon=cv2.imread('./blurry_moon.tif',cv2.IMREAD_GRAYSCALE)
if type(moon)==type(None):
    moon=ReadByteImg(blurry_moon)
bone=cv2.imread('./skeleton_orig.bmp',cv2.IMREAD_GRAYSCALE)
if type(bone)==type(None):
    bone=ReadByteImg(skeleton_orig)

fig = plt.figure()
img_lt=[moon,bone]
ax_lt=[]
for i,(img) in enumerate(img_lt):
    new_img=LaplacianTrans(img)
    PlotHisto(fig,img,ax_lt,i,1)
    PlotHisto(fig,new_img,ax_lt,i,2)

plt.tight_layout()
plt.show()
