from django.urls import path
from weather.views import HomePage, CitySuggestView

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('api/v1/weather/helper/', CitySuggestView.as_view(), name='city_suggest'),
]