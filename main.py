import os
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask

# --- خادم ويب وهمي للاستضافة على Railway ---
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
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_USER_ID = 1422918463034228757

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user.name}")

@bot.command(name="allow_user")
@commands.has_permissions(administrator=True)
async def allow_user_channels(ctx):
    guild = ctx.guild
    
    target_user = guild.get_member(TARGET_USER_ID)
    if not target_user:
        try:
            target_user = await guild.fetch_member(TARGET_USER_ID)
        except discord.NotFound:
            await ctx.send("❌ لم يتم العثور على هذا الشخص في السيرفر.")
            return

    status_msg = await ctx.send("⏳ جاري تعديل صلاحيات جميع القنوات والأقسام بدون استثناء...")

    # تعديل كافة القنوات والأقسام مهما كان نوعها (صوتية، نصية، إعلانات، فوروم)
    for channel in guild.channels:
        try:
            await channel.set_permissions(
                target_user,
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                connect=True,
                speak=True,
                reason="منح صلاحية الوصول الكاملة بواسطة السكربت"
            )
        except Exception as e:
            print(f"فشل تعديل القناة {channel.name}: {e}")

    await status_msg.edit(content=f"✅ تم منح <@{TARGET_USER_ID}> صلاحية رؤية والتحدث في جميع رومات السيرفر بنجاح!")

# جلب التوكين من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ خطأ: لم يتم العثور على التوكين في متغيرات البيئة!")
