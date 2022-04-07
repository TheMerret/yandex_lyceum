import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

import discord
from discord import Message, File
import requests

from bot_token import TOKEN

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
))
logger.addHandler(handler)


def get_message_type(message):
    if any(i in message for i in ["пес", "собака", "собачка"]):
        return "dog"
    elif any(i in message for i in ["кошка", "кот"]):
        return "cat"
    else:
        return None


async def get_animal_image_data(message):
    message_type = get_message_type(message)
    if message_type == "dog":
        url = "https://dog.ceo/api/breeds/image/random"
        getter = (lambda x: x["message"])
    elif message_type == "cat":
        url = "https://api.thecatapi.com/v1/images/search"
        getter = (lambda x: x[0]["url"])
    else:
        return
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=16) as executor:
        resp = await loop.run_in_executor(executor, requests.get, url)
        resp = resp.json()
        url = getter(resp)
    return url


class BotClient(discord.Client):

    async def on_ready(self):
        logger.info(f"{self.user} подключен! Котики (песики) на готове.")
        for guild in self.guilds:
            logger.info(
                f"{self.user} подключился к чату: {guild.name}(id: {guild.id})"
            )

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        res = await get_animal_image_data(message.content)
        if res is None:
            await message.channel.send("есть что по делу?")
            return
        url = res
        await message.channel.send(url)
        logger.info("Картинка отправлена")


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True
    client = BotClient(intents=intents)
    client.run(TOKEN)
