from flask import Flask, request, jsonify
import time
import hand_gesture

app = Flask(__name__)


@app.route('/test_post', methods=['POST'])
def post():
    data = request.get_json()
    img = hand_gesture.base64_to_image(data['image'])
    gesture = hand_gesture.hand_inputs(img)

    print('gesture :: ', gesture)
    response = {
        'message': 'post test',
        'data': gesture
    }
    return jsonify(response)


@app.route('/test_get', methods=['GET'])
def get():
    response = {
        'message': 'get test',
        'data': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='192.168.2.48', port=5000, debug=True)
