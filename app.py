from flask import Flask, render_template
import requests
import pyowm
import json

try:
    config = open('config.json', 'r')
    API_KEY = json.load(config)["API_KEY"]
except Exception as err:
    print(err)
finally:
    config.close()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate/<text>')
def translate(text):
    url = 'https://translation-endpoint.trafficmanager.net/v1//translate'
    data = {"text": text , "target_language":"tw","source_language": 'en'}
    headers = {'Content-type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers)
    except:
        return render_template('issues.html')
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
    return f'<h1>{response.json().message}<h1>'

@app.route('/weather/<place>')
def weather(place):
    #owm = pyowm.OWM(f"{API_KEY}")
    #m = owm.weather_manager()
    
    #w = m.weather_at_place(place).weather
    #wind = w.wind()
    #humidity = w.humidity
                         
    try:
        r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={place}&APPID={API_KEY}')
    except:
        return render_template('issues.html')
    
    return f'<h3>{r.json()}<h3>'




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
