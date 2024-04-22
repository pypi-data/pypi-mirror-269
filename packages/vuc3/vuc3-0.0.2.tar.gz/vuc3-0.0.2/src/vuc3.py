import pandas as pd
import sys
import subprocess as sp
import warnings
warnings.filterwarnings('ignore')
sp.call('wget -nc https://data.cdc.gov/api/views/ukww-au2k/rows.csv',shell=True)
d=pd.read_csv('rows.csv')
months=d.mmwr_week.unique()
#months=d.month.unique()
#age=50-64,65+,all_ages
#product=all_types,Pfizer,Moderna,Janssen
if len(sys.argv)==1: 
 print('age:50-64,65+,all_ages;product:Pfizer,Moderna,Janssen,all_types;outcome:death or case')
 sys.exit(0)
else:
 age=sys.argv[1]
 #age='all_ages'
 product=sys.argv[2]
 #product='Pfizer'
 outcome=sys.argv[3]
 #outcome='death'
for i in months:
 b=d.loc[(d.outcome==outcome)  & (d['vaccine_product']==product) & (d['age_group']==age),'vaccinated_with_outcome']
 bp=d.loc[(d.outcome==outcome) & (d['vaccine_product']==product) & (d['age_group']==age),'fully_vaccinated_population']
 v=b/bp
 b1=d.loc[(d.outcome==outcome)  & (d['vaccine_product']==product) & (d['age_group']==age),'one_boosted_with_outcome']
 bp1=d.loc[(d.outcome==outcome) & (d['vaccine_product']==product) & (d['age_group']==age),'one_booster_population']
 v1=b1/bp1
 b2=d.loc[(d.outcome==outcome)  & (d['vaccine_product']==product) & (d['age_group']==age),'two_boosted_with_outcome']
 bp2=d.loc[(d.outcome==outcome) & (d['vaccine_product']==product) & (d['age_group']==age),'two_booster_population']
 v2=b2/bp2
 uo=d.loc[(d.outcome==outcome) & (d['vaccine_product']==product) & (d['age_group']==age),'unvaccinated_with_outcome']
 up=d.loc[(d.outcome==outcome) & (d['vaccine_product']==product) & (d['age_group']==age),'unvaccinated_population']
 u=uo/up
#print(len(v1),len(v2),len(u))
months=range(len(v1))
import matplotlib.pyplot as plt
import numpy as np
def main():
 fig,ax1=plt.subplots()
 ax1.set_xticklabels(['march22','april22','may22','june22','july22','aug22','sept22','oct22'],rotation=90)
 plt.plot(months,v2,':k')
 plt.plot(months,v1,'-k')
 plt.plot(months,v,'-.k')
 plt.plot(months,u,'--k')
 plt.legend(('2-boost','1-boost','fully vaccinated','unvaccinated'))
 plt.title('COVID-19 '+outcome+'_'+product+' for '+age+'_group')
 plt.savefig(outcome+'_'+product+'_'+age+'.png',bbox_inches='tight')
 plt.show()
main()
