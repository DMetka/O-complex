from django.test import TestCase, Client
from unittest.mock import patch


class WeatherViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('weather.views.request_city_helper')
    @patch('weather.views.weather_in_city')
    def test_homepage_with_city(self, mock_weather_in_city, mock_request_city_helper):
        mock_request_city_helper.return_value = {
            'results': [
                {'name': 'Москва', 'latitude': 55.7558, 'longitude': 37.6173}
            ]
        }

        mock_weather_in_city.return_value = {
            'hourly': {
                'time': ['2025-05-25T00:00', '2025-05-25T01:00'],
                'temperature_2m': [10.0, 11.0]
            }
        }

        response = self.client.get('/?city=Москва')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/homePage.html')

        weather_data = response.context['weather']
        city = response.context['city']

        self.assertEqual(city['name'], 'Москва')
        self.assertEqual(len(weather_data), 2)
        self.assertEqual(weather_data[0][1], 10.0)

    @patch('weather.views.request_city_helper')
    def test_city_suggest_view(self, mock_request_city_helper):
        mock_request_city_helper.return_value = {
            'results': [
                {'name': 'Санкт-Петербург', 'country': 'RU', 'latitude': 59.93, 'longitude': 30.31}
            ]
        }

        response = self.client.get('/api/v1/weather/helper/?key_words=Санкт')

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn('results', json_data)
        self.assertEqual(len(json_data['results']), 1)
        self.assertEqual(json_data['results'][0]['name'], 'Санкт-Петербург')
