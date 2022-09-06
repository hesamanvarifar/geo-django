from django.shortcuts import render, get_object_or_404

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from .models import Meaurements
from .froms import MeasureForms
from .utils import get_geo, get_centre_coordinates,get_zoom

import folium

# Create your views here.
def calculate_distance_view(request):
    # initial values
    distance = None
    destination = None

    obj = get_object_or_404(Meaurements, id=1)
    form = MeasureForms(request.POST or None)
    geolocator = Nominatim(user_agent="measurements")

    ip = "72.14.207."
    country, city, lat, lon = get_geo(ip)

    location = geolocator.geocode(city)

    # location coordinate
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    # initial folium map
    m = folium.Map(width=800, height=500, location=get_centre_coordinates(l_lat, l_lon),zoom_start=8)

    # location maker
    folium.Marker(
        [l_lat, l_lon],
        tooltip="click here for more",
        popup=city["city"],
        icon=folium.Icon(color="brown"),
    ).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get("destination")
        destination = geolocator.geocode(destination_)

        # destination coordinate
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)

        # distance calculate
        distance = round(geodesic(pointA, pointB).km, 2)

        # folium map modification
        m = folium.Map(width=800, height=500, location=pointA,zoom_start=get_zoom(distance))

        # location maker
        folium.Marker(
            [l_lat, l_lon],
            tooltip="click here for more",
            popup=city["city"],
            icon=folium.Icon(color="brown"),
        ).add_to(m)

        # destination maker
        folium.Marker(
            [d_lat, d_lon],
            tooltip="click here for more",
            popup=destination,
            icon=folium.Icon(color="red", icon="cloud"),
        ).add_to(m)

        # draw the line between location and destination
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)

        instance.location = location
        instance.distance = distance
        instance.save()

    m = m.__repr__html_()

    context = {
        "distance": obj,
        "form": form,
        "m": m,
    }

    return render(request, "measurements/main.html", context)
