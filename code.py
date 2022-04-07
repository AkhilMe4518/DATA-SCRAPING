import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import datetime
import smtplib
dataset=pd.read_csv("/Users/akhil/Downloads/Amazon Scraping.csv")
print(dataset)
url_list=[]
for i in range(1000):
    row=dataset.iloc[i]
    Asin,country=row[2],row[3]
    new_url=str("https://www.amazon.")+str(country)+str("/dp/")+str(Asin)
    url_list.append(new_url)
Scraped_data=[]
iterations=100
cur_iteration=0
start = time.time()
Time=[]
for URL in url_list:
# if True:
#     URL='https://www.amazon.in/SUPIERIORITY-Waterproof-Piping-Weather-Continental/dp/B09PGPQ6MG/ref=sr_1_1_sspa?pd_rd_r=03bcaa20-884f-4986-9854-a9d9e22b2fc7&pd_rd_w=5IqzH&pd_rd_wg=QkpQY&pf_rd_p=1dd1f792-d184-4a51-8ab0-7f28cbaee21e&pf_rd_r=57NN5M4SY66QS9MBWG28&qid=1649335708&refinements=p_85%3A10440599031&rps=1&s=automotive&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyVEhPWTZFMVJVWkxXJmVuY3J5cHRlZElkPUEwNTE4NzE0MkFIUjFLOTIyRlJENCZlbmNyeXB0ZWRBZElkPUEwMjgwNTkzM1JDNkNYRVNKSUpOQyZ3aWRnZXROYW1lPXNwX2F0Zl9icm93c2UmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl'
    Product_data={}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    page = requests.get(URL, headers=headers) 
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    try:
        Product_title = soup2.find(id='productTitle')
        Product_price = soup2.find('span', {'class': 'a-offscreen'})
    except:
        Product_data[URL]="NOT AVAILABLE"
        Scraped_data.append(Product_data)
        cur_iteration+=1
        if cur_iteration==iterations:
            Time.append(time.time() - start)
            start = time.time()
            cur_iteration=0
        continue
    Product_title=Product_title.text.strip()
    Product_price=Product_price.text.strip()
    img_div = soup2.find(id="imgTagWrapperId")
    imgs_str = img_div.img.get('data-a-dynamic-image')
    imgs_dict = json.loads(imgs_str)
    first_link = list(imgs_dict.keys())[0]
    Product_Details={}
    Product_data['PRODUCT_TITLE']=Product_title
    Product_data['PRODUCT_PRICE']=Product_price
    Product_data['PRODUCT_IMG_URL']=first_link
    Details_1=soup2.find_all('th',{'class':'a-color-secondary a-size-base prodDetSectionEntry'})
    Details_2=soup2.find_all('td',{'class':'a-size-base prodDetAttrValue'})
    for (i,j) in zip(Details_1,Details_2):
        D1=i.get_text().strip()
        D2=j.get_text().strip()
        Product_Details[D1]=D2
    Product_data['PRODUCT_DETAILS']=Product_Details
    Scraped_data.append(Product_data)
    cur_iteration+=1
    if cur_iteration==iterations:
        Time.append(time.time() - start)
        start = time.time()
        cur_iteration=0
f = open('output.json', 'w')
f.write(json.dumps(Scraped_data))
f.close()
print(Time)
