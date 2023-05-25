from flask import Flask, request
import requests
import os

app = Flask(__name__)

api_key = os.environ.get("API_KEY")

@app.route("/weather", methods=["GET"])
def get_weather():
    lat = request.args.get("lat", default=None, type=float)
    lon = request.args.get("lon", default=None, type=float)

    if lat is None or lon is None:
        print("--> Missing parameters")

    data = get_weather(api_key, lat, lon)

    if "error" in data:
        return data, 500
    else:
        return data

def get_weather(API_KEY, LAT, LON):
    # URL definition
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}"

    # HTTP request
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("--> ${}".format(e))

    # JSON response
    if response.status_code == 200:
        return response.json()
    else:
        # showing the error message
        print(f"--> Error in the HTTP request: {response.status_code} - {response.reason}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)