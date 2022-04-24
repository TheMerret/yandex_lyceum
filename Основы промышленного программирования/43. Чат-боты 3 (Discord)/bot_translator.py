import asyncio
import logging
import os
from functools import partial
import re

import requests
from discord.ext import commands

from bot_token import TOKEN

URL = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
API_KEY = os.getenv("API_KEY")
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
}


logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
))
logger.addHandler(handler)


class LangPairMissMatch(Exception):
    """translation text don't match with lang pair"""


async def make_translation(text, lang_from="ru", lang_to="en"):
    params = {
        "langpair": f"{lang_from}|{lang_to}",
        "q": text,
    }
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None,
                                      partial(requests.get, URL, params=params, headers=HEADERS))
    resp.raise_for_status()
    resp_json = resp.json()
    status_code = resp_json["responseStatus"]
    status_code = 200 if status_code is None else int(status_code)
    resp.status_code = status_code
    reason = resp_json["responseDetails"]
    resp.reason = reason
    resp.raise_for_status()
    response_data = resp_json["responseData"]
    translation = response_data["translatedText"]
    if translation == "TXT":
        raise LangPairMissMatch()
    return translation


class TranslatorCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lang_pair = ("en", "ru")

    @commands.command(name="help_bot")
    async def show_help(self, ctx):
        """show this message"""
        commands_descriptions = [(i.name, i.callback.__doc__) for i in self.get_commands()]
        commands_descriptions = [(f"{self.bot.command_prefix}{name}", doc if doc is not None else "")
                                 for name, doc in commands_descriptions]
        commands_descriptions = [f"{name} - {doc}" for name, doc in commands_descriptions]
        help_message = "Commands:\n" + "\n".join(commands_descriptions)
        await ctx.send(help_message)

    @commands.command(name="set_lang")
    async def set_lang(self, ctx, lang_pair):
        """with lang pair (en-pl) changes languages of translation and direction"""
        LANG_PAIR_PATTER = re.compile(r"(\w\w)-(\w\w)")
        match = LANG_PAIR_PATTER.fullmatch(lang_pair)
        if match is None:
            await ctx.send(f"Using:\n{self.bot.command_prefix}{self.set_lang.name} "
                           f" {self.set_lang.callback.__doc__}")
            return
        self.lang_pair = match.groups()
        await ctx.send(f"Type '{self.bot.command_prefix}{self.translate.name}'"
                       f" and text for translate")

    @commands.command(name="text")
    async def translate(self, ctx, *text):
        """with text will translate this text according to lang pair"""
        text = " ".join(text)
        try:
            translation = await make_translation(text, *self.lang_pair)
        except LangPairMissMatch:
            await ctx.send(f"Error: lang pair miss match")
            return
        except requests.exceptions.HTTPError as e:
            await ctx.send(f"Error: {e.args[0].split('.')[0].lower()}")
            return
        await ctx.send(translation)


def main():
    bot = commands.Bot(command_prefix='!!')
    cog = TranslatorCog(bot)
    bot.add_cog(cog)
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
