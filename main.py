import discord
from discord import Guild, app_commands
from discord.ext import commands
from googleapiclient import discovery
import requests
import os
from dotenv import load_dotenv

load_dotenv()

os.system('cls')

intents = discord.Intents.default()
intents.members = False
intents.messages = True
intents.typing = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

API_KEY = os.getenv('API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')


client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)


bot.toxicity_threshold = threshold = 0.8
bot.log_channel = channel_id = None
theme_color = '#ff0000'
ping = bot.latency
totalUsres = len(bot.guilds)

async def check_toxicity(message):
    if message.author == bot.user:
        return
    if message.content == "":
        return

    analyze_request = {
        'comment': {'text': message.content},
        'requestedAttributes': {'TOXICITY': {}},
	'languages': ['en']
    }

    response = client.comments().analyze(body=analyze_request).execute()
    toxicity = response['attributeScores']['TOXICITY']['summaryScore']['value']
    language = response['detectedLanguages'][0]

    if toxicity >= threshold:
        await message.delete()

        if bot.log_channel is not None:
            embed = discord.Embed(title='**Message Deleted for Toxicity**', description=f"Text by: `{message.author.name} ( {message.author.id} )` in `{message.guild.name}` was deleted for toxicity (`{toxicity*100:.2f}%`)\nMessage Content: `{message.content}`\nLanguage Detected: `{language}`", color=0xff0000)
            embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
            await channel_id.send(embed=embed)

        try:
            embed = discord.Embed(title='**Message Deleted for Toxicity**', description=f"Your message in `{message.guild.name}` was deleted for toxicity (`{toxicity*100:.2f}%`)\nMessage Content: `{message.content}`\nLanguage Detected: `{language}`", color=0xff0000)
            embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
            await message.author.send(embed=embed)
        except discord.errors.Forbidden:
            pass

@bot.command(name='memberCount')
@commands.has_permissions(administrator=True)
async def memberCount(ctx):
    total_members = 0
    for guild in bot.guilds:
        total_members += guild.member_count
    await ctx.send(f"{total_members}")
    return total_members


# ON READY
@bot.event
async def on_ready():
    
    total_members = 0
    for guild in bot.guilds:
        total_members += guild.member_count

    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print(f"Ping: {bot.latency:.2f}ms")
    try:
       synced = await bot.tree.sync()
       print(f"synced {len(synced)} slash command(s)")
    except Exception as e:
       print(e)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{total_members} People"))

# MAIN COMMAND
@bot.event
async def on_message(message):
    await check_toxicity(message)
    await bot.process_commands(message)


@bot.command()
@commands.has_permissions(administrator=True)
async def setthreshold(ctx, threshold: float):
    if 0 < threshold < 1:
        bot.toxicity_threshold = threshold
        await ctx.send(f"Toxicity threshold set to {threshold}")
    else:
        await ctx.send("Threshold must be between 0 and 1")


@bot.command()
@commands.has_permissions(administrator=True)
async def setlogchannel(ctx, channel: discord.TextChannel):
    bot.log_channel = channel
    await ctx.send(f"Log channel set to {channel.mention}")

@bot.tree.command(name="setthreshold", description="configure threshold value")
@discord.app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(value = "Threshold value between 0-1 [Default = 0.8]")
async def setthreshold(interaction: discord.interactions, value: float):
    if 0 < value < 1:
        bot.toxicity_threshold = value
        threshold = value
        embed=discord.Embed(title="**DONE** <:done:1127647334944219186>", description=f"**Toxicity threshold set to {threshold}**", COLOUR=0Xff000)
        await interaction.response.send_message(embed=embed,ephemeral=True)
    else:
        embed=discord.Embed(title="**ERROR <:error:1127655083631444019>**", description="**Threshold must be between 0 and 1**\nE.g: set threshold to 0.75 for 75%", colour=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)


    
@bot.tree.command(name="status", description="see bot settings")
async def status(interaction: discord.interactions):

    total_members = 0
    for guild in bot.guilds:
        total_members += guild.member_count

    embed = discord.Embed(title='**Bot Status**', description="Get basic info about bot and bot setings in this server", colour=0xff0000)
    embed.add_field(name="**Threshold value**", value=f"{bot.toxicity_threshold} ({bot.toxicity_threshold*100}%)")
    embed.add_field(name="**Log Channel**", value=f"{bot.log_channel}")
    embed.add_field(name="**Total Users**", value=f"{total_members}")
    embed.add_field(name="**Ping**", value=f"{bot.latency:.2f}ms")

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="help", description="Get basic info about bot and get started.")
async def help(interaction: discord.interactions):
    embed = discord.Embed(title="**Get some HELP**", description=f"**About de.tox**:Don't let toxicity spread anymore in your server. This bot detects toxicity of a message send by users and detele them.This AI integrated bot works with the API by Google .This bot delete the toxic messages.\n\n\n**Get Started**: -Use `/setthreshold` to set minimum value to for toxicity.\n-Use `/setlogchannel` to set channel where bot logs will be sent.\n\n\n**Website**: https://aviralansh.github.io/detox.github.io/", colour=0xff0000)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="ping", description="Get current ping for bot")
async def ping(interaction: discord.interactions):
    embed = discord.Embed(title=f"ping: {bot.latency:.2f}ms", color=0xff0000)
    await interaction.response.send_message(embed=embed,)

    
@bot.tree.command(name="setlogchannel", description="configure log channel")
@discord.app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(value = "Set Log channel for bot logs [Default = None]")
async def setlogchannel(interaction: discord.interactions, value: discord.TextChannel):
        bot.log_channel = value
        embed=discord.Embed(title=f"**DONE** <:done:1127647334944219186>", description=f"Log channel was set to {bot.log_channel}", colour=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="set", description="set config values of bot")
@discord.app_commands.checks.has_permissions(administrator=True)
async def set(interaction: discord.interactions, channel: discord.TextChannel, threshold: float):
        channel_id = channel
        embed = discord.Embed(title="**Server Config**", description=f"Mod Log Channel: `<#{channel_id}>`\nThreshold value: {threshold} ({threshold*100})", colour=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)



bot.run(BOT_TOKEN)
