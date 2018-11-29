# -*- coding: utf-8 -*-
import time
import minwonCrawler as mC
import dbModule as dB


def makeAnswerForm(type, data_dict=None):
    if type == 'default':
        return {'fulfillmentText': data_dict["answer"]}
    elif type == 'introduce':
        return {"fulfillmentText": "저는 상담사의 업무를 조금이라도 줄여드리기 위해 생겨났습니다. \n세금에 대한 정보와 간단한 민원은 저에게 맡겨주세요.\n\n\n세금 정보를 알고싶으시면 \"취득세 알려줘 / 알려줄래?\"라고 물어봐 주세요.\n\n\n",
         "payload": {"slack":{
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
                     "pretext": "저는 상담사의 업무를 조금이라도 줄여드리기 위해 생겨났습니다. \n세금에 대한 정보와 간단한 민원은 저에게 맡겨주세요.:+1:\n\n\n세금 정보를 알고싶으시면 *\"취득세 알려줘 / 알려줄래?\"* 라고 물어봐 주세요.\n\n\n",
                     "title": "Wetax 지방세 온라인 신고, 납부, 조회",
                     "color": "#36a64f",
                     "title_link": "https://www.wetax.go.kr/main/"
                 }
             ]
         }}
         }
    elif type == 'db':
        return {"fulfillmentText": data_dict["answer"],
         "fulfillmentMessages": [
             {
                 "card": {
                     "title": data_dict["name"],
                     "subtitle": data_dict["answer"],
                     "imageUri": "http://203.253.21.85:8080/info.png",
                     "buttons": [{
                         "text": data_dict["name"] + " " + data_dict["category"] + " link",
                         "postback": "http://203.253.21.85:8080/info.png"
                     }
                     ]
                 }
             }],
         "payload": {
             "slack": {
                 "text": data_dict["answer"],
                 "attachments": [
                     {
                         "text": "*" + data_dict["category"] + "*",
                         "image_url": "http://203.253.21.85:8080/info.png",
                         "color": "#764FA5"
                     }
                 ]
             }
         }
         }
    else:
        # Can't find answer
        return {
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
                            "pretext": "제가 답변 드리기 어려운 질문이네요 :cry:\n고객센터로 연락 주시면 친철하게 상담해 드리겠습니다.\n\n\n",
                            "title": "Wetax 지방세 온라인 신고, 납부, 조회",
                            "color": "#36a64f",
                            "title_link": "https://www.wetax.go.kr/main/",
                            "ts": time.time()
                        }
                    ]
                }
            }
        }


def makeCategoriesAndDataListFromDB(datas):
    categories = ['id','name','과세대상', '납부방법', '납세의무자', '과세표준', '신고납부', '과세표준과 세율',
       '납세의무자, 과세표준 및 세율', '납기', '정의', '세율', '정보']
    return [(categories[i], v) for i, v in enumerate(datas[0]) if v != '']


def toMakeAnswerFromDBdataList(categories):
    answer = ''
    data = ''
    name = ''
    info = ''
    category = ''

    for i in categories:
        if str(i[0]) == "name":
            name = i[1]
        if str(i[0]) == "정보":
            info = i[1]
        if (str(i[0]) != "id") and (str(i[0]) != "name") and (str(i[0]) != "정보"):
            if str(i[1])[-3:] == "png":
                data = i[1]
                category = i[0]
            else:
                answer = answer + "*" + str(i[0]) + "*" + "\n" + str(i[1]) + "\n\n"

    return [name,info, data,category,answer]


def find_answerDB(hometax,Question):
    data_path = ''
    datas = dB.selectNameFromTable(hometax)
    if datas == []:
        # Answer is not in db
        Question.questionValue(Question.__question)
        return data_path,makeAnswerForm('default', data_dict={"answer" : "음.. 저에게 해당 질문에 대한 정보가 없네요..:thinking_face: \n검색을 그만 둘까요?\n\n 계속하기 원하시면 *\"아니 / 계속 검색해줘 \"*\n그만 두기 원하시면 *\"그만 / 그만하자 /그만둘래\"* 라고 입력해 주세요.})"})

    categories = makeCategoriesAndDataListFromDB(datas)
    values = toMakeAnswerFromDBdataList(categories)
    keys = ["name", "info", "data", "category", "answer"]
    data_dict = {k: v for k, v in zip(keys,values)}

    data_dict["answer"] = "*" + data_dict["name"] + "*" + " 에 대한 정보는 다음과 같습니다.\n\n" + data_dict["info"] \
                          + "\n\n" + data_dict["answer"] + "\n\n" + " 원하시는 답변이 맞으신가요? :thinking_face:"

    if len(data_dict["data"]) > 0:
        data_path = 'pic/' + data_dict["data"]
        answerForm = makeAnswerForm("db", data_dict=data_dict)
    else:
        answerForm = makeAnswerForm('default', data_dict=data_dict)

    return data_path,answerForm


def introduce_myself():
    return makeAnswerForm("introduce")


def findAnswerFromCrawler(question):
    answer = mC.crawling_AnswerByQuestion(question)
    answer = answer + "\n\n 제공해드린 답변이 도움이 되었나요? :thinking_face:\n원치 않는 답변이라면 *\"아니야\"* 라고 답변해주세요"
    return {'fulfillmentText': answer}


def cantFindAnswer():
    return makeAnswerForm('')


def get_requestParams(req):
    question = req['queryResult'].get('queryText')
    minwon_info = req['queryResult']['parameters'].get('minwon-infomation')
    hometax = req['queryResult']['parameters'].get('hometax')
    return question, minwon_info, hometax


def get_intent(req):
    return req["queryResult"]["intent"].get('displayName')


def coreEngine(req, Question):
    data = ''
    answerForm = {}
    question, minwon_info, hometax = get_requestParams(req)
    Question.setInitial(question)
    intent = get_intent(req)

    # print(req)
    # print(question,minwon_info,hometax)
    # print("intent : ",intent)

    # split intent follow string -> "intent - follow up type"
    intent_followup = intent.split(" - ")
    if intent_followup[0] == "hometax_info":
        try:
            intent_followup[1]
        except:
            data, answer = find_answerDB(hometax, Question)
        else:
            if intent_followup[1] == "no":
                if Question.before_question == '':
                    question = Question.beforeQuestion
                answer = findAnswerFromCrawler(question)
                Question.setBeforeQuestionInitial()
                # answer = makeAnswerForm('default', data_dict={"answer": "제공해드린 답변이 도움이 되었나요? :thinking_face:"})

    elif intent_followup[0] == "introduce":
        answer = introduce_myself()
    else:
        answer = cantFindAnswer()

    answerForm.update(answer)
    return data,answerForm


if __name__ == '__main__':
    pass


