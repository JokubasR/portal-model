__author__ = 'e.dunajevas'
import requests
import re
from bs4 import BeautifulSoup

BASE_URL = "http://www.delfi.lt/news/daily/"
#number of pages
PAGES = 121
THEMES = ['lithuania/', 'world/', 'emigrants/', 'crime/', 'education/', 'health/', 'hot/', 'law/']
def scrape_blog_posts():
    """ get post urls and scrape them """

    results = []
    for theme in THEMES:
        pages = range(1, PAGES)
        for page in pages:
            response = requests.get(BASE_URL + theme + "?page=" + str(page))

            # parse HTML using Beautiful Soup
            # this returns a `soup` object which
            # gives us convenience methods for parsing html

            soup = BeautifulSoup(response.content)

            # find all the posts in the page.

            posts = soup.find_all('div', {'class':'category-headline-item'})


            for post in posts:

                #get url of post
                url = post.find_all('a')[0]['href']
                print url
                results += scrape_info(url)

    f = open('dictionaries/dictionary.txt', 'wb+')
    for item in results:
        f.write(item.encode('UTF-8') + "\n")
        #f.write(u"%s\n" % item.encode('utf-8'))
    f.close()


def find_words(s):
    return re.findall(re.compile('\w+'), s)

def scrape_info(url):
    """ Extract information from a missed connections's page. """
    results = []
    # retrieve the missed connection with requests
    response = requests.get(url)

    soup = BeautifulSoup(response.content)
    ps = soup.find_all('p')

    for p in ps:
        results.append(p.text)
    return results


if __name__ == '__main__':
    scrape_blog_posts()