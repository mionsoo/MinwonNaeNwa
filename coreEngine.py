# -*- coding: utf-8 -*-
import time
import minwonCrawler as mc
import dbModule as db


def check_Categories(datas):
    categories = ['id','name','과세대상', '납부방법', '납세의무자', '과세표준', '신고납부', '과세표준과 세율',
       '납세의무자, 과세표준 및 세율', '납기', '정의', '세율', '정보']

    return [(categories[i],v) for i,v in enumerate(datas[0]) if v != '']


def find_answerDB(hometax):
    data = ''
    data_path = ''
    answer=''
    print("hometax : ",hometax)

    datas = db.selectNameFromTable(hometax)
    categories = check_Categories(datas)

    for i in categories:
        if str(i[0]) == "name":
            name = i[1]
        if str(i[0]) == "정보":
            info = i[1]
        if (str(i[0]) != "id") and (str(i[0]) != "name") and (str(i[0]) !="정보"):
            if str(i[1])[-3:] == "png":
                data = i[1]
                category = i[0]
            else:
                answer = answer + "*" + str(i[0]) + "*" + "\n" + str(i[1]) + "\n\n"

    answer = "*"+name+"*"+" 에 대한 정보는 다음과 같습니다.\n" + info + "\n\n" + answer


    if len(data) > 0:
        data_path = 'pic/'+ data
        answerForm= {"fulfillmentText": answer,
            "fulfillmentMessages": [
             {
                 "card": {
                     "title": name ,
                     "subtitle": answer,
                     "imageUri": "http://203.253.21.85:8080/info.png",
                     "buttons":[{
                         "text":name+" "+category+" link",
                         "postback":"http://203.253.21.85:8080/info.png"
                     }
                     ]
                 }
             }],
            "payload":{
                "slack":{
                    "text": answer,
                    "attachments": [
                        {
                            "text": "*"+category+"*",
                            "image_url": "http://203.253.21.85:8080/info.png",
                            "color": "#764FA5"
                        }
                    ]
                }
            }
        }

    else:
        answerForm = {'fulfillmentText': answer}

    return data_path,answerForm


def introduce_myself():
    answer = { "fulfillmentText":"저는 상담사의 업무를 조금이라도 줄여드리기 위해 생겨났습니다. \n세금에 대한 정보와 간단한 민원은 저에게 맡겨주세요. \n",
        "payload":{
        "attachments": [
            {
                "footer": "Wetax",
                "fallback": "Required plain-text summary of the attachment.",
                "fields": [
                    {
                        "value": ":slack_call: (+82) *110번*",
                        "short": True,
                        "title": " 고객센터 번호"
                    },
                    {
                        "value": ":clock930:  *07:00 ~ 23:30*",
                        "short": True,
                        "title": "위택스 신고·납부시간"
                    },
                    {
                        "value": ":clock930:  *09:00 ~ 21:00*",
                        "short": True,
                        "title": "월 ~ 금 (공휴일 제외)"
                    },
                    {
                        "value": ":clock930:  *09:00 ~ 13:00*",
                        "short": True,
                        "title": "토요일"
                    }
                ],
                "pretext": "저는 상담사의 업무를 조금이라도 줄여드리기 위해 생겨났습니다 :smile:\n세금에 대한 정보와 간단한 민원은 저에게 맡겨주세요 :+1: \n",
                "title": "Wetax 지방세 온라인 신고, 납부, 조회",
                "color": "#36a64f",
                "title_link": "https://www.wetax.go.kr/main/"
            }
        ]
    }
    }

    return answer


def find_answerCrawling(question):
    #ToDo: need to searching question in FAQ page and return Answer
    #ToDo: make info response using db select Function

    answer = mc.crawling_AnswerByQuestion(question)
    answerForm = {'fulfillmentText': answer}

    return answerForm


def cantFindAns():
    answer = {
        "payload": {
            "slack": {
                "attachments": [
                    {
                        "footer": "Wetax",
                        "fallback": "Required plain-text summary of the attachment.",
                        "fields": [
                            {
                                "value": ":slack_call: (+82) *110번*",
                                "short": True,
                                "title": " 고객센터 번호"
                            },
                            {
                                "value": ":clock930:  *07:00 ~ 23:30*",
                                "short": True,
                                "title": "위택스 신고·납부시간"
                            },
                            {
                                "value": ":clock930:  *09:00 ~ 21:00*",
                                "short": True,
                                "title": "월 ~ 금 (공휴일 제외)"
                            },
                            {
                                "value": ":clock930:  *09:00 ~ 13:00*",
                                "short": True,
                                "title": "토요일"
                            }
                        ],
                        "pretext": "제가 답변 드리기 어려운 질문이네요 :cry:\n고객센터로 연락 주시면 친철하게 상담해 드리겠습니다.",
                        "title": "Wetax 지방세 온라인 신고, 납부, 조회",
                        "color": "#36a64f",
                        "title_link": "https://www.wetax.go.kr/main/",
                        "ts": time.time()
                    }
                ]
            }
        }
    }

    return answer


def get_requestParams(req):
    question = req['queryResult'].get('queryText')
    minwon_info = req['queryResult']['parameters'].get('minwon-infomation')
    hometax = req['queryResult']['parameters'].get('hometax')
    return question,minwon_info,hometax


def get_intent(req):
    intent = req["queryResult"]["intent"].get('displayName')
    return intent


def coreEngine(req):
    data = ''
    answerForm= {}
    print(req)
    question, minwon_info, hometax = get_requestParams(req)
    print(question,minwon_info,hometax)
    intent = get_intent(req)
    print("intent : ",intent)

    if intent == "hometax_info":
        data, answer = find_answerDB(hometax)
    elif intent == "introduce":
        answer = introduce_myself()
    else:
        answer = cantFindAns()

    # else:
    # need to speed up
    #     answer = find_answerCrawling(question)
    print("answer : ",answer)
    answerForm.update(answer)

    return data,answerForm


if __name__ == '__main__':
    pass


