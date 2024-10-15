from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
t1=time.perf_counter()
url='https://www.ucl.ac.uk/library/forms/indigo-seat-availability.php?loc=all'
response=requests.get(url)
soup=BeautifulSoup(response.text, 'html.parser')
lst=soup.find_all('span', {'class': 'mainStat'})
lst1=soup.find_all('h2')
lst=list(zip(lst,lst1))
lst=[(y.text,x.text.split()[0],float(x.text.split()[0])/float(x.text.split()[4])*100) for (x,y) in lst]
# for (x,y) in lst:
#     print(f'{y} { float(x[0])/float(x[4])*100:.2f} {int(x[0])}')
# print(soup.prettify())
df=pd.DataFrame(lst,columns=['Library','Free Seats','% Free'])
df.style.hide(axis='index')
df=df.sort_values(by='% Free', ascending=False)
print(df.to_string(index=False))
t2=time.perf_counter()
print(t2-t1)