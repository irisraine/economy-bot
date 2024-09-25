import nextcord
import logging
import engine.bot as bot
import engine.sql as sql
import engine.messages as messages
import engine.utils as utils
import engine.config as config


def items():
    return {
        "track": {"price": config.PRICES['track'], "description": "Трек про Леху"},
        "frog": {"price": config.PRICES['frog'], "description": "Лягушку"},
        "cite": {"price": config.PRICES['cite'], "description": "Мудрую мысль"},
        "animal": {"price": config.PRICES['animal'], "description": "Питомца"},
        "meme": {"price": config.PRICES['meme'], "description": "Мем"},
        "food": {"price": config.PRICES['food'], "description": "Пищу аристократов"},
        "soundpad": {"price": config.PRICES['soundpad'], "description": "Саундпад"},
        "drawing": {"price": config.PRICES['drawing'], "description": "Скетч"},
        "rain": {"price": config.PRICES['rain'], "description": "Дождь из лягушек"},
        "event": {"price": config.PRICES['event'], "description": "Ивент"},
        "role": {"price": config.PRICES['role'], "description": "Роль"},
        "band": {"price": config.PRICES['band'], "description": "Банду"},
    }


def probabilities():
    return {
        "common": int(config.PROBABILITIES['common'] * 100),
        "uncommon": int(config.PROBABILITIES['uncommon'] * 100),
        "epic": int(config.PROBABILITIES['epic'] * 100),
        "legendary": int(config.PROBABILITIES['legendary'] * 100)
    }


options = [
    nextcord.SelectOption(label="Послушать случайный трек про Леху", value="track", emoji=f"{config.ITEMS_EMOJI['track']}"),
    nextcord.SelectOption(label="Случайная лягушка", value="frog", emoji=f"{config.ITEMS_EMOJI['frog']}"),
    nextcord.SelectOption(label="Случайная мудрая мысль на день", value="cite", emoji=f"{config.ITEMS_EMOJI['cite']}"),
    nextcord.SelectOption(label="Случайное фото домашнего любимца", value="animal", emoji=f"{config.ITEMS_EMOJI['animal']}"),
    nextcord.SelectOption(label="Случайный мем", value="meme", emoji=f"{config.ITEMS_EMOJI['meme']}"),
    nextcord.SelectOption(label="Сделать заказ в ресторане «Жабий квак»", value="food", emoji=f"{config.ITEMS_EMOJI['food']}"),
    nextcord.SelectOption(label="Случайный саундпад Лехи", value="soundpad", emoji=f"{config.ITEMS_EMOJI['soundpad']}"),
    nextcord.SelectOption(label="Авторский скетч", value="drawing", emoji=f"{config.ITEMS_EMOJI['drawing']}"),
    nextcord.SelectOption(label="Дождь из лягушек", value="rain", emoji=f"{config.ITEMS_EMOJI['rain']}"),
    nextcord.SelectOption(label="Ивент", value="event", emoji=f"{config.ITEMS_EMOJI['event']}"),
    nextcord.SelectOption(label="Роль «Легушька» на 1 месяц", value="role", emoji=f"{config.ITEMS_EMOJI['role']}"),
    nextcord.SelectOption(label="Создать свою банду", value="band", emoji=f"{config.ITEMS_EMOJI['band']}"),
]


