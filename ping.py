import discord
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("PingCog가 준비되었습니다.")

    @commands.command(name="핑", help="퐁과 핑을 출력합니다.")
    async def ping(self, ctx):
        bot_latency = round(self.client.latency * 1000)

        await ctx.send(f"퐁! {bot_latency}ms :ping_pong:")

async def setup(client):
    await client.add_cog(PingCog(client))

