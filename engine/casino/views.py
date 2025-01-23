import nextcord
import logging
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
        slot_machine = utils.set_game(player=self.player, game="slot_machine")
        await interaction.edit_original_message(
            **messages.slot_machine(),
            view=SlotMachineView(slot_machine)
        )

    @nextcord.ui.button(label="Рулетка", style=nextcord.ButtonStyle.blurple, emoji="🟢")
    async def roulette_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        roulette = utils.set_game(self.player, game="roulette")
        await interaction.edit_original_message(
            **messages.roulette(),
            view=RouletteBetsView(roulette)
        )

    @nextcord.ui.button(label="Покер на костях", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def yahtzee_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        yahtzee = utils.set_game(self.player, game="yahtzee")
        await interaction.edit_original_message(
            **messages.yahtzee(),
            view=YahtzeeView(yahtzee)
        )

    @nextcord.ui.button(label="Закрыть казино", style=nextcord.ButtonStyle.gray, emoji="❌", row=2)
    async def close_notify_message_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()


class OriginalPlayerBasicView(nextcord.ui.View):
    def __init__(self, player: nextcord.User):
        super().__init__(timeout=None)
        self.player = player

    async def interaction_check(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.player.id:
            await interaction.response.send_message(
                **messages.wrong_player_error(original_player=self.player), ephemeral=True)
            return False
        return True


class RouletteBetsView(OriginalPlayerBasicView):
    def __init__(self, roulette):
        super().__init__(player=roulette.player)
        self.roulette = roulette

    @nextcord.ui.button(label="Число", style=nextcord.ButtonStyle.blurple, emoji="🟢", row=0)
    async def straight_up_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteStraightUpBetModal(self.roulette))

    @nextcord.ui.button(label="Красное", style=nextcord.ButtonStyle.blurple, emoji="🟥", row=0)
    async def red_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("red", self.roulette))

    @nextcord.ui.button(label="Черное", style=nextcord.ButtonStyle.blurple, emoji="⬛", row=0)
    async def black_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("black", self.roulette))

    @nextcord.ui.button(label="Чет", style=nextcord.ButtonStyle.blurple, emoji="🇪", row=1)
    async def even_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("even", self.roulette))

    @nextcord.ui.button(label="Нечет", style=nextcord.ButtonStyle.blurple, emoji="🇴", row=1)
    async def odd_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("odd", self.roulette))

    @nextcord.ui.button(label="Высокие", style=nextcord.ButtonStyle.blurple, emoji="🔼", row=1)
    async def high_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("high", self.roulette))

    @nextcord.ui.button(label="Низкие", style=nextcord.ButtonStyle.blurple, emoji="🔽", row=1)
    async def low_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteBinaryBetModal("low", self.roulette))

    @nextcord.ui.button(label="Дюжина", style=nextcord.ButtonStyle.blurple, emoji="⏹️", row=2)
    async def dozen_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteTrinaryBetModal("dozen", self.roulette))

    @nextcord.ui.button(label="Ряд", style=nextcord.ButtonStyle.blurple, emoji="↔️", row=2)
    async def row_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteTrinaryBetModal("row", self.roulette))

    @nextcord.ui.button(label="Сикслайн", style=nextcord.ButtonStyle.blurple, emoji="⏸️", row=2)
    async def sixline_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RouletteSixlineBetModal(self.roulette))

    @nextcord.ui.button(label="Список всех ставок", style=nextcord.ButtonStyle.green, emoji="✅", row=4)
    async def bets_listing_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        overall_bet = self.roulette.overall_bet()
        if not overall_bet:
            return await interaction.followup.send(
                **messages.roulette_no_bets_error(), ephemeral=True)
        table_with_bets_image = self.roulette.draw(image_type='table')
        await interaction.edit_original_message(
            **messages.roulette_bets_listing(
                bets=self.roulette.bets,
                overall_bet=overall_bet,
                image_binary_data=table_with_bets_image),
            view=RouletteBetsConfirmView(self.roulette)
        )

    @nextcord.ui.button(label="Отказаться от игры в рулетку", style=nextcord.ButtonStyle.gray, emoji="❌", row=4)
    async def close_roulette_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_game(self.player, game="roulette", reset=True)
        await interaction.delete_original_message()


