import nextcord
import logging
import asyncio
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
        "role_lite": {"price": config.PRICES['role_lite'], "description": "Роль лягушонка"},
        "role": {"price": config.PRICES['role'], "description": "Роль лягушки"},
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
    nextcord.SelectOption(label="Роль «Лягушонок» на 1 месяц", value="role_lite", emoji=f"{config.ITEMS_EMOJI['role_lite']}"),
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
        user_balance = sql.get_user_balance(interaction.user)
        await interaction.response.defer()
        if self.price > user_balance:
            return await interaction.edit_original_message(
                **messages.insufficient_balance(),
                view=None
            )
        if self.shop_item in ["role_lite", "role"]:
            premium_roles = [
                nextcord.utils.get(interaction.guild.roles, id=config.PREMIUM_ROLE['lite']),
                nextcord.utils.get(interaction.guild.roles, id=config.PREMIUM_ROLE['basic']),
                nextcord.utils.get(interaction.guild.roles, id=config.PREMIUM_ROLE['max'])
            ]
            assigned_premium_role = next((role for role in premium_roles if role in interaction.user.roles), None)
            if assigned_premium_role:
                return await interaction.edit_original_message(
                    **messages.already_has_premium_role(interaction.user, assigned_premium_role),
                    view=None
                )
        sql.set_user_balance(interaction.user, -self.price)
        sql.set_bank_balance(self.price)
        purchased_item_message = messages.item_purchased(self.shop_item)
        if self.shop_item in ["drawing", "rain", "role_lite", "role", "band"]:
            request_to_admin = bot.client.get_user(config.ADMIN_ID)
            await request_to_admin.send(**messages.service_request(interaction.user.mention, self.shop_item))
        if self.shop_item == "role_lite":
            premium_role_lite = interaction.guild.get_role(config.PREMIUM_ROLE['lite'])
            expiration_time = utils.get_timestamp() + config.PREMIUM_ROLE_DURATION
            sql.add_premium_role_user(interaction.user, expiration_time, role_tier="lite")
            await interaction.user.add_roles(premium_role_lite)
        if self.shop_item == "role":
            premium_role_basic = interaction.guild.get_role(config.PREMIUM_ROLE['basic'])
            expiration_time = utils.get_timestamp() + config.PREMIUM_ROLE_DURATION
            sql.add_premium_role_user(interaction.user, expiration_time)
            await interaction.user.add_roles(premium_role_basic)
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
    def __init__(self, transfer_amount, other_user, original_user):
        super().__init__(timeout=None)
        self.transfer_amount = transfer_amount
        self.other_user = other_user
        self.original_user = original_user

    @nextcord.ui.button(label="Подтвердить перевод", style=nextcord.ButtonStyle.green, emoji="✅")
    async def transfer_confirm_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if interaction.user.id != self.original_user.id:
            return await interaction.edit_original_message(
                **messages.other_user_transfer_error(),
                view=None
            )
        user_balance = sql.get_user_balance(interaction.user)
        if self.transfer_amount > user_balance:
            return await interaction.edit_original_message(
                **messages.transfer_confirmation(self.other_user, self.transfer_amount, is_failed=True),
                view=None
            )
        sql.set_user_balance(interaction.user, -self.transfer_amount)
        sql.set_user_balance(self.other_user, self.transfer_amount)
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
                label="Посмотреть счёта всех участников",
                value="all_users_balance",
                description="Изучить содержимое прудов всех участников",
                emoji="📈"),
            nextcord.SelectOption(
                label="Посмотреть счёт банка",
                value="bank_balance",
                description="Посмотреть, сколько лягушек потратили участники",
                emoji="🪙"),
            nextcord.SelectOption(
                label="Посмотреть счёт казино",
                value="casino_balance",
                description="Посмотреть, сколько выиграли и проиграли участники",
                emoji="🎰"),
            nextcord.SelectOption(
                label="Статистика викторин",
                value="quiz_statistics",
                description="Посмотреть на достижения эрудитов",
                emoji="🎓"),
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
                label="Установить налог",
                value="taxes_setup",
                description="Активировать сбор налога и задать его размер",
                emoji="💸"),
            nextcord.SelectOption(
                label="Отправить сообщение от лица бота в канал новостей",
                value="post_news",
                description="Говорить от имени лягушачьего предводителя",
                emoji="💬"),
            nextcord.SelectOption(
                label="Проверить статусы обладателей ролей лягушонка и лягушки",
                value="role_manage",
                description="Кому и сколько еще осталось квакать",
                emoji="👑"),
            nextcord.SelectOption(
                label="Кэшировать файлы",
                value="cache",
                description="Выполнить при первом запуске бота",
                emoji="⚙️"),
            nextcord.SelectOption(
                label="Обнулить базу данных",
                value="reset_database",
                description="Устроить финансовый апокалипсис",
                emoji="🔪"),
        ]
    )
    async def select_admin_menu_callback(self, select, interaction: nextcord.Interaction):
        admin_actions = {
            "all_users_balance": {"message": messages.all_users_balances(), "view": None},
            "bank_balance": {"message": messages.bank_balance(), "view": None},
            "casino_balance": {"message": messages.casino_balance(), "view": None},
            "quiz_statistics": {"message": messages.quiz_statistics(), "view": None},
            "gift": {"message": messages.gift(), "view": GiftView()},
            "prices": {"message": messages.set_price(), "view": SetPriceView()},
            "probabilities": {"message": messages.set_probabilities(), "view": SetProbabilitiesView()},
            "cooldown": {"message": messages.set_cooldown(), "view": SetCooldownView()},
            "taxes_setup": {"message": messages.taxes_setup(), "view": TaxesSetupView()},
            "post_news": {"message": messages.post_news(), "view": PostNewsView()},
            "role_manage": {"message": messages.role_manage(), "view": RoleManageView()},
            "cache": {"message": messages.cache(), "view": CacheView()},
            "reset_database": {"message": messages.reset_database(), "view": ResetDatabaseView()},
        }
        await interaction.response.defer()
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
            placeholder=f"Текущая продолжительность: "
                        f"{config.CATCHING_COOLDOWN} {utils.numeral(config.CATCHING_COOLDOWN, value_type='hours')}",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.cooldown)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        is_valid = utils.validate(self.cooldown.value, check_type='cooldown')
        if is_valid:
            utils.set_cooldown(self.cooldown.value)
            logging.info(f"Администратор устанавливает величину кулдауна равной {self.cooldown.value} ч.")
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
        gift_confirmation_message = messages.gift_confirmation(other_user, self.gift_amount.value, is_valid)
        if other_user and is_valid:
            sql.set_user_balance(other_user, int(self.gift_amount.value))
            await interaction.edit_original_message(**gift_confirmation_message, view=None)
            logging.info(f"Администратор переводит пользователю {self.username.value} лягушек "
                         f"в количестве {self.gift_amount.value} шт.")
        else:
            await interaction.followup.send(**gift_confirmation_message, ephemeral=True)


