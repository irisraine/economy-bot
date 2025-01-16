import nextcord
import logging
import engine.bot as bot
import engine.sql as sql
import engine.casino.messages as messages
import engine.casino.utils as utils


class CasinoMenuView(nextcord.ui.View):
    def __init__(self, player):
        super().__init__(timeout=None)
        self.player = player

    @nextcord.ui.button(label="Однорукий бандит", style=nextcord.ButtonStyle.blurple, emoji="🎰")
    async def slot_machine_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        slot_machine = utils.set_game(self.player, game="slot_machine")
        await interaction.edit_original_message(
            **messages.slot_machine(),
            view=SlotMachineView(self.player, slot_machine)
        )

    @nextcord.ui.button(label="Рулетка", style=nextcord.ButtonStyle.blurple, emoji="🟢")
    async def roulette_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        roulette = utils.set_game(self.player, game="roulette")
        await interaction.edit_original_message(
            **messages.roulette(),
            view=RouletteBetsView(self.player, roulette)
        )

    @nextcord.ui.button(label="Покер на костях", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def yahtzee_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        yahtzee = utils.set_game(self.player, game="yahtzee")
        await interaction.edit_original_message(
            **messages.yahtzee(),
            view=YahtzeeView(self.player, yahtzee)
        )

    @nextcord.ui.button(label="Закрыть казино", style=nextcord.ButtonStyle.gray, emoji="❌", row=2)
    async def close_notify_message_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()

############################### РУЛЕТКА ############################

class RouletteBetsView(nextcord.ui.View):
    def __init__(self, player, roulette_game):
        super().__init__(timeout=None)
        self.player = player
        self.roulette_game = roulette_game

    @nextcord.ui.button(label="Число", style=nextcord.ButtonStyle.blurple, emoji="🟢", row=0)
    async def straight_up_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteStraightUpBetModal(self.roulette_game))

    @nextcord.ui.button(label="Красное", style=nextcord.ButtonStyle.blurple, emoji="🟥", row=0)
    async def red_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("red", self.roulette_game))

    @nextcord.ui.button(label="Черное", style=nextcord.ButtonStyle.blurple, emoji="⬛", row=0)
    async def black_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("black", self.roulette_game))

    @nextcord.ui.button(label="Чет", style=nextcord.ButtonStyle.blurple, emoji="🇪", row=1)
    async def even_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("even", self.roulette_game))

    @nextcord.ui.button(label="Нечет", style=nextcord.ButtonStyle.blurple, emoji="🇴", row=1)
    async def odd_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("odd", self.roulette_game))

    @nextcord.ui.button(label="Высокие", style=nextcord.ButtonStyle.blurple, emoji="🔼", row=1)
    async def high_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("high", self.roulette_game))

    @nextcord.ui.button(label="Низкие", style=nextcord.ButtonStyle.blurple, emoji="🔽", row=1)
    async def low_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("low", self.roulette_game))

    @nextcord.ui.button(label="Дюжина", style=nextcord.ButtonStyle.blurple, emoji="⏹️", row=2)
    async def dozen_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteTrinaryBetModal("dozen", self.roulette_game))

    @nextcord.ui.button(label="Ряд", style=nextcord.ButtonStyle.blurple, emoji="↔️", row=2)
    async def row_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteTrinaryBetModal("row", self.roulette_game))

    @nextcord.ui.button(label="Сикслайн", style=nextcord.ButtonStyle.blurple, emoji="⏸️", row=2)
    async def sixline_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteSixlineBetModal(self.roulette_game))

    @nextcord.ui.button(label="Список всех ставок", style=nextcord.ButtonStyle.green, emoji="✅", row=4)
    async def all_bets_listing_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        total_bets = self.roulette_game.overall_bet()
        if not total_bets:
            return await interaction.followup.send(
                **messages.roulette_no_bets_error(), ephemeral=True)
        self.roulette_game.draw()
        await interaction.edit_original_message(
            **messages.roulette_all_bets_listing(self.roulette_game.bets, total_bets, image_binary_data=self.roulette_game.image),
            view=RouletteBetsConfirmView(self.player, self.roulette_game)
        )

    @nextcord.ui.button(label="Отказаться от игры в рулетку", style=nextcord.ButtonStyle.gray, emoji="❌", row=4)
    async def close_roulette_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        # bot.gambling_pool[self.player]['roulette'] = None
        utils.set_game(self.player, game="roulette", reset=True)
        await interaction.delete_original_message()


