import pandas as pd
import subprocess as sp
import sys
import numpy as np
import matplotlib.pyplot as plt
sp.call('wget -nc https://covid.ourworldindata.org/data/owid-covid-data.csv', shell=True)

d=pd.read_csv('owid-covid-data.csv')
d.fillna(0,inplace=True)
lastday=str(d.date.iloc[-1:]).split()[1]
print(lastday)
n=len(sys.argv)-1
print('countries',n)
countries=[]
for i in range(n):
 countries.append(sys.argv[i+1])
#print(countries)

from datetime import date
d0 = date(2020, 3, 3)
d1 = date(int(lastday.split('-')[0]),int(lastday.split('-')[1]),int(lastday.split('-')[2]))
delta = d1 - d0 
days=delta.days

dd=pd.DataFrame(
  {
   "country": countries,
   "population": range(len(countries)),
  })

daysdate=sorted(d.date.unique())
daysdate=daysdate[len(daysdate)-days:-1]
#print(daysdate)
for i in countries:
 if i=='United Arab Emirates':
  po=(9441138.0/1000000.0)
  dd.loc[dd.country=='United Arab Emirates','population']=po
 else:
  po=round((d.loc[(d.location==i),'population'][0:1].values[0]/1000000.0),3)
  dd.loc[dd.country==i,'population']=po
print(dd)

ddd=pd.DataFrame(
  {
   "date": daysdate,
   "deaths": range(len(daysdate)),
   "score": range(len(daysdate)),
  })

for i in countries:
 print(i)
 pop=dd.loc[dd.country==i,'population'].astype(float)
 #print(pop)
 for j in daysdate:
  t=d.loc[(d.date==j) & (d.location==i),'total_deaths'].astype(int)
  if not t.empty:
   tt=t.values[0]
   tp=(tt/pop).values[0]
   #print(j,tt,tp)
   ddd.loc[ddd.date==j,'deaths']=tt
   ddd.loc[ddd.date==j,'score']=round(tp,2)
 ddd.to_csv(i+'.csv',index=False)

def main():
 for i in range(len(countries)):
  i=pd.read_csv(countries[i]+'.csv') 
  plt.ylabel('score')
  plt.plot(i.date[0:-5],i.score[0:-5])
  plt.xticks(np.arange(0,days,30*days/770),rotation=90)
  fig=plt.figure(1)
  fig.set_size_inches(10,3)
 plt.legend(countries)
 plt.savefig('result.png',dpi=300,bbox_inches='tight')
 plt.show()

if __name__ == "__main__":
 main()
