import numpy as np
import matplotlib.pyplot as plt
import pyimgur
import cv2
import requests
import io
from PIL import Image

def draw(CLIENT_ID,values,point,difference):


  #圖表
  features = ['Frequency','Speed','Contents','Amounts','Call']
  data_length = len(values)
  angles = np.linspace(0,2*np.pi,data_length,endpoint=False)
  values = np.concatenate((values,[values[0]]))
  angles = np.concatenate((angles,[angles[0]]))
  features = np.concatenate((features,[features[0]]))
  theta = np.linspace(0,np.pi*2,6)

  values1=[(values[0]+values[1])/2,(values[2]+values[3])/2,values[4]]
  max1=max(values1)
  values2=values1.copy()
  values2[np.argmax(values2)]=np.min(values1)
  max2=max(values2)

  if max1-max2 >10:
    plt.polar(theta,values,color="#8BCCD0",marker='.')
    plt.xticks(theta,features)
    plt.fill(theta,values,color="#56F1D7")
    plt.savefig('report.png', bbox_inches='tight', pad_inches=0.1,transparent = True)
    PATH='report.png'
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Report")
    img_response = requests.get(uploaded_image.link)
    imageB = Image.open(io.BytesIO(img_response.content))
    imageB = imageB.convert('RGBA')
    widthB , heightB = imageB.size

#Unicorn
    if max(values1)==values1[0]:
        imageA = cv2.imread('./toolmanbot/unicorn.png')
        text = point
        cv2.putText(imageA, text, (7, 195), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,3.4,(0, 0, 0), 6, cv2.LINE_AA)
        text1 = difference
        cv2.putText(imageA, text1, (135, 190), cv2.FONT_HERSHEY_COMPLEX,0.55,(22, 116, 226), 1, cv2.LINE_AA)
        imageA = Image.fromarray(cv2.cvtColor(imageA,cv2.COLOR_BGR2RGB))
        imageA = imageA.convert('RGBA')
        widthA , heightA = imageA.size

#PloarBear
    elif max(values1)==values1[1]:
        imageA = cv2.imread('./toolmanbot/polarbear.png')
        text = point
        cv2.putText(imageA, text, (5, 150), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,3.4,(0, 0, 0), 6, cv2.LINE_AA)
        text1 = difference
        cv2.putText(imageA, text1, (85, 170), cv2.FONT_HERSHEY_COMPLEX,0.55,(22, 116, 226), 1, cv2.LINE_AA)
        imageA = Image.fromarray(cv2.cvtColor(imageA,cv2.COLOR_BGR2RGB))
        imageA = imageA.convert('RGBA')
        widthA , heightA = imageA.size

#Peacock
    elif max(values1)==values1[2]:
        imageA = cv2.imread('./toolmanbot/peacock.png')
        text = point
        cv2.putText(imageA, text, (45, 155), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,3.4,(0, 0, 0), 6, cv2.LINE_AA)
        text1 = difference
        cv2.putText(imageA, text1, (120, 180), cv2.FONT_HERSHEY_COMPLEX,0.55,(22, 116, 226), 1, cv2.LINE_AA)
        imageA = Image.fromarray(cv2.cvtColor(imageA,cv2.COLOR_BGR2RGB))
        imageA = imageA.convert('RGBA')
        widthA , heightA = imageA.size

#deer
  else:
    plt.polar(theta,values,color="#000000")
    plt.xticks(theta,features)
    plt.fill(theta,values,color="#DD2D57")
    plt.savefig('report.png', bbox_inches='tight', pad_inches=0.1,transparent = True)
    PATH='report.png'
    im = pyimgur.Imgur("e00f48cb1956755")
    uploaded_image = im.upload_image(PATH, title="Report")
    img_response = requests.get(uploaded_image.link)
    imageB = Image.open(io.BytesIO(img_response.content))
    imageB = imageB.convert('RGBA')
    widthB , heightB = imageB.size
    imageA = cv2.imread('./toolmanbot/deer.png')
    text = point
    cv2.putText(imageA, text, (40, 110), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,3.4,(0, 0, 0), 6, cv2.LINE_AA)
    text1 = difference
    cv2.putText(imageA, text1, (105, 130), cv2.FONT_HERSHEY_COMPLEX,0.55,(22, 226, 195), 1, cv2.LINE_AA)
    imageA = Image.fromarray(cv2.cvtColor(imageA,cv2.COLOR_BGR2RGB))
    imageA = imageA.convert('RGBA')
    widthA , heightA = imageA.size

#重設簽名檔的寬為照片的1/2
  newWidthB = int(widthA/2)
#重設簽名檔的高依據新的寬度等比例縮放
  newHeightB = int(heightB/widthB*newWidthB)
#重設簽名檔圖片
  imageB_resize = imageB.resize((newWidthB, newHeightB))
#新建一個透明的底圖
  resultPicture = Image.new('RGBA', imageA.size, (0, 0, 0, 0))
#把照片貼到底圖
  resultPicture.paste(imageA,(0,0))
#設定簽名檔的位置參數
  right_bottom = (widthA - newWidthB, heightA - newHeightB)
#為了背景保留透明度，將im參數與mask參數皆帶入重設過後的簽名檔圖片
  resultPicture.paste(imageB_resize, right_bottom, imageB_resize)
#儲存新的照片
  resultPicture.save("report.png")
  #儲存圖片到imgur
  #plt.savefig('report.png', bbox_inches='tight', pad_inches=0.1)
  PATH='report.png'
  im = pyimgur.Imgur(CLIENT_ID)
  uploaded_image = im.upload_image(PATH, title="Report")
  print(uploaded_image.link)
  return uploaded_image.link


def text_report(values,values_p):

  values1=[(values[0]+values[1])/2,(values[2]+values[3])/2,values[4]]
  values2=[(values_p[0]+values_p[1])/2,(values_p[2]+values_p[3])/2,values_p[4]]

  text_description=[]

  for i in range(len(values1)):
    if values1[i]>=values2[i]:

      if values1[i]-values2[i]>=20:
        text_description.append("進步幅度：高")

      elif values1[i]-values2[i]>=10:
        text_description.append("進步幅度：中")

      else:
       text_description.append("進步幅度：低")

    else:
      if values2[i]-values1[i]>=20:
        text_description.append("退步幅度：高")

      elif values2[i]-values1[i]>=10:
        text_description.append("退步幅度：中")

      else:
       text_description.append("退步幅度：低")

  description =f"回話速度＆頻率的{text_description[0]}\
                \n回話內容＆情感的{text_description[1]}\
                \n通話時間＆頻率的{text_description[2]}"
  print(description)
  return description

