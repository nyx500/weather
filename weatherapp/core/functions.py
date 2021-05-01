import requests
from bs4 import BeautifulSoup
import mimetypes
from .models import *


VALID_IMAGE_MIMETYPES = [
    "image"
]

VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]

def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    # https://timmyomahony.com/blog/upload-and-validate-image-from-url-in-django
    # http://stackoverflow.com/a/10543969/396300
    # Checks if the image URL ends with any of the valid extensions and returns true if it does and false otherwise
    return any([url.endswith(e) for e in extension_list])

def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
    # https://timmyomahony.com/blog/upload-and-validate-image-from-url-in-django
    # http://stackoverflow.com/a/10543969/396300
    # The guess_type function returns the type of object (should be an image) and the encoding, then these are stored in two separate variables
    mimetype, encoding = mimetypes.guess_type(url)
    # Checks if the value (the only one is image) in the list of valid formats is the same as the returned mimetype and prints True if this is the case
    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False

def encode_weather_based_on_temp(condition, temp):
    if temp <= - 10:
        pass
    elif temp > -10 and temp <= 0:
        condition += 1
    elif temp > 0 and temp <= 5:
        condition += 2
    elif temp > 5 and temp <= 10:
        condition += 3
    elif temp > 10 and temp <= 15:
        condition += 4
    elif temp > 15 and temp <= 20:
        condition += 5
    elif temp > 20 and temp <= 25:
        condition += 6
    elif temp > 25 and temp <= 30:
        condition += 7
    elif temp > 30 and temp <= 35:
        condition += 8
    elif temp > 35 and temp <= 40:
        condition += 9
    else:
        condition += 10
    return(condition)

def change_feels_like_weather(humidity, wind, weather, hot_or_cold, weather_data):

    print(f"WIND: {wind}")

    if wind <= 20:
        weather_data['is_it_windy'] = "calm and still."
        weather += 3
    elif wind > 20 and wind <= 30:
        weather_data['is_it_windy'] = "quite windy."
        weather += 2
    elif wind > 30 and wind < 45:
        weather_data['is_it_windy'] = "very windy."
        weather += 1
    else:
        weather_data['is_it_windy'] = "extremely windy."
    
    if hot_or_cold == 'cold':
        if humidity > 50 and humidity < 70:
           weather += 2
        elif humidity >= 70 and humidity < 90:
            weather += 1
        elif humidity >= 90:
            pass

    if hot_or_cold == 'hot':
        if humidity > 50 and humidity < 70:
            pass
        elif humidity >= 70 and humidity < 90:
            weather += 1
        elif humidity >= 90:
            weather += 2

    return(weather)
    

def get_html_content(city, time):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
    LANGUAGE = "en-gb;q=0.8, en;q=0.7"
    # Makes a session object
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # Replaces all the spaces in the string to a '+'
    city = city.replace(' ', '+')
    if time == 'now':
        html_content = session.get(f"https://www.google.co.uk/search?q=weather+in+{city}").text
    elif time == 'later':
        html_content = session.get(f"https://www.google.co.uk/search?q=weather+in+{city}+in+two+hours").text
    else:
        html_content = session.get(f"https://www.google.co.uk/search?q=weather+in+{city}+tomorrow").text
    return html_content


