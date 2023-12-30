from flask import Flask, render_template, request, jsonify
# from flask_socketio import SocketIO
#from flask_pymongo import PyMongo
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import requests

app = Flask(__name__)
# socketio = SocketIO(app)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/safepark'
# mongo = PyMongo(app)
payload, headers= {}, {}
INRIX_AUTH_URL = 'https://api.iq.inrix.com/auth/v1/appToken?appId=mpdesmsn7h&hashToken=bXBkZXNtc243aHxjNlNXYXhBaXU1NktMaFZpMll2dnNhT3VTTnU2cTFZSDZKaHF4SFE5'
response = requests.request("GET", INRIX_AUTH_URL, headers=headers, data=payload).json()
INRIX_TOKEN = response["result"]["token"]

lots = {}
vals = {}




# API endpoint for getting parking options
@app.route('/api/get_parking', methods=['POST'])
def get_parking():
    try:
        data = request.get_json()
        
        # Get coordinates and bounding box using the helper functions
        lat = getLatitude(data)
        long = getLongitude(data)
        limit = 25
        headers = {
        'Content-Type': 'application/json',
        'Authorization':
                'Bearer [eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6Im1wZGVzbXNuN2giLCJ0b2tlbiI6eyJpdiI6IjA1ZDgxNDg5MzVlN2FkZmEzMjFmZDlkODJmNjJhZmNlIiwiY29udGVudCI6IjBkYmM2YzhhMjA1NDI3MzZlNmM4NTdiNDdkYzE3NGMzMjk2ODI3ZGMyOTM0NzE1MmJlNDM4Njc3ZWRkNTc5NzkxMmMyYzhmY2IwOTU1Y2U4MGQ2OWIwYzFkMjMzOTlhMDQ0Y2EyNDQ4Yzk3ZTg5NjU5MDhkOWJiMGVjMjc5N2QwNzNhYmNhMzY5NDk4MjRiMGFmNTZlNDlhM2UxZDZlNzVlZTJmZjc5M2I5MTllODQxNmNhMGQ4MmFjOGY0ZmU4Y2ZhM2UwM2U3MmMzNTU0NWI1MjRiNDBhNWM3OWY4ZDk4ZmI0OTIyZjg3ODExODVlNzI4MzA1ZDY5OGM3ZWU5NGIyNTMzM2I2ZDFhZDZlNDc1MzYzNWMxN2RkYTBjYzJmNWI3MDI1OWU4OWMzOTZiZDVhYTE5MWJiNDAxZDE4NzE3NGRkZTZmMDhkZGNlMTgzNTU4OTUxMzcwMDEzZTRlNGQ4YTcwYmI3ZTExOGE4NGNiOTg4Njg5ZWViZGQ5MTA1ZjUzMWQ1MGFjNjE2ZmVkMTEzMmFhMmYwMTJiMTdmYzRjZjcyMzAwYmFhZjNjMWM3NTU5ZTI0YTEyYTBkOGU0ZjExYTQyODQwYzNlZGVhZmQ0MGY3OGU2MGI1NzFiNmUwYmM1YmFjMGNlNjIzYmQ5NTQ1ZjI5MWU0MzdjYzczMzEyMjdhNDU5YTQzOTdlM2EwYmI0MDBmYzE2ZTAyYzJkM2JmNGUxZmY3MTY3ZDM0NThhNTRiM2Q0MmJmOWUwN2JjMDI2YjRmYzJhNjY4ZmQyYWFiMjc1NTdhNmM4MDlhMWI2MTljMDYxYjQzNmQwYzMwNzEyYzc5MDBjNGU5MDBhODQ4NzBmNDNkYmJiZTZhNWMzNTEzNjM4In0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiIwNWQ4MTQ4OTM1ZTdhZGZhMzIxZmQ5ZDgyZjYyYWZjZSIsImNvbnRlbnQiOiIzMmFiMTZhMzA3N2IzZDA4ZTRjODZjYTg3YjhiMDljNzI1MzkwM2Y1NTExNjU5MTFiZTZlOTkzM2ZlY2I2ZTQ3MDhmNmYzYjFkMTg5NjNkMjEzNDliMWZmIn0sImp0aSI6ImRlMzhlYTIxLTIxZDQtNDZhMy05ZDg4LWNiZGE4YzAzNTk3MSIsImlhdCI6MTY5OTgwMzQ5OSwiZXhwIjoxNjk5ODA3MDk4fQ.-ekm5xjDFBHx1XedChqx4Sh1-R2uL2OmJQjgD7AAGZA]'
        }
        
        INRIX_OFF_PARKING_URL = f"https://api.iq.inrix.com/lots/v3?point={lat}%7C{long}&radius=150&token={INRIX_TOKEN}"
        off_response = requests.request("GET", INRIX_OFF_PARKING_URL, headers=headers, data=payload)
        INRIX_ON_PARKING_URL = f'https://api.iq.inrix.com/blocks/v3?point={lat}%7C{long}&radius=150&limit=25&token={INRIX_TOKEN}'
        on_response = requests.request("GET", INRIX_ON_PARKING_URL, headers=headers, data=payload)

        combined_response = {"response1": off_response.json(), "response2": on_response.json()}
        lots[data] = combined_response

        return combined_response, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def convertToCoordinates_addy(place):
    payload, headers= {}, {}
    placee = '+'.join(place.split())

    base_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={placee}&key=AIzaSyBCVX3901fCD-pTLejQ8_O0nDvgZK3_E9c'

    response = requests.request("GET", base_url, headers=headers, data=payload)
    data = response.json() 
    if response.status_code == 200 and data['status'] == 'OK':
        # Extract the coordinates from the response
        location = data['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        
        formatted_coordinates = f"{latitude}|{longitude}"
        return formatted_coordinates
    else:
        return None

def getLatitude(place):
    payload, headers= {}, {}
    placee = '+'.join(place.split())

    base_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={placee}&key=AIzaSyBCVX3901fCD-pTLejQ8_O0nDvgZK3_E9c'

    response = requests.request("GET", base_url, headers=headers, data=payload)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        return latitude
    else:
        print(f"Error: {data['status']}")
        return None

def getLongitude(place):
    payload, headers= {}, {}
    placee = '+'.join(place.split())

    base_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={placee}&key=AIzaSyBCVX3901fCD-pTLejQ8_O0nDvgZK3_E9c'

    response = requests.request("GET", base_url, headers=headers, data=payload)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        longitude = location['lng']
        return longitude
    else:
        print(f"Error: {data['status']}")
        return None
    
#Incident API
@app.route('/assess_parking_safety', methods=['POST'])
def get_incidents_data(place):
    try:
        lat = getLatitude(place)
        long = getLongitude(place)
        headers = {
        'Content-Type': 'application/json',
        'Authorization':
                'Bearer [eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6Im1wZGVzbXNuN2giLCJ0b2tlbiI6eyJpdiI6IjA1ZDgxNDg5MzVlN2FkZmEzMjFmZDlkODJmNjJhZmNlIiwiY29udGVudCI6IjBkYmM2YzhhMjA1NDI3MzZlNmM4NTdiNDdkYzE3NGMzMjk2ODI3ZGMyOTM0NzE1MmJlNDM4Njc3ZWRkNTc5NzkxMmMyYzhmY2IwOTU1Y2U4MGQ2OWIwYzFkMjMzOTlhMDQ0Y2EyNDQ4Yzk3ZTg5NjU5MDhkOWJiMGVjMjc5N2QwNzNhYmNhMzY5NDk4MjRiMGFmNTZlNDlhM2UxZDZlNzVlZTJmZjc5M2I5MTllODQxNmNhMGQ4MmFjOGY0ZmU4Y2ZhM2UwM2U3MmMzNTU0NWI1MjRiNDBhNWM3OWY4ZDk4ZmI0OTIyZjg3ODExODVlNzI4MzA1ZDY5OGM3ZWU5NGIyNTMzM2I2ZDFhZDZlNDc1MzYzNWMxN2RkYTBjYzJmNWI3MDI1OWU4OWMzOTZiZDVhYTE5MWJiNDAxZDE4NzE3NGRkZTZmMDhkZGNlMTgzNTU4OTUxMzcwMDEzZTRlNGQ4YTcwYmI3ZTExOGE4NGNiOTg4Njg5ZWViZGQ5MTA1ZjUzMWQ1MGFjNjE2ZmVkMTEzMmFhMmYwMTJiMTdmYzRjZjcyMzAwYmFhZjNjMWM3NTU5ZTI0YTEyYTBkOGU0ZjExYTQyODQwYzNlZGVhZmQ0MGY3OGU2MGI1NzFiNmUwYmM1YmFjMGNlNjIzYmQ5NTQ1ZjI5MWU0MzdjYzczMzEyMjdhNDU5YTQzOTdlM2EwYmI0MDBmYzE2ZTAyYzJkM2JmNGUxZmY3MTY3ZDM0NThhNTRiM2Q0MmJmOWUwN2JjMDI2YjRmYzJhNjY4ZmQyYWFiMjc1NTdhNmM4MDlhMWI2MTljMDYxYjQzNmQwYzMwNzEyYzc5MDBjNGU5MDBhODQ4NzBmNDNkYmJiZTZhNWMzNTEzNjM4In0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiIwNWQ4MTQ4OTM1ZTdhZGZhMzIxZmQ5ZDgyZjYyYWZjZSIsImNvbnRlbnQiOiIzMmFiMTZhMzA3N2IzZDA4ZTRjODZjYTg3YjhiMDljNzI1MzkwM2Y1NTExNjU5MTFiZTZlOTkzM2ZlY2I2ZTQ3MDhmNmYzYjFkMTg5NjNkMjEzNDliMWZmIn0sImp0aSI6ImRlMzhlYTIxLTIxZDQtNDZhMy05ZDg4LWNiZGE4YzAzNTk3MSIsImlhdCI6MTY5OTgwMzQ5OSwiZXhwIjoxNjk5ODA3MDk4fQ.-ekm5xjDFBHx1XedChqx4Sh1-R2uL2OmJQjgD7AAGZA]'
        }
        INRIX_INCIDENTS_URL = f"https://api.iq.inrix.com/v1/incidents?box={lat}%7C{long}%2C37.746138%7C-122.395481&radius=150&incidentoutputfields=All&incidenttype=Incidents,Flow,Construction&locale=en&token={INRIX_TOKEN}"
        response = requests.request("GET", INRIX_INCIDENTS_URL, headers=headers, data=payload)
        return response.json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def assess_parking_safety(place):
    try:
        # Use INRIX Incidents API to get safety information
        incidents_data = get_incidents_data(place)

        # Calculate the total number of incidents, which will dictate how dangerous or safe a certain area is
        num_of_incidents = len(incidents_data)

        return num_of_incidents

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def crim_file_data(latitude, longitude):
    df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv", delimiter = ",")
    df.drop(columns=['Current Police Districts','Supervisor District 2012', 'Analysis Neighborhood', 'CNN','CAD Number', 'Filed Online','ESNCAG - Boundary File', 'Invest In Neighborhoods (IIN) Areas','Central Market/Tenderloin Boundary Polygon - Updated', 'HSOC Zones as of 2018-06-05', 'Civic Center Harm Reduction Project Boundary']) #removing those with >35% null vals
    key_strings = [
    'Vandalism',
    'Motor Vehicle Theft',
    'Larceny Theft',
    'Robbery'
    ]

    df = df[df['Incident Category'].isin(key_strings)]
    df = df.dropna(subset='Point')

    square_corners = calc_square(latitude, longitude)

    top_left = square_corners[0]
    top_right = square_corners[1]
    bottom_left = square_corners[2]
    bottom_right = square_corners[3]

    lat_TL = top_left[0]
    long_TL = top_left[1]

    lat_TR = top_right[0]
    long_TR = top_right[1]

    lat_BL = bottom_left[0]
    long_BL = bottom_left[1]

    lat_BR = bottom_right[0]
    long_BR = bottom_right[1]

    boundary_points = [(lat_TL, long_TL), (lat_TR, long_TR), (lat_BL, long_BL), (lat_BR, long_BR)]
    polygon = Polygon(boundary_points)

    crimes_inside = 0

    for index, row in df.iterrows():
        tlat = row['Latitude']
        tlong = row['Longitude']
        lat = round(tlat, 4)
        long = round(tlong, 4)
        test_point = Point(lat, long)
        if test_point.within(polygon):
            crimes_inside += 1

    return crimes_inside;


def calc_square(latitude, longitude):
    side = 0.0006

    top_left = (latitude + side, longitude - side)
    top_right = (latitude + side, longitude + side)
    bottom_left = (latitude - side, longitude - side)
    bottom_right = (latitude - side, longitude + side)

    return [top_left, top_right, bottom_left, bottom_right]


def assess_safety(): # test this
    try:
        for place in lots:
            crime = crim_file_data(getLatitude(place), getLongitude(place))
            incidents = assess_parking_safety(place)
            score_denom = (1.5 * crime) + incidents + 1
            score = 1 / score_denom
            vals[place] = score

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def sort_search(): # test this
    return dict(sorted(vals.items(), key=lambda item: item[1], reverse=True))  

if __name__ == "__main__":
    app.run(debug = True)