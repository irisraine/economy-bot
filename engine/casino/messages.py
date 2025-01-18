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
        color = ERROR_COLOR_CODE if title == ERROR_HEADER else BASIC_COLOR_CODE
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
        description="Приветствуем тебя, ковбой! Именно для тебя открывает двери первое в мире казино на лаграсских "
                    "болотах, где ты сможешь испытать собственную удачу. Стань богат, как никогда прежде и покинь наше "
                    "заведение с карманами, полными лягушек - или уйди ни с чем и оставь здесь последние штаны. "
                    "Ибо, как писал великий поэт: \n\n *Умей поставить в радостной надежде \nНа карту все, "
                    "что накопил с трудом - \nВсе проиграй, и нищим стань как прежде, \nИ никогда не пожалей о том!*",
        file_path=config.CASINO_ENTRANCE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def slot_machine():
    embed_message = MessageContainer(
        title="**Однорукий бандит**",
        description=f"Испытай свою удачу в игре с одноруким бандитом и сорви свой джекпот! Выбирай между двумя "
                    f"режимами игры: более доступным «Жабьим чвяком» и дорогим «Отчаянным ковбоем», каждый из которых "
                    f"предлагает свои шансы на победу и уникальные комбинации!\n"
                    f"После выбора режима дергай за рычаг однорукого бандита и жди, когда замершие барабаны отобразят "
                    f"результат игры - он определяется в зависимости от символов, выпавших на центральной линии.\n\n"
                    f"- **Жабий чвяк** "
                    f"(стоимость игры **{config.SLOT_MACHINE_BET_AMOUNTS['low']}** {FROG_EMOJI})\n"
                    f"Это классический режим для тех, кто хочет испытать свою удачу без лишнего риска. На барабане "
                    f"всего три типа символов - три лягушки разных цветов, а вероятность победы ниже.\n\n"
                    f"*Выигрышные комбинации:*\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_symbols']['frog_white']['low']}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_symbols']['frog_orange']['low']}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frogs_all_colors']['low']}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_symbols']['frog_green']['low']}** {FROG_EMOJI}\n\n"
                    f"- **Отчаянный ковбой** "
                    f"(стоимость игры **{config.SLOT_MACHINE_BET_AMOUNTS['high']}** {FROG_EMOJI})\n"
                    f"Для настоящих искателей приключений! Этот режим обойдется тебе дороже, но и предлагает более "
                    f"щедрые шансы на выигрыш. На барабане целых восемь символов, в каждом из которых отразился один "
                    f"из аспектов жизни на Диком Западе, а количество победных комбинаций увеличено до девяти!\n\n"
                    f"*Выигрышные комбинации:*\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['rare_symbols']['gold'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['cart']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['cart']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['cart']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['rare_symbols']['cart'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['star']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['star']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['star']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['rare_symbols']['star'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['horseshoe']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['horseshoe']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['horseshoe']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['rare_symbols']['horseshoe'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['moonshine']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['moonshine']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['moonshine']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['rare_symbols']['moonshine'][3]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_symbols']['frog_white']['high']}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} :x:** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['rare_symbols']['gold'][2]}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_symbols']['frog_orange']['high']}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_orange']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_white']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frogs_all_colors']['high']}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']} "
                    f"{config.SLOT_MACHINE_REEL_SYMBOLS['frog_green']['emoji']}** "
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['frog_symbols']['frog_green']['high']}** {FROG_EMOJI}\n"
                    f"**{config.SLOT_MACHINE_REEL_SYMBOLS['gold']['emoji']} :x: :x:**"
                    f" - выплата "
                    f"**{config.SLOT_MACHINE_PAYOUT_AMOUNTS['rare_symbols']['gold'][1]}** {FROG_EMOJI}\n\n"
                    f"Сможешь ли ты обхитрить однорукого бандита и стать настоящим чемпионом? Дерзай, ведь удача "
                    f"любит смелых!",
        file_path=config.SLOT_MACHINE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def slot_machine_result(player, reels, bet, payout, image_binary_data):
    description = ("Машина оживает от твоего прикосновения, и барабаны начинают своё вращение, словно в ритме твоего "
                   "пульса. Ты наблюдаешь за мелькающими символами, чувствуя, как напряжение нарастает. И вот барабаны "
                   "замедляются, один за другим встают на место - и ты видишь результат. \n\n")

    income = payout - bet
    if payout == 0:
        title = "Увы и ах, сегодня тебе не повезло!"
        description += (f"К сожалению, символы центральной линии не сложились ни в одну из выигрышных комбинаций! "
                        f"<@{player.id}>, сегодня ты проиграл **{bet}** {FROG_EMOJI}!\n"
                        f"Ты чувствуешь разочарование. Но прислушайся к себе, и услышишь, как азарт "
                        f"шепчет - попробуй еще раз! Может, стоит прислушаться к нему?")
    elif payout < 50:
        title = "Чвяк-чвяк, ты выиграл, ковбой!"
        description += (f"<@{player.id}>, к твоей радости, символы на центральной сложились в выигрышную комбинацию: "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][0]]['emoji']} "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][1]]['emoji']} "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][2]]['emoji']}.\n\n"
                        f"Она принесла тебе выигрыш в размере **{payout}** {FROG_EMOJI}. \n"
                        f"💰 **С учетом ставки твоя чистая прибыль составила {income} {FROG_EMOJI}.**\n\n"
                        f"Эта скромная победа приятно согревает душу — пускай это не джекпот, но всё же фортуна "
                        f"улыбнулась тебе.")
    else:
        title = "Счастливчик, ты сорвал джекпот!!!"
        description += (f"<@{player.id}>, ты не веришь собственным глазам, однако это правда: символы центральной "
                        f"линии действительно сложились в идеальную комбинацию: "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][0]]['emoji']} "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][1]]['emoji']} "
                        f"{config.SLOT_MACHINE_REEL_SYMBOLS[reels[1][2]]['emoji']}.\n\n"
                        f"Ее прежде тщетно жаждали увидеть целые поколения игроков - однако удача улыбнулась именно "
                        f"тебе! Машина вспыхивает огнями, сирена победы оглушает зал, а целый поток лягушек с "
                        f"оглушительным кваканьем льется на тебя. \n"
                        f"Толпа вокруг аплодирует и поздравляет — ты сорвал джекпот, и выиграл невероятные "
                        f"**{payout}** {FROG_EMOJI}! \n"
                        f"💰 **С учетом ставки твоя чистая прибыль составила {income} {FROG_EMOJI}.**\n\n"
                        f"Улыбка не сходит с твоего лица: удача сегодня была на твоей стороне!")
    description += "\n\nУдачи в следующей игре! 🍀"

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
        description=f"Европейская рулетка — это классическая азартная игра, в которой игроки делают ставки на то, куда "
                    f"упадёт шарик, брошенный на вращающееся колесо. Колесо разделено на 37 секторов, пронумерованных "
                    f"от 0 до 36. Каждый номер имеет свой цвет: либо красный, либо чёрный, за исключением зелёного "
                    f"сектора «0». Твоя задача — угадать, где окажется шарик после остановки колеса. \n"
                    f"Используй соответствующие кнопки для того, чтобы сделать ставку. Допускается делать одновременно "
                    f"несколько ставок. Имей в виду, что повторная ставка при уже сделанной ранее ставке перезапишет "
                    f"предыдущее значение. \n\n"
                    f"*Лимиты ставок*: \n\n "
                    f"- Ставка на число: от **1** до **10** {FROG_EMOJI}\n"
                    f"- Ставка на диапазон: от **3** до **15** {FROG_EMOJI}\n"
                    f"- Ставка на равные шансы: от **5** до **25** {FROG_EMOJI}\n\n"
                    f"*Типы ставок и коэффициенты выплат:*\n\n"
                    f"- **Прямая ставка** (одно число): **35:1**\n"
                    f"- **Равные шансы** (красное/чёрное, чёт/нечёт или низкие/высокие числа): **1:1**\n"
                    f"- **Дюжина** (1–12, 13–24, 25–36) или **ряд** (1–34, 2–35, 3–36): **2:1**\n"
                    f"- **Сикслайн** (1–6, 7–12, 13–18, 19–24, 25–30, 31–36): **5:1**\n\n"
                    f"Когда ставки сделаны, колесо раскручивается и шарик начинает своё путешествие. Как только он "
                    f"остановится на одной из ячеек, ты узнаешь, улыбнулась ли тебе удача!",
        file_path=config.ROULETTE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def roulette_single_bet_confirmation(is_valid=True, category=None):
    if not is_valid:
        title = ERROR_HEADER
        file_path = config.SEPARATOR_ERROR
        if category == "sector":
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


