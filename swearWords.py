__author__ = 'e.dunajevas'
import requests
import re
from bs4 import BeautifulSoup
#source http://www.zodynas.lt/jaunimo-zodynas
URL = 'http://www.zodynas.lt/jaunimo-zodynas/?page='

f = open('dictionaries/swear-words.txt', 'wb+')
for page in range(1, 44):
    response = requests.get(URL + str(page))
    soup = BeautifulSoup(response.content)

    list = soup.find_all('ul', {'class' : 'abc_list'})[0].find_all('li')

    for l in list:
        word = l.find('a')['title']
        if not " " in word:
            f.write(word.encode('UTF-8') + "\n")

f.close()
