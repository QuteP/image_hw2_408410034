# 影像處理作業2——Image Sharpening

### 作業描述：

Give two gray-level images, sharpen the two images using the Laplacian operator, unsharp masking, and high-boost filtering in the spatial and frequency domains.

Platform:

(1) Matlab, python, or others … 只要讓助教在windows電腦上不必額外安裝任何軟體就能執行並顯示結果即可。

(2) 結果需show出原始images與三種方法做完sharpening之後的images。

### 作業成果：

- Highpass_filter_frequency.py：

  上面是原圖，下面是處理過的圖。此時的k設為20。

  <img src="https://github.com/QuteP/image_hw2_408410034/blob/main/result/Figure_1.png" alt="image-20221004104145624" style="zoom:50%;" align='left'/>

- Highpass_filter_spatial.py：

  上面是原圖，下面是處理過的圖。此時的k設為2。

  <img src="https://github.com/QuteP/image_hw2_408410034/blob/main/result/Figure_2.png" alt="image-20221004104320215"  style="zoom:50%;" align='left' />

- Laplacian_filter_frequency.py：

  上面是原圖，下面是處理過的圖。

  <img src="https://github.com/QuteP/image_hw2_408410034/blob/main/result/Figure_3.png" alt="image-20221004104407727" style="zoom:50%;" align='left' />

- Laplacian_filter_spatial.py：

  上面是原圖，中間是用對角線為0的mask處理的結果，下面是用對角線不為0的mask處理的結果。

  <img src="https://github.com/QuteP/image_hw2_408410034/blob/main/result/Figure_4.png" alt="image-20221004104529140" style="zoom:65%;" align='left' />

- Unsharp_mask_frequency.py：

  上面是原圖，下面是處理過的圖。

  <img src="https://github.com/QuteP/image_hw2_408410034/blob/main/result/Figure_5.png" alt="image-20221004104558893" style="zoom:50%;" align='left' />

- Unsharp_mask_spatial.py：

  上面是原圖，下面是處理過的圖。

  <img src="https://github.com/QuteP/image_hw2_408410034/blob/main/result/Figure_6.png" alt="image-20221004104626679" style="zoom:50%;" align='left' />
