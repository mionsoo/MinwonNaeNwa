from flask import Flask, make_response, request, send_file
import json
import io
import coreEngine

app = Flask(__name__)


class Minwon:
    def __init__(self):
        self.img_path = ''


@app.route('/webhook', methods=['POST', 'GET'])
def webhookController():
    req = request.get_json(force=True)
    Minwon.img_path,res = coreEngine.coreEngine(req)
    return make_response(json.dumps(res))


@app.route('/info.png')
def showController():
    return show_image(Minwon.img_path)


def show_image(img_path):
    data = open(img_path,'rb').read()
    return send_file(
        io.BytesIO(data),
        attachment_filename=img_path.split('/')[-1],
        mimetype='image/jpg'
    )


if __name__ == '__main__':
    app.run(host='203.253.21.85',port=8888)
