import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))

KEYWORDS = [
    "morgen",
    "moin",
    "servus",
    "hallo",
    "abend",
    "schönen tag",
    "schönen abend",
    "schönes wochenende"
]

@client.event
async def on_ready():
    print(f"Bot eingeloggt als {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id != CHANNEL_ID:
        return

    content = message.content.lower()
    if any(keyword in content for keyword in KEYWORDS):
        try:
            await message.add_reaction("🤗")
        except discord.HTTPException:
            pass

client.run(os.getenv("DISCORD_TOKEN"))
