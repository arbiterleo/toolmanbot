import numpy as np
import cv2
import matplotlib.pyplot as plt

def asd():

  img = cv2.imread("./toolmanbot/bg.png")
# 文字
  text = point
  cv2.putText(img, text, (273, 210), cv2.FONT_HERSHEY_SIMPLEX,2,(5, 209, 255), 6, cv2.LINE_AA)
# 將 BGR 圖片轉為 RGB 圖片
  img = img[:,:,::-1]

# 繪圖
  fig=plt.figure(figsize=(8,10))

  ax1=fig.add_subplot(211)
  ax1.axis('off')
  ax1.imshow(img)

  feature = ['Frequency', 'Speed', 'Contents', 'Amounts', 'Call frequency', 'Call time']
  values=[-0.1, 0.2, 0.3, 0.4, -0.3, 0.5]
# 設置每個數據點的顯示位置，在雷達圖上用角度表示
  angles=np.linspace(0, 2*np.pi,len(values), endpoint=False)
# 設置爲極座標格式
  ax = fig.add_subplot(212, polar=True)
# 繪製折線圖
  ax.plot(angles, values, 'o-', linewidth=2)
  # 填充顏色
  ax.fill(angles, values, alpha=0.25)

  # 設置圖標上的角度劃分刻度，爲每個數據點處添加標籤
  ax.set_thetagrids(angles * 180/np.pi, feature)

  ax.set_rlim(-2.0, 2.0)
# 添加網格線
  ax.grid(True)
# 添加標題
  plt.title('Favorability Report')

  plt.show
