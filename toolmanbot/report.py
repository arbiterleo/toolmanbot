import numpy as np
import matplotlib.pyplot as plt
import pyimgur
import cv2

def draw(CLIENT_ID,values,point):

  #上半部
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

  #下半部
  plt.rcParams['axes.unicode_minus'] = False  #用於正常顯示符號
  feature = ['Frequency', 'Speed', 'Contents', 'Amounts', 'Call frequency', 'Call time']
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

  #雷達圖數值分佈
  ax.set_rlim(-2.0, 2.0)
  plt.title(u'Favorability Report')
  # 添加網格線
  ax.grid(True)

  #儲存圖片到imgur
  plt.savefig('report.png', bbox_inches='tight', pad_inches=0.1)
  PATH='report.png'
  im = pyimgur.Imgur(CLIENT_ID)
  uploaded_image = im.upload_image(PATH, title="Report")

  return uploaded_image.link



