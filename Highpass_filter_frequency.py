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

def GLPF(four,d):
    height,width=four.shape
    new_img=np.zeros((height,width),dtype=np.complex128)
    for u in range(0,height):
        for v in range(0,width):
            new_img[u][v]=np.exp(-1*GetDis(four,u,v)/(2*(d**2)))
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

def IFTrans(img):#待修理
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

def HighpassTrans(img,d=500,k=20):
    height, width =img.shape
    fp=np.pad(img,[(0,height),(0,width)],mode="constant")
    four=FTrans(fp)
    Hlp=GLPF(four,d)
    flp=IFTrans(four*Hlp)
    max_v=np.max(abs(flp))
    new_flp=abs(flp/max_v*255)
    new_flp=np.clip(img-new_flp[:height,:width],0,255)
    return np.clip(img+k*new_flp,0,255).astype(np.uint8)

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
som = Slider(om, r'k', 0.0, 100.0, valinit=20.0)
def update(val):
    s = som.val
    cnt=0
    for i in range(1,len(ax_lt),2):
        ax_lt[i].imshow(HighpassTrans(img_lt[cnt],k=s),cmap='gray')
        cnt+=1
som.on_changed(update)
plt.tight_layout()
plt.show()
