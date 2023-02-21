
import asyncio
import os
import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot
import random
from datetime import datetime
import threading
import aiocron
import requests
from dotenv import load_dotenv
import openai
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
load_dotenv()

DISCORD_API_KEY = os.getenv('DISCORDAPI_KEY')
OPENAI_API_KEY = os.getenv('OPENAPI_KEY')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

##############

openai.api_key = OPENAI_API_KEY
model_engine = "text-davinci-003"

######################

cancelNextDay = False #used in a function call below, made it global so other functions could read it


@client.event
async def on_ready(): #event handler that handles the event when the Client has established a connection to discord and finsiehd prepping the data that discord has sent
    #on_ready() gets called once client is ready for further action
    print('We have logged in as {0.user}'.format(client))

    channel = client.get_channel(380936459496062981) # This will load the channel ID I want to transmit in
    await channel.send("Sup guys")
    print("We are in!!!!!!!!!!!!!!!!!")
    cron_min = aiocron.crontab('30 17 * * 1-5', func=checkWarzoneTime, args='', start=True) #cron job that will run every 1730 CEST


#When invoked, it will invoke the ChatGPT API to answer a question 
@client.command()
async def q(ctx, *, question: str): #question needs str as a type, or else the code fails
    print(f"The input is:  {question}\n")
    completion = openai.Completion.create(
    engine=model_engine,
    prompt=question,
    temperature=random.randrange(50, 90) / 100, # make it random how smart the bot should be
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    timeout=10
    )
    response = completion.choices[0].text
    await ctx.send(response)


@client.command()
async def shutdown(ctx):
    role = discord.utils.get(ctx.guild.roles, name="God") #id of the admins
    person = ctx.author.id #this gets your id
  

    if role in ctx.author.roles:
        await ctx.send("I am going to shut down")
        exit()
    else:
        #sends a Confucius saying from a webpage made in 2002
        #scrapes the webpage using edge, clicks the javascript button
        #and returns the output
        driver = webdriver.Edge()
        driver.minimize_window()
        driver.get('http://generatorland.com/glgenerator.aspx?id=86')
        driver.implicitly_wait(180)
        driver.find_element(By.XPATH,"//a/img[@alt='Confucius']").click()

        msg = driver.find_element(By.XPATH,"//div[@class='confucius']")
        msg_content = msg.get_attribute('innerHTML')
        await ctx.send(msg_content.strip())

#When invoke, it will ping the group for the warzone notification 
async def checkWarzoneTime():
    GUILD = "Merry Band of Minorities" # server name3
    channel = client.get_channel(380936459496062981)
    g = discord.utils.get(client.guilds, name = GUILD) 
    roleMention = discord.utils.get(g.roles, id = 929444477515497513)
    if cancelNextDay == True:
        await channel.send("No warzone today :( ")
        cancelNextDay = False
    else:
        #sends the poll for lunchtime warzone
        poll = await channel.send(f"{roleMention.mention}Are you going to be there for lunchtime warzone? ")
        await poll.add_reaction("✅")
        await poll.add_reaction("❌")
         
      

#When invoked, it will invoke the DALL-E API from openapi to generate an image   
@client.command()
async def i(ctx, *, question: str): #question needs str as a type, or else the code fails
    response = openai.Image.create(
    prompt=question,
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    full_path = 'test' + '.jpg'
    f = open(full_path, 'wb')
    f.write(requests.get(image_url).content)
    f.close()
    await ctx.send(file=discord.File(full_path))
    os.remove(full_path) # remove the generated file. This is the best way not to bloat the PC while temporarly sending pics to the discord chat

#added the confucius quote command so admins could call it without it shutting down
@client.command()
async def quote(ctx):
    driver = webdriver.Edge()
    driver.minimize_window()
    driver.get('http://generatorland.com/glgenerator.aspx?id=86')
    driver.implicitly_wait(180)
    driver.find_element(By.XPATH,"//a/img[@alt='Confucius']").click()

    msg = driver.find_element(By.XPATH,"//div[@class='confucius']")
    msg_content = msg.get_attribute('innerHTML')
    await ctx.send(msg_content.strip())


@client.command()
async def cancel(ctx):
    cancelNextDay = True
    await ctx.send("I canceled the warzone notification for the next day :sob: ")

client.run(DISCORD_API_KEY)


