from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from flask import json
from responses import get_response
import requests
import json
from keep_alive import keep_alive


def get_quote():
    response =requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


# Load token
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Message FUncitonality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Handling startup for bot
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")

# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Main entry point
def main() -> None:
    client.run(token=TOKEN)

keep_alive()

if __name__ == "__main__":
    main()








