import numpy as np
import matplotlib.pyplot as plt
import pyimgur

def draw(CLIENT_ID,values):

  # 用於正常顯示中文
  plt.rcParams['font.sans-serif'] = 'SimHei'
  #用於正常顯示符號
  plt.rcParams['axes.unicode_minus'] = False
  # 構造數據

  feature = [u'Frequency', u'Speed', u'Contents', u'Amounts', u'Call frequency', u'Call time']

  # 設置每個數據點的顯示位置，在雷達圖上用角度表示
  angles=np.linspace(0, 2*np.pi,len(values), endpoint=False)

  # 繪圖
  fig=plt.figure()
  # 設置爲極座標格式
  ax = fig.add_subplot(111, polar=True)
  # 繪製折線圖
  ax.plot(angles, values, 'o-', linewidth=2)
  # 填充顏色
  ax.fill(angles, values, alpha=0.25)

  # 設置圖標上的角度劃分刻度，爲每個數據點處添加標籤
  ax.set_thetagrids(angles * 180/np.pi, feature)

  ax.set_rlim(-0.5, 0.5)

  # 添加標題
  plt.title(u'Favorability Report')
  # 添加網格線
  ax.grid(True)

  plt.savefig('report.png', bbox_inches='tight', pad_inches=0.1)

  PATH='report.png'
  im = pyimgur.Imgur(CLIENT_ID)
  uploaded_image = im.upload_image(PATH, title="Report")

  return uploaded_image.link



