# Delete messages from certain users based on filters without a bot or banning them
# uninstall discord.py first or run this in a venv and only then install requirements.txt
import discord
from datetime import datetime
import json
import inotify.adapters
import threading
import os

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("You need to set the TOKEN env variable in order to run this selfbot")
    exit(1)

allow_filters = json.load(open("allow.json", "r"))
deny_filters = json.load(open("deny.json", "r"))


# true = pass, false = filtered
def filter_message(message):
    if message.guild is None:
        return True  # we don't care about messages in DMs

    for allow in allow_filters:
        if allow["guild"] == str(message.guild.id) or allow["guild"] == "*":
            if allow["user"] == str(message.author.id) or allow["user"] == "*":
                if (
                    allow["channel"] == str(message.channel.id)
                    or allow["channel"] == "*"
                ):
                    return True

    for deny in deny_filters:
        if deny["guild"] == str(
            message.guild.id
        ):  # guild cannot be "*" for safety reasons
            if deny["user"] == str(message.author.id) or deny["user"] == "*":
                if deny["channel"] == str(message.channel.id) or deny["channel"] == "*":
                    return False

    return True


class MessageDeleterClient(discord.Client):
    async def on_ready(self):
        print("Logged in as", self.user)

    async def on_message(self, message):
        if not filter_message(message):
            await message.delete()
            print(
                f"Deleted message from {message.author.name} in {message.guild.name}/{message.channel.name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            print(
                f"Message was (truncated): {message.content[:100]}"
                + ("..." if len(message.content) > 100 else "")
            )


def updater():
    global allow_filters
    global deny_filters
    i = inotify.adapters.Inotify()

    i.add_watch(".")

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event  # type: ignore

        if "IN_CLOSE_WRITE" in type_names:
            if filename == "allow.json":
                allow_filters = json.load(open(filename, "r"))
                print("Allow filters updated")
            if filename == "deny.json":
                deny_filters = json.load(open(filename, "r"))
                print("Deny filters updated")


threading.Thread(target=updater).start()

client = MessageDeleterClient()
client.run(TOKEN)
