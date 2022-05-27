from ast import alias
import discord
import os
from discord import VoiceChannel
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix='.')

#Running confirmation
@client.event
async def on_ready():
  print("Party-Time-Bot running")

@client.event
async def on_message(message):
  msg = message
  if msg.content.startswith(".hello"):
      await msg.channel.send(f'Hello {msg.author.name}')
  await client.process_commands(msg)

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cog.{extension}')
	print(f'Loaded cog.{extension}')

@client.command()
async def ping(ctx):
  await ctx.send('pong')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')
		print(f'Cog loaded cogs.{filename}')
 


client.run(TOKEN)