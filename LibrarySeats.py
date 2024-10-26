from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import time
import os
# t1=time.perf_counter()
url='https://www.ucl.ac.uk/library/forms/indigo-seat-availability.php?loc=all'
response=requests.get(url)
soup=BeautifulSoup(response.text, 'html.parser')
lst=soup.find_all('span', {'class': 'mainStat'})
lst1=soup.find_all('h2')
lst=list(zip(lst,lst1))
lst=[(y.text,x.text.split()[0] if 'Currently' not in x.text.split() else -1,float(x.text.split()[0])/float(x.text.split()[4])*100 if 'Currently' not in x.text.split() else -1,datetime.datetime.today().date(),datetime.datetime.now().time()) for (x,y) in lst]
df=pd.DataFrame(lst,columns=['Library','Free Seats','% Free','Date', 'Time'])
df.style.hide(axis='index')
date=datetime.datetime.today().date()
url='https://library-calendars.ucl.ac.uk/widget/hours/grid?iid=4014&lid=0&date='+str(date)
soup=BeautifulSoup(requests.get(url).text,'html.parser')
lib=['Great Ormond Street Institute of Child Health Library',
 'UCL East Library', 'Language & Speech Science Library', 'SSEES Library',
 'School of Pharmacy Library','Joint Library of Ophthalmology',
 'Bartlett Library', 'Graduate Hub',
 'Queen Square Library',
 'Cruciform Hub','Institute of Archaeology Library','   Science Library',
 'Main Library','Student Centre', 'IOE Library']
x=soup.find_all('tr',{'class':'s-lc-whw-loc'})
# print(soup.prettify())
lst3=[('12:01am','11:59pm',a[1]) if 'Student Centre' in a[1] else (a[0][0],a[0][2],a[1].strip()) if 'Closed' not in a[0] else ('Closed','Closed',a[1]) for a in [(tuple(i.find_all('td')[datetime.datetime.today().weekday()+1].span.text.strip().split()),b) for b in set([l1 for l1 in lib for i in x if l1 in i.text]) for i in x if b in i.text]]
lst3=[a if 'Closed' in a[0] else (datetime.datetime.strptime(a[0], "%I:%M%p") if ":" in a[0] else datetime.datetime.strptime(a[0], "%I%p"),datetime.datetime.strptime(a[1], "%I:%M%p") if ":" in a[1] else datetime.datetime.strptime(a[1], "%I%p"),str(a[2])) for a in lst3]
df1=pd.DataFrame(lst3,columns=['Opening Hour', 'Closing Hour','Library'])
df['key']=1
df1['key']=1
df2=pd.merge(df,df1,on='key',suffixes=['_1','_2'])
df2['isin']=df2.apply(lambda row: row['Library_2'] in row['Library_1'] and not ('Language' in row['Library_1'] and 'Language' not in row['Library_2']), axis=1)
df2=df2[df2['isin']==True]
df2.drop(columns=['key','Library_2','isin'])
# df2=df2.sort_values(by='% Free', ascending=False)
# print(df.to_string(index=False))
df2.copy().to_csv('data/resultsophr.csv', mode='a', header=not os.path.exists('data/results.csv'), index=False)
# t2=time.perf_counter()
# print(t2-t1)