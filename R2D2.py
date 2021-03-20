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
import random
import sys
import json
import requests
from gpiozero import CPUTemperature

description = '''R2D2'''
intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

tk = open('Token Discord.txt', 'r')
TOKEN = tk.read()

tenor_api = open('Tenor API Key.txt', 'r')
TENOR_API_KEY = tenor_api.read()
Limit_Tenor = 1

def search_tenor(term):
    """Searches a Meme on Tenor.com for a given search term"""
    r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (term, TENOR_API_KEY, Limit_Tenor))
    if r.status_code == 200:
        top_gif = json.loads(r.content)
        if 'results' in top_gif:
            return((top_gif['results'][0])['media'][0]['gif']['url'])
        else:
            return('https://tenor.com/view/somethings-not-right-there-regina-mom-theres-something-wrong-there-somethings-wrong-gif-19844156')
        
    else:
        return('https://tenor.com/view/somethings-not-right-there-regina-mom-theres-something-wrong-there-somethings-wrong-gif-19844156')

@bot.event
#starting the bot
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name='Star Wars'))
    

@bot.command()
#Checks if Bot is online and responsing. 
async def up(ctx):
    """Checks if the Bot is running"""
    await ctx.send('awaiting further instructions. Order 66 cannot be executed')


@bot.command()
#Sends the Boom Gif
async def r2d2(ctx):
    """Returns a surprise"""
    await ctx.send('https://tenor.com/view/happy-rocking-r2d2-star-wars-artoo-gif-15352285')
    
@bot.command()
async def ping(ctx):
    """Returns the latency of the bot"""
    #edit = str(ctx.message.created_at - datetime.datetime.utcnow())
    #test = 'Latency is ' +str(int(float(edit.split(':')[2])*1000)) + 'ms'
    now = datetime.datetime.now()
    answer = 'Your Ping to the Bot is ' + str(int(((ctx.message.created_at - now).microseconds)/1000)) + 'ms'
    await ctx.send(answer)

@bot.command()
#test shutdown of the bot and even the Raspberry Pi if active
async def sudo_poweroff(ctx):
    """Shutdown Command of the Bot. Only working for oo_emperor"""
    if ctx.author.id == 484437386575740939:
        await ctx.send('Powering down')
        await call('sudo nohup shutdown -h now', shell=True)
        sys.exit()
    else:
        await ctx.send('Nice Try :joy:')
        
@bot.command()
async def rand(ctx, number):
    """ generates a random number between 1 and you given number"""
    r = random.randint(1, int(number))
    await ctx.send(r)
    
@bot.command()
async def meme(ctx, term):
    """gives you a meme for the search term"""
    back = search_tenor(term)
    await ctx.send(back)
        
@bot.command()
async def temp(ctx):
    """Returns the CPU Temp of R2D2"""
    cpu=CPUTemperature()
    temp = str((int(10*(cpu.temperature)))/10)
    await ctx.send('CPU temperature is ' + temp + '°C')


bot.run(TOKEN)
