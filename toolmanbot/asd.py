import numpy as np
import matplotlib.pyplot as plt
# 用於正常顯示中文
plt.rcParams['font.sans-serif'] = 'SimHei'
#用於正常顯示符號
plt.rcParams['axes.unicode_minus'] = False

# 使用ggplot的繪圖風格，這個類似於美化了，可以通過plt.style.available查看可選值，你會發現其它的風格真的醜。。。
#plt.style.use('ggplot')

# 構造數據
values = [0.6,0.1,0.4,0.3,0.1,-0.5]
feature = ['對話頻率', '回話速度', '回話內容', '訊息內容量', '通話頻率', '通話時間']

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

# 添加標題
plt.title('好感度報表')
# 添加網格線
ax.grid(True)

plt.show()