from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/dummy', methods=['GET'])
def dummy():
    val = request.args.get('val')
    if val is None:
      return 'Value is missing.', 400
    return val + "_x", 200

@app.route('/upload', methods=['POST'])
def upload():
    if "file_upload" not in request.files:
        return 'File missing.', 400
    else:
        f = request.files['file_upload']
        return f.read(), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)