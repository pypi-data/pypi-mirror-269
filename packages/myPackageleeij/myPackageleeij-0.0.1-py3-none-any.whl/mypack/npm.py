
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def hist(file_path, bin): # 히스토그램 제공, csv파일을 읽어 히스토그램을 만든다.
  data = pd.read_csv(file_path)

  plt.hist(data, label = 'label='+str(bin), bins=int(bin))
  plt.legend()
  plt.show()

def pie(ratio_list, label_list): # 두 리스트를 입력하면, 원 그래프 제공
  plt.pie(ratio_list, labels=label_list, autopct='%.1f%%')
  plt.show()


def bar(a_list, b_list):  # 두 리스트에 관한 막대그래프 제공
  a = np.array(a_list)
  b = np.array(b_list)
  plt.bar(a, b)
  plt.show()

def plot(x_list, y_list, title_name, lab): # (x리스트, y리스트, 제목, 라벨) 으로 입력시 꺾은 선 그래프를 제공
  x = x_list
  y = y_list

  plt.plot(x, y, linestyle='solid', label= lab)

  plt.legend(loc='best')

  plt.title(title_name)
  plt.show()