class RouletteStraightUpBetModal(nextcord.ui.Modal):
    def __init__(self, roulette):
        super().__init__("Сделать прямую ставку на число")
        self.roulette = roulette

        self.number = nextcord.ui.TextInput(
            label="Сектор",
            max_length=2,
            required=True,
            placeholder="Введите число в диапазоне от 0 до 36",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.number)
        self.bet_amount = nextcord.ui.TextInput(
            label="Величина ставки",
            max_length=2,
            required=True,
            placeholder="Введите размер ставки в диапазоне от 1 до 10 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        sector = utils.roulette_valid_field(self.number.value)
        if sector is False:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="straight"), ephemeral=True
            )
        bet = utils.valid_bet(self.bet_amount.value, lower_limit=1, upper_limit=10)
        if not bet:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet, self.roulette.overall_bet())
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.roulette.place_bet(category="straight", value=sector, amount=bet)
        await interaction.followup.send(
            **messages.roulette_bet_confirmation(), ephemeral=True
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

    def __init__(self, bet_type, roulette):
        super().__init__(f"Сделать ставку на {self.DESCRIPTION[bet_type][0]}")
        self.bet_type = bet_type
        self.roulette = roulette

        self.bet_amount = nextcord.ui.TextInput(
            label="Величина ставки",
            max_length=2,
            required=True,
            placeholder="Введите размер ставки в диапазоне от 5 до 25 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        bet = utils.valid_bet(self.bet_amount.value, lower_limit=5, upper_limit=25)
        if not bet:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet, self.roulette.overall_bet())
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.roulette.place_bet(category=self.DESCRIPTION[self.bet_type][1], value=self.bet_type, amount=bet)
        await interaction.followup.send(
            **messages.roulette_bet_confirmation(), ephemeral=True
        )


class RouletteTrinaryBetModal(nextcord.ui.Modal):
    DESCRIPTION = {
        'dozen': {'title': "дюжину", 'placeholder': "дюжины"},
        'row': {'title': "ряд", 'placeholder': "ряда"},
    }

    def __init__(self, bet_type, roulette):
        super().__init__(f"Сделать ставку на {self.DESCRIPTION[bet_type]['title']}")
        self.bet_type = bet_type
        self.roulette = roulette

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
            placeholder="Введите размер ставки в диапазоне от 3 до 15 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        number_of_range = utils.roulette_valid_field(self.number_of_range.value, field_type="trinary")
        if number_of_range is False:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="trinary"), ephemeral=True
            )
        bet = utils.valid_bet(self.bet_amount.value, lower_limit=3, upper_limit=15)
        if not bet:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet, self.roulette.overall_bet())
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.roulette.place_bet(category=self.bet_type, value=number_of_range, amount=bet)
        await interaction.followup.send(
            **messages.roulette_bet_confirmation(), ephemeral=True
        )


class RouletteSixlineBetModal(nextcord.ui.Modal):
    def __init__(self, roulette):
        super().__init__("Сделать ставку на сикслайн")
        self.roulette = roulette

        self.number_of_range = nextcord.ui.TextInput(
            label="Номер сикслайна",
            max_length=1,
            required=True,
            placeholder="Введите номер сикслайна в диапазоне от 1 до 6",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.number_of_range)
        self.bet_amount = nextcord.ui.TextInput(
            label="Величина ставки",
            max_length=2,
            required=True,
            placeholder="Введите размер ставки в диапазоне от 3 до 15 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        sixline = utils.roulette_valid_field(self.number_of_range.value, field_type="sixline")
        if sixline is False:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="sixline"), ephemeral=True
            )
        bet = utils.valid_bet(self.bet_amount.value, lower_limit=3, upper_limit=15)
        if not bet:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet, self.roulette.overall_bet())
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.roulette_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.roulette.place_bet(category="sixline", value=sixline, amount=bet)
        await interaction.followup.send(
            **messages.roulette_bet_confirmation(), ephemeral=True
        )


