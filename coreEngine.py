# -*- coding: utf-8 -*-

from flask import Flask,jsonify, make_response, request, send_file
import time
import io
import minwonCrawler as mc

import base64
app = Flask(__name__)

class adict(dict):
    def __init__(self, *av, **kav):
        dict.__init__(self, *av, **kav)
        self.__dict__ = self

def find_answerDB(hometax):
    #ToDo: change title, card text to data's Tax Category and Contents
    answer = "~입니다."
    data = '/home/gon/Pictures/unnamed.jpg'
    answer= {'fulfillmentText': answer,
     "fulfillmentMessages": [
         {
             "card": {
                 "title": "card title",
                 "subtitle": "card text",
                 "imageUri": "http://203.253.21.85:8080/unnamed.jpg"}
         }]
             }
    return data,answer

def find_answerCrawling(question):
    #ToDo: need to searching question in FAQ page and return Answer
    answer = "~입니다."
    result = mc.get_result()
    # 답변의 범위를 넘어서는 경우
    if result == -1:
        answer = cantFindAns()
    return answer

def cantFindAns():
    cont = [
      {
        "text": {
          "text": [
            ""
          ]
        }
      },
      {
        "payload": {
          "slack": {
            "attachments": [
              {
                "footer": "Wetax",
                "fallback": "Required plain-text summary of the attachment.",
                "fields": [
                  {
                    "value": "110번",
                    "short": True,
                    "title": "고객센터 번호"
                  },
                  {
                    "value": "07:00 ~ 23:30",
                    "short": True,
                    "title": "위택스 신고·납부시간"
                  },
                  {
                    "value": "- 09:00 ~ 21:00",
                    "short": True,
                    "title": "월 ~ 금 (공휴일 제외)"
                  },
                  {
                    "value": "09:00 ~ 13:00",
                    "short": True,
                    "title": "토요일"
                  }
                ],
                "pretext": "제가 답변 드리기 어려운 질문이네요.\n고객센터로 연락 주시면 친철하게 상담해 드리겠습니다.",
                "title": "Wetax 지방세 온라인 신고, 납부, 조회",
                "color": "#36a64f",
                "title_link": "https://www.wetax.go.kr/main/"
              }
            ]
          }
        }
      }
    ]

    return adict(fulfillmentMessages=cont)

def get_requestParams(req):
    question = req['queryResult'].get('queryText')
    minwon_info = req['queryResult']['parameters'].get('minwon-infomation')
    hometax = req['queryResult']['parameters'].get('hometax')
    return question,minwon_info,hometax

def coreEngine(req):
    data = ''
    answerForm= {}

    question,minwon_info,hometax = get_requestParams(req)

    #ToDo: need to store chat data and searching data to db
    if len(hometax) > 0:
        data, answer = find_answerDB(hometax)
    else:
        answer = find_answerCrawling(question)
    answerForm.update(answer)


    return data,answerForm

if __name__ == '__main__':
    find_answerDB()
