from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()


def get_weather_data():
    headers = {'User-Agent': 'FCC-Student-App'}
    results = []

    # US Data (NWS)
    us_cities = {
        "Fresno": "https://api.weather.gov/gridpoints/HNX/53,100/forecast",
        "New York": "https://api.weather.gov/gridpoints/OKX/33,37/forecast"
    }

    for city, url in us_cities.items():
        try:
            res = requests.get(url, headers=headers).json()
            latest = res['properties']['periods'][0]
            results.append({"city": city, "temp": f"{latest['temperature']}°F", "desc": latest['shortForecast']})
        except:
            results.append({"city": city, "temp": "N/A", "desc": "Error fetching data"})

    # London Data (Open-Meteo Bonus)
    try:
        london_url = "https://api.open-meteo.com/v1/forecast?latitude=51.5085&longitude=-0.1257&current_weather=true"
        lon_res = requests.get(london_url).json()
        results.append({
            "city": "London",
            "temp": f"{lon_res['current_weather']['temperature']}°C",
            "desc": "International Source"
        })
    except:
        pass

    return results


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    weather = get_weather_data()
    cards = "".join([f"""
        <div style="background:white; padding:20px; border-radius:15px; box-shadow:0 4px 6px rgba(0,0,0,0.1); width:200px; text-align:center;">
            <h2 style="color:#1a73e8;">{w['city']}</h2>
            <p style="font-size:2em; font-weight:bold;">{w['temp']}</p>
            <p>{w['desc']}</p>
        </div>
    """ for w in weather])

    return f"""
    <html>
        <body style="font-family:sans-serif; background:#f0f2f5; display:flex; justify-content:center; gap:20px; padding:50px;">
            {cards}
        </body>
    </html>
    """