import discord
from discord.ext import commands
from discord.ui import Button, View


class VerifyView(discord.ui.View):
    def __init__(self, role, client):
        super().__init__(timeout=None)
        self.role = role
        self.client = client

        description = f"아래 버튼을 눌러 {role.mention} 역할을 부여받으세요."
        self.embed = discord.Embed(
            title="인증",
            description=description,
            color=0x13B2FC
        )

        emoji = discord.PartialEmoji(name="✅")
        button = VerifyButton(role=role, emoji=emoji)
        self.add_item(button)

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if self.role in user.roles:
            self.embed.description = f"{user.mention}, 이미 {self.role.mention} 역할을 보유하고 있습니다."
            self.embed.color = discord.Color.red()
            message = await interaction.response.edit_message(embed=self.embed, view=None)
        else:
            await user.add_roles(self.role)
            self.embed.description = f"{user.mention}, 정상적으로 {self.role.mention} 역할이 부여되었습니다."
            self.embed.color = discord.Color.brand_green()
            message = await interaction.response.edit_message(embed=self.embed, view=None)
            self.clear_items()

        await interaction.response.delete_message()
        await interaction.followup(content=None, embed=self.embed)

    def disable_buttons(self):
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = True

    def enable_buttons(self):
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = False

    async def on_timeout(self):
        self.disable_buttons()


class VerifyButton(Button):
    def __init__(self, role, **kwargs):
        super().__init__(**kwargs)
        self.role = role
        self.label = f"인증하기"
        self.custom_id = "verify_button"
    
    async def callback(self, interaction: discord.Interaction):
        view = self.view
        await view.callback(interaction)
        view.disable_buttons()


class VerifyCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.role_id = 1104043865180217394  # 역할 ID를 입력해주세요.
        self.role = None

    async def cog_before_invoke(self, ctx):
        if not self.role:
            self.role = ctx.guild.get_role(self.role_id)

    @commands.command()
    async def 인증(self, ctx):
        view = VerifyView(self.role, self.client)  # 'client' 인자도 함께 전달
        message = await ctx.reply(embed=view.embed, view=view)
        view.message = message

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        except discord.NotFound:
            pass

    @staticmethod
    async def setup(client):
        cog = VerifyCog(client)
        await cog.cog_before_invoke(None)
        client.add_cog(cog)
