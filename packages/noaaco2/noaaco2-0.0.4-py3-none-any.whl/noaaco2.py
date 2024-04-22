import subprocess as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
Nmonths='+1'
if len(sys.argv)==2:
 Nmonths=sys.argv[1]
sp.call('wget -nc ftp://aftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.csv',shell=True)
sp.call("cat co2_mm_mlo.csv|sed 's/ndays/ndays\,unc/'>co2.csv",shell=True)
#sp.call('tail -n '+str(Nmonths)+' co2_mm_mlo.csv  >>co2.csv',shell=True)
d=pd.read_csv('co2.csv',comment='#')
# units: micromol mol-1 (10^6 mol CO2 per mol of dry air)
dn=pd.DataFrame()
dn['co2']=pd.NaT
dn['date']=pd.NaT
def main():
 if Nmonths=='+1': months=len(d)
 else: months=int(Nmonths)
 dn['co2']=d.average
 dn.date=d.year.astype(str)+'.'+d.month.astype(str)
 dn.to_csv('result.csv',index=False)
 plt.ylabel('10^-6 mol co2/mol')
 plt.xlabel('year.month')
 if int(months)<25:plt.xticks(rotation=90)
 else:plt.xticks(np.arange(0,months,30*months/770),rotation=90)
 if Nmonths=='+1':
  plt.plot(dn.date,dn.co2,'ko')
 else:
  plt.plot(dn.date[-int(Nmonths)-1:-1],dn.co2[-int(Nmonths)-1:-1],'ko')
 sp.call('rm co2.csv', shell=True)
 fig=plt.figure(1)
 fig.set_size_inches(10,3)
 plt.savefig('noaaco2.png',dpi=fig.dpi,bbox_inches='tight')
 plt.show()
 plt.close()
if __name__ == "__main__":
 main()
