from dotenv import dotenv_values
from discord import Client, Intents

class ArchiverBot(Client):
    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "ping":
            await message.channel.send("pong")

def main(discord_api_key):
    intents = Intents.default()
    intents.message_content = True
    client = ArchiverBot(intents=intents)
    client.run(discord_api_key)

if __name__ == "__main__":
    discord_api_key = dotenv_values()["DISCORD_API_KEY"]
    main(discord_api_key)
