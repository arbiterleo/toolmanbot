import numpy as np
import matplotlib.pyplot as plt
import pyimgur

def draw(CLIENT_ID,attributes):

  # Label
  labels = np.array(['a', 'b', 'c', 'd', 'e', 'f'])
  # Value
  data = np.array(attributes)
  angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
  data = np.hstack((data, [data[0]]))
  angles = np.hstack((angles, [angles[0]]))
  fig = plt.figure(figsize=(10, 10))
  ax = fig.add_subplot(111, polar=True)
  ax.plot(angles, data, 'ro-', linewidth=2)
  plt.savefig('report.png', bbox_inches='tight', pad_inches=0.1)

  PATH='report.png'
  im = pyimgur.Imgur(CLIENT_ID)
  uploaded_image = im.upload_image(PATH, title="Report")

  return uploaded_image.link



