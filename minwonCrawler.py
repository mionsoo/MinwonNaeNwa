from bs4 import BeautifulSoup as bs
import urllib.request as ul
import requests
import re
import time
import sqlite3
from pandas import DataFrame,Series


root_url = 'https://www.wetax.go.kr'
faq_each_page = 'https://www.wetax.go.kr/main/?cmd=LPTIAD0R1&faqDiv=@FAQPAGE@'
faq_url= "https://www.wetax.go.kr/main/?cmd=LPTIAD0R1&faqDiv=&faqField=&faqKeyword="
navigate_url = root_url + '/main/?cmd=LPTIIA1R1'

def saveCrawlingDataToDB():
    soup = get_soup(navigate_url)
    category_list = soup.find_all("div",{"class":"council"})

    i = 0
    nameList = []
    categories_list = []
    contents_list = []


    for category_infos in category_list:

        category_data = category_infos.find(["dl"])

        nameList.append(category_infos.find("strong").get_text())
        categories = category_data.find_all("dt")
        category_contents = category_data.find_all("dd")
        categories2 = [value.get_text() for value in categories if value.get_text() not in categories_list if value.get_text() != "세율"]

        # asd = {categories_list.index(value):category_contents[categories_list.index(value)] for value in categories if categories_list[value.get_text()]}

        categories_list = categories_list + categories2
        asd = [(categories_list.index(value.get_text()), category_contents[idx].get_text()) for idx,value in enumerate(categories) if value.get_text() in categories_list]
        contents_list = contents_list + [asd]



    column = ["id","name"] + categories_list

    df = DataFrame(columns=column)
    for idx,val in enumerate(contents_list):
        contents = [str("Null")] * (len(categories_list) + 2)
        contents[0] = str(idx+1)
        contents[1] = nameList[idx]
        for v in val:
            contents[v[0]+2] = v[1]

        df = df.append(Series(contents,index=df.columns),ignore_index=True)
        i+=1

    conn = sqlite3.connect("minwon.db")

    df.to_sql("minwon_info",conn,if_exists="append",index=False)

def get_soup(url):
    """
    get html response at url and make soup
    :param url: type (string), webpage url
    :return: soup
    """
    # return bs(requests.get(url).text, 'html.parser')
    return bs(requests.get(url).text,'lxml')

def get_faqCategory(root_url):
    """
    get faqCategory id and content at url then make Dictionary set
    ex ) 01 : 전자신고 ...
    :param root_page: type (string) , webpage url
    :return: Dictionary { id : content, ... }
    """
    pageDict = {}
    soup = get_soup(root_url+"/main/?cmd=LPTIAD0R1")
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
    make searching func at Faq using question
    get first row answer by using user question search
    :param question: type (string) , user input string
    :return: answer string
    '''
    #ToDo: need to speed up (Dialogflow get response time limit is 5 sec but module elapse time is minimum 18 sec)
    # search by question
    crawler_startTimevect = time.time()
    timeout = time.time() + 60*5


    soup = get_soup(faq_url + ul.quote(question, encoding='euc-kr'))
    answerUrl = soup.find("ul", {"class": "faq"}).find("a")['href']
    soup = get_soup(root_url + answerUrl)
    print("1")

    faq_question = soup.find("dl", {"class": "w_view"}).find("strong").get_text()
    answer = soup.find("dl", {"class": "w_view"}).find("pre").get_text()
    print("Finished time: %0.2f Minutes" % ((time.time() - crawler_startTimevect) / 60))
    return "질문 검색결과와 유사한 FAQ :\n" + faq_question + "\n\nFAQ답변 :\n" + answer


if __name__ == '__main__':
    pass






