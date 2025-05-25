from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import requests as req


class HomePage(View):
    template_name = 'weather/homePage.html'

    def get(self, request):
        city = request.GET.get('city')

        if city:
            city_params = request_city_helper(query=city)
            city = city_params['results'][0]
        else:
            city = {}

        latitude = city.get('latitude', False)
        longitude = city.get('longitude', False)

        if latitude and longitude:
            weather = weather_in_city(latitude=latitude, longitude=longitude)
            times = weather['hourly']['time']
            temps = weather['hourly']['temperature_2m']
            weather_data = list(zip(times, temps))
        else:
            weather_data = None

        print(weather_data)

        return render(request, self.template_name, {
            'weather': weather_data,
            'city': city,
        })


class CitySuggestView(View):
    def get(self, request):
        query = request.GET.get('key_words', '')
        if not query:
            return JsonResponse({'results': []})

        res = request_city_helper(query=query)

        results = []

        if "results" in res:
            for city in res["results"]:
                results.append({
                    "name": city["name"],
                    "country": city.get("country", ""),
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                })

        return JsonResponse({"results": results})


def request_city_helper(query: str) -> dict:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=5&language=ru"
    res = req.get(url)
    res.raise_for_status()
    return res.json()


def weather_in_city(latitude: float, longitude: float) -> dict:
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&forecast_days=1'
    res = req.get(url)
    res.raise_for_status()
    return res.json()

