# 이것을 수행하고 http://localhost:5005 를 수행하면, hello를 볼 수 있음.

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/info')
def info():
    return 'Info'

if __name__ == '__main__':
    if False :
        app.run(debug=True , host='0.0.0.0')
    else : #jupyer
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5005, app)