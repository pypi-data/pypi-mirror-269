import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#자체 함수 두게 이상

def table(data,bins,max,min,extent): #도수 분표표 만들기 최대 최소 간격 data 입력이 필요
    freq, _ = np.histogram(data, bins=bins, range=(min, max))
    fclass = [f'{i} ~ {i + max/bins}' for i in range(min, max, extent)]
    dist = pd.DataFrame({'frequency data ': freq}, index=pd.Index(fclass, name='Class'))
    print(dist)

def graph(data,r,x = 0,y = 0,l = "",c = ""): #한글자만 입력 해도 그래프 그려주기 scatter에 경우 x,y까지
    if r == 'h' :
        plt.hist(data,label= l ,color= c)
        plt.legend()
        plt.show()
    elif r == 'b':
        plt.bar(data,x,y,label= l ,color= c)
        plt.legend()
        plt.show()
    elif r == 'o':
        plt.pie(data,label= l ,color= c)
        plt.legend()
        plt.show()
    elif r == 'p':
        plt.plot(data,label= l ,color= c)
        plt.legend()
        plt.show()
    elif r == 's':
        plt.scatter(data,x ,y ,label= l ,color= c)
        plt.legend()
        plt.show()


