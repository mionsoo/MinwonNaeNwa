from bs4 import BeautifulSoup as bs
import urllib.request as ul
import requests
import re
import time
import sqlite3
import string
from pandas import DataFrame


root_url = 'https://www.wetax.go.kr'
faq_each_page = 'https://www.wetax.go.kr/main/?cmd=LPTIAD0R1&faqDiv=@FAQPAGE@'
faq_url= "https://www.wetax.go.kr/main/?cmd=LPTIAD0R1&faqDiv=&faqField=&faqKeyword="
navigate_url = root_url + '/main/?cmd=LPTIIA1R1'


def saveCrawlingDataToDB():
    # ToDo: This function need clean up
    soup = getSoup(navigate_url)
    category_list = soup.find_all("div",{"class":"council"})

    nameList = []
    categories_list = []
    contents_list = []
    columns = []
    imgDict = {"자동차세": ("세율","car.png"), "지방교육세": ("납세의무자, 과세표준 및 세율","education.png"), "재산세": ("세율","jaesan.png"), "등록면허세(면허)": ("세율","myunher.png"), "지역자원시설세": ("과세표준과 세율","sisul.png")}

    # column count=12, # of hometax = 12
    df = DataFrame(index=list(range(12)), columns=list(string.ascii_uppercase[:12]))

    # make name, category, value for each categories then append to lists
    for _category in category_list:
        name = _category.find("strong").get_text()
        categ = [i.get_text() for i in _category.find_all("dt")] + ["정보"]
        info = [' '.join(i.next.split()) for i in _category.find_all("div")]
        categ_values = [' '.join(i.get_text().split()) for i in _category.find_all("dd") if not i.find("div",{"class":"w_list"})] + info
        for i in categ:
            columns.append(i)

        nameList.append(name)
        categories_list.append(categ)
        contents_list.append(zip(categ, categ_values))

    # remove duplication columns
    columns = ["name"] + list(set(columns))
    # input columns to dataframe
    df.columns = columns

    # input all values to dataframe
    for idx,value in enumerate(contents_list):
        df.ix[idx]["name"] = nameList[idx]
        for i,_v in enumerate(list(value)):
            k,v = _v
            df.ix[idx][categories_list[idx][i]] = v

    # input imgPath to each categories
    for i in imgDict:
        idx = nameList.index(i)
        df.loc[idx][imgDict[i][0]] = imgDict[i][1]

    # connection to db and input dataframe to db
    conn = sqlite3.connect("minwon.db")
    df.to_sql("minwon_info",conn,if_exists="append",index=False)


def getSoup(url):
    """
    get html response at url and make soup
    :param url: type (string), webpage url
    :return: soup
    """
    return bs(requests.get(url).text,'lxml')


def getFaqCategory(root_url):
    """
    get faqCategory id and content at url then make Dictionary set
    ex ) 01 : 전자신고 , 02 : 전자 납부 ...
    :param root_page: type (string) , webpage url
    :return: Dictionary { id : content, ... }
    """
    pageDict = {}
    soup = getSoup(root_url+"/main/?cmd=LPTIAD0R1")
    pagelist = soup.find("div", {"class": "list_search"}).find_all("option")

    for i in pagelist:
        p = re.compile("\d{2}")
        if i.get('value') != '' and p.match(i.get('value')):
            name = i.contents[0]
            num = i.get('value')
            pageDict[num] = name

    return pageDict


def crawling_AnswerByQuestion(question):
    '''
    searching and making answer function at Faq with question
    get FAQ first row answer using user question
    :param question: user input string, type: String
    :return: answer type: String
    '''
    #ToDo: need to speed up more
    # search by question
    crawler_startTimevect = time.time()
    soup = getSoup(faq_url + ul.quote(question, encoding='euc-kr'))
    faq_page = soup.find("ul", {"class": "faq"})

    try:
        if faq_page.find("li",{"class":"data_no"}).get_text() == '검색결과가 없습니다.':
            return -1
    except AttributeError:
        pass

    # get first row url parameter
    answerUrlParam = soup.find("ul", {"class": "faq"}).find("a")['href']
    soup = getSoup(root_url + answerUrlParam)

    # get first row's question and answer and return
    faq_question = soup.find("dl", {"class": "w_view"}).find("strong").get_text()
    answer = soup.find("dl", {"class": "w_view"}).find("pre").get_text()
    print("Finished time: %0.2f Minutes" % ((time.time() - crawler_startTimevect) / 60))
    return "질문 검색결과와 유사한 FAQ :\n *" + faq_question + "* \n\nFAQ답변 :\n *" + answer+" * "


if __name__ == '__main__':
    pass






