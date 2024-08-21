import asyncio
import os

from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputUser, Channel, InputChannel

# Your API credentials
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)

# List of usernames to add
user_list = ['username1', 'username2', 'username3']

# Target group/channel username or ID
target_group = 'https://t.me/your_group_link'  # or use the group ID

# Throttle delay in seconds
throttle_delay = 60


async def main():
    await client.connect()

    # Get and prepare the target entity
    target_entity = await client.get_entity(target_group)
    if isinstance(target_entity, Channel):
        target_entity = InputChannel(target_entity.id, target_entity.access_hash)
    else:
        print("Target group/channel not found or invalid.")
        return

    for username in user_list:
        try:
            user = await client.get_entity(username)
            if user.bot:
                print(f"Cannot add bots: {username}")
                continue
            user_entity = InputUser(user.id, user.access_hash)
            await client(InviteToChannelRequest(channel=target_entity, users=[user_entity]))
            print(f"Successfully added {username}")

            # Throttle to respect Telegram's rate limits
            await asyncio.sleep(throttle_delay)

        except FloodWaitError as e:
            print(f"Flood wait error. Sleeping for {e.seconds} seconds.")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Failed to add {username}: {e}")


async def run():
    async with client:
        await main()


# Run the script
asyncio.run(run())
