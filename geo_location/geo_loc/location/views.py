from django.shortcuts import render,get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from .utils import get_center_coordinates,get_zoom

# Create your views here.

def calculate_distance_view(request):
    # obj=get_object_or_404(Measurement, id=1)
    distance=None
    location=None
    destination=None
    form=MeasurementModelForm(request.POST or None)
    geolocator= Nominatim(user_agent='location')

    m=folium.Map(width=800, height=400)

    if form.is_valid():
        instance=form.save(commit=False)
        location_=form.cleaned_data.get('location')
        location=geolocator.geocode(location_)
        destination_=form.cleaned_data.get('destination')
        destination=geolocator.geocode(destination_)


        l_lat=location.latitude
        l_lon=location.longitude

        d_lat=destination.latitude
        d_lon=destination.longitude

        PointA=(l_lat,l_lon)
        PointB=(d_lat,d_lon)

        distance=round(geodesic(PointA,PointB).km, 2)

        m=folium.Map(width=800, height=500,location=get_center_coordinates(l_lat,l_lon,d_lat,d_lon),
                    zoom_start=get_zoom(distance) )

        folium.Marker([l_lat,l_lon], tooltip=location,
                     icon=folium.Icon(color='blue')).add_to(m)
        folium.Marker([d_lat,d_lon], tooltip=destination,
                     icon=folium.Icon(color='red')).add_to(m)


        line=folium.PolyLine(locations=[PointA,PointB],color='green',weight=3)
        m.add_child(line)

        instance.distance= distance
        instance.save()

    m=m._repr_html_()

    context={
        'distance':distance,
        'location':location,
        'destination':destination,
        'form':form,
        'map':m,
    }

    return render(request,'location/main.html',context)
