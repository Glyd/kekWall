import json
import discord
import asyncio
import datetime

config = {}
with open("config.json", "r") as configfile:
    config = json.load(configfile)
CHANNEL_ID_TO_WATCH = config["CHANNEL_ID_TO_WATCH"]
TOKEN = config["DISCORD_TOKEN"]
REACT_THRESHOLD = config["REACT_THRESHOLD"]
EMOJI_NAME_TO_COUNT = config["EMOJI_NAME_TO_COUNT"]

CHANNEL = None

intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)
    
async def wakeLaurelin():
    await client.start(TOKEN)

@client.event
async def on_ready():
    print(f'{client.user} is here')
    await init()

async def getMessages(channel, limit, an_hour_ago):
    print(f'{client.user} is fetching messages with params: {channel, limit, an_hour_ago}...')
    if channel is None:
        print("Error: Invalid channel")
        return []
    messages = [ message async for message in channel.history(limit=limit, after=an_hour_ago, oldest_first=False)]
    await asyncio.sleep(1)
    return messages

async def mainTask():
    print('running main task')
    await check_channel_reactions()

async def init():
    if(client.is_ready()):
        await mainTask()
        await asyncio.sleep(5)
    else:
        print('not ready yet')

async def check_reactions(messages, channel):
    count=0
    for message in messages:
        count = count + 1
        print(f'Checking message: {count}')
        kekw_reactions = [reaction for reaction in message.reactions if reaction.emoji.name == EMOJI_NAME_TO_COUNT]
        print(f'Checking message: {kekw_reactions}')
        if kekw_reactions:
            total_reactions = sum(reaction.count for reaction in kekw_reactions)
            print(f'Checking message: {total_reactions}')
            if total_reactions >= 1:
                print(f'{total_reactions} "kekw" reactions on message {message.id}!')
                await channel.send(f'{total_reactions} "kekw" reactions on message {message.id}!')

async def check_channel_reactions(limit=100):
    CHANNEL = client.get_channel(CHANNEL_ID_TO_WATCH)
    print(f'{client.user} is starting up')
    now = datetime.datetime.now()
    an_hour_ago = now - datetime.timedelta(hours=2)
    print('dates setup')

    messages = await getMessages(CHANNEL, 100, an_hour_ago)
    print('messages setup')
    await check_reactions(messages, CHANNEL)

async def main():
    while True:
        try:
            await wakeLaurelin()
        except:
            print('failed to wake - instance already exists?')

if __name__ == '__main__':
    asyncio.run(main())
        
