import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm

def index(request):

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
       # print(city.name)
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=8ca80589931ec1213580983469f0673d'
		
        r = requests.get(url.format(city.name)).json()
        if(r['cod']==200):
            city_weather = {
                'id' : city.id,
                'city' : r['name'],
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }

            weather_data.append(city_weather)
   
        else :
            #print(city.name)
            instance = City.objects.get(name=city.name)
            print(instance)
            instance.delete()
            return render(request,'weather/error.html')

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)



def delete(request, id):

    if request.method == 'POST':
        City.objects.filter(id=id).delete()

    return redirect('/')
