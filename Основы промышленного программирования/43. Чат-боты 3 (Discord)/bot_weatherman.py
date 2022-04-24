import asyncio
import logging
import os
from datetime import datetime
from functools import partial

import requests
from discord.ext import commands

from bot_token import TOKEN

URL = "http://api.openweathermap.org"
API_KEY = os.getenv("API_KEY")  # open weather api

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
))
logger.addHandler(handler)


class PlaceNotFound(Exception):
    ...


class ErrorNoWeather(Exception):
    ...


async def get_geocode_coord(city_name):
    url = f"{URL}/geo/1.0/direct"
    params = {"q": city_name, "appid": API_KEY}
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None,
                                      partial(requests.get, url, params=params))
    resp.raise_for_status()
    resp_json = resp.json()
    if not resp_json:
        raise PlaceNotFound
    coord = resp_json[0]["lat"], resp_json[0]["lon"]
    return coord


def get_weather_data_for_user(place, raw_weather_data):
    compass_sector = ['n', 'nne', 'ne', 'ene', 'e', 'ese', 'se', 'sse', 's', 'ssw', 'sw', 'wsw', 'w',
                      'wnw', 'nw', 'nnw', 'n']
    wind_direction = compass_sector[int(raw_weather_data["wind_deg"] / 22.5)]
    dt = datetime.fromtimestamp(raw_weather_data["dt"])
    temperature = raw_weather_data["temp"]
    try:
        temperature = temperature["day"]
    except TypeError:
        pass
    res = [
        (None, f"weather forecast in {place} for {dt.date().isoformat()}:"),
        ("temperature", f'{temperature} ℃'),
        ("pressure", f'{raw_weather_data["pressure"]} mm'),
        ("humidity", f'{raw_weather_data["humidity"]}%'),
        ("description", raw_weather_data["weather"][0]["description"]),
        ("wind", f'{wind_direction}, {raw_weather_data["wind_speed"]} m/s')
    ]
    return res


def get_user_weather_formatted(place, raw_weather_data):
    user_weather_data = get_weather_data_for_user(place, raw_weather_data)
    msg = ""
    for k, v in user_weather_data:
        if k is None:
            row = v
        else:
            row = f"{k}: {v}"
        msg += row[0].title() + row[1:]
        msg += "\n"
    return msg


async def get_weather(weather_type, lat, lon):
    url = f"{URL}/data/2.5/onecall"
    exclude_weathers = ["current", "minutely", "hourly", "daily", "alerts"]
    exclude_weathers.remove(weather_type)
    params = {
        "lat": lat, "lon": lon, "appid": API_KEY,
        "exclude": ",".join(exclude_weathers),
        "units": "metric",
    }
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None,
                                      partial(requests.get, url, params=params))
    resp.raise_for_status()
    resp_json = resp.json()
    if not resp_json:
        raise ErrorNoWeather
    return resp_json[weather_type]


class WeatherCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.place = "Moscow"
        self.coord = asyncio.run(get_geocode_coord(self.place))

    @commands.command(name="help_bot")
    async def show_help(self, ctx):
        """show this message"""
        commands_descriptions = [(i.name, i.callback.__doc__) for i in self.get_commands()]
        commands_descriptions = [(f"{self.bot.command_prefix}{name}", doc if doc is not None else "")
                                 for name, doc in commands_descriptions]
        commands_descriptions = [f"{name} - {doc}" for name, doc in commands_descriptions]
        help_message = "Commands:\n" + "\n".join(commands_descriptions)
        await ctx.send(help_message)

    @commands.command(name="place")
    async def change_place(self, ctx, place):
        """change forecast place (default is Moscow)"""
        try:
            coord = await get_geocode_coord(place)
        except PlaceNotFound:
            await ctx.send(f"Place {place} not found")
            return
        except requests.exceptions.HTTPError:
            await ctx.send(f"Weather server error")
            return
        self.place = place
        self.coord = coord
        await ctx.send(f"Place changed to {place}")

    @commands.command(name="current")
    async def show_current_weather(self, ctx):
        """show current weather in specified place"""
        raw_weather_data = await get_weather("current", *self.coord)
        msg = get_user_weather_formatted(self.place, raw_weather_data)
        await ctx.send(msg)

    @commands.command(name="forecast")
    async def show_daily_weather(self, ctx, cnt):
        """with number parameter show weather for n days in specified place"""
        raw_weather_data = await get_weather("daily", *self.coord)
        try:
            cnt = int(cnt)
        except ValueError:
            await ctx.send(f"You must specify NUMBER of days for forecast")
            return
        forecast_len = len(raw_weather_data)
        if cnt > len(raw_weather_data):
            await ctx.send(f"Can only show {forecast_len} forecasts.")
        raw_weather_data = raw_weather_data[:cnt]
        msg = "\n".join(get_user_weather_formatted(self.place, i) for i in raw_weather_data)
        await ctx.send(msg)


def main():
    bot = commands.Bot(command_prefix='#!')
    cog = WeatherCog(bot)
    bot.add_cog(cog)
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
