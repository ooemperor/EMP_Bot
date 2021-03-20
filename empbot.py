# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 12:59:20 2021

@author: mikai
"""
import nest_asyncio
nest_asyncio.apply()
import discord
from discord.ext import commands

description = '''EMP_bot'''
intents = discord.Intents.default()

bot = commands.Bot(command_prefix='§', description=description, intents=intents)

tk = open('Token.txt', 'r')
TOKEN = tk.read()

client= discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    

client.run(TOKEN)
