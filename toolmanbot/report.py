import numpy as np
import matplotlib.pyplot as plt
import pyimgur

def draw(CLIENT_ID,attributes):

  plt.rcParams['font.sans-serif']=['SimHei']# 設定載入的字型名
  plt.rcParams['axes.unicode_minus']=False #解決儲存影象是負號'-'顯示為方塊的問題

  # Label
  labels = np.array([u'對話頻率', u'回話速度', u'回話內容', u'訊息內容量', u'通話頻率', u'通話時間'])

  # Value
  data = np.array(attributes)
  angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
  data = np.hstack((data, [data[0]]))
  angles = np.hstack((angles, [angles[0]]))
  fig = plt.figure(figsize=(10, 10))
  ax = fig.add_subplot(111, polar=True)
  ax.plot(angles, data, 'ro-', linewidth=2)
  plt.title(u'好感度報表')
  plt.savefig('report.png', bbox_inches='tight', pad_inches=0.1)

  PATH='report.png'
  im = pyimgur.Imgur(CLIENT_ID)
  uploaded_image = im.upload_image(PATH, title="Report")

  return uploaded_image.link



