import urllib.request
import json
from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')  # Safely fetch 'city' from the POST data
        api_key = "API-KEY-HERE" 
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        full_url = f"{base_url}?q={city}&appid={api_key}&units=metric"  

        try:
            # Fetch data from the API
            source = urllib.request.urlopen(full_url).read()
            list_of_data = json.loads(source)

            # Extract relevant data
            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": f"{list_of_data['coord']['lon']}, {list_of_data['coord']['lat']}",
                "temp": f"{list_of_data['main']['temp']} °C",
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                "main": str(list_of_data['weather'][0]['main']),
                "description": str(list_of_data['weather'][0]['description']),
                "icon": list_of_data['weather'][0]['icon'],
            }
        except urllib.error.HTTPError as e:
            # Handle HTTP errors
            if e.code == 401:
                data = {"error": "Unauthorized: Please check your API key."}
            else:
                data = {"error": f"HTTP Error {e.code}: {e.reason}"}
        except Exception as e:
            # Handle other exceptions
            data = {"error": f"An error occurred: {str(e)}"}
    else:
        data = {}

    return render(request, "main/index.html", data)
