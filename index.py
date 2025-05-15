from telethon import TelegramClient, events, Button
import json
import random
import asyncio
import os
from PIL import Image, ImageDraw, ImageFont
import pytz
from datetime import datetime

# ------------------ CONFIGURATION ------------------
API_ID = 23350184                # Your API ID
API_HASH = '41f0c2a157268e158f91ab7d59f4fc19'      # Your API Hash
BOT_TOKEN = '8073314116:AAFfxiLVPoo8s43Ytd_U4NDvNL4MVukSG7U'
CHAT_ID = -1002504867718    # Your group chat ID
WELCOME_IMAGE = '2.png'         # Welcome image path

# ------------------ IMAGE ANNOTATION SETTINGS ------------------
FONT_PATH = 'arialbd.ttf'       # Bold Arial font
FONT_SIZE = 40
TEXT_OFFSET_X = -60
TEXT_OFFSET_Y = 135
TEXT_POSITIONS = [
    (80 + TEXT_OFFSET_X, 120 + TEXT_OFFSET_Y),
    (80 + TEXT_OFFSET_X, 220 + TEXT_OFFSET_Y),
    (80 + TEXT_OFFSET_X, 320 + TEXT_OFFSET_Y),
    (80 + TEXT_OFFSET_X, 420 + TEXT_OFFSET_Y),
    (80 + TEXT_OFFSET_X, 520 + TEXT_OFFSET_Y),
    (80 + TEXT_OFFSET_X, 620 + TEXT_OFFSET_Y)
]

# ------------------ IMAGE FUNCTIONS ------------------

def load_games():
    with open('game.json', 'r', encoding='utf-8') as f:
        return json.load(f)["games"]


def get_random_games(game_list):
    return random.sample(game_list, 6)


def draw_on_image(games):
    base_image = Image.open('1.png').convert('RGBA')
    draw = ImageDraw.Draw(base_image)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    for game, pos in zip(games, TEXT_POSITIONS):
        draw.text(pos, game, font=font, fill=(255, 255, 255, 255))

    output_path = 'output.png'
    base_image.save(output_path)
    return output_path

# ------------------ WELCOME HANDLER ------------------
async def welcome_new(event):
    if not (event.user_joined or event.user_added):
        return

    user = await event.get_user()
    chat = await event.get_chat()
    group_title = getattr(chat, 'title', 'Grubumuz')
    username = f"@{user.username}" if user.username else '—'
    first_name = user.first_name or '—'
    user_id = user.id

    tz = pytz.timezone('Europe/Istanbul')
    join_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    caption = f"""art analiz

𝚂𝙴𝚅𝙶𝙸‌𝙻𝙸‌ • {group_title}
  𝙶𝚁𝚄𝙱𝚄𝙼𝚄𝚉𝙰 𝙷𝙾𝚂‌𝙶𝙴𝙻𝙳𝙸‌𝙽 ⚜️
▬▬▬▬▬๑۩۞۩๑▬▬▬▬▬▬
╔════════════════╗
║•●۞ • {username}
║•●۞ • {first_name}
║•●۞ • {user_id}
║•●۞ • {join_time}
╚════════════════╝"""

    # Send welcome image with caption
    await event.client.send_file(event.chat_id, WELCOME_IMAGE, caption=caption)

# ------------------ PERIODIC ANALYSIS IMAGE TASK ------------------
async def periodic_image():
    while True:
        games = load_games()
        selected = get_random_games(games)
        output = draw_on_image(selected)

        buttons = [
            Button.url("🌐 Siteye Git", "https://heylink.me/G%C3%BCvenilirsitelerartslotanaliz"),
            Button.url("👤 Kurucu", "https://t.me/artkurucu")
        ]

        await client.send_file(
            CHAT_ID,
            output,
            caption="🎯 Yeni analiz görseli yayında!",
            buttons=[buttons]
        )

        os.remove(output)
        await asyncio.sleep(3600)  # 1 hours

# ------------------ PERIODIC PROMO MESSAGE TASK ------------------
async def periodic_promo():
    while True:
        # Send promotional text with emoji and button
        buttons = [Button.url("🌐 Siteye Git", "https://heylink.me/G%C3%BCvenilirsitelerartslotanaliz")]
        promo_text = "🎁 Kazanmak için gel! 🎉"
        await client.send_message(
            CHAT_ID,
            promo_text,
            buttons=[buttons]
        )
        await asyncio.sleep(1800)  # 30 minutes

# ------------------ START BOT ------------------
if __name__ == '__main__':
    client = TelegramClient('session', API_ID, API_HASH)
    client.start(bot_token=BOT_TOKEN)

    # Register event handlers
    client.add_event_handler(welcome_new, events.ChatAction)

    # Start periodic tasks
    client.loop.create_task(periodic_image())
    client.loop.create_task(periodic_promo())

    print('Bot başladı: yeni üyeleri karşılama, periyodik analiz ve promo mesajlarini bekliyorum...')
    client.run_until_disconnected()