import json
from os import getenv

from dotenv import load_dotenv

import aiohttp


load_dotenv()

WEATHER_TOKEN = getenv('WEATHER_TOKEN')

async def get_weather(lat: float, lon: float) -> str:
	url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}'

	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			json_text = await response.text()
			return json.loads(json_text)['weather'][0]['main']

async def get_city_coordinates(city: str) -> tuple[float, float]:
	url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_TOKEN}"

	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			data = await response.json()
			if data:
				lat = data[0]['lat']
				lon = data[0]['lon']
				return lat, lon
			else:
				raise ValueError(f"City '{city}' not found.")