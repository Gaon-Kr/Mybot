import discord
from discord.ext import commands


class VerifiedChannelCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel_id = 1104764073482133574  # 채널 ID를 입력해주세요.
        self.channel = None

    async def cog_before_invoke(self, ctx):
        if not self.channel:
            self.channel = self.client.get_channel(self.channel_id)

    @commands.command()
    async def clear_all_messages(self, ctx):
        def check(message):
            return message.author != self.client.user and not message.content.startswith('!인증')

        deleted_messages = await self.channel.purge(limit=None, check=check)
        await ctx.send(f'{len(deleted_messages)}개의 메시지를 삭제했습니다.', delete_after=5)

    @staticmethod
    async def setup(client):
        cog = VerifiedChannelCog(client)
        await cog.cog_before_invoke(None)
        client.add_cog(cog)
