# importing necessary modules
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
# for taking geolocations of people on start
from plyer import gps
import requests
import geocoder
import platform
import os
# for loading api key from virtual environment
from dotenv import load_dotenv
# for converting some float value to integer
import math
# modules for splash screen
from kivy.clock import Clock
import time

# passing api key
load_dotenv()
api_key = os.getenv('API_KEY')

# for setting window size
Window.size = (400,600)

# Home main page
class WeatherScreen(Screen):
    pass

# Splash Screen Page
class SplashScreen(Screen):
    """This class will show the splash screen of WeatherAPP"""
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_home, 5)

    def switch_to_home(self, dt):
        self.manager.current = 'weather'

# RootWidget
class RootWidget(ScreenManager):
    pass

# main class
class WeatherApp(MDApp):
    def build(self):

        # themes
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        # design
        return Builder.load_file('weatherdesign.kv')

    # function to pull all the necessary data on starting application
    def on_start(self):
        # Asking for location permission and start updating data
        try:
            if platform.system() == "Windows":
                g = geocoder.ip('me')
                lat, lng = g.latlng
            else:
                # location = gps.getlocation()
                # lat, lng = location["lat"], location["lon"]
                lat, lng = '41.350794', '69.221263'
            if lat and lng:
                self.get_weather_by_location(lat, lng)
            else:
                self.root.get_screen('weather').ids.location_label.text = "Tashkent"
                self.root.get_screen('weather').ids.temperature_label.text = "35°"
                self.root.get_screen('weather').ids.description_label.tooltip_text = "SunnyDay"
                self.root.get_screen('weather').ids.wind_label.text = "44 km/h"
                self.root.get_screen('weather').ids.rain_label.text = "5%"

        except Exception as e:
            print("Error:", e)

    def get_weather(self, params):
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        response = requests.get(weather_url, params=params)
        weather_data = response.json()

        if response.status_code == 200:
            city = weather_data["name"]
            temperature = math.floor(weather_data["main"]["temp"])
            description = weather_data["weather"][0]["description"].capitalize()
            wind = math.floor(weather_data["wind"]["speed"]*18/5)
            rain = math.floor(weather_data["main"]["humidity"])

            self.root.get_screen('weather').ids.location_label.text = city
            self.root.get_screen('weather').ids.temperature_label.text = f"{temperature}°"
            self.root.get_screen('weather').ids.description_label.tooltip_text = description
            self.root.get_screen('weather').ids.wind_label.text = f"{wind}km/h"
            self.root.get_screen('weather').ids.rain_label.text = f"{rain}%"

            # Set weather icon based on weather condition
            id = str(weather_data["weather"][0]["id"])
            # id = "200"
            if id == "800":
                self.root.get_screen('weather').ids.weather_icon.source = "assets/icon/sun_icon.png"
            elif "200" <= id <= "232":
                self.root.get_screen('weather').ids.weather_icon.source = "assets/icon/dark_rain.png"
                self.root.get_screen('weather').ids.bg_image.source = "assets/bg_darkraining.jpg"
            elif "300" <= id <= "321":
                self.root.get_screen('weather').ids.weather_icon.source = "assets/icon/rain.png"
                self.root.get_screen('weather').ids.bg_image.source = "assets/bg_rainy.jpg"
            elif "500" <= id <= "531":
                self.root.get_screen('weather').ids.weather_icon.source = "assets/icon/rain.png"
                self.root.get_screen('weather').ids.bg_image.source = "assets/bg_rainy.jpg"
            elif "600" <= id <= "622":
                self.root.get_screen('weather').ids.weather_icon.source = "assets/icon/snow.png"
                self.root.get_screen('weather').ids.bg_image.source = "assets/bg_snow.jpg"
            elif "701" <= id <= "781":
                self.root.get_screen('weather').ids.weather_icon.source = "assets/icon/moon.png"
                self.root.get_screen('weather').ids.bg_image.source = "assets/bg_night.jpg"
            elif "801" <= id <= "804":
                self.root.get_screen('weather').ids.weather_icon.source = "assets/icon/sun_undercloud.png"
                self.root.get_screen('weather').ids.bg_image.source = "assets/bg_sunundercloud.jpg"
        else:
            self.root.get_screen('weather').ids.location_label.text = "Tashkent"
            self.root.get_screen('weather').ids.temperature_label.text = "35°"
            self.root.get_screen('weather').ids.description_label.tooltip_text = "SunnyDay"
            self.root.get_screen('weather').ids.wind_label.text = "44 km/h"
            self.root.get_screen('weather').ids.rain_label.text = "5%"

    def get_weather_by_location(self, lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"
        }
        self.get_weather(params)

    def get_weather_by_city(self, city):
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        self.get_weather(params)


# executing program
if __name__ == '__main__':
    WeatherApp().run()