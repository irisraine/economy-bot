import nextcord
import engine.sql as sql
import engine.messages as messages
import engine.utils as utils
import engine.config as config


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
            bought_item_message = messages.item_purchased(self.shop_item)

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
            sql.create_user_balance(self.other_user.id)
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
        options=[
            nextcord.SelectOption(label=f"Послушать эпичный трек про Леху", value="track", description=f"Стоимость - {config.PRICES['track']} лягушка", emoji="🎸"),
            nextcord.SelectOption(label=f"Лягушка", value="frog", description=f"Стоимость - {config.PRICES['frog']} лягушки", emoji="🐸"),
            nextcord.SelectOption(label=f"Случайная мудрая мысль на день", value="cite", description=f"Стоимость - {config.PRICES['cite']} лягушек", emoji="📖"),
            nextcord.SelectOption(label=f"Случайное фото домашнего любимца", value="animal", description=f"Стоимость - {config.PRICES['animal']} лягушек", emoji="🦊"),
            nextcord.SelectOption(label=f"Случайный мем", value="meme", description=f"Стоимость - {config.PRICES['animal']} лягушек", emoji="🎭"),
            nextcord.SelectOption(label=f"Сделать заказ в ресторане 'Жабий квак'", value="food", description=f"Стоимость - {config.PRICES['food']} лягушек", emoji="🥐"),
            nextcord.SelectOption(label=f"Случайный саундпад Лехи", value="soundpad", description=f"Стоимость - {config.PRICES['soundpad']} лягушек", emoji="🔊"),
            nextcord.SelectOption(label=f"Авторский рисунок", value="drawing", description=f"Стоимость - {config.PRICES['drawing']} лягушек", emoji="🏞"),
            nextcord.SelectOption(label=f"Дождь из лягушек", value="rain", description=f"Стоимость - {config.PRICES['rain']} лягушек", emoji="🌧"),
            nextcord.SelectOption(label=f"Ивент", value="event", description=f"Стоимость - {config.PRICES['event']} лягушек", emoji="🚀"),
            nextcord.SelectOption(label=f"Роль 'Легушька' на 1 месяц", value="role",description=f"Стоимость - {config.PRICES['role']} лягушек", emoji="🎖"),
            nextcord.SelectOption(label=f"Создать свою банду", value="band", description=f"Стоимость - {config.PRICES['band']} лягушек",emoji="🥷"),
        ]
    )
    async def select_purchase_callback(self, select, interaction: nextcord.Interaction):
        items = {
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
        item = items[select.values[0]]['description']
        price = items[select.values[0]]['price']

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
            nextcord.SelectOption(label=f"Кэшировать файлы", value="cache", description="Выполнить при первом запуске бота, либо добавлении нового контента", emoji="⚙️"),
            nextcord.SelectOption(label=f"Посмотреть счёт банка", value="bank_balance", description="Посмотреть, сколько всего лягушек потратили участники", emoji="🪙"),
            nextcord.SelectOption(label=f"Посмотреть счёт участника", value="show_user_balance", description="Заглянуть в кошелек участника и посчитать чужие деньги", emoji="💰"),
            nextcord.SelectOption(label=f"Посмотреть счёта всех участников", value="show_all_users_balance", description="Посмотреть баланс всех, у кого есть хоть одна лягушка", emoji="📈"),
            nextcord.SelectOption(label=f"Перевести сколько угодно лягушек участнику", value="unlimited_transfer", description="Одарить участника сокровищем", emoji="💎"),
            nextcord.SelectOption(label=f"Установить цены", value="prices", description="Изменить текущие цены или установить дефолтные значения", emoji="🧮"),
            nextcord.SelectOption(label=f"Установить вероятности отлова", value="probabilities", description="Побыть властелином вероятностей", emoji="🕹"),
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
