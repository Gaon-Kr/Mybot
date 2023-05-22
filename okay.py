import discord
from discord.ext import commands

class AuthCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.allowed_command = "!인증"  # 채널에서 허용되는 명령어
        self.allowed_channel_id = 1104129224819875860  # 채널 ID로 대체하세요

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id == self.allowed_channel_id:
            if not message.content.startswith(self.allowed_command):
                await message.delete()
                
                embed = discord.Embed(
                    title="!인증 명령어만 허용됩니다",
                    description="이 채널에서는 !인증 명령어만 사용할 수 있습니다.",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=embed)

def setup(client):
    client.add_cog(AuthCog(client))
