from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import time
import os
t1=time.perf_counter()
url='https://www.ucl.ac.uk/library/forms/indigo-seat-availability.php?loc=all'
response=requests.get(url)
soup=BeautifulSoup(response.text, 'html.parser')
lst=soup.find_all('span', {'class': 'mainStat'})
lst1=soup.find_all('h2')
lst=list(zip(lst,lst1))
lst=[(y.text,x.text.split()[0] if 'Currently' not in x.text.split() else -1,float(x.text.split()[0])/float(x.text.split()[4])*100 if 'Currently' not in x.text.split() else -1,datetime.datetime.today().date(),datetime.datetime.now().time()) for (x,y) in lst]
df=pd.DataFrame(lst,columns=['Library','Free Seats','% Free','Date', 'Time'])
df.style.hide(axis='index')
df=df.sort_values(by='% Free', ascending=False)
print(df.to_string(index=False))
df.copy().to_csv('data/results.csv', mode='a', header=not os.path.exists('data/results.csv'), index=False)
t2=time.perf_counter()
print(t2-t1)
