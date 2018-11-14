from flask import Flask, jsonify, make_response, request
import coreEngine

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhookController():
    req = request.get_json(force=True)
    res = coreEngine.coreEngine(req)

    return make_response(jsonify(res))

if __name__ == '__main__':
    app.run(host='203.253.21.85',port=8080)
