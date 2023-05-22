import discord
from discord.ext import commands
from discord.ui import Button, View

class HelpView(discord.ui.View):
    def __init__(self, ctx, client, **kwargs):
        super().__init__(timeout=None, **kwargs)
        self.client = client
        self.ctx = ctx

        self.add_item(GenralButton())
        self.add_item(GameButton())
        self.add_item(MusicButton())
        self.add_item(CancelButton())
        
    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.client.user:
            if interaction.component.custom_id == "genral_button":
                embed = discord.Embed(title="일반 도움말", description="일반적인 도움말 정보입니다.")
            elif interaction.component.custom_id == "game_button":
                embed = discord.Embed(title="게임 도움말", description="게임 도움말 정보입니다.")
            elif interaction.component.custom_id == "music_button":
                embed = discord.Embed(title="음악 도움말", description="음악 도움말 정보입니다.")
            elif interaction.component.custom_id == "cancel_button":
                embed = discord.Embed(title="취소", description="취소 되었습니다.")
                self.stop()
            else:
                return await interaction.message.delete()
            await interaction.message.edit(embed=embed, view=None)

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.ctx.author

class GenralButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = f"💬일반"
        self.style = discord.ButtonStyle.green
        self.custom_id = "genral_button"

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        embed = discord.Embed(title="💬일반 도움말", description="일반적인 도움말 정보입니다.")
        embed.add_field(name="!도움말", value="도움말을 표시합니다.", inline=False)
        embed.add_field(name="!핑", value="현재 핑과 퐁을 출력합니다.", inline=False)
        await interaction.response.edit_message(content=" ", view=None, embed=embed)

class GameButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = f"🎮게임"
        self.style = discord.ButtonStyle.green
        self.custom_id = "game_button"

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        embed = discord.Embed(title="🎮게임 도움말", description="게임 도움말 정보입니다.")
        embed.add_field(name="!레벨", value="현재레벨과 다음 레벨까지의 필요한 경험치 량을 표시합니다. ", inline=False)
        await interaction.response.edit_message(content=" ", view=None, embed=embed)

class MusicButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = f"🎵음악"
        self.style = discord.ButtonStyle.green
        self.custom_id = "music_button"

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        embed = discord.Embed(title="🎵음악 도움말", description="음악 도움말 정보입니다.")
        embed.add_field(name="!재생 <타이틀|URL>", value="노래를 재생해요. ('!p, !play, !ㅔ' 명령어로도 사용 가능)", inline=False)
        embed.add_field(name="!대기리스트", value="노래를 재생해요. ('!q, !queue, !ㅂ' 명령어로도 사용 가능)", inline=False)
        embed.add_field(name="!일시정지", value="음악을 일시정지합니다. ('!ps, !pause, !i '명령어로도 사용 가능)", inline=False)
        embed.add_field(name="!계속재생", value="음악 일시정지를 해제합니다. ('!r, !resume, !ㄱ' 명령어로도 사용 가능)", inline=False)
        embed.add_field(name="!정지", value="음악 재생을 멈추고 음성채팅방에서 나갑니다. ('!st, !stop' 명령어로도 사용 가능)", inline=False)
        embed.add_field(name="!스킵", value="재생중인 음악을 스킵합니다. ('!s, !skip' 명령어로도 사용 가능)", inline=False)
        embed.add_field(name="!루프", value="재생중인 음악을 무한 반복하거나 무한 반복을 해제합니다. ('!u, !loop' 명령어로도 사용 가능)", inline=False)
        embed.add_field(name="!셔플", value="대기 리스트에서 음악을 무작위로 재생합니다. ('!sf, !shuffle' 명령어로도 사용 가능)", inline=False)
        embed.add_field(name="!볼륨", value="음악의 볼륨을 조절합니다. ('!v, !volume' 명령어로도 사용 가능)", inline=False)
        embed.add_field(name="!강제연결해제", value="봇 오류로 음악 재생에 문제가 발생했을 때 강제로 접속을 해제합니다. ('!l, !leave' 명령어로도 사용 가능)", inline=False)
        await interaction.response.edit_message(content=" ", view=None, embed=embed)

class CancelButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = f"❌취소"
        self.style = discord.ButtonStyle.red
        self.custom_id = "cancel_button"

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        embed = discord.Embed(title="도움말", description="요청이 취소 되었습니다.")
        await interaction.response.edit_message(content=" ", view=None, embed=embed)

class HelpCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.view = HelpView(ctx=client, client=client)

    @commands.command(name='도움말')
    async def help_command(self, ctx):
        view = HelpView(ctx=ctx, client=self.client)
        embed = discord.Embed(title='도움말', description='카테고리를 선택하세요.', color=0x26FFC7)
        message = await ctx.send(embed=embed, view=view)
    
    @staticmethod
    async def setup(client):
        cog = HelpCog(client)
        client.add_cog(cog)
