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
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user.name}")

@bot.command(name="spam")
@commands.has_permissions(administrator=True)
async def spam_channels(ctx):
    await ctx.send("⏳ جاري إرسال الرسالة في كافة الرومات النصية...")

    # المرور على جميع قنوات السيرفر النصية
    for channel in ctx.guild.text_channels:
        try:
            await channel.send("اطردني اطردني")
        except Exception as e:
            print(f"فشل الإرسال في القناة {channel.name}: {e}")

    await ctx.send("✅ تم إرسال الرسالة في جميع الرومات المتاحة!")

# جلب التوكين من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ خطأ: لم يتم العثور على التوكين في متغيرات البيئة!")
