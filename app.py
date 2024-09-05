from flask import Flask, render_template, redirect
import requests
import pyowm
import json
from pprint import pprint
from datetime import datetime
import random

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
    return redirect('/weather/ghana/tw')

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
    return response.json()['message']

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

@app.route('/weather/<place>/<lang>')
def weather(place,lang):
    #owm = pyowm.OWM(f"{API_KEY}")
    #m = owm.weather_manager()
    
    #w = m.weather_at_place(place).weather
    #wind = w.wind()
    #humidity = w.humidity
    today = datetime.now()
    time = today.strftime('%I : %M %p')
    date = today.strftime("%d %b %Y")
    try:
        #r = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API_KEY}')
        r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={place}&APPID={API_KEY}')
        out = r.json()
        if out['cod'] != 200:
            raise Exception('wrong response')
    except Exception as err:
        #out = json.load('sample.json')
        #print(err)
        return render_template('issues.html')
    description = generate_description(out,place)
    w_m = out['weather'][0]['main']
    w_d = out['weather'][0]['description']
    temp = 'weather.html'
    if lang == 'tw':
        description = translate(description)
        w_m = translate(w_m)
        w_d = translate(w_d)
        temp = 'weather_twi.html'
    #description = get_wikipedia_description(place)
    return render_template(temp,weather = out, time= time,date= date,location= place.capitalize(),description= description,weather_desc =w_d,weather_main =w_m )

def generate_description(weather,location):
    
    temperature = weather['main']['temp']
    feels_like = weather['main']['feels_like']
    humidity = weather['main']['humidity']
    clouds = weather['weather'][0]['description']
    visibility = weather['visibility']
    wind_speed = weather['wind']['speed']
    try:
        wind_gust = weather['wind']['gust']
    except KeyError as err:
        wind_gust = 20
    wind_dir = weather['wind']['deg']
    sunrise_str = weather['sys']['sunrise']
    sunset_str = weather['sys']['sunset']
    
    templates = [
        f"In {location}, the current temperature is around {temperature:.1f}°C, but it feels like {feels_like:.1f}°C due to the humidity at {humidity}%. The sky is {clouds}% covered with clouds, and visibility is quite clear at {visibility / 1000:.1f} km. Winds are blowing at {wind_speed:.1f} m/s with gusts reaching {wind_gust:.1f} m/s from {wind_dir}°. Sunrise occurred at {sunrise_str} UTC, and sunset will be at {sunset_str} UTC.",
        f"Today in {location}, you can expect a temperature of {temperature:.1f}°C, but it feels more like {feels_like:.1f}°C thanks to {humidity}% humidity. The weather is mostly cloudy with {clouds}% cloud cover. Visibility extends up to {visibility / 1000:.1f} kilometers, and winds are blowing at {wind_speed:.1f} meters per second, gusting up to {wind_gust:.1f} meters per second from {wind_dir}°. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        f"Current conditions in {location} show a temperature of {temperature:.1f}°C, which feels like {feels_like:.1f}°C due to {humidity}% humidity. The sky is {clouds}% overcast. Visibility is good at {visibility / 1000:.1f} km. Wind speeds are {wind_speed:.1f} m/s with gusts up to {wind_gust:.1f} m/s from {wind_dir}°. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        f"Weather in {location} is quite warm with a temperature of {temperature:.1f}°C, though it feels more like {feels_like:.1f}°C because of the {humidity}% humidity. The sky is covered by {clouds}% clouds. Visibility is clear up to {visibility / 1000:.1f} kilometers. Winds are at {wind_speed:.1f} m/s with occasional gusts reaching {wind_gust:.1f} m/s coming from {wind_dir}°. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC."
        f"In {location}, the temperature is currently {temperature:.1f}°C. It feels more like {feels_like:.1f}°C due to the {humidity}% humidity. The sky is mostly covered with clouds ({clouds}% cloud cover), and visibility extends for {visibility / 1000:.1f} kilometers. Winds are blowing from {wind_dir}° at {wind_speed:.1f} meters per second, with gusts reaching up to {wind_gust:.1f} meters per second. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        f"Today's weather in {location} features a temperature of {temperature:.1f}°C, though it feels like {feels_like:.1f}°C given the {humidity}% humidity. The sky is predominantly cloudy with {clouds}% cloud cover. Visibility is good, up to {visibility / 1000:.1f} km. The wind is blowing at {wind_speed:.1f} m/s with occasional gusts up to {wind_gust:.1f} m/s from {wind_dir}°. Sunrise was at {sunrise_str} UTC, and sunset will be at {sunset_str} UTC.",
        f"Currently in {location}, it’s {temperature:.1f}°C outside, but it feels like {feels_like:.1f}°C due to the humidity level of {humidity}%. The weather is overcast with {clouds}% cloud coverage. Visibility reaches {visibility / 1000:.1f} kilometers. The wind is blowing from {wind_dir}° at {wind_speed:.1f} m/s, with gusts up to {wind_gust:.1f} m/s. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        f"The current weather in {location} shows a temperature of {temperature:.1f}°C, feeling like {feels_like:.1f}°C due to {humidity}% humidity. Cloud cover is extensive at {clouds}%, with visibility extending up to {visibility / 1000:.1f} km. Winds are blowing at a speed of {wind_speed:.1f} m/s, gusting up to {wind_gust:.1f} m/s from {wind_dir}°. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        f"In {location}, the temperature is currently {temperature:.1f}°C. It feels more like {feels_like:.1f}°C, influenced by {humidity}% humidity. The sky is overcast with {clouds}% cloud cover. Visibility is clear for {visibility / 1000:.1f} kilometers. Wind speeds are around {wind_speed:.1f} m/s, with gusts reaching {wind_gust:.1f} m/s from a direction of {wind_dir}°. Sunrise was at {sunrise_str} UTC and sunset will be at {sunset_str} UTC.",
        f"In {location}, the temperature is currently {temperature:.1f}°C. It feels more like {feels_like:.1f}°C, influenced by {humidity}% humidity. The sky is overcast with {clouds}% cloud cover. Visibility is clear for {visibility / 1000:.1f} kilometers. Wind speeds are around {wind_speed:.1f} m/s, with gusts reaching {wind_gust:.1f} m/s from a direction of {wind_dir}°. Sunrise was at {sunrise_str} UTC and sunset will be at {sunset_str} UTC."
    ]
    
    return templates[random.randint(0,len(templates)-1)]

def get_wikipedia_description(place_name):
    # Wikipedia API endpoint for querying pages
    url = 'https://en.wikipedia.org/w/api.php'
    
    # Parameters for the API request
    params = {
        'action': 'query',
        'format': 'json',
        'titles': place_name,
        'prop': 'extracts',
        'exintro': True,  # Get only the introduction section
        'explaintext': True  # Return plain text, not HTML
    }
    
    # Make the request
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract the page content
    pages = data['query']['pages']
    for page_id, page in pages.items():
        if 'extract' in page:
            return page['extract']
        else:
            return "Description not found."



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
