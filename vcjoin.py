import asyncio
import logging
import os

import discord
from discord.ext.native_voice import VoiceClient

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "1575118260515635221" # vc channel id

client = discord.Client()
started = False


async def join(channel):
    voice = await channel.connect(cls=VoiceClient)
    print(f"[+] Joined {channel}")
    return voice


async def keep_alive(channel):
    voice = None
    while True:
        try:
            if voice is None or not voice.is_connected():
                if voice is not None:
                    print("[!] Disconnected, rejoining...")
                    try:
                        await voice.disconnect(force=True)
                    except Exception:
                        pass
                voice = await join(channel)
        except Exception as e:
            print(f"[!] Join failed: {e!r}. Retrying in 30s...")
            voice = None
        await asyncio.sleep(30)


@client.event
async def on_ready():
    global started
    if started:  # on_ready can fire more than once
        return
    started = True
    print(f"[+] Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID) or await client.fetch_channel(CHANNEL_ID)
    client.loop.create_task(keep_alive(channel))


client.run(TOKEN)
