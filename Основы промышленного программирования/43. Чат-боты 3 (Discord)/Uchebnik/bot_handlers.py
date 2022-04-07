import logging

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


class YLBotClient(discord.Client):

    async def on_ready(self):
        logger.info(f"{self.user} подключен!")
        for guild in self.guilds:
            logger.info(
                f"{self.user} подключился к чату: {guild.name}(id: {guild.id})"
            )

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f"Привет, {member.name}"
        )

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        elif "привет" in message.content.lower():
            await message.channel.send("тебе тоже привет)")
        await message.channel.send("Спасибо за сообщение")


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True
    client = YLBotClient(intents=intents)
    client.run(TOKEN)
