import logging

import pymorphy2
from discord.ext import commands

from bot_token import TOKEN

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
))
logger.addHandler(handler)


class MorphCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.morph = pymorphy2.MorphAnalyzer()

    @commands.command(name="help_bot")
    async def show_help(self, ctx):
        """show this message"""
        commands_descriptions = [(i.name, i.callback.__doc__) for i in self.get_commands()]
        commands_descriptions = [(f"{self.bot.command_prefix}{name}", doc if doc is not None else "")
                                 for name, doc in commands_descriptions]
        commands_descriptions = [f"{name} - {doc}" for name, doc in commands_descriptions]
        help_message = "Commands:\n" + "\n".join(commands_descriptions)
        await ctx.send(help_message)

    @commands.command(name="numerals")
    async def numeral_agreement(self, ctx, word, num):
        """agreement with numerals"""
        word: pymorphy2.analyzer.Parse = self.morph.parse(word)[0]
        try:
            num = int(num)
        except ValueError:
            await ctx.send(f"{num} is not a number")
            return
        agreed_word = word.make_agree_with_number(num)
        await ctx.send(agreed_word.word)

    @commands.command(name="alive")
    async def check_is_alive(self, ctx, word):
        """define alive or not"""
        word: pymorphy2.analyzer.Parse = self.morph.parse(word)[0]
        animacy = word.tag.animacy
        alive = self.morph.parse("живой")[0].normalized
        word = word.inflect({"nomn"})
        alive = alive.inflect({word.tag.gender}).inflect({word.tag.number})
        if animacy == "anim":
            res = f"{word.word} {alive.word}"
        else:
            res = f"{word.word} не {alive.word}"
        await ctx.send(res)

    @commands.command(name="noun")
    async def noun_decline(self, ctx, word, case, number):
        """noun case (nomn, gent, datv, accs, ablt, loct) and number state (sing, plur)"""
        word: pymorphy2.analyzer.Parse = self.morph.parse(word)[0]
        if case not in ("nomn", "gent",
                        "datv", "accs", "ablt", "loct") or number not in ("sing", "plur"):
            await ctx.send(f"Using:\n{self.bot.command_prefix}{self.noun_decline.name}"
                           f" {self.noun_decline.callback.__doc__}")
            return
        word = word.inflect({case, number})
        await ctx.send(word.word)

    @commands.command(name="inf")
    async def inf_state(self, ctx, word):
        """infinitive state"""
        word: pymorphy2.analyzer.Parse = self.morph.parse(word)[0]
        word = word.normal_form
        await ctx.send(word)

    @commands.command(name="morph")
    async def full_morph(self, ctx, word):
        """full morphological analysis"""
        word: pymorphy2.analyzer.Parse = self.morph.parse(word)[0]
        res = word.tag.lat2cyr(word.tag._str)  # noqa
        await ctx.send(res)


def main():
    bot = commands.Bot(command_prefix='#!')
    cog = MorphCog(bot)
    bot.add_cog(cog)
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
