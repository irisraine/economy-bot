import nextcord
import engine.bot as bot
import engine.sql as sql
import engine.messages as messages
import engine.utils as utils
import engine.config as config


def items():
    return {
        "track": {"price": config.PRICES['track'], "description": "Трек про леху"},
        "frog": {"price": config.PRICES['frog'], "description": "Фото лягушки"},
        "cite": {"price": config.PRICES['cite'], "description": "Цитата дня"},
        "animal": {"price": config.PRICES['animal'], "description": "Животное"},
        "meme": {"price": config.PRICES['meme'], "description": "Мем"},
        "food": {"price": config.PRICES['food'], "description": "Еда"},
        "soundpad": {"price": config.PRICES['soundpad'], "description": "Саундпад"},
        "drawing": {"price": config.PRICES['drawing'], "description": "Рисунок"},
        "rain": {"price": config.PRICES['rain'], "description": "Дождь из лягушек"},
        "event": {"price": config.PRICES['event'], "description": "Ивент"},
        "role": {"price": config.PRICES['role'], "description": "Роль"},
        "band": {"price": config.PRICES['band'], "description": "Банда"},
    }

def probabilities():
    return {
        "common": int(config.PROBABILITIES['common'] * 100),
        "uncommon": int(config.PROBABILITIES['uncommon'] * 100),
        "rare": int(config.PROBABILITIES['rare'] * 100),
        "legendary": int(config.PROBABILITIES['legendary'] * 100)
    }

options = [
    nextcord.SelectOption(label=f"Послушать эпичный трек про Леху", value="track", emoji="🎸"),
    nextcord.SelectOption(label=f"Лягушка", value="frog", emoji="🐸"),
    nextcord.SelectOption(label=f"Случайная мудрая мысль на день", value="cite", emoji="📖"),
    nextcord.SelectOption(label=f"Случайное фото домашнего любимца", value="animal", emoji="🦊"),
    nextcord.SelectOption(label=f"Случайный мем", value="meme", emoji="🎭"),
    nextcord.SelectOption(label=f"Сделать заказ в ресторане 'Жабий квак'", value="food", emoji="🥐"),
    nextcord.SelectOption(label=f"Случайный саундпад Лехи", value="soundpad", emoji="🔊"),
    nextcord.SelectOption(label=f"Авторский рисунок", value="drawing", emoji="🏞"),
    nextcord.SelectOption(label=f"Дождь из лягушек", value="rain", emoji="🌧"),
    nextcord.SelectOption(label=f"Ивент", value="event", emoji="🚀"),
    nextcord.SelectOption(label=f"Роль 'Легушька' на 1 месяц", value="role", emoji="🎖"),
    nextcord.SelectOption(label=f"Создать свою банду", value="band", emoji="🥷"),
]

class PurchaseButton(nextcord.ui.View):
    def __init__(self, price, shop_item):
        super().__init__(timeout=None)
        self.price = price
        self.shop_item = shop_item

    @nextcord.ui.button(label="Приобрести товар", style=nextcord.ButtonStyle.green, emoji="💵")
    async def purchase_confirm_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_balance = sql.get_user_balance(interaction.user.id)
        await interaction.response.defer()
        if self.price > user_balance:
            await interaction.edit_original_message(
                embed=messages.insufficient_balance().embed,
                file=messages.insufficient_balance().file,
                view=None
            )
        else:
            sql.set_user_balance(interaction.user.id, -self.price)
            sql.set_bank_balance(self.price)
            bought_item_message = messages.item_purchased(self.shop_item)

            if self.shop_item in ["drawing", "rain", "event", "role", "band"]:
                request_to_admin = bot.client.get_user(config.ADMIN_ID)
                await request_to_admin.send(
                    embed=messages.service_purchased_and_requested(interaction.user.mention, self.shop_item).embed,
                    file=messages.service_purchased_and_requested(interaction.user.mention, self.shop_item).file,
                )

            await interaction.edit_original_message(
                content=bought_item_message.content,
                embed=bought_item_message.embed,
                file=bought_item_message.file,
                view=None
            )

    @nextcord.ui.button(label="Вернуться к прилавку", style=nextcord.ButtonStyle.gray, emoji="◀️")
    async def return_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=messages.shop().embed,
            file=messages.shop().file,
            view=ShopList()
        )

