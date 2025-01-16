import nextcord
import io
import engine.casino.config as config

ERROR_HEADER = "Ошибка"
SUCCESS_HEADER = "Успешно"

ERROR_DESCRIPTION_SHOP = ("К сожалению, данный товар по неизвестной причине отсутствует на нашем складе. "
                          "Приносим извинения за доставленные неудобства. \n\n "
                          "*Пожалуйста, обратитесь к администратору для возврата потраченных средств.*")

ERROR_DESCRIPTION_GENERAL = ("Что-то пошло не так. :(\n "
                             "В этой жизни всегда так, что порой что-то может пойти не так.")


class MessageContainer:
    def __init__(self, title=None, description=None, file_path=None, image_binary_data=None):
        self.__content = None
        self.__embed = None
        if image_binary_data:
            fp = io.BytesIO(image_binary_data)
        else:
            if not file_path:
                file_path = config.SEPARATOR
            fp = file_path
        file_name = file_path.split('/')[-1]
        if file_name.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif']:
            self.__embed = nextcord.Embed(
                title=title,
                description=description,
                colour=nextcord.Colour.from_rgb(*config.BASIC_COLOR_CODE),
            )
            image_attachment = f"attachment://{file_name}"
            self.__embed.set_image(url=image_attachment)
        else:
            self.__content = description
        self.__file = nextcord.File(fp=fp, filename=file_name)

    @property
    def content(self):
        return self.__content

    @property
    def embed(self):
        return self.__embed

    @property
    def file(self):
        return self.__file

