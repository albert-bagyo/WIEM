from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate/<lang>/<text>')
def translate(lang, text):
    url = 'https://translation-endpoint.trafficmanager.net/v1//translate'
    data = {"text": text , "target_language":"tw","source_language": lang}
    headers = {'Content-type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print('Success!')
    else:
        print('An error occurred.')
    return f'<h1>{response.json()}<h1>'

@app.route('/tts/<lang>/<text>')
def tts(lang):
    url = 'https://tts-endpoint.trafficmanager.net/tts'
    data = {"text":"bra fie","language":"tw"}
    headers = {'Content-type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print('Success!')
    else:
        print('An error occurred.')
    return f'<h1>{response.json()}<h1>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