class RouletteStraightUpBetModal(nextcord.ui.Modal):
    def __init__(self, roulette_game):
        super().__init__(f"Сделать прямую ставку на число")
        self.roulette_game = roulette_game

        self.number = nextcord.ui.TextInput(
            label="Сектор",
            max_length=2,
            required=True,
            placeholder=f"Введите число в диапазоне от 0 до 36",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.number)
        self.bet_amount = nextcord.ui.TextInput(
            label="Величина ставки",
            max_length=2,
            required=True,
            placeholder=f"Введите размер ставки в диапазоне от 1 до 10 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        sector = utils.get_valid_field(self.number.value)
        if sector is False:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="sector"), ephemeral=True
            )
        bet = utils.get_valid_bet(self.bet_amount.value, limit=10)
        if not bet:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet, self.roulette_game.overall_bet())
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.roulette_game.place_bet(category="straight", value=sector, amount=bet)
        await interaction.followup.send(
            **messages.roulette_single_bet_confirmation(), ephemeral=True
        )


class RouletteBinaryBetModal(nextcord.ui.Modal):
    DESCRIPTION = {
        'even': ("четные числа", "even_odd"),
        'odd': ("нечетные числа", "even_odd"),
        'red': ("красное", "color"),
        'black': ("черное", "color"),
        'high': ("высокие числа", "high_low"),
        'low': ("низкие числа", "high_low")
    }

    def __init__(self, bet_type, roulette_game):
        super().__init__(f"Сделать ставку на {self.DESCRIPTION[bet_type][0]}")
        self.bet_type = bet_type
        self.roulette_game = roulette_game

        self.bet_amount = nextcord.ui.TextInput(
            label="Величина ставки",
            max_length=2,
            required=True,
            placeholder=f"Введите размер ставки в диапазоне от 1 до 25 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        bet = utils.get_valid_bet(self.bet_amount.value, limit=25)
        if not bet:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet, self.roulette_game.overall_bet())
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.roulette_game.place_bet(category=self.DESCRIPTION[self.bet_type][1], value=self.bet_type, amount=bet)
        await interaction.followup.send(
            **messages.roulette_single_bet_confirmation(), ephemeral=True
        )


class RouletteTrinaryBetModal(nextcord.ui.Modal):
    DESCRIPTION = {
        'dozen': {'title': "дюжину", 'placeholder': "дюжины"},
        'row': {'title': "ряд", 'placeholder': "ряда"},
    }

    def __init__(self, bet_type, roulette_game):
        super().__init__(f"Сделать ставку на {self.DESCRIPTION[bet_type]['title']}")
        self.bet_type = bet_type
        self.roulette_game = roulette_game

        self.number_of_range = nextcord.ui.TextInput(
            label=f"Номер {self.DESCRIPTION[bet_type]['placeholder']}",
            max_length=1,
            required=True,
            placeholder=f"Введите номер {self.DESCRIPTION[bet_type]['placeholder']} в диапазоне от 1 до 3",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.number_of_range)
        self.bet_amount = nextcord.ui.TextInput(
            label="Величина ставки",
            max_length=2,
            required=True,
            placeholder=f"Введите размер ставки в диапазоне от 1 до 25 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        number_of_range = utils.get_valid_field(self.number_of_range.value, field_type="trinary")
        if number_of_range is False:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="trinary"), ephemeral=True
            )
        bet = utils.get_valid_bet(self.bet_amount.value, limit=25)
        if not bet:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet, self.roulette_game.overall_bet())
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.roulette_game.place_bet(category=self.bet_type, value=number_of_range, amount=bet)
        await interaction.followup.send(
            **messages.roulette_single_bet_confirmation(), ephemeral=True
        )

