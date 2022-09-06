from django.shortcuts import render, get_object_or_404

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from .models import Meaurements
from .froms import MeasureForms
from .utils import get_geo

# Create your views here.
def calculate_distance_view(request):
    obj = get_object_or_404(Meaurements, id=1)
    form = MeasureForms(request.POST or None)
    geolocator = Nominatim(user_agent="measurements")

    ip = "72.14.207."
    country, city, lat, lon = get_geo(ip)

    location = geolocator.geocode(city)

    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get("destination")
        destination = geolocator.geocode(destination_)
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)

        distance = round(geodesic(pointA, pointB).km, 2)

        instance.location = location
        instance.distance = distance
        instance.save()

    context = {
        "distance": obj,
        "form": form,
    }

    return render(request, "measurements/main.html", context)
