import openrouteservice
from openrouteservice import convert

# Replace YOUR_API_KEY with your actual key
client = openrouteservice.Client(key='5b3ce3597851110001cf624817b7b3de72904988ba71c2dc500b964b')

# Example coordinates: user and hospital
user_coords = [ -87.629799, 41.878113 ]       # Chicago (User)
hospital_coords = [ -87.623177, 41.881832 ]   # Nearby hospital

# Request directions
route = client.directions(
    coordinates=[user_coords, hospital_coords],
    profile='driving-car',
    format='geojson'
)

# Extract results
distance_km = route['features'][0]['properties']['segments'][0]['distance'] / 1000
duration_min = route['features'][0]['properties']['segments'][0]['duration'] / 60

print(f"Distance: {distance_km:.2f} km")
print(f"Duration: {duration_min:.1f} minutes")