def casino():
    embed_message = MessageContainer(
        title="**Добро пожаловать в болотное казино «Три лягушки»!**",
        description="Приветствуем тебя, ковбой! Именно для тебя открывает двери первое в мире казино на лаграсских болотах, где "
                    "ты сможешь испытать собственную удачу. Стань богат, как никогда прежде и покинь наше заведение с карманами, "
                    "полными лягушек - или уйди ни с чем и оставь здесь последние штаны. "
                    "Ибо, как писал великий поэт: \n\n *Умей поставить в радостной надежде \nНа карту все, "
                    "что накопил с трудом - \nВсе проиграй, и нищим стань как прежде, \nИ никогда не пожалей о том!*",
        file_path=config.CASINO_ENTRANCE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


############################### ОДНОРУКИЙ БАНДИТ ############################

def slot_machine():
    embed_message = MessageContainer(
        title="**Однорукий бандит**",
        description="Испытай свою удачу в игре с одноруким бандитом и сорви свой джекпот! Выбирай между двумя режимами "
                    "игры: более доступным 'Жабьим чвяком' и дорогим 'Отчаянным ковбоем', каждый из которых предлагает "
                    "свои шансы на победу и уникальные комбинации!\n"
                    "После выбора режима игры дергай за рычаг однорукого бандита и жди, когда замершие барабаны отобразят "
                    "результат игры - он определяется в зависимости от символов, выпавших на центральной линии.\n\n"
                    f"- **Жабий чвяк** (стоимость игры **5** {config.FROG_EMOJI})\n"
                    "Это классический режим для тех, кто хочет испытать свою удачу без лишнего риска. На барабане "
                    "всего три типа символов - три лягушки разных цветов, а вероятность победы ниже.\n\n"
                    "*Выигрышные комбинации:*\n"
                    f"**{config.EMOJI['frog_white']} {config.EMOJI['frog_white']} {config.EMOJI['frog_white']}** "
                    f" - выплата **25** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['frog_orange']} {config.EMOJI['frog_orange']} {config.EMOJI['frog_orange']}** "
                    f" - выплата **20** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['frog_green']} {config.EMOJI['frog_orange']} {config.EMOJI['frog_white']}** "
                    f" - выплата **15** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['frog_green']} {config.EMOJI['frog_green']} {config.EMOJI['frog_green']}** "
                    f" - выплата **10** {config.FROG_EMOJI}\n\n"
                    f"- **Отчаянный ковбой** (стоимость игры **8** {config.FROG_EMOJI})\n"
                    "Для настоящих искателей приключений! Этот режим обойдется тебе дороже, но и предлагает более щедрые шансы "
                    "на выигрыш. На барабане целых восемь символов, в каждом из которых отразился один из аспектов "
                    "жизни на Диком Западе, а количество победных комбинаций увеличено до девяти!\n\n"
                    "*Выигрышные комбинации:*\n"
                    f"**{config.EMOJI['gold']} {config.EMOJI['gold']} {config.EMOJI['gold']}** "
                    f" - выплата **300** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['cart']} {config.EMOJI['cart']} {config.EMOJI['cart']}** "
                    f" - выплата **100** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['star']} {config.EMOJI['star']} {config.EMOJI['star']}** "
                    f" - выплата **75** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['horseshoe']} {config.EMOJI['horseshoe']} {config.EMOJI['horseshoe']}** "
                    f" - выплата **50** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['moonshine']} {config.EMOJI['moonshine']} {config.EMOJI['moonshine']}** "
                    f" - выплата **35** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['gold']} {config.EMOJI['gold']} :x:** " 
                    f" - выплата **25** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['frog_white']} {config.EMOJI['frog_white']} {config.EMOJI['frog_white']}** "
                    f" - выплата **25** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['frog_orange']} {config.EMOJI['frog_orange']} {config.EMOJI['frog_orange']}** "
                    f" - выплата **20** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['frog_green']} {config.EMOJI['frog_orange']} {config.EMOJI['frog_white']}** "
                    f" - выплата **15** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['frog_green']} {config.EMOJI['frog_green']} {config.EMOJI['frog_green']}** "
                    f" - выплата **10** {config.FROG_EMOJI}\n"
                    f"**{config.EMOJI['gold']} :x: :x:**"
                    f" - выплата **10** {config.FROG_EMOJI}\n\n"
                    "Сможешь ли ты обхитрить однорукого бандита и стать настоящим чемпионом? Дерзай, ведь удача "
                    "любит смелых!",
        file_path=config.SLOT_MACHINE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}

def slot_machine_result(player, reels, payout, image_binary_data=None):
    if payout == 0:
        title = "Увы и ах, сегодня тебе не повезло!"
        result = (f"К сожалению, символы центральной линии не сложились ни в одну из выигрышных комбинаций! <@{player.id}>, ты чувствуешь разочарование, "
                  "но прислушайся к себе - и услышишь, как азарт шепчет 'Попробуй еще раз!'\n Может, стоит прислушаться к нему?")
    elif payout < 50:
        title = "Чвяк-чвяк, ты выиграл, ковбой!"
        result = (f"<@{player.id}>, к твоей радости, символы на центральной сложились в выигрышную комбинацию: "
                  f"{config.EMOJI[reels[1][0]]} {config.EMOJI[reels[1][1]]} {config.EMOJI[reels[1][2]]}.\n\n"
                  f"Она принесла тебе **выигрыш в размере {payout}** {config.FROG_EMOJI}. Эта скромная победа приятно "
                  f"согревает душу — это не джекпот, но всё же удача улыбнулась тебе.")
    else:
        title = "Счастливчик, ты сорвал джекпот!!!"
        result = (f"<@{player.id}>, ты не веришь собственным глазам, однако это правда: символы центральной линии действительно сложились в идеальную комбинацию: "
                   f"{config.EMOJI[reels[1][0]]} {config.EMOJI[reels[1][1]]} {config.EMOJI[reels[1][2]]}.\n\n"
                   "Ее прежде тщетно жаждали увидеть целые поколения игроков - однако удача улыбнулась именно тебе! "
                   "Машина вспыхивает огнями, сирена победы оглушает зал, а целый поток лягушек с оглушительным кваканьем льется на тебя. \n"
                   f"Толпа вокруг аплодирует и поздравляет — **ты сорвал джекпот, и выиграл невероятные {payout} {config.FROG_EMOJI}!** "
                   "Улыбка не сходит с твоего лица: удача сегодня была на твоей стороне!")
    description = ("Машина оживает от твоего прикосновения, и барабаны начинают своё вращение, словно в ритме твоего "
                   "пульса. Ты наблюдаешь за мелькающими символами, чувствуя, как напряжение нарастает. И вот барабаны "
                   f"замедляются, один за другим встают на место - и ты видишь результат. \n\n {result}")

    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path="slot_machine_result.jpg",
        image_binary_data=image_binary_data.getvalue()
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


############################### РУЛЕТКА ############################

def roulette():
    embed_message = MessageContainer(
        title="**Рулетка**",
        description="Европейская рулетка — это классическая азартная игра, где удача решает всё! На игровом поле есть "
                    "колесо с 37 пронумерованными ячейками от 0 до 36. Ячейки чередуются между красным и чёрным "
                    "цветами, а «0» выделяется зелёным. Цель игры проста: угадать, куда попадёт шарик после вращения "
                    "колеса. \n\n "
                    "В нашем болотном казино ты можешь делать несколько видов ставок. Можно поставить на конкретный "
                    "номер от 0 до 36 — это рискованно, но выигрыш будет крупным! Если хочешь что-то попроще, "
                    "ставь на красное или чёрное — угадай цвет ячейки, и победа твоя. Также доступны ставки на чётные "
                    "или нечётные числа, ставки на низкие или высокие числа, а ещё можно выбирать дюжины, ряды и сикслайны (пары "
                    "двух соседних колонок). Каждая ставка имеет свой коэффициент выигрыша, так что выбирай стратегию мудро!\n"
                    "Используй соответствующие кнопки для того, чтобы сделать ставку. Допускается делать одновременно "
                    "несколько ставок. Имей в виду, что повторная ставка при уже сделанной ранее ставке перезапишет "
                    "предыдущее значение. \n\n"
                    f"На ставки существуют ограничения: ты можешь поставить не более **25** {config.FROG_EMOJI} на любой "
                    f"из диапазонов, и не более **10** {config.FROG_EMOJI} на отдельные числа.\n\n" 
                    "Когда ставки сделаны, колесо раскручивается, и шарик начинает своё путешествие. Как только он "
                    "остановится на одной из ячеек, ты узнаешь, улыбнулась ли тебе удача! Если твоя ставка сыграла, "
                    "ты получаешь выигрыш в зависимости от типа ставки. \n\n"
                    "__Выплаты в зависимости от типа ставки:__\n\n"
                    "- Одно число: **35:1**\n"
                    "- Красное/чёрное, чёт/нечёт или низкие/высокие числа (1–18/19–36): **1:1**\n"
                    "- Дюжина (1–12, 13–24, 25–36) или ряд (1–34, 2–35, 3–36): **2:1**\n"
                    "- Сикслайн (1–6, 7–12, 13–18, 19–24, 25–30, 31–36): **5:1**\n\n"
                    "*Готов испытать удачу? Тогда делай свои ставки и наслаждайся игрой!*",
        file_path=config.ROULETTE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}

def roulette_single_bet_confirmation(is_valid=True, category=None):
    if not is_valid:
        title = ERROR_HEADER
        if category == "sector":
            description = ("Ставка не принята, вы ввели некорректное значение сектора. Он должен быть целым числом в "
                           "диапазоне от 0 до 36.")
        elif category == "trinary":
            description = ("Ставка не принята, вы ввели некорректный номер диапазона. Номер дюжины или ряда должен быть "
                           "целым числом в диапазоне от 1 до 3.")
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
    embed_message = MessageContainer(
        title=title,
        description=description,
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}

def roulette_no_bets_error():
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description="Ты не сделал ни одной ставки!",
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

def roulette_all_bets_listing(bets, overall_bet, image_binary_data=None):
    def bet_value_transcript(bet_category, value):
        if bet_category == "straight":
            return f"сектор {value}"
        elif bet_category == "color":
            return "красное" if value == "red" else "черное"
        elif bet_category == "even_odd":
            return "четное" if value == "even" else "нечетное"
        elif bet_category == "high_low":
            return "высокие" if value == "high" else "низкие"
        elif bet_category == "dozen":
            return f"{value}-ю дюжину"
        elif bet_category == "row":
            return f"{value}-й ряд"
        elif bet_category == "sixline":
            return f"{value}-й сикслайн"
    bet_categories = {
        "straight": "Число",
        "color": "Красное/черное",
        "even_odd": "Чет/нечет",
        "high_low": "Высокие/низкие",
        "dozen": "Дюжина",
        "row": "Ряд",
        "sixline": "Сикслайн"
    }
    description = "Ниже ты можешь видеть все сделанные тобою ставки. Теперь остается лишь подтвердить их.\n\n"
    "и игра начнется!\n"
    for bet in bets:
        bet_category = bet_categories[bet['category']]
        bet_amount = bet['amount']
        bet_value = bet_value_transcript(bet['category'], bet['value'])
        description += (f"- _{bet_category}_: "
                         f"ставка **{bet_amount}** {config.FROG_EMOJI} на **{bet_value}**\n")

    description += f"\n🎟 ***Общая сумма всех твоих ставок***: **{overall_bet}** {config.FROG_EMOJI}\n"

    embed_message = MessageContainer(
        title="Список всех ставок",
        description=description,
        file_path="roulette_table_all_bets.jpg",
        image_binary_data=image_binary_data.getvalue()
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def roulette_result(player, number, color, overall_bet, payout):
    def bet_value_transcript(bet_category, value):
        if bet_category == "straight":
            return f"сектор {value}"
        elif bet_category == "color":
            return "красное" if value == "red" else "черное"
        elif bet_category == "even_odd":
            return "четное" if value == "even" else "нечетное"
        elif bet_category == "high_low":
            return "высокие" if value == "high" else "низкие"
        elif bet_category == "dozen":
            return f"{value}-ю дюжину"
        elif bet_category == "row":
            return f"{value}-й ряд"
        elif bet_category == "sixline":
            return f"{value}-й сикслайн"

    bet_categories = {
        "straight": "Число",
        "color": "Красное/черное",
        "even_odd": "Чет/нечет",
        "high_low": "Высокие/низкие",
        "dozen": "Дюжина",
        "row": "Ряд",
        "sixline": "Сикслайн"
    }

    income = payout["total_winnings"] - overall_bet
    if income > 0:
        title = "Чвяк-чвяк, ты выиграл, ковбой!"
        file_path = config.ROULETTE_RESULT_WIN
        overall_result = (f"Поздравления, <@{player.id}>, cегодня ты поймал удачу за хвост!\n **Твой выигрыш составил {income}** {config.FROG_EMOJI}. \n"
                          f"Может быть, это твой счастливый день, и тебе стоит сыграть еще один раунд? Или ты можешь забрать выигрыш "
                          f"и просто уйти, оставив за собой воспоминание о магии этого вечера.")
    else:
        title = "Увы и ах, сегодня тебе не повезло!"
        file_path = config.ROULETTE_RESULT_LOSE
        if income < 0:
            overall_result = (f"К сожалению, не всегда удача улыбается игрокам. \n"
                              f"<@{player.id}>, сегодня **ты проиграл {-income}** {config.FROG_EMOJI}. \n"
                              f"Но это не повод унывать, ведь ты всегда можешь попробовать сыграть еще, и обязательно "
                              f"с лихвой наверстать упущенное!")
        else:
            overall_result = (f"<@{player.id}>, в этот раз тебе не удалось выиграть, однако же ты и ничего не потерял. Самое время "
                              "попробовать сыграть еще, в надежде на успех")


    if color == "green":
        sector = "0 (зеро) 🟢"
    else:
        sector = f"{number} (красное) 🔴" if color == "red" else f"{number} (черное) ⚫️"

    winning_bets = "\n"
    if not payout["winning_bets"]:
        winning_bets += "- *Ни одна из твоих ставок не выиграла :(*"
    else:
        for winning_bet in payout["winning_bets"]:
            winning_bet_category = bet_categories[winning_bet['category']]
            winning_bet_amount = winning_bet['amount']
            winning_bet_value = bet_value_transcript(winning_bet['category'], winning_bet['value'])
            winning_bet_winnings = winning_bet['winnings']
            winning_bets += (f"- _{winning_bet_category}_: "
                             f"ставка **{winning_bet_amount}** {config.FROG_EMOJI} на **{winning_bet_value}**, "
                             f"выигрыш: **{winning_bet_winnings}** {config.FROG_EMOJI}\n")
        winning_bets += f"💰 ***Сумма всех выигравших ставок***: **{payout['total_winnings']}** {config.FROG_EMOJI}"

    embed_message = MessageContainer(
        title=title,
        description="Колесо рулетки замерло, и в зале повисла тишина, нарушаемая только мерным ночным кваканьем "
                    "лягушек за окнами. Шарик, прыгавший в хаотичном ритме, наконец нашел свое место. \n\n"
                    f"🏆 ***Выпавший сектор***: __**{sector}**__\n"
                    f"🎟 ***Общая сумма всех твоих ставок***: **{overall_bet}** {config.FROG_EMOJI}\n"
                    f"🎯 ***Выигравшие ставки***: {winning_bets}\n\n"
                    f"{overall_result} \n\nУдачи в следующей игре! 🍀",
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


############################### ПОИГРАЕМ В ПОХЕР? ############################

def yahtzee():
    embed_message = MessageContainer(
        title="**Покер на костях**",
        description="Добро пожаловать в захватывающий мир 'Покера на костях' — игру, где удача и стратегия идут "
                    "рука об руку! Испытай свою судьбу, бросая пять кубиков, чтобы собрать одну из выигрышных "
                    "комбинаций и получить заслуженную награду!\n\n"
                    "Правила игры просты. Сделайте ставку и бросьте пять кубиков - после чего посмотрите, что выпадет. "
                    "В случае, если вы сразу собрали одну из выигрышных комбинаций — поздравляем, вы победитель! "
                    "Если же удача не на вашей стороне, не беда! У вас есть второй шанс: выберите до двух кубиков и "
                    "перебросьте их, чтобы улучшить свой результат. После второго броска ваш набор считается "
                    "окончательным, и производится расчет выигрыша.\n\n"
                    "*Список выигрышных комбинаций и коэффициенты выплат:*\n\n"
                    "- **Тройка** (три кости с одинаковым значением): **1.5:1**\n"
                    "- **Фулл-хаус** (пара и тройка с одинаковыми значениями): **2:1**\n"
                    "- **Каре** (четыре кости с одинаковым значением): **3:1**\n"
                    "- **Малый стрит** (последовательность из четырех чисел): **5:1**\n"
                    "- **Большой стрит** (последовательность из пяти чисел): **10:1**\n"
                    "- **Покер** (все пять костей одинаковы): **25:1**\n\n"
                    f"Минимальный размер ставки: **3** {config.FROG_EMOJI}, максимальный: **15** {config.FROG_EMOJI}\n\n"
                    "Используйте свою интуицию, стратегию и немного удачи, чтобы стать мастером покера на костях! "
                    "Готовы испытать судьбу? Бросайте кости и собирайте лучшие комбинации!",
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
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def yahtzee_no_bet_error():
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description="Ты не сделал ставку!",
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
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}

def yahtzee_reroll_set(dice_index):
    dice = ["Первая", "Вторая", "Третья", "Четвертая", "Пятая"]

    embed_message = MessageContainer(
        title="Установлено",
        description=f"{dice[dice_index]} кость будет брошена повторно.",
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}

def yahtzee_roll_result_no_winning(player=None, final_roll=False, bet=0, dice=None, image_binary_data=None):
    title = "Нет выигрышных комбинаций"
    description = ("Приглушенный свет ламп в зале скользил по поверхности стола, где ты с напряжением наблюдал "
                   "за результатом броска костей. Увы кубики, словно насмехаясь, остановились на комбинации, "
                   f"далёкой от победы:\n\n **{'-'.join(map(str, dice))}**\n\n")
    if not final_roll:
        description += ("Однако отчаиваться было еще рано! У тебя еще есть возможность улучшить свой результат. "
                        "Для этого выбери одну или две кости, которые бы ты хотел выбросить повторно. "
                        "Возможно, именно это позволит тебе собрать выигрышную комбинацию!")
    else:
        description += (f"**<@{player.id}>, ты проиграл {bet} {config.FROG_EMOJI}.\n**"
                        "Ты медленно выдохнул, отпуская надежду на удачу. Карман опустел, но азарт всё ещё пульсировал в "
                        "груди. Со стола раздался чей-то смешок — игра продолжалась, но для тебя она уже закончилась.")

    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path="yahtzee_result.jpg",
        image_binary_data=image_binary_data.getvalue()
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}

def yahtzee_roll_result_winning(player, winning_combination, bet, winnings, dice=None, image_binary_data=None):
    winning_type = {
        'small': ["three-of-a-kind", "four-of-a-kind", "full-house", "small-straight"],
        'large': ["large-straight", "yahtzee"]
    }
    winning_name = {
        "three-of-a-kind": "тройка",
        "four-of-a-kind": "каре",
        "full-house": "фулл хаус",
        "small-straight": "малый стрит",
        "large-straight": "большой стрит",
        "yahtzee": "покер"
    }
    if winning_combination in winning_type['small']:
        description = (f"Кости с глухим стуком ударились о стол и замерли, показывая скромную, но выигрышную комбинацию:\n\n "
                       f"**{'-'.join(map(str, sorted(dice)))}**\n"
                       f"(*{winning_name[winning_combination]}*)\n\n"
                       f"<@{player.id}>, ты выиграл **{winnings}** {config.FROG_EMOJI}.\n💰 **С учетом ставки твоя "
                       f"чистая прибыль составила {winnings - bet} {config.FROG_EMOJI}**\n\n"
                       f"Ты выдохнул с облегчением, чувствуя лёгкий прилив радости. Пусть это не было триумфом, но "
                       f"небольшая победа согревала душу. Ты собрал свои фишки — немного больше, чем было в начале "
                       f"игры, — и задумался: продолжить или уйти на этой ноте? Ведь вечер ещё не кончился, а удача всё "
                       f"ещё могла улыбнуться шире!")
    if winning_combination in winning_type['large']:
        description = ("Кубики прыгали по столу, как будто решая твою судьбу. Сердце замерло, когда они остановились, "
                       "и вот — идеальная комбинация:\n\n"
                       f"**{'-'.join(map(str, sorted(dice)))}**\n"
                       f"(*{winning_name[winning_combination]}*)\n\n"
                       f"<@{player.id}>, ты выиграл баснословные **{winnings}** {config.FROG_EMOJI}.\n💰 **С учетом ставки твоя "
                       f"чистая прибыль составила {winnings - bet} {config.FROG_EMOJI}**\n\n"
                       f"Взрыв радости и завистливые взгляды соперников окутали тебя. Ты не мог поверить своим "
                       f"глазам: это и впрямь был {winning_name[winning_combination]}! Выигранные лягушки с громким кваканьем прыгали в "
                       f"твою сторону, и ты почувствовал себя королём этого вечера. Сегодня удача была твоей спутницей, "
                       f"и весь Лаграс казался готовым склониться перед твоей победой!")
    embed_message = MessageContainer(
        title="Это победа! Болотные сокровища теперь твои!",
        description=description,
        file_path="yahtzee_result.jpg",
        image_binary_data=image_binary_data.getvalue()
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}