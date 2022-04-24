import logging
import random

import discord
from discord import Message

from bot_token import TOKEN

EMOJIS = ['☀️', '☝️', '☹️', '☺️', '✅', '✋', '✌️', '✔️', '✨', '❗', '❣️', '❤️', '⭐', '🌈', '🌟', '🌷',
          '🌸', '🌹', '🌺', '🍀', '🎉', '🎊', '🎶', '🏃', '👀', '👇', '👉', '👊', '👌', '👍', '👏',
          '💃', '💋', '💐', '💔', '💕', '💖', '💘', '💞', '💥', '💦', '💪', '💯', '🔥', '😀', '😁',
          '😂', '😃', '😄', '😅', '😆', '😇', '😈', '😉', '😊', '😋', '😌', '😍', '😎', '😏', '😑',
          '😒', '😓', '😔', '😕', '😘', '😚', '😜', '😝', '😞', '😠', '😡', '😢', '😣', '😥', '😩',
          '😪', '😬', '😭', '😱', '😳', '😴', '😻', '🙂', '🙃', '🙄', '🙈', '🙋', '🙌', '🙏', '🤔',
          '🤗', '🤘', '🤣', '🤤', '🤦', '🤩', '🤪', '🤭', '🤷']


logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
))
logger.addHandler(handler)


class BotClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_emojis = EMOJIS.copy()
        random.shuffle(self.game_emojis)
        self.user_score = 0
        self.bot_score = 0

    def init_game(self):
        self.game_emojis = EMOJIS.copy()
        random.shuffle(self.game_emojis)
        self.user_score = 0
        self.bot_score = 0

    async def on_ready(self):
        logger.info(f"{self.user} подключен!")
        for guild in self.guilds:
            logger.info(
                f"{self.user} подключился к чату: {guild.name}(id: {guild.id})"
            )

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        if message.content.startswith("/help"):
            await self.send_help(message.channel)
            return
        if message.content.startswith("/stop"):
            msg = "Stopping the game..."
            await self.end_game(msg, message.channel)
            return
        try:
            number = int(message.content)
        except ValueError:
            await self.send_help(message.channel)
            return
        try:
            user_emoji = self.get_game_emoji(number)
            bot_emoji = self.get_game_emoji(random.randint(0, len(self.game_emojis)))
        except (IndexError, ZeroDivisionError):
            msg = "Emoticons are over"
            await self.end_game(msg, message.channel)
            return
        if user_emoji > bot_emoji:
            self.user_score += 1
        else:
            self.bot_score += 1
        msg = (f"Your emoji {user_emoji}\n"
               f"Bot emoji {bot_emoji}\n"
               f"Score: You {self.user_score} - Bot {self.bot_score}")
        random.shuffle(self.game_emojis)
        await message.channel.send(msg)

    def get_game_emoji(self, ind):
        ind = ind % len(self.game_emojis)
        emoji = self.game_emojis.pop(ind)
        return emoji

    async def end_game(self, msg, channel):
        if self.bot_score > self.user_score:
            winner = "bot win"
        elif self.user_score > self.bot_score:
            winner = "you win"
        else:
            winner = "toe"
        res = f"{msg.capitalize()}\n" \
              f"Score: You {self.user_score} - Bot {self.bot_score}\n" \
              f"{winner.capitalize()}!"
        self.init_game()
        await channel.send(res)

    async def send_help(self, channel):
        await channel.send("Назовите номер смайла (любой)."
                           " Затем бот выберет свое число."
                           " Чей смайлик окажется далше в алфавите, тот и ваиграл раунд."
                           " После каждого раунда смайлы перемешиваются")


def main():
    client = BotClient()
    client.run(TOKEN)


if __name__ == '__main__':
    main()
