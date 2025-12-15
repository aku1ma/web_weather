import os
import requests
from django.shortcuts import render

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def index(request):
    weather = None
    error = None

    if request.method == "POST":
        city = request.POST.get("city", "").strip()
        if not city:
            error = "Введи город."
        elif not API_KEY:
            error = "Нет переменной окружения OPENWEATHER_API_KEY."
        else:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "ru"}
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json()
                weather = {
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "desc": data["weather"][0]["description"],
                }
            else:
                error = "Город не найден или ошибка API."

    return render(request, "weather/index.html", {"weather": weather, "error": error})