class ShopMenuView(nextcord.ui.View):
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
            **messages.purchasing_confirmation(item, price),
            view=PurchaseView(price, select.values[0])
        )

    @nextcord.ui.button(label="Закрыть магазин", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()


class PurchaseView(nextcord.ui.View):
    def __init__(self, price, shop_item):
        super().__init__(timeout=None)
        self.price = price
        self.shop_item = shop_item

    @nextcord.ui.button(label="Приобрести товар", style=nextcord.ButtonStyle.green, emoji="💵")
    async def purchase_confirm_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_balance = sql.get_user_balance(interaction.user.id)
        await interaction.response.defer()
        if user_balance is None:
            sql.create_user_balance(interaction.user.id, interaction.user.name)
            user_balance = sql.get_user_balance(interaction.user.id)
        if self.price > user_balance:
            await interaction.edit_original_message(
                **messages.insufficient_balance(),
                view=None
            )
        else:
            sql.set_user_balance(interaction.user.id, -self.price)
            sql.set_bank_balance(self.price)
            purchased_item_message = messages.item_purchased(self.shop_item)
            if self.shop_item in ["drawing", "rain", "event", "role", "band"]:
                request_to_admin = bot.client.get_user(config.ADMIN_ID)
                await request_to_admin.send(**messages.service_request(interaction.user.mention, self.shop_item))
            if self.shop_item == "role":
                premium_role = interaction.guild.get_role(config.PREMIUM_ROLE_ID)
                expiration_time = utils.get_timestamp() + config.PREMIUM_ROLE_DURATION
                sql.add_premium_role_owner(interaction.user.id, interaction.user.name, expiration_time)
                await interaction.user.add_roles(premium_role)
            logging.info(f"Пользователь {interaction.user.name} покупает предмет из категории '{self.shop_item}'.")
            await interaction.edit_original_message(
                **purchased_item_message,
                view=None
            )

    @nextcord.ui.button(label="Вернуться к прилавку", style=nextcord.ButtonStyle.gray, emoji="◀️")
    async def return_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            **messages.shop(),
            view=ShopMenuView()
        )


