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
from pythonping import ping

description = '''R2D2'''
intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

tk = open('Token Discord.txt', 'r')
TOKEN = tk.read()

tenor_api = open('Tenor API Key.txt', 'r')
TENOR_API_KEY = tenor_api.read()
Limit_Tenor = 1

Started = datetime.datetime.now()


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

def google():
    info = str(ping('8.8.8.8'))
    data = info.split()
    back = (data[6] +' '+ data[13] +' '+ data[20] +' '+ data[27])
    return(back)

def warzone(username):
    url = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone/" + replace(username)+"/battle"
    
    wz = open('Warzone API Key.txt', 'r')
    warzone_API_key = wz.read()
    
    headers = {
    'x-rapidapi-key': warzone_API_key,
    'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.content)
        return((int(1000*(data['br']['kdRatio'])))/1000)
    else: 
        return('404')
    
def replace(input):
    output = input.replace('#', '%23')
    return(output)

def check_userlist(username):
    f = open('userlist.json')
    userlist = json.load(f)
    if username in userlist.keys():
        return(userlist[username])
    else:
        return('404')

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
async def botping(ctx):
    """Returns the latency of the bot"""
    #edit = str(ctx.message.created_at - datetime.datetime.utcnow())
    #test = 'Latency is ' +str(int(float(edit.split(':')[2])*1000)) + 'ms'
    now = datetime.datetime.utcnow()
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
async def meme(ctx, *, term):
    """gives you a meme for the search term"""
    back = search_tenor(term)
    await ctx.send(back)
 
     
@bot.command()
async def temp(ctx):
    """Returns the CPU Temp of R2D2"""
    cpu=CPUTemperature()
    temp = str((int(10*(cpu.temperature)))/10)
    await ctx.send('CPU temperature is ' + temp + '°C')
    
@bot.command()
async def stats(ctx):
    """Returns the actual stats of the bot/raspberry in a privat message"""
    user = ctx.author
    cpu=CPUTemperature()
    temp = str((int(10*(cpu.temperature)))/10)
    time = google()
    now = datetime.datetime.utcnow()
    botlatency = 'Your Ping to the Bot is ' + str(int(((ctx.message.created_at - now).microseconds)/1000)) + 'ms'
    await user.send(temp + '°C')
    await user.send('Running since: ' + Started.strftime("%d %B %Y, %H:%M"))
    await user.send('Latencys are: '+ time)
    await user.send(botlatency)
    
@bot.command()
async def latency(ctx):
    """Bot tells you how much Latency it has at the moment to google"""
    time = google()
    await ctx.send('Latencys are: '+ time)
    
@bot.command()
async def kd(ctx):
    """Returns the K/D in Warzone"""
    username = check_userlist(str(ctx.author))
    if username == '404':
        await ctx.send('User not in Userlist. Use !add to add the user to the Userlist')
        await ctx.send(ctx.author)
    else:
        KD = warzone(username)
        await ctx.send('The K/D Ratio of ' + username +' is ' + str(KD))

@bot.command()
async def adduser(ctx, battlenet):
    """Adds a user to the userlist"""
    f = open('userlist.json')
    userlist = json.load(f)
    userlist[str(ctx.author)] = str(battlenet)
    f.close()
    f = open('userlist.json', 'w')
    json.dump(userlist, f)
    await ctx.send('User has benn added to Userlist')
    
bot.run(TOKEN)
