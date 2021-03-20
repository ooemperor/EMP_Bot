# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 12:59:20 2021

@author: mikai
"""
import nest_asyncio
nest_asyncio.apply()
import discord
from discord.ext import commands
from subprocess import call
import datetime

description = '''EMP_bot'''
intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

tk = open('Token.txt', 'r')
TOKEN = tk.read()

@bot.event
#starting the bot
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name='Tetris'))
    

@bot.command()
#Checks if Bot is online and responsing. 
async def up(ctx):
    """Checks if the Bot is running"""
    await ctx.send('awaiting further orders ')
    
@bot.command()
#Sends the Boom Gif
async def emp(ctx):
    """Returns a surprise"""
    await ctx.send('https://tenor.com/view/explosion-boom-iron-man-gif-14282225')
    
@bot.command()
async def ping(ctx):
    """Returns the latency of the bot"""
    edit = str(ctx.message.created_at - datetime.datetime.utcnow())
    answer = 'Latency is ' +str(int(float(edit.split(':')[2])*1000)) + 'ms'
    await ctx.send(answer)


@bot.command()
#test shutdown of the bot and even the Raspberry Pi if active
async def sudo_poweroff(ctx):
    """Shutdown Command of the Bot. Only working for oo_emperor"""
    if ctx.author.id == 484437386575740939:
        await ctx.send('Powering down')
        #await call('sudo nohup shutdown -h now', shell=True)
    else:
        await ctx.send('Nice Try :joy:')

    

bot.run(TOKEN)
