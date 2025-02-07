from flask import Flask, request, jsonify
import time
import hand_gesture

app = Flask(__name__)


@app.route('/test_get', methods=['GET'])
def get():
    response = {
        'message': 'get test',
        'data': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }
    return jsonify(response)


@app.route('/landmarks_post', methods=['POST'])
def landmarks_post():
    data = request.get_json()
    img = hand_gesture.base64_to_image(data['image'])
    _, landmarks = hand_gesture.hand_inputs(img)

    response = {
        'message': 'landmarks',
        'data': landmarks
    }

    print(response)

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='192.168.2.48', port=5000, debug=True)
