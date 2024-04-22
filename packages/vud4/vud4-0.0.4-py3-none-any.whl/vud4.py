import pandas as pd
import sys
import subprocess as sp
import warnings
warnings.filterwarnings("ignore")
sp.call('wget -nc https://data.cdc.gov/api/views/54ys-qyzm/rows.csv',shell=True)
d=pd.read_csv('rows.csv')
months=d.mmwr_week.unique()
#months=d.month.unique()
#age=18-29,30-49,50-64,65-79,80+,all_ages
#
if len(sys.argv)==1: 
 print('enter one of age groups: vud4 80+')
 print('18-29,30-49,50-64,65-79,80+,all_ages')
 sys.exit(0)
else:
 age=sys.argv[1]
 #age='all_ages'
 #vaccination_statust=sys.argv[1]
 # vaccinated, vax with updated booster
import numpy as np
for i in months:
 b1=d.loc[(d.outcome=='death') &  (d.vaccination_status=='vaccinated') & (d['age_group']==age),'vaccinated_with_outcome']
 bp1=d.loc[(d.outcome=='death') & (d.vaccination_status=='vaccinated') & (d['age_group']==age),'vaccinated_population']
 v1=b1/bp1

 bb=d.loc[(d.outcome=='death')  & (d.vaccination_status=='vax with updated booster') & (d['age_group']==age),'vaccinated_with_outcome']
 bp2=d.loc[(d.outcome=='death') & (d.vaccination_status=='vax with updated booster') & (d['age_group']==age),'vaccinated_population']
 v2=bb/bp2

 uo=d.loc[(d.outcome=='death') & (d['age_group']==age),'unvaccinated_with_outcome']
 up=d.loc[(d.outcome=='death') & (d['age_group']==age),'unvaccinated_population']
 u=uo/up

v1=np.array(v1)
v2=np.array(v2)
vv1=np.zeros(len(u))
vv2=np.zeros(len(u))
for i in range(int(len(u)/2)):
 vv1[i*2]=v1[i]
 vv1[i*2+1]=v1[i]
 vv2[i*2]=v2[i]
 vv2[i*2+1]=v2[i]

#print(len(months),len(v1),len(v2),len(u))
import matplotlib.pyplot as plt
import numpy as np
def main():
 fig,ax1=plt.subplots()
 plt.plot(range(len(u)),u,'--k')
 plt.plot(range(len(vv2)),vv2,':k')
 plt.plot(range(len(vv1)),vv1,'-k')
 ax1.set_xticklabels(d.month.unique()[::2],rotation=90)
 plt.legend(('unvaccinated','bivalent-boost','vaccinated'))
 plt.title('COVID-19 death for '+age+'_age group')
 plt.savefig('bivalent_'+age+'.png',bbox_inches='tight')
 plt.show()
main()
plt.close()
