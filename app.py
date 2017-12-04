import os
from flask import Flask


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/test')
def hello():
	print(os.environ['APP_SETTINGS'])
    return "OK"

if __name__ == '__main__':
    app.run()