class TransferButton(nextcord.ui.View):
    def __init__(self, transfer_amount, other_user):
        super().__init__(timeout=None)
        self.transfer_amount = transfer_amount
        self.other_user = other_user

    @nextcord.ui.button(label="Подтвердить перевод", style=nextcord.ButtonStyle.green, emoji="✅")
    async def transfer_confirm_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_balance = sql.get_user_balance(interaction.user.id)
        await interaction.response.defer()
        if self.transfer_amount > user_balance:
            return await interaction.edit_original_message(
                embed=messages.transfer_denied(self.other_user, self.transfer_amount).embed,
                file=messages.transfer_denied(self.other_user, self.transfer_amount).file,
                view=None
            )

        other_user_balance = sql.get_user_balance(self.other_user.id)
        if other_user_balance is None:
            sql.create_user_balance(self.other_user.id, self.other_user.name)
        sql.set_user_balance(interaction.user.id, -self.transfer_amount)
        sql.set_user_balance(self.other_user.id, self.transfer_amount)

        await interaction.edit_original_message(
            embed=messages.transfer_successful(self.other_user, self.transfer_amount).embed,
            file=messages.transfer_successful(self.other_user, self.transfer_amount).file,
            view=None
        )

    @nextcord.ui.button(label="Отказаться от перевода", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message(
        )


class ShopList(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.select(
        placeholder="Выбери нужный товар",
        options=options
    )
    async def select_purchase_callback(self, select, interaction: nextcord.Interaction):
        item = items()[select.values[0]]['description']
        price = items()[select.values[0]]['price']

        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=messages.buying_confirmation(item, price).embed,
            file=messages.buying_confirmation(item, price).file,
            view=PurchaseButton(price, select.values[0])
        )

    @nextcord.ui.button(label="Закрыть магазин", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()

class AdminPanel(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.select(
        placeholder="Выбери нужную опцию",
        options=[
            nextcord.SelectOption(label=f"Кэшировать файлы", value="cache", description="Выполнить при первом запуске бота", emoji="⚙️"),
            nextcord.SelectOption(label=f"Посмотреть счёт банка", value="bank_balance", description="Посмотреть, сколько лягушек потратили участники", emoji="🪙"),
            nextcord.SelectOption(label=f"Посмотреть счёта всех участников", value="show_all_users_balance", description="Изучить содержимое карманов всех участников", emoji="📈"),
            nextcord.SelectOption(label=f"Перевести сколько угодно лягушек участнику", value="unlimited_transfer", description="Одарить участника болотным сокровищем", emoji="💎"),
            nextcord.SelectOption(label=f"Установить цены", value="prices", description="Изменить текущие цены или установить дефолтные", emoji="🧮"),
            nextcord.SelectOption(label=f"Установить вероятности отлова", value="probabilities", description="Побыть властелином вероятностей", emoji="🕹"),
            nextcord.SelectOption(label=f"Установить кулдаун", value="cooldown", description="Определить допустимую частоту отлова", emoji="⏰"),
            nextcord.SelectOption(label=f"Отправить любое сообщение от имени бота в салун", value="say", description="Говорить от имени лягушачьего предводителя", emoji="💭"),
        ]
    )
    async def select_admin_panel_callback(self, select, interaction: nextcord.Interaction):
        await interaction.response.defer()

        if select.values[0] == "cache":
            files_count_printable = utils.refresh_cache()
            await interaction.edit_original_message(
                embed=messages.caching_successful(files_count_printable).embed,
                file=messages.caching_successful(files_count_printable).file,
                view=AdminPanelAfterActionButtons()
            )
        elif select.values[0] == "bank_balance":
            await interaction.edit_original_message(
                embed=messages.bank_balance().embed,
                file=messages.bank_balance().file,
                view=AdminPanelAfterActionButtons()
            )
        elif select.values[0] == "show_all_users_balance":
            await interaction.edit_original_message(
                embed=messages.all_users_balances().embed,
                file=messages.all_users_balances().file,
                view=AdminPanelAfterActionButtons()
            )
        elif select.values[0] == "say":
            await interaction.edit_original_message(
                embed=messages.send_message_by_bot().embed,
                file=messages.send_message_by_bot().file,
                view=MessageByBot()
            )
        elif select.values[0] == "prices":
            await interaction.edit_original_message(
                embed=messages.set_price().embed,
                file=messages.set_price().file,
                view=SetPrice()
            )
        elif select.values[0] == "probabilities":
            await interaction.edit_original_message(
                embed=messages.set_probabilities().embed,
                file=messages.set_probabilities().file,
                view=SetProbabilities()
            )
        elif select.values[0] == "cooldown":
            await interaction.edit_original_message(
                embed=messages.set_cooldown().embed,
                file=messages.set_cooldown().file,
                view=SetCooldown()
            )
        elif select.values[0] == "unlimited_transfer":
            await interaction.edit_original_message(
                embed=messages.unlimited_transfer().embed,
                file=messages.unlimited_transfer().file,
                view=UnlimitedTransfer()
            )
        else:
            await interaction.edit_original_message(
                embed=messages.not_applied_yet().embed,
                file=messages.not_applied_yet().file,
                view=AdminPanelAfterActionButtons()
            )

    @nextcord.ui.button(label="Закрыть админку", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()

class AdminPanelAfterActionButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Вернуться в админку", style=nextcord.ButtonStyle.gray, emoji="◀️")
    async def return_to_admin_panel_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=messages.admin_panel().embed,
            file=messages.admin_panel().file,
            view=AdminPanel()
        )

    @nextcord.ui.button(label="Закрыть", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_notify_message_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()

class MessageWindow(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Отправка сообщения в новостной канал")

        self.message_title = nextcord.ui.TextInput(
            label="Заголовок",
            max_length=100,
            required=True,
            placeholder="Текст заголовка",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.message_title)
        self.message_description = nextcord.ui.TextInput(
            label="Сообщение",
            required=True,
            placeholder="Текст сообщения",
            style=nextcord.TextInputStyle.paragraph
        )
        self.add_item(self.message_description)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        channel = interaction.guild.get_channel(config.NEWS_CHANNEL_ID)
        await channel.send(
            embed=messages.news_channel_message(self.message_title.value, self.message_description.value).embed,
            file=messages.news_channel_message(self.message_title.value, self.message_description.value).file)
        await interaction.followup.send(
            embed=messages.send_message_by_bot_confirmed().embed,
            file=messages.send_message_by_bot_confirmed().file,
            ephemeral=True)

class MessageByBot(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Создать новость", style=nextcord.ButtonStyle.green, emoji="🗞")
    async def send_message_by_bot_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(MessageWindow())

    @nextcord.ui.button(label="Вернуться в админку", style=nextcord.ButtonStyle.gray, emoji="◀️")
    async def return_to_admin_panel_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=messages.admin_panel().embed,
            file=messages.admin_panel().file,
            view=AdminPanel()
        )

    @nextcord.ui.button(label="Закрыть", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_message_by_bot_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()

class SetPrice(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.select(
        placeholder="Выбери нужный товар",
        options=options
    )
    async def set_price_callback(self, select, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SetPriceWindow(select.values[0]))

    @nextcord.ui.button(label="По умолчанию", style=nextcord.ButtonStyle.gray, emoji="💲")
    async def default_prices_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_price(reset=True)
        await interaction.followup.send(
            embed=messages.reset_price_confirmed().embed,
            file=messages.reset_price_confirmed().file, ephemeral=True
        )

    @nextcord.ui.button(label="Вернуться в админку", style=nextcord.ButtonStyle.gray, emoji="◀️")
    async def return_to_admin_panel_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=messages.admin_panel().embed,
            file=messages.admin_panel().file,
            view=AdminPanel()
        )

    @nextcord.ui.button(label="Закрыть", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_message_by_bot_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()


class SetPriceWindow(nextcord.ui.Modal):
    def __init__(self, item):
        self.item = item
        super().__init__(f"Установить новую цену на {items()[self.item]['description']}")

        self.price = nextcord.ui.TextInput(
            label="Новая цена",
            max_length=4,
            required=True,
            placeholder=f"Текущая цена: {items()[self.item]['price']} лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.price)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        is_valid_price = utils.validate_price(self.price.value)
        if is_valid_price:
            utils.set_price(self.item, self.price.value)
        await interaction.followup.send(
            embed=messages.set_price_confirmed(is_valid_price).embed,
            file=messages.set_price_confirmed(is_valid_price).file, ephemeral=True)

class SetProbabilitiesWindow(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Установить значения вероятностей поимки")

        self.common = nextcord.ui.TextInput(
            label="Стандартный улов",
            max_length=4,
            required=True,
            placeholder=f"Текущая вероятность: {probabilities()['common']} процентов",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.common)
        self.uncommon = nextcord.ui.TextInput(
            label="Редкий улов",
            max_length=4,
            required=True,
            placeholder=f"Текущая вероятность: {probabilities()['uncommon']} процентов",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.uncommon)
        self.rare = nextcord.ui.TextInput(
            label="Эпичный улов",
            max_length=4,
            required=True,
            placeholder=f"Текущая вероятность: {probabilities()['rare']} процентов",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.rare)
        self.legendary = nextcord.ui.TextInput(
            label="Легендарный улов",
            max_length=4,
            required=True,
            placeholder=f"Текущая вероятность: {probabilities()['legendary']} процентов",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.legendary)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        updated_probabilities = {
            "common": self.common.value,
            "uncommon": self.uncommon.value,
            "rare": self.rare.value,
            "legendary": self.legendary.value
        }
        is_valid_probabilities = utils.validate_probabilities(updated_probabilities)
        if is_valid_probabilities:
            utils.set_probabilities(updated_probabilities)
        await interaction.followup.send(
            embed=messages.set_probabilities_confirmed(is_valid_probabilities).embed,
            file=messages.set_probabilities_confirmed(is_valid_probabilities).file, ephemeral=True)


class SetProbabilities(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Установить вероятности", style=nextcord.ButtonStyle.green, emoji="🎲")
    async def set_probabilities_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SetProbabilitiesWindow())

    @nextcord.ui.button(label="По умолчанию", style=nextcord.ButtonStyle.gray, emoji="💯")
    async def default_probabilities_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_probabilities(reset=True)
        await interaction.followup.send(
            embed=messages.reset_probabilities_confirmed().embed,
            file=messages.reset_probabilities_confirmed().file, ephemeral=True
        )

    @nextcord.ui.button(label="Вернуться в админку", style=nextcord.ButtonStyle.gray, emoji="◀️")
    async def return_to_admin_panel_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=messages.admin_panel().embed,
            file=messages.admin_panel().file,
            view=AdminPanel()
        )

class SetCooldownWindow(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Установить значения времени между ловлей")

        self.cooldown = nextcord.ui.TextInput(
            label="Кулдаун",
            max_length=2,
            required=True,
            placeholder=f"Текущая продолжительность: {config.CATCHING_COOLDOWN} секунд",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.cooldown)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        is_valid_cooldown = utils.validate_cooldown(self.cooldown.value)
        if is_valid_cooldown:
            utils.set_cooldown(self.cooldown.value)
        await interaction.followup.send(
            embed=messages.set_cooldown_confirmed(is_valid_cooldown).embed,
            file=messages.set_cooldown_confirmed(is_valid_cooldown).file, ephemeral=True)

class SetCooldown(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Установить кулдаун", style=nextcord.ButtonStyle.green, emoji="⏳")
    async def set_cooldown_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SetCooldownWindow())

    @nextcord.ui.button(label="По умолчанию", style=nextcord.ButtonStyle.gray, emoji="⏱")
    async def default_cooldown_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_cooldown(reset=True)
        await interaction.followup.send(
            embed=messages.reset_cooldown_confirmed().embed,
            file=messages.reset_cooldown_confirmed().file, ephemeral=True
        )

    @nextcord.ui.button(label="Вернуться в админку", style=nextcord.ButtonStyle.gray, emoji="◀️")
    async def return_to_admin_panel_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=messages.admin_panel().embed,
            file=messages.admin_panel().file,
            view=AdminPanel()
        )

class UnlimitedTransferWindow(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Подарить участнику лягушачье сокровище")

        self.username = nextcord.ui.TextInput(
            label="discord username",
            required=True,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.username)
        self.transferred_amount = nextcord.ui.TextInput(
            label="Размер сокровища",
            max_length=4,
            required=True,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.transferred_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        is_valid_transfer = self.transferred_amount.value.isdigit()
        if is_valid_transfer:
            sql.set_user_balance_by_username(self.username.value, int(self.transferred_amount.value))
        await interaction.followup.send(
            embed=messages.unlimited_transfer_confirmed(self.username.value, int(self.transferred_amount.value), is_valid_transfer).embed,
            file=messages.unlimited_transfer_confirmed(self.username.value, int(self.transferred_amount.value), is_valid_transfer).file, ephemeral=True)

class UnlimitedTransfer(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Сделать перевод", style=nextcord.ButtonStyle.green, emoji="⏳")
    async def set_cooldown_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(UnlimitedTransferWindow())

    @nextcord.ui.button(label="Вернуться в админку", style=nextcord.ButtonStyle.gray, emoji="◀️")
    async def return_to_admin_panel_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=messages.admin_panel().embed,
            file=messages.admin_panel().file,
            view=AdminPanel()
        )