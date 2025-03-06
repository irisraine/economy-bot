import nextcord
import io
import engine.casino.config as config
from engine.config import FROG_EMOJI, BASIC_COLOR_CODE, ERROR_COLOR_CODE
import engine.casino.utils as utils

ERROR_HEADER = "Ошибка"
SUCCESS_HEADER = "Успешно"


class MessageContainer:
    def __init__(self, title=None, description=None, file_path=None, image_binary_data=None):
        self.__embed = None
        fp = io.BytesIO(image_binary_data) if image_binary_data else file_path
        file_name = file_path.split('/')[-1]
        color = BASIC_COLOR_CODE if title != ERROR_HEADER else ERROR_COLOR_CODE
        self.__embed = nextcord.Embed(
            title=title,
            description=description,
            colour=nextcord.Colour.from_rgb(*color),
        )
        image_attachment = f"attachment://{file_name}"
        self.__embed.set_image(url=image_attachment)
        self.__file = nextcord.File(fp=fp, filename=file_name)

    @property
    def embed(self):
        return self.__embed

    @property
    def file(self):
        return self.__file


def casino():
    embed_message = MessageContainer(
        title="**Добро пожаловать в болотное казино «Три лягушки»!**",
        description="Для тебя открывает двери первое в мире казино на лаграсских болотах, где ты сможешь испытать "
                    "собственную удачу. Стань богат, как никогда прежде и покинь наше заведение с карманами, полными "
                    "лягушек - или уйди ни с чем и оставь здесь последние драные штаны. "
                    "Ибо, как писал великий поэт: \n\n *Умей поставить в радостной надежде \nНа карту все, "
                    "что накопил с трудом - \nВсе проиграй, и нищим стань как прежде, \nИ никогда не пожалей о том!*",
        file_path=config.CASINO_ENTRANCE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def slot_machine():
    embed_message = MessageContainer(
        title="**Однорукий бандит**",
        description=f"Испытай свою удачу и сорви лягушачий джекпот! Выбирай между двумя режимами игры: "
                    f"дешевой «Однолапой жабой» и дорогой «Трехлапой жабой»!\n"
                    f"После выбора режима дергай за рычаг и жди, пока замершие барабаны не отобразят результат игры "
                    f"на центральной линии.\n\n"
                    f"- **Однолапая жаба** "
                    f"(стоимость игры **{config.SLOT_MACHINE_BET_AMOUNTS['low']}** {FROG_EMOJI})\n"
                    f"Это классический режим для тех, кто хочет испытать свою удачу без лишнего риска. На барабане "
                    f"всего три типа символов - лягушки разных цветов, а вероятность победы ниже.\n\n"
                    f"*Выигрышные комбинации:*\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_white'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_orange'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_green'][3]}** {FROG_EMOJI}\n\n"
                    f"- **Трехлапая жаба** "
                    f"(стоимость игры **{config.SLOT_MACHINE_BET_AMOUNTS['high']}** {FROG_EMOJI})\n"
                    f"Для настоящих искателей приключений! Этот режим обойдется тебе дороже, однако предлагает более "
                    f"высокие шансы на выигрыш, а также существенно более крупные награды.\n\n"
                    f"*Выигрышные комбинации:*\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['gold'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['cart']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['cart']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['cart']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['cart'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['star']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['star']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['star']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['star'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['horseshoe']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['horseshoe']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['horseshoe']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['horseshoe'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['moonshine']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['moonshine']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['moonshine']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['moonshine'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} :x:** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['gold'][2]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_white'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_orange'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']}** "
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_green'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} :x: :x:**"
                    f" - выплата **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['gold'][1]}** {FROG_EMOJI}\n\n"
                    f"Дерзай! Ведь кто не рискует, тот не пьёт с лягушками шампанское!",
        file_path=config.SLOT_MACHINE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def slot_machine_result(player, reels, bet, payout, image_binary_data):
    income = payout - bet
    description = ("Ты наблюдаешь за мелькающими символами, чувствуя, как напряжение нарастает. И вот барабаны "
                   "замедляются, один за другим встают на место - и ты видишь результат. \n\n")
    if payout == 0:
        title = "Увы и ах, тебе не повезло!"
        description += (f"К сожалению, символы центральной линии не сложились ни в одну из выигрышных комбинаций! "
                        f"<@{player.id}>, сегодня **ты проиграл {bet}** {FROG_EMOJI}\n"
                        f"Ты чувствуешь разочарование. Но прислушайся к себе - и услышишь, как азарт шепчет: попробуй "
                        f"еще раз!\n\nУдачи в следующей игре! 🍀")
    elif payout == bet:
        title = "Ни дать, ни взять"
        description += (f"На центральной линии не сложилось ни одной из выигрышных комбинаций. Тем не менее, благодаря "
                        f"единственному выпавшему символу {config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} ты "
                        f"заработал **{config.SLOT_MACHINE_PAYOUT_AMOUNTS['gold'][1]}** {FROG_EMOJI} и вернул свою "
                        f"ставку! Не выигрыш, конечно - но и не потеря.\n\n"
                        f"Не сдавайся, <@{player.id}>! Может быть, следующий спин принесет тебе удачу? 🍀")
    elif payout < 50:
        title = "Я живой, спасибо фортуне!"
        description += (f"<@{player.id}>, символы на центральной сложились в выигрышную комбинацию: "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][0]]['emoji']} "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][1]]['emoji']} "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][2]]['emoji']}. "
                        f"Она принесла тебе выигрыш в размере **{payout}** {FROG_EMOJI}!\n"
                        f"💰 **С учетом ставки твоя чистая прибыль составила {income} {FROG_EMOJI}.**\n\n"
                        f"Скромная победа согревает душу, а новые лягушки — приятно утяжеляют карман.")
    else:
        title = "Джекпот!!!"
        description += (f"<@{player.id}>, ты не веришь собственным глазам, однако это правда: символы центральной "
                        f"линии действительно сложились в идеальную комбинацию: "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][0]]['emoji']} "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][1]]['emoji']} "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][2]]['emoji']}\n\n"
                        f"Машина вспыхивает огнями, сирена победы оглушает зал, а целый поток лягушек с "
                        f"оглушительным кваканьем высыпается на тебя.Толпа вокруг аплодирует и поздравляет — ты "
                        f"сорвал джекпот, и выиграл невероятные **{payout}** {FROG_EMOJI}!\n"
                        f"💰 **С учетом ставки твоя чистая прибыль составила {income} {FROG_EMOJI}.**\n\n"
                        f"Хорошо тому щеголять, у кого в пруду много лягушек квакает!")

    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path="slot_machine_result.jpg",
        image_binary_data=image_binary_data
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def roulette():
    embed_message = MessageContainer(
        title="**Рулетка**",
        description=f"В рулетке игроки делают ставки на то, куда упадёт шарик, брошенный на вращающееся колесо. "
                    f"Колесо разделено на 37 секторов, пронумерованных от 0 до 36. Каждый номер имеет свой цвет: "
                    f"либо красный, либо чёрный, за исключением зелёного сектора «0». Твоя задача — угадать, где "
                    f"окажется шарик после остановки колеса. \n"
                    f"Используй соответствующие кнопки для того, чтобы сделать ставку. Допускается делать одновременно "
                    f"несколько ставок. Имей в виду, что повторная ставка при уже сделанной ранее ставке перезапишет "
                    f"предыдущее значение. \n\n"
                    f"*Лимиты ставок*: \n\n"
                    f"- Ставка на число: от **1** до **3** {FROG_EMOJI}\n"
                    f"- Ставка на диапазон: от **3** до **10** {FROG_EMOJI}\n"
                    f"- Ставка на равные шансы: от **5** до **15** {FROG_EMOJI}\n\n"
                    f"*Типы ставок и коэффициенты выплат:*\n\n"
                    f"- **Прямая ставка** (одно число): **x36**\n"
                    f"- **Равные шансы** (красное/чёрное, чёт/нечёт или низкие/высокие числа): **x2**\n"
                    f"- **Дюжина** (1–12, 13–24, 25–36) или **ряд** (1–34, 2–35, 3–36): **x3**\n"
                    f"- **Сикслайн** (1–6, 7–12, 13–18, 19–24, 25–30, 31–36): **x6**\n\n"
                    f"Дерзай! Ведь кто не рискует, тот не пьёт с лягушками шампанское!",
        file_path=config.ROULETTE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def roulette_bet_confirmation(is_valid=True, category=None):
    if not is_valid:
        title = ERROR_HEADER
        file_path = config.SEPARATOR_ERROR
        if category == "straight":
            description = ("Ставка не принята, вы ввели некорректное значение сектора. Он должен быть целым числом в "
                           "диапазоне от 0 до 36.")
        elif category == "trinary":
            description = ("Ставка не принята, вы ввели некорректный номер диапазона. Номер дюжины или ряда должен "
                           "быть целым числом в диапазоне от 1 до 3.")
        elif category == "sixline":
            description = ("Ставка не принята, вы ввели некорректный номер диапазона. Номер сикслайна должен быть "
                           "целым числом в диапазоне от 1 до 6.")
        elif category == "bet":
            description = ("Ставка не принята, вы ввели некорректное значение. Ставка должна быть целым числом больше "
                           "нуля и меньше указанного лимита.")
        elif category == "balance":
            description = ("Ставка не принята. На вашем балансе недостаточно средств, чтобы сделать такую ставку. При "
                           "подсчете учитывается величина уже сделанных вами ставок, если таковые имеются.")
    else:
        title = SUCCESS_HEADER
        description = "Ставка принята!"
        file_path = config.SEPARATOR_CONFIRM
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def roulette_no_bets_error():
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description="Ты не сделал ни одной ставки!",
        file_path=config.SEPARATOR_ERROR
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def roulette_bets_listing(bets, overall_bet, image_binary_data):
    bet_categories = {
        "straight": "Число",
        "color": "Красное/черное",
        "even_odd": "Чет/нечет",
        "high_low": "Высокие/низкие",
        "dozen": "Дюжина",
        "row": "Ряд",
        "sixline": "Сикслайн"
    }
    description = ("Ниже ты можешь видеть все сделанные тобою ставки. "
                   "Теперь остается лишь подтвердить их, и игра начнется!\n\n")
    for bet in bets:
        bet_category = bet_categories[bet['category']]
        bet_amount = bet['amount']
        bet_value = utils.roulette_bet_value_transcript(bet['category'], bet['value'])
        description += f"- _{bet_category}_: ставка **{bet_amount}** {FROG_EMOJI} на **{bet_value}**\n"
    description += f"\n🎟 ***Общая сумма всех твоих ставок***: **{overall_bet}** {FROG_EMOJI}\n"

    embed_message = MessageContainer(
        title="Список всех ставок",
        description=description,
        file_path="roulette_result.jpg",
        image_binary_data=image_binary_data
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def roulette_result(player, sector, overall_bet, winnings, image_binary_data):
    bet_categories = {
        "straight": "Число",
        "color": "Красное/черное",
        "even_odd": "Чет/нечет",
        "high_low": "Высокие/низкие",
        "dozen": "Дюжина",
        "row": "Ряд",
        "sixline": "Сикслайн"
    }
    income = winnings["total_payout"] - overall_bet
    description = ("Колесо рулетки замерло, и в зале повисла тишина, нарушаемая только мерным ночным кваканьем лягушек "
                   "за окнами. Шарик, прыгавший в хаотичном ритме, наконец нашел свое место. \n\n")
    description += "💠 ***Выпавший сектор***: "
    if sector['color'] == "green":
        description += "__**0 (зеро)**__ :green_circle:\n"
    else:
        if sector['color'] == "red":
            description += f"__**{sector['number']} (красное)**__ :red_circle:\n"
        elif sector['color'] == "black":
            description += f"__**{sector['number']} (черное)**__ :black_circle:\n"
    description += "🎯 ***Выигравшие ставки***:\n"
    if not winnings["winning_bets"]:
        description += "- *Ни одна из твоих ставок не выиграла :(*\n\n"
    else:
        for winning_bet in winnings["winning_bets"]:
            winning_bet_category = bet_categories[winning_bet['category']]
            winning_bet_amount = winning_bet['amount']
            winning_bet_value = utils.roulette_bet_value_transcript(winning_bet['category'], winning_bet['value'])
            winning_bet_winnings = winning_bet['winnings']
            description += (f"- _{winning_bet_category}_: "
                            f"ставка **{winning_bet_amount}** {FROG_EMOJI} на **{winning_bet_value}**, "
                            f"выигрыш: **{winning_bet_winnings}** {FROG_EMOJI}\n")
        description += f"💵 ***Сумма всех выигравших ставок***: **{winnings['total_payout']}** {FROG_EMOJI}\n\n"

    if income > 0:
        title = "Я живой, спасибо фортуне!"
        description += (f"Поздравления, <@{player.id}>, cегодня ты поймал удачу за хвост!\n "
                        f"💰 **С учетом ставки твоя чистая прибыль составила {income}** {FROG_EMOJI}. \n\n"
                        f"Может быть, это твой счастливый день, и тебе стоит сыграть еще один раунд? "
                        f"Или ты можешь забрать выигрыш и просто уйти, оставив за собой воспоминание "
                        f"о магии этого вечера.")
    else:
        if income < 0:
            title = "Увы и ах!"
            description += (f"К сожалению, <@{player.id}>, сегодня **ты проиграл {-income}** {FROG_EMOJI}. \n"
                            f"Но это не повод унывать, ведь ты всегда можешь попробовать сыграть еще, и обязательно "
                            f"с лихвой наверстать упущенное!")
        else:
            title = "Ни дать, ни взять"
            description += (f"<@{player.id}>, в этот раз тебе не удалось выиграть, однако же ты и ничего не потерял. "
                            f"Самое время попробовать сыграть еще, в надежде на успех.")
        description += "\n\nУдачи в следующей игре! 🍀"
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path="roulette_wheel_with_ball.jpg",
        image_binary_data=image_binary_data
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def yahtzee():
    embed_message = MessageContainer(
        title="**Покер на костях**",
        description=f"Добро пожаловать в покер на костях — игру, где прихотливые законы вероятностей и стратегия идут "
                    f"рука об руку!\n"
                    f"Сделай ставку и брось пять кубиков, после чего посмотри, что выпадет. В случае, если ты сразу "
                    f"собрал одну из выигрышных комбинаций — поздравляем, ты победитель! Если же при первом броске "
                    f"удача отвернулась от тебя, у тебя есть второй шанс: выбери до двух кубиков и перебрось их, чтобы "
                    f"улучшить свой результат. После второго броска твой набор считается окончательным, и производится "
                    f"расчет выигрыша.\n\n"
                    f"*Лимит ставок*: от **3** до **10** {FROG_EMOJI}\n\n"
                    f"*Список выигрышных комбинаций и коэффициенты выплат:*\n\n"
                    f"- **Малый стрит** (последовательность из четырех чисел): **x1**\n"
                    f"- **Фулл-хаус** (пара и тройка с одинаковыми значениями): **x2**\n"
                    f"- **Каре** (четыре кости с одинаковым значением): **x3**\n"
                    f"- **Большой стрит** (последовательность из пяти чисел): **x5**\n"
                    f"- **Покер** (все пять костей одинаковы): **x10**\n\n"
                    f"Используй свою интуицию, стратегию и немного удачи, чтобы стать мастером покера на костях! "
                    f"Готов добавить огоньку в этот вечер? 🔥",
        file_path=config.YAHTZEE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def yahtzee_bet_confirmation(is_valid=True, category=None):
    if not is_valid:
        title = ERROR_HEADER
        file_path = config.SEPARATOR_ERROR
        if category == "bet":
            description = ("Ставка не принята, вы ввели некорректное значение. Ставка должна быть целым числом в "
                           "пределах указанного диапазона.")
        elif category == "balance":
            description = ("Ставка не принята. На вашем балансе недостаточно средств, чтобы сделать такую ставку. При "
                           "подсчете учитывается величина уже сделанных вами ставок, если таковые имеются.")
    else:
        title = SUCCESS_HEADER
        description = "Ставка принята!"
        file_path = config.SEPARATOR_CONFIRM
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def yahtzee_no_bet_error():
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description="Ты не сделал ставку!",
        file_path=config.SEPARATOR_ERROR
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def yahtzee_reroll_error(is_filled=True):
    if is_filled:
        description = "Вы уже выбрали две кости для повторного броска!"
    else:
        description = "Вы не выбрали ни одной кости для повторного броска!"
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description=description,
        file_path=config.SEPARATOR_ERROR
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def yahtzee_reroll_set(dice_index):
    dice = ["Первая", "Вторая", "Третья", "Четвертая", "Пятая"]

    embed_message = MessageContainer(
        title="Установлено",
        description=f"{dice[dice_index]} кость будет брошена повторно.",
        file_path=config.SEPARATOR_CONFIRM
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def yahtzee_result(player, bet, payout, roll_outcome, image_binary_data, is_reroll=False):
    winning_type = {
        'drawn': ["small_straight"],
        'small': ["full_house", "four_of_a_kind"],
        'large': ["large_straight", "yahtzee"]
    }
    winning_name = {
        "full_house": "фулл хаус",
        "four_of_a_kind": "каре",
        "small_straight": "малый стрит",
        "large_straight": "большой стрит",
        "yahtzee": "покер"
    }
    income = payout - bet
    if income < 0:
        description = (f"Приглушенный свет ламп в зале скользил по поверхности стола, где ты с напряжением наблюдал "
                       f"за результатом броска костей. Увы кубики, словно насмехаясь, остановились на комбинации, "
                       f"далёкой от победы:\n\n 🎲 **{'-'.join(map(str, roll_outcome['dice']))}**\n\n")
        if not is_reroll:
            title = "Это не конец - все только начиналось"
            description += ("Однако отчаиваться еще рано! У тебя еще есть возможность улучшить свой результат. "
                            "Для этого выбери одну или две кости, которые бы ты хотел выбросить повторно. Возможно, "
                            "именно это позволит тебе собрать выигрышную комбинацию!")
        else:
            title = "Ебманый рот этого казино"
            description += (f"**<@{player.id}>, ты проиграл {bet} {FROG_EMOJI}.\n**"
                            f"Ты медленно выдохнул, отпуская надежду на удачу. Карман опустел, но азарт всё ещё "
                            f"пульсировал в груди. Со стола раздался чей-то смешок - игра продолжалась, но для тебя "
                            f"она уже закончилась.\n\nУдачи в следующей игре! 🍀")
    else:
        if roll_outcome['winning_combination'] in winning_type['drawn']:
            title = "Ни дать, ни взять"
            description = (f"Пятерка игральных костей прокатилась по зеленому сукну стола и, остановившись, сложилась "
                           f"в самую младшую из выигрышных комбинаций:"
                           f"\n\n 🎲 **{'-'.join(map(str, sorted(roll_outcome['dice'])))}**\n"
                           f"(*{winning_name[roll_outcome['winning_combination']]}*)\n\n"
                           f"<@{player.id}>, ты выиграл **{payout}** {FROG_EMOJI}.\n"
                           f"Учитывая количество тех лягушек, которых ты поставил на кон, эта победа не принесла "
                           f"тебе чистой прибыли. Ты просто вернул свою ставку. Согласись, это отличный повод "
                           f"сыграть еще раз в надежде на нечто большее!\n\nУдачи в следующей игре! 🍀")
        elif roll_outcome['winning_combination'] in winning_type['small']:
            title = "Это немного, но это честная работа"
            description = (f"Кости с глухим стуком ударились о стол и замерли, показав скромную выигрышную комбинацию:"
                           f"\n\n 🎲 **{'-'.join(map(str, sorted(roll_outcome['dice'])))}**\n"
                           f"(*{winning_name[roll_outcome['winning_combination']]}*)\n\n"
                           f"<@{player.id}>, ты выиграл **{payout}** {FROG_EMOJI}.\n"
                           f"💰 **С учетом ставки твоя чистая прибыль составила {income} {FROG_EMOJI}**\n\n"
                           f"Ты выдохнул с облегчением, чувствуя лёгкий прилив радости. Это не было триумфом, но "
                           f"небольшая победа согревала душу. Ты забрал своих лягушек — немного больше, чем было в "
                           f"начале игры, — и задумался: продолжить или уйти? Ведь вечер ещё не кончился...")
        elif roll_outcome['winning_combination'] in winning_type['large']:
            title = "Забыть невозможно, победа, какой ты досталась ценой!"
            description = (f"Кубики прыгали по столу, будто бы решая твою судьбу. Сердце замерло, когда они "
                           f"остановились, и вот — идеальная комбинация:\n\n"
                           f"🎲 **{'-'.join(map(str, sorted(roll_outcome['dice'])))}**\n"
                           f"(*{winning_name[roll_outcome['winning_combination']]}*)\n\n"
                           f"<@{player.id}>, ты выиграл баснословные **{payout}** {FROG_EMOJI}.\n"
                           f"💰 **С учетом ставки твоя чистая прибыль составила {income} {FROG_EMOJI}**\n\n"
                           f"Взрыв радости и завистливые взгляды соперников окутали тебя. Ты не мог поверить своим "
                           f"глазам: это и впрямь был {winning_name[roll_outcome['winning_combination']]}! Выигранные "
                           f"лягушки с громким кваканьем прыгали в твою сторону, и ты почувствовал себя королём этого "
                           f"вечера. Сегодня удача была твоей спутницей, и будто бы весь Лаграс был готов склониться "
                           f"перед этой славной победой!")
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path="yahtzee_result.jpg",
        image_binary_data=image_binary_data
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def balance_error(is_fraud=True):
    description = "На твоем счету недостаточно средств для игры. "
    if is_fraud:
        description += ("Параллельно с текущей игрой ты играл в другую игру, совершил покупки или перевод средств "
                        "другому участнику. Данное поведение запрещено правилами казино, и за это ты будешь подвергнут "
                        "наказанию. Бот уже сообщил о твоем проступке администрации. Готовь жепу!")
        file_path = config.CASINO_FRAUD_BAN
    else:
        description += ("Поймай лягушек на болоте, или попроси у кого-нибудь взаймы с непременным обещанием вернуть "
                        "после выигрыша - и начинай игру!")
        file_path = config.SEPARATOR_ERROR
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def wrong_player_error(original_player):
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description=f"Это не твоя игровая сессия! Ее начал <@{original_player.id}>, и только он имеет доступ "
                    f"к панели игры. Если хочешь сыграть в казино, используй команду `/casino` и выбери для себя "
                    f"игру самостоятельно!",
        file_path=config.CASINO_WRONG_PLAYER
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}
