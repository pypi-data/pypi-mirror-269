import subprocess as sp
import numpy as np
import netCDF4
sp.call('wget -nc  -r -np -nd -e robots=off --glob=on -A.nc https://www.ncei.noaa.gov/data/total-solar-irradiance/access/yearly/',shell=True)
sp.call('ls tsi*.nc >filename',shell=True)
f=open('filename','r')
sp.call('rm filename',shell=True)
file=f.read().strip()
sp.call('wget -A.nc -O - https://www.ncei.noaa.gov/data/total-solar-irradiance/access/monthly|grep href|cut -d \'"\' -f 2 >list',shell=True)
li=open('list','r')
#print(li.read())
f=netCDF4.Dataset(file)
tsi=[]
for i in f['TSI']:
 tsi.append(str(i))
year=[]
for i in range(1610,2023):
 year.append(str(i))
new=[]
for i in range(len(tsi)):
 new.append(str(year[i])+','+str(tsi[i]))
new=np.array(new)
np.savetxt('tsi.csv',new,delimiter=',',fmt='%s')
def main():
 import pandas as pd
 import matplotlib.pyplot as plt
 df=pd.read_csv('tsi.csv')
 df.columns=['year','watt']
 plt.xlabel('year')
 plt.ylabel('W/m^2')
 plt.plot(df.year,df.watt,'ko')
 fig=plt.figure(1)
 fig.set_size_inches(10,3)
 plt.savefig('noaatsi.png',dpi=fig.dpi,bbox_inches='tight')
 plt.show()
 plt.close()
if __name__ == "__main__":
 main()

