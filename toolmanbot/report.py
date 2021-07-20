import numpy as np
import matplotlib.pyplot as plt


#def plot(analysis_point):
labels=["對話頻率","回話速度","情感分析","訊息內容量","通話頻率","通話時間"]


#資料個數
dataLenth =6
#資料
data = np.array([0.3,0.5,0,0.78,0.65,0.9])

angles = np.linspace(0, 2*np.pi, dataLenth, endpoint=False)
data = np.concatenate((data, [data[0]])) # 閉合 # #將資料結合起來
angles = np.concatenate((angles, [angles[0]])) # 閉合

fig = plt.figure()
ax = fig.add_subplot(121, polar=True)# polar引數！！代表畫圓形！！！！
    #111代表總行數總列數位置
ax.plot(angles, data, 'bo-', linewidth=1)# 畫線四個引數為x,y,標記和顏色，閒的寬度
ax.fill(angles, data, facecolor='r', alpha=0.1)# 填充顏色和透明度
ax.set_thetagrids(angles * 180/np.pi, labels, fontproperties="SimHei")
ax.set_title("老齊屬性分析", va='baseline', fontproperties="SimHei")
ax.set_rlim(0,10)
ax.grid(True)
plt.show()


