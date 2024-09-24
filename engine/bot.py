import nextcord
from nextcord.ext import commands, application_checks
import os
import logging
import random
import engine.config as config
import engine.sql as sql
import engine.views as views
import engine.messages as messages
import engine.utils as utils


intents = nextcord.Intents.all()
client = commands.Bot(command_prefix=':', intents=intents, default_guild_ids=[config.GUILD_ID])


@client.slash_command(description="Поймать лягушку")
async def catch(interaction: nextcord.Interaction):
    user_balance = sql.get_user_balance(interaction.user.id)
    if user_balance is None:
        sql.create_user_balance(interaction.user.id, interaction.user.name)

    current_time = utils.get_timestamp()
    delta_time = current_time - sql.get_last_catching_time(interaction.user.id)
    if delta_time < config.CATCHING_COOLDOWN:
        return await interaction.response.send_message(
            embed=messages.cooldown(delta_time).embed,
            file=messages.cooldown(delta_time).file)

    logging.info(f"Пользователь {interaction.user.name} пытается поймать лягушку.")
    amount_of_caught_frogs = 0
    rand = random.random()
    if rand < config.PROBABILITIES['legendary']:
        amount_of_caught_frogs = random.randint(7, 45)
    elif rand < config.PROBABILITIES['epic']:
        amount_of_caught_frogs = random.choice([5, 6])
    elif rand < config.PROBABILITIES['uncommon']:
        amount_of_caught_frogs = random.choice([3, 4])
    elif rand < config.PROBABILITIES['common']:
        amount_of_caught_frogs = random.choice([1, 2])

    sql.set_last_catching_time(interaction.user.id, current_time)
    if amount_of_caught_frogs > 0:
        sql.set_user_balance(interaction.user.id, amount_of_caught_frogs)
        logging.info(f"Пользователь {interaction.user.name} поймал лягушек в количестве {amount_of_caught_frogs} шт.")

    await interaction.response.send_message(
        embed=messages.catch(interaction.user.mention, amount_of_caught_frogs).embed,
        file=messages.catch(interaction.user.mention, amount_of_caught_frogs).file)


@client.slash_command(description="Посмотреть свой баланс")
async def balance(interaction: nextcord.Interaction):
    user_balance = sql.get_user_balance(interaction.user.id)
    if user_balance is None:
        sql.create_user_balance(interaction.user.id, interaction.user.name)
        user_balance = sql.get_user_balance(interaction.user.id)
    return await interaction.response.send_message(
        embed=messages.balance(interaction.user.mention, user_balance).embed,
        file=messages.balance(interaction.user.mention, user_balance).file
    )


@client.slash_command(description="Подарить лягушек другому участнику")
async def transfer(
    interaction: nextcord.Interaction,
    amount: int = nextcord.SlashOption(
        name="amount",
        description="Количество отдаваемых лягушек"),
    other_user: nextcord.Member = nextcord.SlashOption(
        name="username",
        description="Имя получателя"),
):
    if other_user == interaction.user or other_user.bot:
        fault_message = messages.transfer_failed("to_bot") if other_user.bot else messages.transfer_failed("to_self")
        return await interaction.response.send_message(
            embed=fault_message.embed,
            file=fault_message.file,
        )

    await interaction.response.send_message(
        embed=messages.transfer(other_user, amount).embed,
        file=messages.transfer(other_user, amount).file,
        view=views.TransferView(amount, other_user)
    )


@client.slash_command(description="Магазин West Wolves")
async def shop(interaction: nextcord.Interaction):
    await interaction.response.send_message(
        embed=messages.shop().embed,
        file=messages.shop().file,
        view=views.ShopMenuView()
    )


@client.slash_command(description="Админка")
@application_checks.has_permissions(administrator=True)
async def admin(interaction: nextcord.Interaction):
    await interaction.response.send_message(
        embed=messages.admin().embed,
        file=messages.admin().file,
        view=views.AdminMenuView()
    )


@client.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message(
            embed=messages.admin_option_only_warning().embed,
            file=messages.admin_option_only_warning().file,
            ephemeral=True
    )
    else:
        logging.error(f"При использовании команды произошла непредвиденная ошибка: '{error}'")


@client.event
async def on_ready():
    logging.info(f'Бот залогинен под именем: {client.user.name}')
    if not os.path.exists('database'):
        os.makedirs('database')
    sql.create_tables()
