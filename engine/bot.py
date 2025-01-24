import nextcord
from nextcord.ext import commands, application_checks, tasks
import logging
import engine.config as config
import engine.sql as sql
import engine.views as views
import engine.messages as messages
import engine.utils as utils


intents = nextcord.Intents.all()
client = commands.Bot(command_prefix=';', intents=intents, default_guild_ids=[config.GUILD_ID])

current_quiz = None


@client.slash_command(description="Поймать лягушку")
async def catch(interaction: nextcord.Interaction):
    sql.get_user_balance(interaction.user)
    current_time = utils.get_timestamp()
    delta_time = current_time - sql.get_last_catching_time(interaction.user)
    if delta_time < config.CATCHING_COOLDOWN * 3600:
        return await interaction.response.send_message(**messages.cooldown(delta_time))
    amount_of_caught_frogs = utils.catch_attempt()
    sql.set_last_catching_time(interaction.user, current_time)
    logging.info(f"Пользователь {interaction.user.name} пытается поймать лягушку.")
    if amount_of_caught_frogs > 0:
        sql.set_user_balance(interaction.user, amount_of_caught_frogs)
        logging.info(f"Пользователь {interaction.user.name} поймал лягушек в количестве {amount_of_caught_frogs} шт.")
    await interaction.response.send_message(**messages.catch(interaction.user.mention, amount_of_caught_frogs))


@client.slash_command(description="Посмотреть свой баланс")
async def balance(interaction: nextcord.Interaction):
    user_balance = sql.get_user_balance(interaction.user)
    return await interaction.response.send_message(**messages.balance(interaction.user.mention, user_balance))


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
    if amount <= 0:
        return await interaction.response.send_message(**messages.transfer_denied("non_positive_amount"))
    elif other_user == interaction.user:
        return await interaction.response.send_message(**messages.transfer_denied("to_self"))
    elif other_user.bot:
        return await interaction.response.send_message(**messages.transfer_denied("to_bot"))
    await interaction.response.send_message(
        **messages.transfer(other_user, amount),
        view=views.TransferView(amount, other_user, interaction.user)
    )


@client.slash_command(description="Магазин West Wolves")
async def shop(interaction: nextcord.Interaction):
    await interaction.response.send_message(
        **messages.shop(),
        view=views.ShopMenuView()
    )


@client.slash_command(description="Провести викторину")
@application_checks.has_permissions(administrator=True)
async def quiz(interaction: nextcord.Interaction):
    await interaction.response.send_modal(views.QuizModal())


@client.slash_command(description="Выдать награду победителю викторины")
@application_checks.has_permissions(administrator=True)
async def prize(
        interaction: nextcord.Interaction,
        quiz_winner: nextcord.Member = nextcord.SlashOption(
            name="username",
            description="Имя победителя викторины")
):
    if not current_quiz or not current_quiz.is_active():
        return await interaction.response.send_message(**messages.quiz_error("no_active_quiz"), ephemeral=True)
    elif quiz_winner.bot:
        return await interaction.response.send_message(**messages.quiz_error("to_bot"), ephemeral=True)
    elif current_quiz.in_progress():
        return await interaction.response.send_message(**messages.quiz_error("in_progress"), ephemeral=True)
    sql.set_user_balance(quiz_winner, current_quiz.prize_amount)
    current_quiz.close()
    logging.info(f"Пользователь {quiz_winner.name} становится победителем викторины и получает в награду "
                 f"лягушек в количестве {current_quiz.prize_amount} шт.")
    await interaction.response.send_message(**messages.quiz_prize(quiz_winner, **current_quiz.get_contents()))


@client.slash_command(description="Админка")
@application_checks.has_permissions(administrator=True)
async def admin(interaction: nextcord.Interaction):
    await interaction.response.send_message(
        **messages.admin(),
        view=views.AdminMenuView()
    )


@tasks.loop(time=utils.get_taxes_and_encashment_collection_time())
async def scheduled_collection():
    channel = client.get_channel(config.ECONOMY_BOT_MAIN_CHANNEL)
    administrator = await client.fetch_user(config.ADMIN_ID)
    taxes_and_encashment = config.TAXES_AND_ENCASHMENT
    current_timestamp = utils.get_timestamp()
    current_month = utils.get_short_date(current_timestamp)
    if taxes_and_encashment["is_taxes_active"] and taxes_and_encashment["tax_collection_date"] != current_month:
        taxes = 0
        single_tax = taxes_and_encashment['tax_value']
        all_users_balances = sql.get_all_users_balances()
        for user_id, _, user_balance in all_users_balances:
            if user_id == config.ADMIN_ID or user_balance < single_tax:
                continue
            user = await client.fetch_user(user_id)
            sql.set_user_balance(user, -single_tax)
            taxes += single_tax
        taxes_and_encashment["tax_collection_date"] = current_month
        utils.set_taxes(taxes_and_encashment)
        if taxes:
            sql.set_user_balance(administrator, taxes)
            previous_month = utils.get_short_date(current_timestamp, previous=True)
            logging.info(f"Произведен сбор налогов в размере {taxes} шт. лягушек.")
            await channel.send(
                **messages.taxes_collection(amount=taxes, tax_period=previous_month)
            )
    encashment_amount = sql.get_encashment_amount()
    if encashment_amount:
        sql.set_user_balance(administrator, encashment_amount)
        sql.reset_encashment_amount()
        logging.info(f"Произведена инкассация, на счет администратора переведено {encashment_amount} шт. лягушек.")
        await channel.send(
            **messages.encashment(amount=encashment_amount, encashment_day=utils.get_previous_day(current_timestamp))
        )


@client.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message(**messages.admin_option_only_warning(), ephemeral=True)
    else:
        logging.error(f"При использовании команды произошла непредвиденная ошибка: '{error}'")


@client.event
async def on_ready():
    logging.info(f'Бот залогинен под именем: {client.user.name}')
    sql.create_tables()
    if not scheduled_collection.is_running():
        scheduled_collection.start()
