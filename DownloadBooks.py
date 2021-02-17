from urllib import request, error
from bs4 import BeautifulSoup
import requests
import re
import urllib

links = []
numbers = list(range(1, 500

                     ))
for item in numbers:
    url = "https://itpanda.net/book/" + str(item)
    links.append(url)

finalLink = []

for link in links:
    try:
        response = urllib.request.urlopen(link)
        if response.code == 200:
            finalLink.append(link)
    except error.HTTPError:
        pass
    continue

password_link = []
for download_link in finalLink:
    panlink = requests.get(download_link)
    pan = panlink.text
    soup = BeautifulSoup(pan, 'html.parser')
    for pan_link in soup.find_all(href=re.compile('download')):
        password_link.append(pan_link.get('href'))

yeah_list = []
for password in password_link:
    yeah = "https://itpanda.net" + password
    yeah_list.append(yeah)

info_list = []
for saving_link in yeah_list:
    saving_page = requests.get(saving_link)
    final_text = saving_page.text
    soup = BeautifulSoup(final_text, 'html.parser')
    info = soup.find(class_= re.compile("alert "))
    info_list.append(info)

import csv

with open('D:\Anaconda\.AJupyterFile\data3.csv', 'w+', newline='')as f:
    for each_info in info_list:
        write = csv.writer(f)
        write.writerow([str(each_info)])