class GiftView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Сделать подарок с барского плеча", style=nextcord.ButtonStyle.green, emoji="💰")
    async def gift_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(GiftModal())


class TaxesSetupModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Установить размер налога")

        self.tax = nextcord.ui.TextInput(
            label="Размер налога",
            max_length=1,
            required=True,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.tax)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        is_valid = utils.validate(self.tax.value, check_type='tax')
        if not is_valid:
            return await interaction.followup.send(
                **messages.taxes_setup_error(),
                ephemeral=True
            )
        taxation = config.TAXATION
        taxation["tax_value"] = int(self.tax.value)
        utils.set_taxation(taxation)
        logging.info(f"Администратор устанавливает размер налога, равный {self.tax.value} лягушек.")
        await interaction.edit_original_message(
            **messages.taxes_setup_confirmation_message(value=int(self.tax.value), change_tax_value=True),
            view=None
        )


class TaxesSetupView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Изменить статус налогообложения", style=nextcord.ButtonStyle.green, emoji="💵")
    async def tax_status_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        taxation = config.TAXATION
        is_taxes_active = taxation["is_taxes_active"]
        if is_taxes_active:
            taxation["is_taxes_active"] = False
            taxation["tax_collection_date"] = ""
            logging.info("Сбор налогов отключен.")
        else:
            taxation["is_taxes_active"] = True
            current_timestamp = utils.get_timestamp()
            current_month = utils.get_short_date(current_timestamp)
            taxation["tax_collection_date"] = current_month
            logging.info("Сбор налогов включен.")
        utils.set_taxation(taxation)
        await interaction.edit_original_message(
            **messages.taxes_setup_confirmation_message(
                is_taxes_set_active=taxation["is_taxes_active"],
                value=taxation["tax_value"]
            ),
            view=None
        )

    @nextcord.ui.button(label="Величина налога", style=nextcord.ButtonStyle.green, emoji="🧮")
    async def tax_value_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(TaxesSetupModal())


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
        self.image_url = nextcord.ui.TextInput(
            label="Изображение",
            placeholder="(опционально, в форматах jpg/png/gif)",
            required=False,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.image_url)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        image_binary_data, image_filename = utils.image_download(self.image_url.value)
        if self.image_url.value and not image_binary_data:
            return await interaction.followup.send(
                **messages.image_url_error(),
                ephemeral=True
            )
        channel = interaction.guild.get_channel(config.NEWS_CHANNEL_ID)
        await channel.send(**messages.news_channel_message(
            self.message_title.value, self.message_description.value, image_binary_data, image_filename))
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
        expired_premium_role_users_ids = {
            "lite": sql.remove_expired_premium_role_users(utils.get_timestamp(), role_tier="lite"),
            "basic": sql.remove_expired_premium_role_users(utils.get_timestamp())
        }
        if expired_premium_role_users_ids["lite"]:
            premium_role_lite = interaction.guild.get_role(config.PREMIUM_ROLE["lite"])
            for expired_premium_role_lite_user_id in expired_premium_role_users_ids["lite"]:
                expired_premium_role_lite_user = interaction.guild.get_member(expired_premium_role_lite_user_id[0])
                await expired_premium_role_lite_user.remove_roles(premium_role_lite)
            logging.info("Администратор снимает с участников роли лягушонка, срок использования которых истек.")
        if expired_premium_role_users_ids["basic"]:
            premium_role_basic = interaction.guild.get_role(config.PREMIUM_ROLE["basic"])
            for expired_premium_role_basic_user_id in expired_premium_role_users_ids["basic"]:
                expired_premium_role_basic_user = interaction.guild.get_member(expired_premium_role_basic_user_id[0])
                await expired_premium_role_basic_user.remove_roles(premium_role_basic)
            logging.info("Администратор снимает с участников роли лягушки, срок использования которых истек.")
        has_expired_roles = expired_premium_role_users_ids["basic"] or expired_premium_role_users_ids["lite"]
        if has_expired_roles:
            await interaction.edit_original_message(**messages.expired_roles_removal(), view=None)
        else:
            await interaction.followup.send(**messages.expired_roles_removal(has_expired_roles=False), ephemeral=True)


