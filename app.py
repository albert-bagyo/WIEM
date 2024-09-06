from flask import Flask, render_template, redirect, request
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

african_countries = [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
        "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
        "Congo (Congo-Brazzaville)", "Democratic Republic of the Congo", "Djibouti",
        "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini (fmr. Swaziland)", "Ethiopia",
        "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya",
        "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania",
        "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
        "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia",
        "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda",
        "Zambia", "Zimbabwe"
    ]

weather_descriptions = {
        200: "Thunderstorm with light rain",
        201: "Thunderstorm with rain",
        202: "Thunderstorm with heavy rain",
        210: "Light thunderstorm",
        211: "Thunderstorm",
        212: "Heavy thunderstorm",
        221: "Ragged thunderstorm",
        230: "Thunderstorm with light drizzle",
        231: "Thunderstorm with drizzle",
        232: "Thunderstorm with heavy drizzle",

        300: "Light intensity drizzle",
        301: "Drizzle",
        302: "Heavy intensity drizzle",
        310: "Light intensity drizzle rain",
        311: "Drizzle rain",
        312: "Heavy intensity drizzle rain",
        313: "Shower rain and drizzle",
        314: "Heavy shower rain and drizzle",
        321: "Shower drizzle",

        500: "Light rain",
        501: "Moderate rain",
        502: "Heavy intensity rain",
        503: "Very heavy rain",
        504: "Extreme rain",
        511: "Freezing rain",
        520: "Light intensity shower rain",
        521: "Shower rain",
        522: "Heavy intensity shower rain",
        531: "Ragged shower rain",

        600: "Light snow",
        601: "Snow",
        602: "Heavy snow",
        611: "Sleet",
        612: "Light shower sleet",
        613: "Shower sleet",
        615: "Light rain and snow",
        616: "Rain and snow",
        620: "Light shower snow",
        621: "Shower snow",
        622: "Heavy shower snow",

        701: "Mist",
        711: "Smoke",
        721: "Haze",
        731: "Sand/dust whirls",
        741: "Fog",
        751: "Sand",
        761: "Dust",
        762: "Volcanic ash",
        771: "Squalls",
        781: "Tornado",

        800: "Clear sky",
        801: "Few clouds",
        802: "Scattered clouds",
        803: "Broken clouds",
        804: "Overcast clouds"
    }

backgrounds = {
    200: "Storm-Day",
    201: "Storm-Night",
    202: "Storm-Day",
    210: "Storm-Day",
    211: "Thunderstorm",
    212: "Storm-Night",
    221: "Storm-Night",
    230: "Storm-Day",
    231: "Storm-Night",
    232: "Storm-Night",

    300: "Rain-Raindrops",
    301: "Raindrops",
    302: "Raindrops",
    310: "Rain-Raindrops",
    311: "Raindrops",
    312: "Rain",
    313: "Rain",
    314: "Rain",
    321: "Rain",

    500: "Raindrops",
    501: "Raindrops",
    502: "Rain",
    503: "Rain",
    504: "Rain",
    511: "Freezing",
    520: "Rain",
    521: "Rain",
    522: "Rain",
    531: "Rain",

    600: "Snow",
    601: "Snow",
    602: "Freeze",
    611: "Sleet",
    612: "Sleet",
    613: "Sleet",
    615: "Snow",
    616: "Snow",
    620: "Snow",
    621: "Snow",
    622: "Snow",

    701: "Fog",
    711: "Smog",
    721: "Haze",
    731: "Dust",
    741: "Fog",
    751: "Dust",
    761: "Dust",
    762: "Smog",
    771: "Squalls",
    781: "Tornado",

    800: "Day-Clear",
    801: "Partly-cloudy",
    802: "Partly-cloudy",
    803: "Cloudy",
    804: "Cloudy"
}

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
    w_id = out['weather'][0]['id']
    temp = 'weather.html'

    background = backgrounds.get(w_id, "default-bg")

    if background == 'Rain':
        condition = '--rain'
    elif background == 'Snow':
        condition = '--snow'
    elif background == 'Clear sky':
        condition = '--clear'
    if lang == 'tw':
        description = translate(description)
        w_m = translate(w_m)
        w_d = translate(w_d)
        temp = 'weather_twi.html'
    #description = get_wikipedia_description(place)
    return render_template(temp,weather = out, time= time,date= date,location= place.capitalize(),description= description,weather_desc =w_d,weather_main =w_m, countries=african_countries, background=background)