class TransferView(nextcord.ui.View):
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
                **messages.transfer_confirmation(self.other_user, self.transfer_amount, is_failed=True),
                view=None
            )
        if sql.get_user_balance(self.other_user.id) is None:
            sql.create_user_balance(self.other_user.id, self.other_user.name)
        sql.set_user_balance(interaction.user.id, -self.transfer_amount)
        sql.set_user_balance(self.other_user.id, self.transfer_amount)
        logging.info(f"Пользователь {interaction.user.name} переводит пользователю {self.other_user.name} лягушек "
                     f"в количестве {self.transfer_amount} шт.")
        await interaction.edit_original_message(
            **messages.transfer_confirmation(self.other_user, self.transfer_amount),
            view=None
        )

    @nextcord.ui.button(label="Отказаться от перевода", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()


class AdminMenuView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: nextcord.Interaction):
        if interaction.user.guild_permissions.administrator:
            return True
        else:
            await interaction.response.send_message(**messages.admin_option_only_warning(), ephemeral=True)
            return False

    @nextcord.ui.select(
        placeholder="Выбери нужную опцию",
        options=[
            nextcord.SelectOption(
                label="Кэшировать файлы",
                value="cache",
                description="Выполнить при первом запуске бота",
                emoji="⚙️"),
            nextcord.SelectOption(
                label="Посмотреть счёт банка",
                value="bank_balance",
                description="Посмотреть, сколько лягушек потратили участники",
                emoji="🪙"),
            nextcord.SelectOption(
                label="Посмотреть счёта всех участников",
                value="all_users_balance",
                description="Изучить содержимое прудов всех участников",
                emoji="📈"),
            nextcord.SelectOption(
                label="Перевести сколько угодно лягушек участнику",
                value="gift",
                description="Одарить участника болотным сокровищем",
                emoji="💎"),
            nextcord.SelectOption(
                label="Установить цены",
                value="prices",
                description="Изменить текущие цены или установить дефолтные",
                emoji="🧮"),
            nextcord.SelectOption(
                label="Установить вероятности отлова",
                value="probabilities",
                description="Побыть властелином вероятностей",
                emoji="🕹"),
            nextcord.SelectOption(
                label="Установить кулдаун",
                value="cooldown",
                description="Определить допустимую частоту отлова",
                emoji="⏰"),
            nextcord.SelectOption(
                label="Отправить любое сообщение от имени бота в салун",
                value="post_news",
                description="Говорить от имени лягушачьего предводителя",
                emoji="💬"),
            nextcord.SelectOption(
                label="Проверить статусы обладателей роли лягушки",
                value="role_manage",
                description="Кому и сколько еще осталось квакать",
                emoji="👑"),
        ]
    )
    async def select_admin_menu_callback(self, select, interaction: nextcord.Interaction):
        admin_actions = {
            "bank_balance": {"message": messages.bank_balance(), "view": AdminActionBasicView()},
            "all_users_balance": {"message": messages.all_users_balances(), "view": AdminActionBasicView()},
            "gift": {"message": messages.gift(), "view": GiftView()},
            "prices": {"message": messages.set_price(), "view": SetPriceView()},
            "probabilities": {"message": messages.set_probabilities(), "view": SetProbabilitiesView()},
            "cooldown": {"message": messages.set_cooldown(), "view": SetCooldownView()},
            "post_news": {"message": messages.post_news(), "view": PostNewsView()},
            "role_manage": {"message": messages.role_manage(), "view": RoleManageView()},
        }
        await interaction.response.defer()

        if select.values[0] == "cache":
            files_count_printable = utils.refresh_cache()
            await interaction.edit_original_message(
                **messages.caching_confirmation(files_count_printable),
                view=AdminActionBasicView()
            )
        else:
            await interaction.edit_original_message(
                **admin_actions[select.values[0]]["message"],
                view=admin_actions[select.values[0]]["view"]
            )

    @nextcord.ui.button(label="Закрыть админку", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()


class AdminActionBasicView(nextcord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(timeout=None, *args, **kwargs)

    async def interaction_check(self, interaction: nextcord.Interaction):
        if interaction.user.guild_permissions.administrator:
            return True
        else:
            await interaction.response.send_message(**messages.admin_option_only_warning(), ephemeral=True)
            return False

    @nextcord.ui.button(label="Вернуться в админку", style=nextcord.ButtonStyle.gray, emoji="◀️", row=2)
    async def return_to_admin_menu_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            **messages.admin(),
            view=AdminMenuView()
        )

    @nextcord.ui.button(label="Закрыть", style=nextcord.ButtonStyle.gray, emoji="❌", row=2)
    async def close_notify_message_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()


class SetPriceModal(nextcord.ui.Modal):
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
        is_valid = utils.validate(self.price.value, check_type='price')
        if is_valid:
            utils.set_price(self.item, self.price.value)
            logging.info(f"Администратор устанавливает цену на товар из категории '{self.item}' "
                         f"равной {self.price.value} лягушек.")
        await interaction.followup.send(**messages.set_price_confirmation(is_valid), ephemeral=True)


class SetPriceView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.select(
        placeholder="Выбери нужный товар",
        options=options
    )
    async def set_price_callback(self, select, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SetPriceModal(select.values[0]))

    @nextcord.ui.button(label="Установить цены по умолчанию", style=nextcord.ButtonStyle.green, emoji="💲")
    async def default_prices_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_price(reset=True)
        logging.info("Администратор устанавливает стандартные цены на все товары в магазине.")
        await interaction.followup.send(**messages.reset_prices_confirmation(), ephemeral=True)


class SetProbabilitiesModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Установить значения вероятностей поимки")

        self.common = nextcord.ui.TextInput(
            label="Стандартный улов",
            max_length=4,
            required=True,
            placeholder=f"Текущая вероятность: {probabilities()['common']} %",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.common)
        self.uncommon = nextcord.ui.TextInput(
            label="Редкий улов",
            max_length=4,
            required=True,
            placeholder=f"Текущая вероятность: {probabilities()['uncommon']} %",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.uncommon)
        self.epic = nextcord.ui.TextInput(
            label="Эпичный улов",
            max_length=4,
            required=True,
            placeholder=f"Текущая вероятность: {probabilities()['epic']} %",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.epic)
        self.legendary = nextcord.ui.TextInput(
            label="Легендарный улов",
            max_length=4,
            required=True,
            placeholder=f"Текущая вероятность: {probabilities()['legendary']} %",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.legendary)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        updated_probabilities = {
            "common": self.common.value,
            "uncommon": self.uncommon.value,
            "epic": self.epic.value,
            "legendary": self.legendary.value
        }
        is_valid = utils.validate(updated_probabilities, check_type='probabilities')
        if is_valid:
            utils.set_probabilities(updated_probabilities)
            logging.info("Администратор устанавливает новые вероятности отлова лягушек: "
                         f"стандартный - {self.common.value}%, "
                         f"редкий - {self.uncommon.value}%, "
                         f"эпичный - {self.epic.value}%, "
                         f"легендарный - {self.legendary.value}%. ")
        await interaction.followup.send(**messages.set_probabilities_confirmation(is_valid), ephemeral=True)


class SetProbabilitiesView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Установить вероятности", style=nextcord.ButtonStyle.green, emoji="🎲")
    async def set_probabilities_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SetProbabilitiesModal())

    @nextcord.ui.button(label="По умолчанию", style=nextcord.ButtonStyle.green, emoji="💯")
    async def default_probabilities_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_probabilities(reset=True)
        logging.info("Администратор устанавливает стандартные вероятности отлова лягушек.")
        await interaction.followup.send(**messages.reset_probabilities_confirmation(), ephemeral=True)


class SetCooldownModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Установить значения времени между ловлей")

        self.cooldown = nextcord.ui.TextInput(
            label="Кулдаун",
            max_length=2,
            required=True,
            placeholder=f"Текущая продолжительность: {config.CATCHING_COOLDOWN} часов",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.cooldown)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        is_valid = utils.validate(self.cooldown.value, check_type='cooldown')
        if is_valid:
            utils.set_cooldown(self.cooldown.value)
            logging.info(f"Администратор устанавливает величину кулдауна равной {self.cooldown.value} часов.")
        await interaction.followup.send(**messages.set_cooldown_confirmation(is_valid), ephemeral=True)


class SetCooldownView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Установить кулдаун", style=nextcord.ButtonStyle.green, emoji="⏳")
    async def set_cooldown_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SetCooldownModal())

    @nextcord.ui.button(label="По умолчанию", style=nextcord.ButtonStyle.green, emoji="⏱")
    async def default_cooldown_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_cooldown(reset=True)
        logging.info("Администратор устанавливает стандартную величину кулдауна.")
        await interaction.followup.send(**messages.reset_cooldown_confirmation(), ephemeral=True)


class GiftModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Подарить участнику болотное сокровище")

        self.username = nextcord.ui.TextInput(
            label="Discord username",
            required=True,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.username)
        self.gift_amount = nextcord.ui.TextInput(
            label="Количество лягушек",
            max_length=4,
            required=True,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.gift_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        is_valid = utils.validate(self.gift_amount.value, check_type='gift')
        other_user = nextcord.utils.get(bot.client.get_all_members(), name=self.username.value)
        if other_user and is_valid:
            if sql.get_user_balance(other_user.id) is None:
                sql.create_user_balance(other_user.id, self.username.value)
            sql.set_user_balance(other_user.id, int(self.gift_amount.value))
            logging.info(f"Администратор переводит пользователю {self.username.value} лягушек "
                         f"в количестве {self.gift_amount.value} шт.")
        await interaction.followup.send(**messages.gift_confirmation(other_user, self.gift_amount.value, is_valid))


class GiftView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Сделать подарок с барского плеча", style=nextcord.ButtonStyle.green, emoji="💰")
    async def gift_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(GiftModal())


class PostNewsWindow(nextcord.ui.Modal):
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
        await channel.send(**messages.news_channel_message(self.message_title.value, self.message_description.value))
        logging.info(f"Администратор отправляет сообщение '{self.message_description.value}' в новостной канал.")
        await interaction.followup.send(**messages.post_news_confirmation(), ephemeral=True)


class PostNewsView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Создать и опубликовать новость", style=nextcord.ButtonStyle.green, emoji="🗞")
    async def send_message_by_bot_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(PostNewsWindow())


class RoleManageView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Снять просроченные роли", style=nextcord.ButtonStyle.green, emoji="➖")
    async def remove_expired_roles_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        expired_premium_role_owners_ids = sql.remove_expired_premium_role_owners(utils.get_timestamp())
        if expired_premium_role_owners_ids:
            premium_role = interaction.guild.get_role(config.PREMIUM_ROLE_ID)
            for expired_premium_role_owner_id in expired_premium_role_owners_ids:
                expired_premium_role_owner = interaction.guild.get_member(expired_premium_role_owner_id[0])
                await expired_premium_role_owner.remove_roles(premium_role)
            logging.info("Администратор снимает с участников роли, срок использования которых истек.")
        await interaction.followup.send(**messages.role_expired_and_removed(expired_premium_role_owners_ids),
                                        ephemeral=True)
