import numpy as np
import matplotlib.pyplot as plt
import pyimgur
import cv2
from matplotlib.gridspec import GridSpec
def draw(CLIENT_ID,values,point,new_data,pst_data):

  #上半部
  img = cv2.imread("./toolmanbot/S__17989845.jpg")
  # 文字
  text = point
  cv2.putText(img, text, (300, 320), cv2.FONT_HERSHEY_SIMPLEX,4.5,(201, 148, 255), 8, cv2.LINE_AA)
  # 將 BGR 圖片轉為 RGB 圖片
  img = img[:,:,::-1]
  # 繪圖
  fig=plt.figure(figsize=(8,8))

  gs=GridSpec(2,2)

  #rect = fig.patch
  #rect.set_facecolor((0, 0, 0,0))

  ax1=fig.add_subplot(gs[0,0])
  ax1.axis('off')
  ax1.imshow(img)
  #圓餅圖
  feature = ['Frequency', 'Speed', 'Contents', 'Amounts', 'Call frequency', 'Call time']

  ax = fig.add_subplot(gs[0,1])
  #color = ['#E6CAFF', '#F1E1FF', '#97CBFF', '#ACD6FF','#AAAAFF', '#D3A4FF']
  color = ['#FFC1E0','#FFD9EC',  '#FF95CA', '#FF60AF','#FF0080', '#FF95CA']
  ax.pie(values,colors=color,labels = feature[0:6],autopct = "%1.2f%%",pctdistance = 0.6)
  plt.axis('equal')                                          # 使圓餅圖比例相等
  #plt.legend(loc = "best")
  # 添加標題
  plt.title("Feature's weight Report")

  ax2 = fig.add_subplot(gs[1,:])
  x = np.arange(0, 6)

  ax2.bar(x+0.1, new_data, width = 0.2,color=(1,0,0.5))
  ax2.bar(x-0.1, pst_data, width = 0.2,color=(1,0.76,0.88))
  ax2.set_axisbelow(True)
  ax2.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)
  ax2.set_ylim(-100, 100)
  plt.xticks(x,feature)
  plt.title("Points (Now v.s Past)")
  plt.legend(["Now","Past"])


  #儲存圖片到imgur
  plt.savefig('report.png', bbox_inches='tight', pad_inches=0.1)
  PATH='report.png'
  im = pyimgur.Imgur(CLIENT_ID)
  uploaded_image = im.upload_image(PATH, title="Report")

  return uploaded_image.link