def generate_description(weather,location):
    try:
        wind_gust = weather['wind']['gust']
    except:
        wind_gust = 20
    
    param = {
    'location' : location,
    'temperature' : weather['main']['temp'] - 273,
    'feels_like' : weather['main']['feels_like'] - 273,
    'humidity' : weather['main']['humidity'],
    'clouds' : weather['weather'][0]['description'],
    'visibility' : weather['visibility'] / 100,
    'wind_speed' : weather['wind']['speed'],
    'wind_gust' : wind_gust,
    'wind_dir' :  weather['wind']['deg'],
    'sunrise_str' : weather['sys']['sunrise'],
    'sunset_str' : weather['sys']['sunset']}
    
    templates = [
        "In {location}, the current temperature is around {temperature:.1f}°C, but it feels like {feels_like:.1f}°C due to the humidity at {humidity}%. The sky is {clouds}% covered with clouds, and visibility is quite clear at {visibility:.1f} km. Winds are blowing at {wind_speed:.1f} m/s with gusts reaching {wind_gust:.1f} m/s from {wind_dir}°. Sunrise occurred at {sunrise_str} UTC, and sunset will be at {sunset_str} UTC.",
        "Today in {location}, you can expect a temperature of {temperature:.1f}°C, but it feels more like {feels_like:.1f}°C thanks to {humidity}% humidity. The weather is mostly cloudy with {clouds}% cloud cover. Visibility extends up to {visibility:.1f} kilometers, and winds are blowing at {wind_speed:.1f} meters per second, gusting up to {wind_gust:.1f} meters per second from {wind_dir}°. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        "Current conditions in {location} show a temperature of {temperature:.1f}°C, which feels like {feels_like:.1f}°C due to {humidity}% humidity. The sky is {clouds}% overcast. Visibility is good at {visibility:.1f} km. Wind speeds are {wind_speed:.1f} m/s with gusts up to {wind_gust:.1f} m/s from {wind_dir}°. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        "Weather in {location} is quite warm with a temperature of {temperature:.1f}°C, though it feels more like {feels_like:.1f}°C because of the {humidity}% humidity. The sky is covered by {clouds}% clouds. Visibility is clear up to {visibility:.1f} kilometers. Winds are at {wind_speed:.1f} m/s with occasional gusts reaching {wind_gust:.1f} m/s coming from {wind_dir}°. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC."
        "In {location}, the temperature is currently {temperature:.1f}°C. It feels more like {feels_like:.1f}°C due to the {humidity}% humidity. The sky is mostly covered with clouds ({clouds}% cloud cover), and visibility extends for {visibility:.1f} kilometers. Winds are blowing from {wind_dir}° at {wind_speed:.1f} meters per second, with gusts reaching up to {wind_gust:.1f} meters per second. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        "Today's weather in {location} features a temperature of {temperature:.1f}°C, though it feels like {feels_like:.1f}°C given the {humidity}% humidity. The sky is predominantly cloudy with {clouds}% cloud cover. Visibility is good, up to {visibility:.1f} km. The wind is blowing at {wind_speed:.1f} m/s with occasional gusts up to {wind_gust:.1f} m/s from {wind_dir}°. Sunrise was at {sunrise_str} UTC, and sunset will be at {sunset_str} UTC.",
        "Currently in {location}, it’s {temperature:.1f}°C outside, but it feels like {feels_like:.1f}°C due to the humidity level of {humidity}%. The weather is overcast with {clouds}% cloud coverage. Visibility reaches {visibility:.1f} kilometers. The wind is blowing from {wind_dir}° at {wind_speed:.1f} m/s, with gusts up to {wind_gust:.1f} m/s. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        "The current weather in {location} shows a temperature of {temperature:.1f}°C, feeling like {feels_like:.1f}°C due to {humidity}% humidity. Cloud cover is extensive at {clouds}%, with visibility extending up to {visibility:.1f} km. Winds are blowing at a speed of {wind_speed:.1f} m/s, gusting up to {wind_gust:.1f} m/s from {wind_dir}°. The sun rose at {sunrise_str} UTC and will set at {sunset_str} UTC.",
        "In {location}, the temperature is currently {temperature:.1f}°C. It feels more like {feels_like:.1f}°C, influenced by {humidity}% humidity. The sky is overcast with {clouds}% cloud cover. Visibility is clear for {visibility:.1f} kilometers. Wind speeds are around {wind_speed:.1f} m/s, with gusts reaching {wind_gust:.1f} m/s from a direction of {wind_dir}°. Sunrise was at {sunrise_str} UTC and sunset will be at {sunset_str} UTC.",
        "In {location}, the temperature is currently {temperature:.1f}°C. It feels more like {feels_like:.1f}°C, influenced by {humidity}% humidity. The sky is overcast with {clouds}% cloud cover. Visibility is clear for {visibility:.1f} kilometers. Wind speeds are around {wind_speed:.1f} m/s, with gusts reaching {wind_gust:.1f} m/s from a direction of {wind_dir}°. Sunrise was at {sunrise_str} UTC and sunset will be at {sunset_str} UTC."
    ]
    #build_desc = template[0] + location + template[1] + "{:.1f}".format(temperature) + template[2] + "{:.1f}".format(feels_like) + template[3] + str(humidity) + template[4] + clouds + template[5] + "{:.1f}".format(visiblity / 1000) + template[6] + "{:.1f}".format(wind_speed) + template[7] + "{:.1f}".format(wind_gust) + template[8] + "{:.1f}".format(wind_dir) + template[9] + sunrice_str + template[10] + sunset_str template[11]
    build_desc = templates[random.randint(0,len(templates)-1)].format(**param)
    return build_desc

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
