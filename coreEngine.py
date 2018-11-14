from flask import Flask,jsonify, make_response, request
import minwonCrawler as mc
app = Flask(__name__)


def find_answerDB(hometax):
    mc.get_soup

    answer = "~입니다."
    return answer

def find_answerCrawling(question):
    answer = "~입니다."
    return answer

def get_requestParams(req):
    question = req['queryResult'].get('queryText')
    minwon_info = req['queryResult']['parameters'].get('minwon-infomation')
    hometax = req['queryResult']['parameters'].get('hometax')
    return question,minwon_info,hometax

def coreEngine(req):
    question,minwon_info,hometax = get_requestParams(req)
    
    if len(minwon_info):
        answer = find_answerDB(hometax)
    else:
        answer = find_answer_module(question)

    return {'fulfillmentText': answer}

if __name__ == '__main__':
    find_answerDB()