
import numpy as np
import matplotlib.pyplot as plt

def scatter_plot(x_label='', y_label='', title=''):
   
    # 사용자로부터 데이터 입력 받기
    x_values = input("x값을 입력해주세요(값 사이에 ,를 넣어주세요): ").split(',')
    y_values = input("y값을 입력해주세요(값 사이에 ,를 넣어주세요): ").split(',')
    x_data = [float(x.strip()) for x in x_values]
    y_data = [float(y.strip()) for y in y_values]
    
    # scatter plot 그리기
    plt.scatter(x_data, y_data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def box_plot(labels=None, title=''):
    
    # 사용자로부터 데이터 입력 받기
    num_datasets = int(input("boxplot을 위한 데이터셋의 수를 입력하세요: "))
    data = []
    for i in range(num_datasets):
        dataset = input(f"쉼표로 구분하여 데이터셋 {i+1} 을 입력하세요: ").split(',')
        dataset = [float(d.strip()) for d in dataset]
        data.append(dataset)
    
    # box plot 그리기
    plt.boxplot(data, labels=labels)
    plt.title(title)
    plt.show()
