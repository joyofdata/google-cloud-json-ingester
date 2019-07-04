from flask import Flask
from flask import request

import utils

BUCKET_NAME_FOR_RAW_DATA = 'raw-json-data-l3z0dbnsd39k'

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
        utils.store_object_in_bucket(
            bucket_name=BUCKET_NAME_FOR_RAW_DATA,
            object_name=f.filename,
            object_data=f.read(),
            prepend_random_string_to_object_name=True
        )
    return "OK", 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)