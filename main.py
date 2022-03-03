#! /usr/bin/python3
# -*- conding: UTF-8 -*-

import discord
from discord.ext import commands
import traceback
import sys
import aiosqlite
import os
import json
import datetime
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('config/.env'))

def get_prefix(bot, message):
    with open("config/prefixes.json", "r") as f:
        prefixes = json.load(f)

    try:
        pre = prefixes[str(message.guild.id)]
    except:
        prefixes[str(message.guild.id)] = "!"
        with open("config/prefixes.json", "w") as f:
            json.dump(prefixes, f)
        pre = prefixes[str(message.guild.id)]
    return pre

bot = commands.Bot(command_prefix= get_prefix, intents = discord.Intents.all())
bot.remove_command('help')

async def find_prefix():
    guild = bot.get_guild(int(os.environ['GUILD_ID']))

    with open('config/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    try:
        pre = prefixes[str(guild.id)]
    except:
        prefixes[str(guild.id)] = "!"
        with open("config/prefixes.json", "w") as f:
            json.dump(prefixes, f)
        pre = prefixes[str(guild.id)]

    print(f"Logged in as {bot.user}")
    return await bot.change_presence(activity= discord.Game(name= f"{pre}help"))

@bot.event
async def on_ready():

    main = await aiosqlite.connect('config/main.sqlite')
    cursor = await main.cursor()

    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS welcome(
            guild_id TEXT,
            channel_id TEXT,
            msg TEXT
        )
    ''')
    await main.commit()

    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS leave(
            guild_id TEXT,
            channel_id TEXT,
            msg TEXT
        )
    ''')
    await main.commit()

    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS setup_admin(
            guild_id INTEGER,
            channel_id INTEGER,
            channel_name TEXT,
            category_id INTEGER
        )
    ''')
    await main.commit()

    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS setup_channel(
            guild_id INTEGER,
            channel_id INTEGER,
            channel_name TEXT
        )
    ''')
    await main.commit()

    await cursor.close()
    await main.close()

    await find_prefix()

@bot.event
async def on_guild_join(guild):

    with open("config/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "!"

    with open("config/prefixes.json", "w") as f:
        json.dump(prefixes,f)


@bot.command()
async def show_prefix(ctx):
    with open("config/prefixes.json", "r") as f:
        prefixes = json.load(f)

    pre = prefixes[str(ctx.guild.id)]
    
    contexte = ctx.channel

    embed = discord.Embed(
        colour = 0xE67D2F,
        title = f"Mon prefixe pour ce serveur est '{pre}'"
    )
    embed.add_field(name="Ma commande pour changer mon prefixe est :", value=f"{pre}change_prefix <prefixe>", inline=True)
    embed.set_thumbnail(url= contexte.guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.channel.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator = True)
async def change_prefix(ctx, prefix):
    with open("config/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("config/prefixes.json", "w") as f:
        json.dump(prefixes,f)

    embed = discord.Embed(
        colour = 0xE67D2F
    )
    embed.add_field(name="Préfixe", value=f"Mon prefixe pour ce serveur à été modifié par ``{prefix}``", inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    return await bot.change_presence(activity= discord.Game(name= f"{prefix}help"))


initial_extensions = [
    'cogs.cog_aahelp',
    'cogs.cog_error',
    'cogs.cog_log',
    'cogs.cog_setup_log'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}", file=sys.stderr)
            traceback.print_exc()

bot.run(os.environ['TOKEN'])