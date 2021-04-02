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
from datetime import datetime
import random
import sys
import json
import requests
from gpiozero import CPUTemperature
import asyncio

description = '''R2D2'''
intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

tk = open('Token Discord.txt', 'r')
TOKEN = tk.read()

tenor_api = open('Tenor API Key.txt', 'r')
TENOR_API_KEY = tenor_api.read()
Limit_Tenor = 1

Started = datetime.now()


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
async def r2d2(ctx):
    """Returns a surprise"""
    if ctx.author.voice != None:
        channel = str(ctx.author.voice.channel)
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = channel)
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        file = "r2d2.mp3"
        voice.play(discord.FFmpegPCMAudio(file))
        await ctx.send('https://tenor.com/view/happy-rocking-r2d2-star-wars-artoo-gif-15352285')
        await asyncio.sleep(2)
        await voice.disconnect()
    else:
        await ctx.send('https://tenor.com/view/happy-rocking-r2d2-star-wars-artoo-gif-15352285')
    
@bot.command()
async def ping(ctx):
    """Returns the latency of the bot"""
    ms = (datetime.utcnow() - ctx.message.created_at).microseconds / 1000
    
    before = datetime.now()
    await ctx.send('Latency: ' + str(int(ms)) + 'ms')
    ms2 = (datetime.now() - before).microseconds / 1000
    await ctx.send('Message delay: '+ str(int(ms2)) + 'ms')

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
    ms = (datetime.utcnow() - ctx.message.created_at).microseconds / 1000
    user = ctx.author
    cpu=CPUTemperature()
    temp = str((int(10*(cpu.temperature)))/10)
    await user.send(content = f"Ping is: `{str(int(ms))}ms`")
    await user.send(temp + '°C')
    await user.send('Running since: ' + Started.strftime("%d %B %Y, %H:%M"))
    
    
@bot.command()
async def kd(ctx):
    """Returns the K/D in Warzone if you are in the Userlist"""
    username = check_userlist(str(ctx.author))
    if username == '404':
        await ctx.send('User not in Userlist. Use !add to add the user to the Userlist')
        await ctx.send(ctx.author)
    else:
        KD = warzone(username)
        await ctx.send('The K/D Ratio of ' + username +' is ' + str(KD))

@bot.command()
async def adduser(ctx, battlenet):
    """Adds a user to the userlist for kd in Warzone. Write !adduser followed by your Battlenetname with ID Number"""
    f = open('userlist.json')
    userlist = json.load(f)
    userlist[str(ctx.author)] = str(battlenet)
    f.close()
    f = open('userlist.json', 'w')
    json.dump(userlist, f)
    await ctx.send('User has benn added to Userlist')
    

@bot.command()
async def upload(ctx):
    """Returns the Link to the Highlights Folder"""
    await ctx.send('You can upload your Highlights here for the others to enjoy it here:')
    await ctx.send('https://drive.google.com/drive/folders/1iYh3dMzjyHiZp4gK7fJZetlHrHzDHjoX?usp=sharing')
    
@bot.command()
async def play(ctx, effect):
    """Plays a soundeffect which keyword you can enter after play if avaible"""
    if ctx.author.voice != None:
        channel = str(ctx.author.voice.channel)
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = channel)
        f = open('sounddata.json')
        sounddata = json.load(f)
        if effect in sounddata.keys():
            await voiceChannel.connect()
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            file = (sounddata[effect][0])
            voice.play(discord.FFmpegPCMAudio(file))
            duration = int(sounddata[effect][1]) + 1
            await asyncio.sleep(duration)
            await voice.disconnect()
        else:
            await ctx.send('404 File not Found')
    else:
        await ctx.send('You must be in a Voice Channel')
    
@bot.command()
async def disconnect(ctx):
    """If the bot is in a Voice Channel it disconnects"""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice != None:
        await voice.disconnect()
    else:
        await ctx.send('Already disconnected')
        
@bot.command()
async def dev(ctx, action):
    """Gives you the Developer Role of the server. """
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name = 'DEV')
    if action == "add" and role not in user.roles:
        await user.add_roles(role)
    elif action == "add" and role in user.roles:
        await ctx.send('You already got this role')
    elif action == "del" and role in user.roles:
        await user.remove_roles(role)
    elif action == "del" and role not in user.roles:
        await ctx.send('Cannot delete a Role that you dont have')
    else:
        await ctx.send('Command not Found. Use add or del for delete')
        
@bot.command()
async def test(ctx):
    await ctx.send(ctx.message.author)
        
    
    
bot.run(TOKEN)

