# bot.py
import asyncio
import json
import os
import random

import aiohttp
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
BOT_PREFIX = ("?", "!")

bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(f'{bot.user.name} is connected to the following guild:\n')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to banana-fish channel'
    )


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='huyendtp-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command(name='bitcoin')
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await ctx.send("Bitcoin price is: $" + response['bpi']['USD']['rate'])


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
        
#
# async def list_servers():
#     await bot.wait_until_ready()
#     while not bot.is_closed:
#         print("Current servers:")
#         for server in bot.servers:
#             print(server.name)
#         await asyncio.sleep(600)
# bot.loop.create_task(list_servers())
bot.run(TOKEN)
