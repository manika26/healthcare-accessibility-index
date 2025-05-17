import pandas as pd
import openrouteservice
import time


client = openrouteservice.Client(key="5b3ce3597851110001cf624817b7b3de72904988ba71c2dc500b964b")

# State capital coordinates (longitude, latitude)
capital_coords = {
    "AL": [-86.3000, 32.3668], "AK": [-134.4197, 58.3019], "AZ": [-112.0960, 33.4484],
    "AR": [-92.2896, 34.7465], "CA": [-121.4944, 38.5816], "CO": [-104.9847, 39.7392],
    "CT": [-72.6851, 41.7640], "DE": [-75.5244, 39.1582], "FL": [-84.2807, 30.4383],
    "GA": [-84.3880, 33.7490], "HI": [-157.8583, 21.3069], "ID": [-116.2035, 43.6150],
    "IL": [-89.6500, 39.7833], "IN": [-86.1581, 39.7684], "IA": [-93.6091, 41.5868],
    "KS": [-95.6890, 39.0473], "KY": [-84.8733, 38.2009], "LA": [-91.1402, 30.4583],
    "ME": [-69.7653, 44.3072], "MD": [-76.4922, 38.9784], "MA": [-71.0589, 42.3601],
    "MI": [-84.5555, 42.7325], "MN": [-93.0940, 44.9537], "MS": [-90.2070, 32.2988],
    "MO": [-92.1735, 38.5767], "MT": [-112.0270, 46.5958], "NE": [-96.6753, 40.8136],
    "NV": [-119.7661, 39.1638], "NH": [-71.5491, 43.2067], "NJ": [-74.7670, 40.2206],
    "NM": [-106.6504, 35.0844], "NY": [-73.7562, 42.6526], "NC": [-78.6382, 35.7796],
    "ND": [-100.7837, 46.8083], "OH": [-82.9988, 39.9612], "OK": [-97.5164, 35.4676],
    "OR": [-123.0351, 44.9429], "PA": [-76.8867, 40.2732], "RI": [-71.4128, 41.8240],
    "SC": [-81.0348, 34.0007], "SD": [-100.3464, 44.3668], "TN": [-86.7844, 36.1627],
    "TX": [-97.7431, 30.2672], "UT": [-111.8910, 40.7608], "VT": [-72.5766, 44.2601],
    "VA": [-77.4605, 37.5407], "WA": [-122.9007, 47.0379], "WV": [-81.6326, 38.3498],
    "WI": [-89.3844, 43.0731], "WY": [-104.8020, 41.1403], "DC": [-77.0369, 38.9072]
}

results = []

print("Calculating travel times using nearest snapped points...\n")

for state, user_coords in capital_coords.items():
    # Offset slightly to simulate another location nearby (fake hospital)
    rough_coords = [user_coords[0] + 0.02, user_coords[1] + 0.02]

    # Try to snap hospital to nearest routable road
    try:
        nearest = client.nearest(coordinates=rough_coords)
        snapped_coords = nearest['coordinates'][0]
    except:
        snapped_coords = rough_coords  # fallback to raw offset

    # Now calculate travel time from user (capital) to hospital (snapped)
    try:
        route = client.directions(
            coordinates=[user_coords, snapped_coords],
            profile='driving-car',
            format='geojson'
        )
        duration_min = route['features'][0]['properties']['segments'][0]['duration'] / 60
        results.append({'State': state, 'Avg_Travel_Time_Min': round(duration_min, 2)})
        print(f"{state}  {round(duration_min, 2)} minutes")

        time.sleep(2.5)  # Rate limit protection

    except Exception as e:
        print(f"{state} Error: {e}")
        results.append({'State': state, 'Avg_Travel_Time_Min': None})

# Save result
df_result = pd.DataFrame(results)
df_result.to_csv("data/raw/state_travel_time.csv", index=False)
print("\nAll done! Travel times saved to: data/raw/state_travel_time.csv")
