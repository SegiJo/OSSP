import discord
from discord.ext import commands

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents= intent)

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("테스트"))

@bot.event
async def on_message(message):
    if message.author.bot: # 봇이 보낸 메시지이면 반응하지 않게 합니다
        return
       
    if message.content == "0110 강의":
        await message.channel.send("오후 1시에 OSSP 강의가 있어요.")


@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕하세요.")

@bot.command()
async def 입장(ctx):
    try:
        channel=ctx.author.voice.channel
        await channel.connect()
    except:
        try:
            await channel.connect()
        except:
            await ctx.send("채널에 유저가 접속해있지 않네요.")

@bot.command()
async def 퇴장(ctx):
    try:
        await ctx.voice_client.disconnect()
    except:
        await ctx.send("이미 그 채널에 속해있지 않아요.")

bot.run('MTA2MjI5NTY0OTQyMjQxMzg0NA.GeXCL1.Ny9ebkbadn_jzsKEM_z2KDpNcv7KUociWWkHTw')