class CacheView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Начать кэширование", style=nextcord.ButtonStyle.green, emoji="📀")
    async def cache_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        files_count_printable = utils.refresh_cache()
        await interaction.edit_original_message(
            **messages.caching_confirmation(files_count_printable),
            view=None
        )


class ResetDatabaseModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Обнулить базу данных")

        self.database_path = nextcord.ui.TextInput(
            label="Путь к базе данных",
            required=True,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.database_path)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        is_valid = False
        if self.database_path.value == config.DATABASE_PATH:
            is_valid = utils.reset_database()
        await interaction.followup.send(**messages.reset_database_confirmation(is_valid), ephemeral=True)


class ResetDatabaseView(AdminActionBasicView):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Пусть все горит", style=nextcord.ButtonStyle.red, emoji="🔥")
    async def reset_database_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(ResetDatabaseModal())


class QuizModal(nextcord.ui.Modal):
    def __init__(self, current_quiz):
        super().__init__("Начать викторину!")
        self.current_quiz = current_quiz

        self.question = nextcord.ui.TextInput(
            label="Вопрос",
            placeholder="Текст вопроса викторины",
            required=True,
            style=nextcord.TextInputStyle.paragraph
        )
        self.add_item(self.question)
        self.answer = nextcord.ui.TextInput(
            label="Ответ",
            placeholder="Правильный ответ",
            required=True,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.answer)
        self.prize_amount = nextcord.ui.TextInput(
            label="Размер награды в лягушках",
            max_length=3,
            required=True,
            default_value="1",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.prize_amount)
        self.prize_special = nextcord.ui.TextInput(
            label="Особая награда",
            placeholder="Только для знатоков высшей лиги!",
            required=False,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.prize_special)
        self.image_url = nextcord.ui.TextInput(
            label="Изображение",
            placeholder="(опционально, в форматах jpg/png/gif)",
            required=False,
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.image_url)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        is_valid = utils.validate(self.prize_amount.value, check_type='quiz')
        if not is_valid:
            return await interaction.followup.send(
                **messages.quiz_error(reason="incorrect_prize_amount"),
                ephemeral=True
            )
        image_binary_data, image_filename = utils.image_download(self.image_url.value)
        if self.image_url.value and not image_binary_data:
            return await interaction.followup.send(
                **messages.image_url_error(),
                ephemeral=True
            )
        self.current_quiz.start(
            self.question.value,
            self.answer.value,
            self.prize_amount.value,
            self.prize_special.value
        )
        logging.info("Администратор начинает викторину.")
        await interaction.followup.send(
            **messages.quiz(self.question.value, image_binary_data, image_filename),
            allowed_mentions=nextcord.AllowedMentions(roles=True)
        )
        await asyncio.sleep(config.QUIZ_ROUND_TIME)
        await interaction.followup.send(**messages.quiz_time_up(self.answer.value))
