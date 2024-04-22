import pandas as pd
import numpy as np
from sklearn.metrics import r2_score as r2
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
from pathlib import Path
p=Path('./data.csv')
if p.is_file():
 d=pd.read_csv('data.csv')
else:
 print('create a data.csv file')
 exit()
m1=d.columns[1]
m2=d.columns[2]
degree1=int(d.degree1[0])
degree2=int(d.degree2[0])
y1low=int(d.y1[0])
y1high=int(d.y1[1])
y2low=int(d.y2[0])
y2high=int(d.y2[1])

from datetime import date
first=date(int(d.day[0].split('/')[0]),int(d.day[0].split('/')[1]),int(d.day[0].split('/')[2]))
days=len(d.day)-1
target=date(int(d.day[days].split('/')[0]),int(d.day[days].split('/')[1]),int(d.day[days].split('/')[2]))
X=[]
X.append(0)
for i in range(1,days+1):
 dd=date(int(d.day[i].split('/')[0]),int(d.day[i].split('/')[1]),int(d.day[i].split('/')[2]))
 X.append((dd-first).days)
def main():
 fig,ax1=plt.subplots()
 ax2 = ax1.twinx()
 ax1.set_xticklabels(d.day,rotation=90)  
 ax1.set_xticks(X)
 model_m1=np.poly1d(np.polyfit(X[0:days],d[m1][0:days],degree1))
 m1_error=r2(model_m1(X[0:days]),d[m1][0:days])
 x1=(target-first).days
 y1=model_m1(x1)
 print(model_m1.coefficients)
 print(m1+': ',round(y1,3))
 d[m1][days]=y1
 plt.ylim(y1low,y1high)
 ax1.plot(X[0:days],d[m1][0:days],linestyle='None',marker='x')
 ax1.plot(X[days],d[m1][days],color='r',linestyle='None',marker='x')
 ax1.plot(X[0:days+1],model_m1(X[0:days+1]),color='k',ls=':')
 ax1.legend([m1],loc=3,bbox_to_anchor= (0.7, 0.7))
 plt.ylim(y2low,y2high)
 ax2.set_xticklabels(d.day,rotation=90)  
 ax2.set_xticks(X)
 model_m2=np.poly1d(np.polyfit(X[0:days],d[m2][0:days],degree2))
 m2_error=r2(model_m2(X[0:days]),d[m2][0:days])
 x2=(target-first).days
 y2=model_m2(x2)
 print(model_m2.coefficients)
 print(m2+': ',round(y2,3))
 d[m2][days]=y2
 ax2.plot(X[0:days],d[m2][0:days],linestyle='None',marker='o')
 ax2.plot(X[days],d[m2][days],linestyle='None',color='r',marker='o')
 ax2.plot(X[0:days+1],model_m2(X[0:days+1]),linestyle='--',color='k')
 ax2.legend([m2],loc=3,bbox_to_anchor= (0.7, 0.6))
 plt.text(10,50,'r2_'+m1+': '+str(round(m1_error,2)))
 plt.text(130,50,'degree: '+str(degree1))
 plt.text(10,70,'r2_'+m2+': '+str(round(m2_error,2)))
 plt.text(130,70,'degree: '+str(degree2))
 plt.savefig(m1+'_'+m2+'.png',bbox_inches='tight')
 plt.show()

if __name__ == '__main__':
 main()