def roulette_all_bets_listing(bets, overall_bet, image_binary_data):
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
    if income > 0:
        title = "Чвяк-чвяк, ты выиграл, ковбой!"
        overall_result = (f"Поздравления, <@{player.id}>, cегодня ты поймал удачу за хвост!\n "
                          f"💰 **С учетом ставки твоя чистая прибыль составила {income}** {FROG_EMOJI}. \n"
                          f"Может быть, это твой счастливый день, и тебе стоит сыграть еще один раунд? "
                          f"Или ты можешь забрать выигрыш и просто уйти, оставив за собой воспоминание "
                          f"о магии этого вечера.")
    else:
        title = "Увы и ах, сегодня тебе не повезло!"
        if income < 0:
            overall_result = (f"К сожалению, не всегда удача улыбается игрокам. \n"
                              f"<@{player.id}>, сегодня **ты проиграл {-income}** {FROG_EMOJI}. \n"
                              f"Но это не повод унывать, ведь ты всегда можешь попробовать сыграть еще, и обязательно "
                              f"с лихвой наверстать упущенное!")
        else:
            overall_result = (f"<@{player.id}>, в этот раз тебе не удалось выиграть, однако же ты и ничего не потерял. "
                              f"Самое время попробовать сыграть еще, в надежде на успех")

    sector_description = ""
    if sector['color'] == "green":
        sector_description = "__**0 (зеро)**__ 🟢"
    else:
        if sector['color'] == "red":
            sector_description = f"__**{sector['number']} (красное)**__ 🔴"
        elif sector['color'] == "black":
            sector_description = f"__**{sector['number']} (черное)**__ ⚫️"

    winning_bets_list = "\n"
    if not winnings["winning_bets"]:
        winning_bets_list += "- *Ни одна из твоих ставок не выиграла :(*"
    else:
        for winning_bet in winnings["winning_bets"]:
            winning_bet_category = bet_categories[winning_bet['category']]
            winning_bet_amount = winning_bet['amount']
            winning_bet_value = utils.roulette_bet_value_transcript(winning_bet['category'], winning_bet['value'])
            winning_bet_winnings = winning_bet['winnings']
            winning_bets_list += (f"- _{winning_bet_category}_: "
                                  f"ставка **{winning_bet_amount}** {FROG_EMOJI} на **{winning_bet_value}**, "
                                  f"выигрыш: **{winning_bet_winnings}** {FROG_EMOJI}\n")
        winning_bets_list += f"💵 ***Сумма всех выигравших ставок***: **{winnings['total_payout']}** {FROG_EMOJI}"

    embed_message = MessageContainer(
        title=title,
        description=f"Колесо рулетки замерло, и в зале повисла тишина, нарушаемая только мерным ночным кваканьем "
                    f"лягушек за окнами. Шарик, прыгавший в хаотичном ритме, наконец нашел свое место. \n\n"
                    f"💠 ***Выпавший сектор***: {sector_description}\n"
                    f"🎯 ***Выигравшие ставки***: {winning_bets_list}\n\n"
                    f"{overall_result} \n\nУдачи в следующей игре! 🍀",
        file_path="roulette_wheel_with_ball.jpg",
        image_binary_data=image_binary_data
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def yahtzee():
    embed_message = MessageContainer(
        title="**Покер на костях**",
        description=f"Добро пожаловать в захватывающий мир покера на костях — игру, где прихотливые законы "
                    f"вероятностей и стратегия идут рука об руку! Испытай свою судьбу, бросая игральные кубики, чтобы "
                    f"собрать одну из выигрышных комбинаций и получить заслуженную награду!\n"
                    f"Правила игры просты. Сделайте ставку и бросьте пять кубиков, после чего посмотрите, что выпадет. "
                    f"В случае, если вы сразу собрали одну из выигрышных комбинаций — поздравляем, вы победитель! "
                    f"Если же при первом броске удача оказалась не на твоей стороне, не беда! У тебя есть второй шанс: "
                    f"выбери до двух кубиков и перебрось их, чтобы улучшить свой результат. После второго броска твой "
                    f"набор считается окончательным, и производится расчет выигрыша.\n\n"
                    f"*Лимит ставок*: от **3** до **15** {FROG_EMOJI}\n\n"
                    f"*Список выигрышных комбинаций и коэффициенты выплат:*\n\n"
                    f"- **Тройка** (три кости с одинаковым значением): "
                    f"**{config.YAHTZEE_PAYOUT_MULTIPLIERS['three_of_a_kind']}:1**\n"
                    f"- **Фулл-хаус** (пара и тройка с одинаковыми значениями): "
                    f"**{config.YAHTZEE_PAYOUT_MULTIPLIERS['full_house']}:1**\n"
                    f"- **Каре** (четыре кости с одинаковым значением): "
                    f"**{config.YAHTZEE_PAYOUT_MULTIPLIERS['four_of_a_kind']}:1**\n"
                    f"- **Малый стрит** (последовательность из четырех чисел): "
                    f"**{config.YAHTZEE_PAYOUT_MULTIPLIERS['small_straight']}:1**\n"
                    f"- **Большой стрит** (последовательность из пяти чисел): "
                    f"**{config.YAHTZEE_PAYOUT_MULTIPLIERS['large_straight']}:1**\n"
                    f"- **Покер** (все пять костей одинаковы): "
                    f"**{config.YAHTZEE_PAYOUT_MULTIPLIERS['yahtzee']}:1**\n\n"
                    f"Используй свою интуицию, стратегию и немного удачи, чтобы стать мастером покера на костях! "
                    f"Готов испытать судьбу? Бросай кости и собирай лучшие комбинации!",
        file_path=config.YAHTZEE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def yahtzee_bet_confirmation(is_valid=True, category=None):
    if not is_valid:
        title = ERROR_HEADER
        if category == "bet":
            description = ("Ставка не принята, вы ввели некорректное значение. Ставка должна быть целым числом в "
                           "пределах указанного диапазона.")
        elif category == "balance":
            description = ("Ставка не принята. На вашем балансе недостаточно средств, чтобы сделать такую ставку. При "
                           "подсчете учитывается величина уже сделанных вами ставок, если таковые имеются.")
    else:
        title = SUCCESS_HEADER
        description = "Ставка принята!"
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=config.SEPARATOR_CONFIRM
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
        'small': ["three_of_a_kind", "four_of_a_kind", "full_house"],
        'large': ["small_straight", "large_straight", "yahtzee"]
    }
    winning_name = {
        "three_of_a_kind": "тройка",
        "four_of_a_kind": "каре",
        "full_house": "фулл хаус",
        "small_straight": "малый стрит",
        "large_straight": "большой стрит",
        "yahtzee": "покер"
    }
    income = payout - bet
    description = ""
    if income < 0:
        title = "Нет выигрышных комбинаций"
        description += (f"Приглушенный свет ламп в зале скользил по поверхности стола, где ты с напряжением наблюдал "
                        f"за результатом броска костей. Увы кубики, словно насмехаясь, остановились на комбинации, "
                        f"далёкой от победы:\n\n **{'-'.join(map(str, roll_outcome['dice']))}**\n\n")
        if not is_reroll:
            description += ("Однако отчаиваться было еще рано! У тебя еще есть возможность улучшить свой результат. "
                            "Для этого выбери одну или две кости, которые бы ты хотел выбросить повторно. "
                            "Возможно, именно это позволит тебе собрать выигрышную комбинацию!")
        else:
            description += (f"**<@{player.id}>, ты проиграл {bet} {FROG_EMOJI}.\n**"
                            f"Ты медленно выдохнул, отпуская надежду на удачу. Карман опустел, но азарт всё ещё "
                            f"пульсировал в груди. Со стола раздался чей-то смешок — игра продолжалась, но для тебя "
                            f"она уже закончилась.\n\nУдачи в следующей игре! 🍀")
    else:
        title = "Это победа! Болотные сокровища теперь твои!"
        if roll_outcome['winning_combination'] in winning_type['small']:
            description = (
                f"Кости с глухим стуком ударились о стол и замерли, показав скромную выигрышную комбинацию:\n\n "
                f"**{'-'.join(map(str, sorted(roll_outcome['dice'])))}**\n"
                f"(*{winning_name[roll_outcome['winning_combination']]}*)\n\n"
                f"<@{player.id}>, ты выиграл **{payout}** {FROG_EMOJI}.\n💰 **С учетом ставки твоя "
                f"чистая прибыль составила {income} {FROG_EMOJI}**\n\n"
                f"Ты выдохнул с облегчением, чувствуя лёгкий прилив радости. Пусть это не было триумфом, но "
                f"небольшая победа согревала душу. Ты забрал своих лягушек — немного больше, чем было в начале "
                f"игры, — и задумался: продолжить или уйти? Ведь вечер ещё не кончился, а удача всё ещё могла "
                f"улыбнуться шире!")
        if roll_outcome['winning_combination'] in winning_type['large']:
            description = (
                f"Кубики прыгали по столу, будто бы решая твою судьбу. Сердце замерло, когда они остановились, "
                f"и вот — идеальная комбинация:\n\n"
                f"**{'-'.join(map(str, sorted(roll_outcome['dice'])))}**\n"
                f"(*{winning_name[roll_outcome['winning_combination']]}*)\n\n"
                f"<@{player.id}>, ты выиграл баснословные **{payout}** {FROG_EMOJI}.\n💰 **С учетом ставки твоя "
                f"чистая прибыль составила {income} {FROG_EMOJI}**\n\n"
                f"Взрыв радости и завистливые взгляды соперников окутали тебя. Ты не мог поверить своим "
                f"глазам: это и впрямь был {winning_name[roll_outcome['winning_combination']]}! "
                f"Выигранные лягушки с громким кваканьем прыгали в твою сторону, и ты почувствовал себя королём "
                f"этого вечера. Сегодня удача была твоей спутницей, и весь Лаграс казался готовым склониться "
                f"перед твоей славной победой!")
        description += "\n\nУдачи в следующей игре! 🍀"
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path="yahtzee_result.jpg",
        image_binary_data=image_binary_data
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def balance_error():
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description="На твоем счету недостаточно средств для игры. Появление этой ошибки свидетельствует, что ты "
                    "параллельно с текущей игрой играл в другую игру, совершил покупки или перевод средств другому "
                    "участнику. Данное поведение запрещено правилами казино, и за это ты будешь подвергнут наказанию. "
                    "Бот уже сообщил о твоем проступке администрации. Готовь жопу!",
        file_path=config.CASINO_FRAUD_BAN
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def wrong_player_error(original_player):
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description=f"Ковбой, это не твоя игровая сессия! Ее начал <@{original_player.id}>, и только он имеет доступ "
                    f"к панели игры. Если хочешь сыграть в казино, используй команду `/casino` и выбери для себя "
                    f"игру самостоятельно!",
        file_path=config.CASINO_WRONG_PLAYER
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}
