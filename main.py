import discord
from discord import Guild, app_commands
from discord.ext import commands
from googleapiclient import discovery
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

os.system('cls')

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.typing = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents.all())

API_KEY = os.getenv('API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS database
             (user_id integer, coins interger, diamonds integer)''')
conn.commit()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print(f"Ping: {bot.latency:.2f}ms")
    try:
       synced = await bot.tree.sync()
       print(f"synced {len(synced)} slash command(s)")
    except Exception as e:
        print(e)

@bot.command(name='create_wallet')
async def create_wallet(ctx):
    user_id = ctx.author.id

    c.execute("SELECT * FROM database WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result is not None:
        await ctx.send("You already have a wallet.")
        return

    c.execute("INSERT INTO database (user_id, coins, diamonds) VALUES (?, 0, 0)", (user_id,))
    conn.commit()

    await ctx.send("Wallet created!")

@bot.command(name="wallet")
async def wallet(ctx):
    user_id = ctx.author.id
    c.execute('SELECT coins, diamonds FROM database WHERE usr_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        coins = result[0]
        diamonds = result[1]
        await ctx.send(f'**Wallet**\nCoins: {coins}\nDiamonds: {diamonds}')
    else:
        await ctx.send('You have not created a wallet yet.')
        

bot.run(BOT_TOKEN)
