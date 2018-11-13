from bs4 import BeautifulSoup as bs
import sqlite3
import urllib.request as ul
import requests
import re
from pandas import DataFrame as df

'LPTIAD0R1'


root_page = 'https://www.wetax.go.kr/main/'
faq_each_page = 'https://www.wetax.go.kr/main/?cmd=LPTIAD0R1&faqDiv=@FAQPAGE@'


def get_soup(url):
    return bs(requests.get(url).text,'html.parser')

def get_faqCategory(root_page):
    soup = get_soup(root_page)
    pagelist = soup.find("div", {"class": "list_search"}).find_all("option")

    for i in pagelist:
        p = re.compile("\d{2}")
        if i.get('value') != '' and p.match(i.get('value')):
            name = i.contents[0]
            num = i.get('value')
            pageDict[num] = name

    return pageDict


if __name__ == '__main__':
    # get FAQ Categories page number dictionary
    pageDict = get_faqCategory(root_page)
    # get data from each page
    faq_page_url_list = [faq_each_page.replace('@FAQPAGE@', pageNum) for pageNum in pageDict.keys()]
    # get navigate each part page
    navigate_url = root_page + '?cmd=LPTIIA1R1'

    soup = get_soup(navigate_url)

    # for page_url in faq_page_url_list:
    #     print(page_url)

    '''
    page_url = 'https://www.wetax.go.kr/main/?cmd=LPTIAD0R1&faqDiv=03'
    soup = get_soup(page_url)
    data = soup.find("ul",{"class":"faq"})
    for idx, content in enumerate(data.find_all('a')):
        content = re.sub('[\n\r\t]', '', .contents[0])
    '''





