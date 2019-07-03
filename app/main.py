from flask import Flask
from flask import request

from google.cloud import storage

app = Flask(__name__)

@app.route('/dummy', methods=['GET'])
def dummy():
    val = request.args.get('val')
    if val is None:
      return 'Value is missing.', 400
    return val + "_x", 200

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    if f is None:
      return 'File is missing. To be specified as string for form text input field named "file".', 400
    else:
        data = f.read()
        client = storage.Client()
        bucket = client.get_bucket('raw-json-data-l3z0dbnsd39k')
        blob = bucket.blob("test-file")
        blob.upload_from_string(data)
        try:
            fn = f.filename
        except:
            fn = "no file name"
    return fn, 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)