class RouletteBetsConfirmView(OriginalPlayerBasicView):
    def __init__(self, roulette):
        super().__init__(player=roulette.player)
        self.roulette = roulette

    @nextcord.ui.button(label="Подтвердить ставки", style=nextcord.ButtonStyle.green, emoji="✅")
    async def confirm_bets_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        overall_bet = self.roulette.overall_bet()
        player_balance = sql.get_user_balance(self.roulette.player)
        if player_balance - overall_bet < 0:
            return await interaction.edit_original_message(**messages.balance_error(), view=None)
        sql.set_user_balance(self.player, -overall_bet)
        self.roulette.play()
        logging.info(f"Пользователь {self.roulette.player.name} играет в рулетку "
                     f"с общей ставкой в размере {overall_bet} шт. лягушек")
        sector = self.roulette.sector
        winnings = self.roulette.winnings
        wheel_with_ball = self.roulette.draw(image_type='wheel')
        if winnings['total_payout'] > 0:
            sql.set_user_balance(self.player, winnings['total_payout'])
            logging.info(f"Пользователь {self.roulette.player.name} выиграл лягушек "
                         f"в количестве {winnings['total_payout']} шт.")
        sql.set_casino_balance(bet=overall_bet, payout=winnings['total_payout'])
        await interaction.edit_original_message(
            **messages.roulette_result(
                player=self.roulette.player,
                sector=sector,
                overall_bet=overall_bet,
                winnings=winnings,
                image_binary_data=wheel_with_ball),
            view=None
        )

    @nextcord.ui.button(label="Отказаться от игры в рулетку", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_roulette_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_game(self.roulette.player, game="roulette", reset=True)
        await interaction.delete_original_message()


class SlotMachineView(OriginalPlayerBasicView):
    def __init__(self, slot_machine):
        super().__init__(player=slot_machine.player)
        self.slot_machine = slot_machine

    async def game(self, bet_type: str, interaction: nextcord.Interaction):
        await interaction.response.defer()
        self.slot_machine.place_bet(bet_type)
        bet = self.slot_machine.bet
        player_balance = sql.get_user_balance(self.player)
        if player_balance - bet < 0:
            return await interaction.followup.send(**messages.balance_error(is_fraud=False), ephemeral=True)
        sql.set_user_balance(self.player, -self.slot_machine.bet)
        self.slot_machine.play()
        logging.info(f"Пользователь {self.slot_machine.player.name} играет в однорукого бандита "
                     f"со ставкой в размере {bet} шт. лягушек")
        result_image = self.slot_machine.draw()
        payout = self.slot_machine.payout
        if payout:
            sql.set_user_balance(self.player, payout)
            logging.info(f"Пользователь {self.slot_machine.player.name} выиграл в одноруком бандите лягушек "
                         f"в количестве {payout} шт.")
        sql.set_casino_balance(bet=bet, payout=payout)
        await interaction.edit_original_message(
            **messages.slot_machine_result(
                player=self.slot_machine.player,
                reels=self.slot_machine.reels,
                bet=bet,
                payout=payout,
                image_binary_data=result_image),
            view=None
        )

    @nextcord.ui.button(label="Трехлапая жаба", style=nextcord.ButtonStyle.blurple, emoji="💵")
    async def cheap_version_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.game('low', interaction)

    @nextcord.ui.button(label="Золото прерий", style=nextcord.ButtonStyle.blurple, emoji="💰")
    async def expensive_version_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.game('high', interaction)

    @nextcord.ui.button(label="Отказаться от игры", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_slot_machine_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_game(self.slot_machine.player, game="slot_machine", reset=True)
        await interaction.delete_original_message()


class YahtzeeView(OriginalPlayerBasicView):
    def __init__(self, yahtzee):
        super().__init__(player=yahtzee.player)
        self.yahtzee = yahtzee

    @nextcord.ui.button(label="Сделать ставку", style=nextcord.ButtonStyle.blurple, emoji="💵")
    async def place_bet_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(YahtzeeBetModal(self.yahtzee))

    @nextcord.ui.button(label="Бросить кости", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def roll_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        bet = self.yahtzee.bet
        if not bet:
            return await interaction.followup.send(**messages.yahtzee_no_bet_error(), ephemeral=True)
        player_balance = sql.get_user_balance(self.player)
        if player_balance - bet < 0:
            return await interaction.edit_original_message(**messages.balance_error(), view=None)
        sql.set_user_balance(self.yahtzee.player, -bet)
        self.yahtzee.play()
        logging.info(f"Пользователь {self.yahtzee.player.name} играет в покер на костях "
                     f"со ставкой в размере {bet} шт. лягушек")
        first_roll_outcome = self.yahtzee.roll_outcome
        first_roll_outcome_image = self.yahtzee.draw()
        payout = self.yahtzee.payout
        if payout:
            sql.set_user_balance(self.yahtzee.player, payout)
            view = None
            logging.info(f"Пользователь {self.yahtzee.player.name} выиграл в покере на костях лягушек "
                         f"в количестве {payout} шт.")
        else:
            view = YahtzeeRerollView(self.yahtzee)
        sql.set_casino_balance(bet=bet, payout=payout)
        await interaction.edit_original_message(
            **messages.yahtzee_result(
                player=self.yahtzee.player,
                bet=bet,
                payout=payout,
                roll_outcome=first_roll_outcome,
                image_binary_data=first_roll_outcome_image
            ),
            view=view)

    @nextcord.ui.button(label="Отказаться от игры", style=nextcord.ButtonStyle.gray, emoji="❌")
    async def close_yahtzee_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_game(self.player, game="yahtzee", reset=True)
        await interaction.delete_original_message()


class YahtzeeBetModal(nextcord.ui.Modal):
    def __init__(self, yahtzee):
        super().__init__("Сделать ставку")
        self.yahtzee = yahtzee

        self.bet_amount = nextcord.ui.TextInput(
            label="Величина ставки",
            max_length=2,
            required=True,
            placeholder="Введите размер ставки в диапазоне от 3 до 15 лягушек",
            style=nextcord.TextInputStyle.short
        )
        self.add_item(self.bet_amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        bet = utils.valid_bet(self.bet_amount.value, lower_limit=3, upper_limit=15)
        if not bet:
            return await interaction.followup.send(
                **messages.yahtzee_bet_confirmation(is_valid=False, category="bet"), ephemeral=True
            )
        is_enough_balance = utils.is_enough_balance(interaction.user, bet)
        if not is_enough_balance:
            return await interaction.followup.send(
                **messages.yahtzee_bet_confirmation(is_valid=False, category="balance"), ephemeral=True
            )
        self.yahtzee.place_bet(bet=bet)
        await interaction.followup.send(
            **messages.yahtzee_bet_confirmation(), ephemeral=True
        )


class YahtzeeRerollView(OriginalPlayerBasicView):
    def __init__(self, yahtzee):
        super().__init__(player=yahtzee.player)
        self.yahtzee = yahtzee

    async def set_reroll_index(self, index: int, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if len(self.yahtzee.reroll_indexes) >= 2:
            return await interaction.followup.send(**messages.yahtzee_reroll_error(), ephemeral=True)
        self.yahtzee.set_reroll(index)
        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.followup.send(**messages.yahtzee_reroll_set(index), ephemeral=True)

    @nextcord.ui.button(label="1", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def one_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.set_reroll_index(0, button, interaction)

    @nextcord.ui.button(label="2", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def two_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.set_reroll_index(1, button, interaction)

    @nextcord.ui.button(label="3", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def three_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.set_reroll_index(2, button, interaction)

    @nextcord.ui.button(label="4", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def four_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.set_reroll_index(3, button, interaction)

    @nextcord.ui.button(label="5", style=nextcord.ButtonStyle.blurple, emoji="🎲")
    async def five_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.set_reroll_index(4, button, interaction)

    @nextcord.ui.button(label="Повторный бросок", style=nextcord.ButtonStyle.green, emoji="✅", row=4)
    async def reroll_dice_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if not self.yahtzee.reroll_indexes:
            return await interaction.followup.send(**messages.yahtzee_reroll_error(is_filled=False), ephemeral=True)
        player_balance = sql.get_user_balance(self.player)
        bet = self.yahtzee.bet
        if player_balance - bet < 0:
            return await interaction.edit_original_message(**messages.balance_error(), view=None)
        self.yahtzee.play()
        second_roll_outcome = self.yahtzee.roll_outcome
        second_roll_outcome_image = self.yahtzee.draw()
        payout = self.yahtzee.payout
        if payout:
            sql.set_user_balance(self.yahtzee.player, payout)
            sql.set_casino_balance(payout=payout)
            logging.info(f"Пользователь {self.yahtzee.player.name} выиграл в покере на костях лягушек "
                         f"в количестве {payout} шт.")
        await interaction.edit_original_message(
            **messages.yahtzee_result(
                player=self.yahtzee.player,
                bet=bet,
                payout=payout,
                roll_outcome=second_roll_outcome,
                image_binary_data=second_roll_outcome_image,
                is_reroll=True
            ),
            view=None)

    @nextcord.ui.button(label="Сдаться и уйти", style=nextcord.ButtonStyle.gray, emoji="❌", row=4)
    async def close_yahtzee_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        utils.set_game(self.player, game="yahtzee", reset=True)
        await interaction.delete_original_message()
