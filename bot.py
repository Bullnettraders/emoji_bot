import discord
import os
import json

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))
KEYWORDS_FILE = "keywords.json"
KEYWORDS = []

# Keywords laden
def load_keywords():
    global KEYWORDS
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            KEYWORDS = json.load(f)
    else:
        KEYWORDS = []

# Keywords speichern
def save_keywords():
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(KEYWORDS, f, ensure_ascii=False, indent=2)

load_keywords()

@client.event
async def on_ready():
    print(f"Bot online als {client.user}")
    print(f"Aktive Keywords: {KEYWORDS}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.strip().lower()

    if message.channel.id != CHANNEL_ID:
        return

    # Emoji-Reaktion
    if any(word in content for word in KEYWORDS):
        try:
            await message.add_reaction("🤗")
        except discord.HTTPException:
            pass

    # Keyword hinzufügen
    if content.startswith("!addkeyword "):
        new_kw = content[12:].strip()
        if new_kw and new_kw not in KEYWORDS:
            KEYWORDS.append(new_kw)
            save_keywords()
            await message.channel.send(f"✅ Keyword **{new_kw}** hinzugefügt.")
        else:
            await message.channel.send("⚠️ Keyword existiert bereits oder ist leer.")

    # Keyword entfernen
    elif content.startswith("!removekeyword "):
        kw = content[16:].strip()
        if kw in KEYWORDS:
            KEYWORDS.remove(kw)
            save_keywords()
            await message.channel.send(f"❌ Keyword **{kw}** entfernt.")
        else:
            await message.channel.send("⚠️ Keyword existiert nicht.")

    # Keywords anzeigen
    elif content == "!listkeywords":
        if KEYWORDS:
            await message.channel.send("📋 Aktive Keywords:\n" + "\n".join(f"- {kw}" for kw in KEYWORDS))
        else:
            await message.channel.send("🚫 Keine Keywords vorhanden.")

client.run(os.getenv("DISCORD_TOKEN"))
