from django.shortcuts import render
import requests
import datetime

def index(request):
    api_key = 'API_KEY'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Fetch current weather data
    response = requests.get(current_weather_url.format(city, api_key)).json()

    # Check if 'coord' key is present in the response
    if 'coord' in response:
        lat, lon = response['coord']['lat'], response['coord']['lon']

        # Fetch forecast data
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

        # Extract relevant weather data
        weather_data = {
            'city': city,
            'temperature': round(response['main']['temp'] - 273.15, 2),
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon']
        }

        # Check if 'daily' key is present in forecast response
        if 'daily' in forecast_response:
            # Extract daily forecast data
            daily_forecast = []
            for daily_data in forecast_response['daily'][:5]:
                daily_forecast.append({
                    'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                    'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
                    'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
                    'description': daily_data['weather'][0]['description'],
                    'icon': daily_data['weather'][0]['icon']
                })
        else:
            # Handle the case where 'daily' key is not present in forecast response
            print(f"Error: 'daily' key not found in forecast response for city: {city}")
            return None, None

        return weather_data, daily_forecast
    else:
        # Handle the case where 'coord' key is not present in current weather response
        print(f"Warning: 'coord' key not found in current weather response for city: {city}")
        
        # Proceed without latitude and longitude information
        lat, lon = None, None

        # Continue with the rest of the function as needed

        return None, None