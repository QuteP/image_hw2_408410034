import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
from matplotlib.widgets import Slider,RadioButtons
from pic2str import blurry_moon,skeleton_orig
import base64

def HighpassTrans(img,num=35,k=2):
    height,width=img.shape
    new_img=np.zeros((height,width),dtype=np.float)
    padded_img=np.pad(img,((num//2,num//2),(num//2,num//2)),'reflect')
    core=np.ones((num,num),dtype=np.float)
    for y in range(0,height):
        for x in range(0,width):
            new_img[y][x]=(np.sum(padded_img[y:y+num,x:x+num]*core))/(num*num)
    new_img=np.clip(img-new_img,0,255)
    result_img=np.clip(img+k*new_img,0,255).astype(np.uint8)
    return result_img

def ReadByteImg(func):
    byte_data = base64.b64decode(func)
    img_buffer_numpy = np.frombuffer(byte_data, dtype=np.uint8) 
    return cv2.imdecode(img_buffer_numpy, cv2.IMREAD_GRAYSCALE)

def PlotHisto(fig,data,ax_lt,x_pos,y_pos):
    pos_num=x_pos+1+2*(y_pos-1)
    ax = axisartist.Subplot(fig, 3,2,pos_num)
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
    new_img=HighpassTrans(img)
    PlotHisto(fig,img,ax_lt,i,1)
    PlotHisto(fig,new_img,ax_lt,i,2)


axcolor = 'lightgoldenrodyellow'
om = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
som = Slider(om, r'k', 0.0, 10.0, valinit=2.0)
def update(val):
    s = som.val
    cnt=0
    for i in range(1,len(ax_lt),2):
        ax_lt[i].imshow(HighpassTrans(img_lt[cnt],k=s),cmap='gray')
        cnt+=1
som.on_changed(update)
plt.tight_layout()
plt.show()