class RouletteSixlineBetModal(nextcord.ui.Modal):
    def __init__(self, roulette_game):
        super().__init__(f"Сделать ставку на сикслайн")
        self.roulette_game = roulette_game

        self.number_of_range = nextcord.ui.TextInput(
            label=f"Номер сикслайна",
            max_length=1,
            required=True,
            placeholder=f"Введите номер сикслайна в диапазоне от 1 до 6",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.number_of_range)
        self.bet_amount = nextcord.ui.TextInput(
            label="Величина ставки",
            max_length=2,
            required=True,
            placeholder=f"Введите размер ставки в диапазоне от 1 до 25 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        sixline = utils.get_valid_field(self.number_of_range.value, field_type="sixline")
        if sixline is False:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="sixline"), ephemeral=True
            )
        bet = utils.get_valid_bet(self.bet_amount.value, limit=25)
        if not bet:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet, self.roulette_game.overall_bet())
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.roulette_game.place_bet(category="sixline", value=sixline, amount=bet)
        await interaction.followup.send(
            **messages.roulette_single_bet_confirmation(), ephemeral=True
        )


class RouletteBetsConfirmView(nextcord.ui.View):
    def __init__(self, player, roulette_game):
        super().__init__(timeout=None)
        self.player = player
        self.roulette_game = roulette_game

    @nextcord.ui.button(label="Подтвердить ставки", style=nextcord.ButtonStyle.green, emoji="✅")
    async def confirm_bets_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        total_bets = self.roulette_game.overall_bet()
        player_balance = sql.get_user_balance(self.player)
        if player_balance - total_bets < 0:
            return await interaction.edit_original_message(**messages.balance_error(), view=None)
        self.roulette_game.spin()
        logging.info(f"Пользователь {self.player.name} играет в рулетку.")
        number, color = self.roulette_game.result, self.roulette_game.COLORS[self.roulette_game.result]
        payout = self.roulette_game.calculate_payout()
        income = payout["total_winnings"] - total_bets
        if income:
            sql.set_user_balance(self.player, income)
        outcome = "выиграл" if income > 0 else "проиграл"
        if income != 0:
            logging.info(f"Пользователь {self.player.name} {outcome} лягушек в количестве {abs(income)} шт.")
        await interaction.edit_original_message(
            **messages.roulette_result(self.player, number, color, total_bets, payout),
            view=None
        )

    @nextcord.ui.button(label="Отказаться от игры в рулетку", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_roulette_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        bot.gambling_pool[self.player]['roulette'] = None
        await interaction.delete_original_message()


class RouletteNoBetsView(nextcord.ui.View):
    def __init__(self, player, roulette_game):
        super().__init__(timeout=None)
        self.player = player
        self.roulette_game = roulette_game

    @nextcord.ui.button(label="Вернуться к ставкам", style=nextcord.ButtonStyle.green, emoji="◀️")
    async def return_to_bets_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(
            **messages.roulette(),
            view=RouletteBetsView(self.player, self.roulette_game)
        )

    @nextcord.ui.button(label="Отказаться от игры в рулетку", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_roulette_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        bot.gambling_pool[self.player]['roulette'] = None
        await interaction.delete_original_message()

############################### ОДНОРУКИЙ БАНДИТ ############################

class SlotMachineView(nextcord.ui.View):
    def __init__(self, player, slot_machine_game):
        super().__init__(timeout=None)
        self.player = player
        self.slot_machine_game = slot_machine_game

    @nextcord.ui.button(label="Жабий чвяк", style=nextcord.ButtonStyle.blurple, emoji="💵")
    async def cheap_version_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        self.slot_machine_game.place_bet('low')
        sql.set_user_balance(self.player, -self.slot_machine_game.BETS['low'])
        self.slot_machine_game.play()
        winning = self.slot_machine_game.winning
        if winning:
            sql.set_user_balance(self.player, winning)
        reels = self.slot_machine_game.reels
        await interaction.edit_original_message(
            **messages.slot_machine_result(self.player, reels, winning, image_binary_data=self.slot_machine_game.image),
            view=None
        )

    @nextcord.ui.button(label="Отчаянный ковбой", style=nextcord.ButtonStyle.blurple, emoji="💰")
    async def expensive_version_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        self.slot_machine_game.place_bet('high')
        sql.set_user_balance(self.player, -self.slot_machine_game.BETS['high'])
        self.slot_machine_game.play()
        winning = self.slot_machine_game.winning
        if winning:
            sql.set_user_balance(self.player, winning)
        reels = self.slot_machine_game.reels
        await interaction.edit_original_message(
            **messages.slot_machine_result(self.player, reels, winning, image_binary_data=self.slot_machine_game.image),
            view=None
        )

    @nextcord.ui.button(label="Отказаться от игры", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_slot_machine_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        # bot.gambling_pool[self.player]['slot_machine'] = None
        utils.set_game(self.player, game="slot_machine", reset=True)
        await interaction.delete_original_message()

############################### ПОКЕР НА КОСТЯХ ############################

class YahtzeeView(nextcord.ui.View):
    def __init__(self, player, yahtzee_game):
        super().__init__(timeout=None)
        self.player = player
        self.yahtzee_game = yahtzee_game

    @nextcord.ui.button(label="Сделать ставку", style=nextcord.ButtonStyle.blurple, emoji="💵")
    async def place_bet_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(YahtzeeBetModal(self.yahtzee_game))

    @nextcord.ui.button(label="Бросить кости", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def roll_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if self.yahtzee_game.bet == 0:
            return await interaction.followup.send(**messages.yahtzee_no_bet_error(), ephemeral=True)
        player_balance = sql.get_user_balance(self.player)
        if player_balance - self.yahtzee_game.bet < 0:
            return await interaction.edit_original_message(**messages.balance_error(), view=None)
        sql.set_user_balance(self.player, -self.yahtzee_game.bet)
        self.yahtzee_game.roll_dice()
        logging.info(f"Пользователь {self.player.name} играет в покер на костях.")
        first_roll_result = self.yahtzee_game.dice
        self.yahtzee_game.draw()
        self.yahtzee_game.check_winning_combinations()
        winning_combination = self.yahtzee_game.winning_combination
        if not winning_combination:
            await interaction.edit_original_message(
                **messages.yahtzee_roll_result_no_winning(final_roll=False, dice=first_roll_result, image_binary_data=self.yahtzee_game.image),
                view=YahtzeeRerollView(self.player, self.yahtzee_game))
        else:
            self.yahtzee_game.calculate_winnings()
            winnings = self.yahtzee_game.winnings
            sql.set_user_balance(self.player, winnings)
            logging.info(f"Пользователь {self.player.name} выиграл в покер на костях лягушек в количестве {winnings - self.yahtzee_game.bet} шт.")
            return await interaction.edit_original_message(
                **messages.yahtzee_roll_result_winning(self.player, winning_combination, self.yahtzee_game.bet,
                                                       winnings, first_roll_result, image_binary_data=self.yahtzee_game.image),
                view=None)

    @nextcord.ui.button(label="Отказаться от игры", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_yahtzee_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        # bot.gambling_pool[self.player]['yahtzee'] = None
        utils.set_game(self.player, game="yahtzee", reset=True)
        await interaction.delete_original_message()


class YahtzeeBetModal(nextcord.ui.Modal):
    def __init__(self, yahtzee_game):
        super().__init__(f"Сделать ставку")
        self.yahtzee_game = yahtzee_game

        self.bet_amount = nextcord.ui.TextInput(
            label="Величина ставки",
            max_length=2,
            required=True,
            placeholder=f"Введите размер ставки в диапазоне от 3 до 15 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        bet = utils.get_valid_bet(self.bet_amount.value, lower_limit=3, limit=15)
        if not bet:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet)
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.roulette_single_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.yahtzee_game.place_bet(amount=bet)
        await interaction.followup.send(
            **messages.roulette_single_bet_confirmation(), ephemeral=True
        )

class YahtzeeRerollView(nextcord.ui.View):
    def __init__(self, player, yahtzee_game):
        super().__init__(timeout=None)
        self.player = player
        self.yahtzee_game = yahtzee_game

    @nextcord.ui.button(label="1", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def one_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if len(self.yahtzee_game.reroll_indexes) < 2:
            self.yahtzee_game.set_reroll(0)
            button.disabled = True
            await interaction.message.edit(view=self)
            return await interaction.followup.send(**messages.yahtzee_reroll_set(0), ephemeral=True)
        else:
            return await interaction.followup.send(**messages.yahtzee_reroll_error(), ephemeral=True)

    @nextcord.ui.button(label="2", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def two_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if len(self.yahtzee_game.reroll_indexes) < 2:
            self.yahtzee_game.set_reroll(1)
            button.disabled = True
            await interaction.message.edit(view=self)
            return await interaction.followup.send(**messages.yahtzee_reroll_set(1), ephemeral=True)
        else:
            return await interaction.followup.send(**messages.yahtzee_reroll_error(), ephemeral=True)

    @nextcord.ui.button(label="3", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def three_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if len(self.yahtzee_game.reroll_indexes) < 2:
            self.yahtzee_game.set_reroll(2)
            button.disabled = True
            await interaction.message.edit(view=self)
            return await interaction.followup.send(**messages.yahtzee_reroll_set(2), ephemeral=True)
        else:
            return await interaction.followup.send(**messages.yahtzee_reroll_error(), ephemeral=True)

    @nextcord.ui.button(label="4", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def four_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if len(self.yahtzee_game.reroll_indexes) < 2:
            self.yahtzee_game.set_reroll(3)
            button.disabled = True
            await interaction.message.edit(view=self)
            return await interaction.followup.send(**messages.yahtzee_reroll_set(3), ephemeral=True)
        else:
            return await interaction.followup.send(**messages.yahtzee_reroll_error(), ephemeral=True)

    @nextcord.ui.button(label="5", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def five_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if len(self.yahtzee_game.reroll_indexes) < 2:
            self.yahtzee_game.set_reroll(4)
            button.disabled = True
            await interaction.message.edit(view=self)
            return await interaction.followup.send(**messages.yahtzee_reroll_set(4), ephemeral=True)
        else:
            return await interaction.followup.send(**messages.yahtzee_reroll_error(), ephemeral=True)

    @nextcord.ui.button(label="Повторный бросок", style=nextcord.ButtonStyle.green, emoji="✅", row=4)
    async def reroll_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if len(self.yahtzee_game.reroll_indexes) == 0:
            return await interaction.followup.send(**messages.yahtzee_reroll_error(is_filled=False), ephemeral=True)
        player_balance = sql.get_user_balance(self.player)
        if player_balance - self.yahtzee_game.bet < 0:
            return await interaction.edit_original_message(**messages.balance_error(), view=None)
        self.yahtzee_game.reroll_dice()
        final_roll_result = self.yahtzee_game.dice
        self.yahtzee_game.draw()
        self.yahtzee_game.check_winning_combinations()
        winning_combination = self.yahtzee_game.winning_combination
        if not winning_combination:
            logging.info(f"Пользователь {self.player.name} проиграл в покер на костях лягушек в количестве {self.yahtzee_game.bet} шт.")
            await interaction.edit_original_message(
                **messages.yahtzee_roll_result_no_winning(self.player, final_roll=True, bet=self.yahtzee_game.bet,
                                                          dice=final_roll_result, image_binary_data=self.yahtzee_game.image),
                view=None)
        else:
            self.yahtzee_game.calculate_winnings()
            winnings = self.yahtzee_game.winnings
            sql.set_user_balance(self.player, winnings)
            return await interaction.edit_original_message(
                **messages.yahtzee_roll_result_winning(self.player, winning_combination, self.yahtzee_game.bet,
                                                       winnings, final_roll_result, image_binary_data=self.yahtzee_game.image),
                view=None)

    @nextcord.ui.button(label="Сдаться и уйти", style=nextcord.ButtonStyle.gray, emoji="❌", row=4)
    async def close_yahtzee_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_game(self.player, game="yahtzee", reset=True)
        await interaction.delete_original_message()