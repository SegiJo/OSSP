import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents= intent)

baseurl = "https://kr.op.gg/summoner/userName="

@bot.event #로그인 확인
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command() #인사말
async def 안녕(ctx):
    await ctx.send("안녕하세요.")

@bot.command() #채널 접속 및 확인
async def 입장(ctx):
    try:
        channel=ctx.author.voice.channel
        await channel.connect()
    except:
        try:
            await channel.connect()
        except:
            await ctx.send("채널에 유저가 접속해있지 않네요.")

@bot.command() #퇴장 및 인원 확인
async def 퇴장(ctx):
    try:
        await ctx.voice_client.disconnect()
    except:
        await ctx.send("이미 그 채널에 속해있지 않아요.")

@bot.event #리그오브레전드 사용자 정보
async def on_message(message):
    if message.content.startswith("!롤"):
        message_content = message.content.replace("!롤 ", "")
        plusurl = message_content.replace(" ", "")
        url = baseurl + plusurl
        res = requests.get(url).text
        soup = BeautifulSoup(res, "html.parser")

        img = soup.find("div", attrs={"class":"SummonerRatingMedium"}).find("img").get('src')
        tiername = soup.find("div", attrs={"class":"TierRank"}).get_text()
        tieraka = soup.find("div", attrs={"class":"LeagueName"}).get_text().strip()

        userlp = soup.find("span", attrs={"class":"LeaguePoints"}).get_text().strip()


        win = soup.find("span", attrs={"class":"wins"}).get_text().replace("W", "승")
        lose = soup.find("span", attrs={"class":"losses"}).get_text().replace("L", "패")
        odds = soup.find("span", attrs={"class":"winratio"}).get_text()


        mostchamp = soup.find_all("div", attrs={"class":"ChampionBox Ranked"}, limit=3)
        mostchamp_list = []
        for most in mostchamp:
            mostchamp_list.append(most.find('div').get('title'))

        embed = discord.Embed(title=message_content + " 님의 플레이어 정보", description="", color=0x62c1cc)
        embed.set_thumbnail(url="http:" + img)

        embed.add_field(name="티어 정보", value="`" + userlp + " | " + tiername + " | " + tieraka + "`", inline=False)
        embed.add_field(name="모스트 챔피언", value="`" + mostchamp_list[0] + ", " + mostchamp_list[1] + ", " + mostchamp_list[2] + "`", inline=False)
        embed.add_field(name="승, 패, 승률", value="`" + win + " " + lose + " | " + odds + "`", inline=False)

        embed.set_footer(text="솔로랭크 기준 티어입니다. | 랭크 정보가 없을 시 출력되지 않습니다.")
        await message.channel.send(embed=embed)

bot.run('token')
