from flask import Flask
from flask import request
from datetime import datetime
import json
app = Flask(__name__)

@app.route('/', methods=['Post'])
def check_currencies():
    print(len(json.loads(request.json)))
    print(datetime.now().strftime("%H:%M:%S"))
    return request.json

if __name__ == '__main__':
    app.run(debug=True, host='localhost')