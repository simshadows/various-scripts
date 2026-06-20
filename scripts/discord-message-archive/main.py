#   file: main.py
# author: simshadows <contact@simshadows.com>
#
# Logs onto a Discord bot, archives all messages it can find to the `out` directory,
# and exits.
#
# The output files are meant to be imported into Obsidian. You should be able to edit
# this script to output in whatever format you want.

import re
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import dotenv_values
from discord import (
    Client,
    Intents,
    TextChannel,
)

ENCODING = "utf-8"

root_path = Path(__file__).resolve().parent
out_path = root_path / "out"

def getenv__discord_api_key():
    return dotenv_values()["DISCORD_API_KEY"]
def getenv__zoneinfo_region():
    return ZoneInfo(dotenv_values()["ZONEINFO_REGION"])

def filter_string(s):
    return re.sub(r"[^a-zA-Z0-9]", "", s)

def to_local_timezone_str(dt, zoneinfo_region):
    if not dt:
        return None
    local = dt.astimezone(zoneinfo_region)
    return local.isoformat(timespec="microseconds")

class ArchiverBot(Client):
    async def on_ready(self):
        print("Logged on as", self.user)
        try:
            await self.do_archive()
        finally:
            await self.close()

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "ping":
            await message.channel.send("pong")

    async def do_archive(self):
        print("= Starting archiving process...")
        messages = {}
        for guild in self.guilds:
            consolidated_messages = []
            messages[guild.id] = consolidated_messages
            await self.do_archive_guild(guild, consolidated_messages)

        folder_path = out_path / "consolidated.json"
        with open(folder_path, "w", encoding=ENCODING) as f:
            f.write(json.dumps(messages))

        print("Done!")

    async def do_archive_guild(self, guild, consolidated_messages):
        print(f"== Found guild: {guild.name} - {guild.id}")
        folder_name = f"{guild.id}_" + filter_string(guild.name)
        folder_path = out_path / folder_name
        # mkdir() will throw error if folder already exists.
        # This is intentional to avoid overwriting data.
        folder_path.mkdir(parents=True, exist_ok=False)
        for channel in guild.channels:
            await self.do_archive_channel(channel, folder_path, consolidated_messages)

    async def do_archive_channel(self, channel, guild_path, consolidated_messages):
        def print_found(category_str):
            print(f"=== Found {category_str} channel: {channel.name} - {channel.id}")

        folder_name = f"{channel.id}_" + filter_string(channel.name)
        folder_path = out_path / folder_name
        attachments_path = folder_path / "_attachments"
        if isinstance(channel, TextChannel):
            print_found("text")
            # Again, mkdir() will throw error if folder already exists.
            folder_path.mkdir(parents=True, exist_ok=False)
            attachments_path.mkdir(parents=True, exist_ok=False)
            async for msg in channel.history(limit=None, before=None, after=None, around=None, oldest_first=True):
                await self.add_to_archive_file(msg, folder_path, attachments_path, channel, consolidated_messages)
        else:
            print_found("other")
            print("Channel type not supported. Skipping.")

    async def add_to_archive_file(self, msg, channel_path, attachments_path, channel, consolidated_messages):
        zoneinfo_region = getenv__zoneinfo_region()

        created_at = msg.created_at.astimezone(zoneinfo_region)
        edited_at = msg.edited_at.astimezone(zoneinfo_region) if msg.edited_at else None

        buf = [f"discord #{filter_string(channel.name)}"]
        if created_at:
            buf.append(" " + created_at.isoformat())
        if msg.author.name:
            buf.append(" " + str(msg.author.name))
        if msg.author.id:
            buf.append(" " + str(msg.author.id))
        if edited_at:
            buf.append(f" (edited {edited_at.isoformat()})")
        if msg.content:
            buf.append(f"\n{msg.content}")
        for i, attachment in enumerate(msg.attachments):
            attachment_filename = f"discord_{created_at.isoformat()[:19]}_{i}_{attachment.filename}"
            attachment_filename = re.sub(r"[^a-zA-Z0-9-_.]", "", attachment_filename).lower()
            try:
                await attachment.save(attachments_path / attachment_filename)
                buf.append(f"\n![[{attachment_filename}]]")
            except:
                buf.append(f"\n(((ATTACHMENT DOWNLOAD FAILED. Filename: `{attachment.filename}`)))")

        archive_filename = f"{msg.created_at.isoformat()[:10]}.md"
        archive_path = channel_path / archive_filename
        if archive_path.is_file():
            extra_space = True
        else:
            extra_space = False

        s = "".join(buf)

        consolidated_messages.append({
            "created_at": msg.created_at.isoformat(),
            "created_at_local": created_at.isoformat(),
            "content": s,
        })

        with open(archive_path, "a", encoding=ENCODING) as f:
            if extra_space:
                f.write("\n\n")
            f.write(s)
            print(s)

def main():
    intents = Intents.default()
    intents.message_content = True
    client = ArchiverBot(intents=intents)
    client.run(getenv__discord_api_key())

if __name__ == "__main__":
    main()
