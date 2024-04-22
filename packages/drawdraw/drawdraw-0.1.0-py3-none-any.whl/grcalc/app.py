
import numpy as np
import matplotlib.pyplot as plt

def getscatter():
  x_values = input("쉼표를 이용해 x값을 입력해주세요: ").split(',')
  y_values = input("쉼표를 이용해 y값을 입력해주세요: ").split(',')
  x_data = [float(x.strip()) for x in x_values]
  y_data = [float(y.strip()) for y in y_values]

  return x_data,y_data

def scatter_plot(x_data,y_data,x_label='', y_label='', title=''):

    # scatter plot 그리기
    plt.scatter(x_data, y_data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def getbox():
  num_datasets = int(input("상자 그림을 그릴 데이터셋의 개수를 입력하세요: "))
  data = []
  for i in range(num_datasets):
    dataset = input(f"데이터셋{i+1}의 값을 쉼표로 구분하여 입력하세요: ").split(',')
    dataset = [float(d.strip()) for d in dataset]
    data.append(dataset)

  return data

def box_plot(data,labels=None, title=''):

    # box plot 그리기
    plt.boxplot(data, labels=labels)
    plt.title(title)
    plt.show()