def get_weather_data(html_content, units):

    recipes = Recipe.objects.all()
    recipe_list = []

    soup = BeautifulSoup(html_content, 'html.parser')
    weather_data = dict()
    if soup.find('div', attrs={'id': 'wob_loc'}) == None:
        return "No such city"
    else:
        weather_data['region'] = soup.find('div', attrs={'id': 'wob_loc'}).text
        weather_data['time'] = soup.find('div', attrs={'id': 'wob_dts'}).text
        weather_data['weather'] = soup.find('div', attrs={'id': 'wob_dcp'}).text.lower()
        weather_data['temp'] = int(soup.find('span', attrs={'id': 'wob_tm'}).text)
        weather_data['precipitation'] = int(soup.find('span', attrs={'id': 'wob_pp'}).text.replace('%', ''))
        weather_data['humidity'] = int(soup.find('span', attrs={'id': 'wob_hm'}).text.replace('%', ''))
        weather_data['wind'] = int(soup.find('span', attrs={'id': 'wob_ws'}).text.replace(' km/h', ''))

        weather_value = 0 

        if weather_data['wind'] > 20:
            weather_types = ['Windy']
            for r in recipes:
                for w in r.weather.all().values_list():
                    for wt in weather_types:
                        if r not in recipe_list:
                            if wt in w[1]:
                                recipe_list.append(r)

        if weather_data['humidity'] > 70:
            weather_types = ['Humid']
            for r in recipes:
                for w in r.weather.all().values_list():
                    for wt in weather_types:
                        if wt in w[1]:
                            if r not in recipe_list:
                                recipe_list.append(r)
        else:
            if weather_data['precipitation'] < 15:
                weather_types = ['Dry']
                for r in recipes:
                    for w in r.weather.all().values_list():
                        for wt in weather_types:
                            if r not in recipe_list:
                                if wt in w[1]:
                                    recipe_list.append(r)
            else:
                weather_types = ['Wet']
                for r in recipes:
                    for w in r.weather.all().values_list():
                        for wt in weather_types:
                            if r not in recipe_list:
                                if wt in w[1]:
                                    recipe_list.append(r)

        if 'sunny' in weather_data['weather'] or 'clear' in weather_data['weather']:
            weather_value = 5
            weather_types = ['Sunny']
            for r in recipes:
                for w in r.weather.all().values_list():
                    for wt in weather_types:
                        if r not in recipe_list:
                            if wt in w[1]:
                                recipe_list.append(r)

        weather4 = ['overcast', 'cloud', 'haze']
        for condition in weather4:
            if condition in weather_data['weather']:
                weather_value = 4
                weather_types = ['Cloudy', 'Grey']
                for r in recipes:
                    for w in r.weather.all().values_list():
                        for wt in weather_types:
                            if r not in recipe_list:
                                if wt in w[1]:
                                    recipe_list.append(r)

        if 'rain' in weather_data['weather'] or 'shower' in weather_data['weather']:
            weather_value = 3
            weather_types = ['Wet']
            for r in recipes:
                for w in r.weather.all().values_list():
                    for wt in weather_types:
                        if r not in recipe_list:
                            if wt in w[1]:
                                recipe_list.append(r)

        if 'storm' in weather_data['weather']:
            weather_value = 2
            weather_types=['Stormy']
            for r in recipes:
                for w in r.weather.all().values_list():
                    for wt in weather_types:
                        if r not in recipe_list:
                            if wt in w[1]:
                                recipe_list.append(r)
        
        weather1 = ['snow', 'freezing', 'mist', 'sleet', 'icy', 'fog', 'flurries', 'hail']
        for condition in weather1:
            if condition in weather_data['weather']:
                weather_value = 1
                weather_types= ['Snowing', 'Frosty']
                for r in recipes:
                    for w in r.weather.all().values_list():
                        for wt in weather_types:
                            if r not in recipe_list:
                                if wt in w[1]:
                                    recipe_list.append(r)
        if weather_value == 0:
            weather = 'Error'
        else:
            weather_value = encode_weather_based_on_temp(weather_value, weather_data['temp'])

            if weather_value <= 10: 
                weather = change_feels_like_weather(weather_data['humidity'], weather_data['wind'], weather_value, 'cold', weather_data)
            else:
                weather = change_feels_like_weather(weather_data['humidity'], weather_data['wind'], weather_value, 'hot', weather_data)

        visibility = 1
        obscured_visibility = ['mist', 'fog', 'dust', 'smoke']
        for condition in obscured_visibility:
            if condition in weather_data['weather']:
                visibility = 0
                weather_types=['Foggy']
                for r in recipes:
                    for w in r.weather.all().values_list():
                        for wt in weather_types:
                            if r not in recipe_list:
                                if wt in w[1]:
                                    recipe_list.append(r)

        weather_data['visibility'] = visibility

        weather_data['overall_assessment'] = weather

        if weather_data['overall_assessment'] <= 13:
            weather_types = ['Cold']
            for r in recipes:
                for w in r.weather.all().values_list():
                    for wt in weather_types:
                        if r not in recipe_list:
                            if wt in w[1]:
                                recipe_list.append(r)
        elif weather_data['overall_assessment'] > 13 and weather_data['overall_assessment'] <= 16:
            weather_types = ['Warm']
            for r in recipes:
                for w in r.weather.all().values_list():
                    for wt in weather_types:
                        if r not in recipe_list:
                            if wt in w[1]:
                                recipe_list.append(r)
        else:
            weather_types = ['Scorching']
            for r in recipes:
                for w in r.weather.all().values_list():
                    for wt in weather_types:
                        if r not in recipe_list:
                            if wt in w[1]:
                                recipe_list.append(r)

        if units == "fahrenheit":
            weather_data['units'] = 'fahrenheit'
            weather_data['temp'] = int(soup.find('span', attrs={'id': 'wob_ttm'}).text)
            weather_data['wind'] = str(soup.find('span', attrs={'id': 'wob_tws'}).text)
        else:
            weather_data['units'] = 'celsius'
            weather_data['wind'] = str(soup.find('span', attrs={'id': 'wob_ws'}).text)

        # Returns a list of recipes as JSON serializable dictionaries
        ids = []
        for r in recipe_list:
            ids.append(r.id)
        recipes_as_dictionaries = []
        for i in ids:
            for r in recipes.values():
                if i == r['id']:
                    recipes_as_dictionaries.append(r)

        weather_data["recipes"] = recipes_as_dictionaries

        print(f"Recipe list: {recipe_list}, {ids}")
        print(f"Recipes as dictionaries: {recipes_as_dictionaries}")

        return weather_data
