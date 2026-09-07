import os
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask

# --- خادم ويب وهمي للاستضافة ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run_web, daemon=True).start()

# --- إعدادات البوت ---
intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user.name}")
    print("⏳ جاري الإرسال في جميع الرومات النصية بكل السيرفرات المتواجد بها البوت...")

    # المرور على جميع السيرفرات التي يتواجد بها البوت
    for guild in bot.guilds:
        # المرور على جميع الرومات النصية في السيرفر
        for channel in guild.text_channels:
            try:
                await channel.send("اطردني اطردني")
                print(f"✅ تم الإرسال في القناة: {channel.name} ({guild.name})")
            except Exception as e:
                print(f"❌ فشل الإرسال في القناة {channel.name}: {e}")

    print("🎉 تم الانتهاء من الإرسال في جميع الرومات!")

# جلب التوكين من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ خطأ: لم يتم العثور على التوكين في متغيرات البيئة!")
