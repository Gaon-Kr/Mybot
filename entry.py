import discord
from discord.ext import commands
from datetime import datetime, timedelta

class EntryCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(1104787523802234961)
        if channel:
            join_count = len(member.guild.members)

            embed = discord.Embed(title=f"{join_count}번째 멤버가 입장했어요",
                                  description=f"**유저**\n<@{member.id}> ({member.name}#{member.discriminator})")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.colour = discord.Colour(0x2FBDFF)
            embed.add_field(name="서버에 입장한 시간", value=f"||{datetime.utcnow().strftime('%Y년 %m월 %d일 %H시 %M분')}||", inline=True)
            embed.add_field(name="계정 생성일", value=f"||{member.created_at.strftime('%Y년 %m월 %d일 %H시 %M분')}||", inline=True)
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(EntryCog(client))
