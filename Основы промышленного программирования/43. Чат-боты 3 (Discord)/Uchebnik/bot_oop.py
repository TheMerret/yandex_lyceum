import logging

import discord

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


if __name__ == '__main__':
    client = YLBotClient()
    client.run(TOKEN)
