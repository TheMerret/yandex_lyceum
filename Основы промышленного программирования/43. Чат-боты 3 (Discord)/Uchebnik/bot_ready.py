import discord

from bot_token import TOKEN

client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} подключен!")
    for guild in client.guilds:
        print(
            f"{client.user} подключился к чату:\n"
            f"{guild.name}(id: {guild.id})"
        )

if __name__ == '__main__':
    client.run(TOKEN)
