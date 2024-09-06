import discord
import httpx
from discord.commands import slash_command
from discord.ext import commands

from config import bot_config


class CreateLoginTokenPanel(discord.ui.view):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="ログイン", style=discord.ButtonStyle.primary, custom_id="create_login_token")
    async def create_login_token(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_id = interaction.user.id

        resp = httpx.post(
            "https://checkin.nxtend.or.jp/auth/discord",
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'user_id': user_id,
                'api_key': bot_config.API_KEY
            }
        )

        if resp.status_code == 200:
            await interaction.response.send_message([
                f"> # [このURLからログインしてください]({resp.json()['url']})",
                f"> - ※ このURLは1回限り、1時間以内のみ有効です。また、このURLは他の人に教えないでください。"
            ], ephemeral=True)
        else:
            await interaction.response.send_message("エラーが発生しました。スタッフにお声がけください。", ephemeral=True)


class CreateLoginToken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        self.bot.add_view(CreateLoginTokenPanel())

    @slash_command(name="login_panel", description="サイトログイン用パネルを表示します。")
    async def room_manager(self, ctx: discord.commands.context.ApplicationContext):
        await ctx.respond(view=CreateLoginTokenPanel())


def setup(bot):
    return bot.add_cog(CreateLoginToken(bot))
