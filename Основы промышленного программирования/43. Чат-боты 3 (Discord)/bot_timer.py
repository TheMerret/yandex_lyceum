import asyncio
import logging
import re

import discord
from discord import Message

from bot_token import TOKEN

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
))
logger.addHandler(handler)


class BotClient(discord.Client):

    async def on_ready(self):
        logger.info(f"{self.user} подключен!")
        for guild in self.guilds:
            logger.info(
                f"{self.user} подключился к чату: {guild.name}(id: {guild.id})"
            )

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        SET_TIMER_PATTERN = re.compile(r"set_timer in (\d+) hours (\d+) minutes")
        match = SET_TIMER_PATTERN.match(message.content)
        if match is not None:
            hours, minutes = map(int, match.groups())
            seconds = hours * 3600 + minutes * 60
            await message.channel.send(f"The timer should start in {hours} hours"
                               f" and {minutes} minutes.")
            await asyncio.sleep(seconds)
            await message.channel.send("⏰ Time X hac come!")
        else:
            await self.send_help(message.channel)

    async def send_help(self, channel):
        await channel.send("Using: set_timer in 0 hours 1 minutes")


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True
    client = BotClient(intents=intents)
    client.run(TOKEN)
