# import required dependencies
import discord
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
import json
import os
from itertools import cycle
import asyncio
from setting import TOKEN

print(discord.__version__)

# import all cogs
from ping import PingCog
from help import HelpCog
from verify import VerifyCog
from verified_channel import VerifiedChannelCog
from entry import EntryCog
from exit import ExitCog
from music import MusicCog
from okay import AuthCog
from levelup import LevelUp


intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)
BotName = "테스트봇"
bot_status = cycle(["접두사는 !", "모든 명령어는 !도움말", "봇은 상시로 업데이트 됩니다!"])

# 상태변경 bot_status 부분에는 계속 변하는 봇 상태가 들어감.
@tasks.loop(seconds=3)
async def change_status():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(next(bot_status)))

#remove the default help command so that we can write out own
client.remove_command('help')

# cogs load
@client.event
async def on_ready():
    await client.add_cog(PingCog(client))
    await client.add_cog(HelpCog(client))
    await client.add_cog(VerifyCog(client))
    await client.add_cog(VerifiedChannelCog(client))
    await client.add_cog(EntryCog(client))
    await client.add_cog(ExitCog(client))
    await client.add_cog(MusicCog(client))
    await client.add_cog(AuthCog(client))
    await client.add_cog(LevelUp(client))

    print(f"봇이 정상적으로 실행되었습니다. 사용이 가능합니다. 봇 이름은 : {client.user} 입니다.")
    print(f"----------------------------------------------")
    if not change_status.is_running():
        change_status.start()


try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("토큰이 일치하지 않습니다.")
