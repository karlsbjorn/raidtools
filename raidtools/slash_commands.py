import discord
from redbot.core import app_commands

from raidtools.event_create import EventCreateView
from raidtools.event_manage import EventManageView


class SlashCommands:
    @app_commands.command(
        name="create",
        description="Kreiraj novi event u ovom kanalu.",
    )
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="Samo klasa/spec", value="no_buttons"),
            # app_commands.Choice(name="Klasa/spec + nedolasci", value="buttons"),
            app_commands.Choice(name="Klasa/spec + jedan offspec", value="offspec_buttons"),
            app_commands.Choice(name="Klasa/spec + više offspeca", value="offspec_buttons_multi"),
        ]
    )
    @app_commands.guild_only()
    async def slash_event_create(
        self, interaction: discord.Interaction, choices: app_commands.Choice[str]
    ):
        # Don't do anything if the user doesn't have manage guild permission
        if not (  # TODO: Add a role check too
            interaction.user.guild_permissions.manage_guild
            or await interaction.client.is_owner(interaction.user)
        ):
            await interaction.response.send_message(
                "Nemaš dozvolu za kreiranje eventa u ovom guildu.", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="Kreirajmo event!",
            description="Upute za kreiranje eventa:",
            color=discord.Color.yellow(),
        )
        embed.add_field(
            name="Datum eventa",
            value="**PROČITAJ ME**\n"
            "Unesi datum kao [vremensku oznaku koju možeš dobit ovdje.]"
            "(https://r.3v.fi/discord-timestamps/)\n"
            "Klikni gumb nakon što imaš vremensku oznaku kopiranu.\n\n"
            "❗**Prijave se zatvore kad event počne**",
            inline=False,
        )

        await interaction.response.send_message(
            embed=embed, ephemeral=True, view=EventCreateView(self.config, choices.value)
        )

    @app_commands.command(name="manage", description="Upravljaj eventima.")
    @app_commands.guild_only()
    async def slash_event_manage(self, interaction: discord.Interaction):
        # Don't do anything if the user doesn't have manage guild permission
        if (  # TODO: Add a role check too
            not interaction.user.guild_permissions.manage_guild
            and not await interaction.client.is_owner(interaction.user)
        ):
            await interaction.response.send_message(
                "Nemaš dozvolu za upravljanje eventima u ovom guildu.", ephemeral=True
            )
            return

        events = await self.config.guild(interaction.guild).events()
        if not events:
            await interaction.response.send_message(
                "U ovom guildu nema aktivnih eventa.", ephemeral=True
            )
            return

        await interaction.response.send_message(
            "Odaberi event kojim želiš upravljati.",
            ephemeral=True,
            view=EventManageView(self.config, events=events),
        )
