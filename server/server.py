from flask import Flask, request, jsonify
import time

app = Flask(__name__)


@app.route('/test_post', methods=['POST'])
def post():
    data = request.get_json()
    print('data :: ', data)
    response = {
        'message': 'post test',
        'data': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='192.168.2.39', port=5000, debug=True)
