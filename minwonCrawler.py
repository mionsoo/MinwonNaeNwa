from bs4 import BeautifulSoup as bs
import urllib.request as ul
import requests
import re
from pandas import DataFrame
from collections import Counter,OrderedDict,ChainMap


'LPTIAD0R1'


root_url = 'https://www.wetax.go.kr/main/'
faq_each_page = 'https://www.wetax.go.kr/main/?cmd=LPTIAD0R1&faqDiv=@FAQPAGE@'
faq_url= "https://www.wetax.go.kr/main/?cmd=LPTIAD0R1&faqDiv=&faqField=&faqKeyword="
navigate_url = root_url + '?cmd=LPTIIA1R1'

class adict(dict):
    def __init__(self, *av, **kav):
        dict.__init__(self, *av, **kav)
        self.__dict__ = self

def get_result():
    return -1


def get_soup(url):
    """
    get html response at url and make soup
    :param url: type (string), webpage url
    :return: soup
    """
    return bs(requests.get(url).text,'html.parser')

def get_faqCategory(root_url):
    """
    get faqCategory id and content at url then make Dictionary set
    ex ) 01 : 전자신고 ...
    :param root_page: type (string) , webpage url
    :return: Dictionary { id : content, ... }
    """
    pageDict = {}
    soup = get_soup(root_url+"?cmd=LPTIAD0R1")
    pagelist = soup.find("div", {"class": "list_search"}).find_all("option")

    for i in pagelist:
        p = re.compile("\d{2}")
        if i.get('value') != '' and p.match(i.get('value')):
            name = i.contents[0]
            num = i.get('value')
            pageDict[num] = name

    return pageDict

if __name__ == '__main__':
    #ToDo: make searching func at Faq using question
    question="자동차세 연납 신청 방법이 어떻게 되나요?"
    #search by keyword
    soup = get_soup(faq_url+ul.quote(question,encoding='euc-kr'))




    # TODO: make sparse html data to database form
    '''
    soup = get_soup(navigate_url)
    category_list = soup.find_all("div",{"class":"council"})

    i = 3
    list_= []
    dict1 = {}
    dict2 = {0:"id",1:"name"}
    nameList = []
    
    for category_infos in category_list:
        dict1[i] = category_infos.find("strong").get_text()
        category_data = category_infos.find(["dl"])
        asd = list(zip(category_data.find_all("dt"), category_data.find_all("dd")))
        list_.append(asd)

    category = [(idx,name) for idx,name in enumerate(nameList)]
    for categ in category:
        [categ[0],categ[1],list_[categ[0]]]
        index = ["id","name"] + [col.get_text() for col in category_data.find_all("dt")]

        # column = [category_infos.find("strong").get_text()] + [row.get_text() for row in category_data.find_all("dd")]

    # get FAQ Categories page number dictionary
    
    # get data from each page
    faq_page_url_list = [faq_each_page.replace('@FAQPAGE@', pageNum) for pageNum in pageDict.keys()]
    # get navigate each part page
    navigate_url = root_url + '?cmd=LPTIIA1R1'
    '''

    '''
    soup = get_soup(navigate_url)

    # for page_url in faq_page_url_list:
    #     print(page_url)
    page_url = 'https://www.wetax.go.kr/main/?cmd=LPTIAD0R1&faqDiv=03'
    soup = get_soup(page_url)
    data = soup.find("ul",{"class":"faq"})
    for idx, content in enumerate(data.find_all('a')):
        content = re.sub('[\n\r\t]', '', .contents[0])
    '''





