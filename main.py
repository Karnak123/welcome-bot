import discord
import os
import requests
import json
import io
import aiohttp
from random import randint
from keep_alive import keep_alive

client = discord.Client()
help_text = '--Usage-- \nbot hello \nbot quote \nbot meme \nbot joke'

def get_quote():
  res = requests.get('https://type.fit/api/quotes')
  json_data = json.loads(res.text)
  quote = json_data[randint(0, len(json_data))]
  quote = quote['text'] + ' -' + quote['author']
  return quote

async def get_meme(message, c=1):
  if c==5:
    message.channel.send('Unable to establish connection')
  res = requests.get('https://meme-api.herokuapp.com/gimme')
  json_data = json.loads(res.text)
  url = json_data['url']
  filename = url.split('/')[-1]
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
      if resp.status != 200:
        get_meme(message, c+1)
      else:
        try:
          data = io.BytesIO(await resp.read())
          await message.channel.send(file=discord.File(data, filename))
        except:
          get_meme(message, c+1)

def get_joke():
  res = requests.get('https://official-joke-api.appspot.com/random_joke')
  json_data = json.loads(res.text)
  joke = json_data['setup'] + '\n' + json_data['punchline']
  return joke

def shake(content):
  res = requests.get('https://api.funtranslations.com/translate/shakespeare.json?text='+content)
  json_data = json.loads(res.text)
  shakes = json_data['contents']['translated']
  return shakes


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  elif message.content.startswith('bot help'):
    await message.channel.send(help_text)
  elif message.content.startswith('bot hello'):
    await message.channel.send('Hello {}'.format(message.author))
  elif message.content.startswith('bot quote'):
    await message.channel.send(get_quote())
  elif message.content.startswith('bot meme'):
    await get_meme(message)
  elif message.content.startswith('bot joke'):
    await message.channel.send(get_joke())
  else:
    t = randint(0,10)
    print(t)
    if t>3:
      await message.channel.send(shake(message.content))

keep_alive()
client.run(os.getenv('TOKEN'))