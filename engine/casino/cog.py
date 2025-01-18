import nextcord
from nextcord.ext import commands
import engine.casino.messages as messages
import engine.casino.views as views


class Casino(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.gambling_pool = {}

    @nextcord.slash_command(description="Казино «Три лягушки»")
    async def casino(self, interaction: nextcord.Interaction):
        gambling_room = {
            "slot_machine": None,
            "roulette": None,
            "yahtzee": None
        }
        self.gambling_pool.setdefault(interaction.user, gambling_room)
        await interaction.response.send_message(
            **messages.casino(),
            view=views.CasinoMenuView(interaction.user)
        )


def setup(client):
    client.add_cog(Casino(client))
