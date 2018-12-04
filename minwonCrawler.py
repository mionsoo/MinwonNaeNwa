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
    # ToDo: This function need supplement
    soup = getSoup(navigate_url)
    category_list = soup.find_all("div",{"class":"council"})

    i = 0
    nameList = []
    categories_list = []
    contents_list = []

    '''
    for _category in category_list:
        name = _category.find("strong").get_text()
        categ = [i.get_text() for i in _category.find_all("dt")]
        categ_values = [' '.join(i.get_text().split()) for i in _category.find_all("dd")]

        nameList.append(name)
    '''

    for category_infos in category_list:
        category_data = category_infos.find(["dl"])

        nameList.append(category_infos.find("strong").get_text())
        categories = category_data.find_all("dt")
        category_contents = category_data.find_all("dd")
        categories2 = [value.get_text() for value in categories if value.get_text() not in categories_list if value.get_text() != "세율"]

        categories_list = categories_list + categories2
        asd = [(categories_list.index(value.get_text()), category_contents[idx].get_text()) for idx,value in enumerate(categories) if value.get_text() in categories_list]
        contents_list = contents_list + [asd]



    column = ["id","name"] + categories_list

    df = DataFrame(columns=column)
    for idx,val in enumerate(contents_list):
        contents = [""] * (len(categories_list) + 2)
        contents[0] = str(idx+1)
        contents[1] = nameList[idx]
        for v in val:
            contents[v[0]+2] = v[1]

        df = df.append(Series(contents,index=df.columns),ignore_index=True)
        i+=1

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






