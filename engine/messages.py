import nextcord
import os
import io
import logging
import engine.config as config
import engine.utils as utils
import engine.sql as sql

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
            if not os.path.isfile(file_path):
                logging.error(f"Произошла ошибка при попытке открытия файла '{file_path}'! Файл не найден.")
                title = ERROR_HEADER
                if "shop_items" in file_path:
                    description = ERROR_DESCRIPTION_SHOP
                    file_path = config.ERROR_SHOP_IMAGE
                else:
                    description = ERROR_DESCRIPTION_GENERAL
                    file_path = config.ERROR_IMAGE
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


def shop():
    embed_message = MessageContainer(
        title="**Добро пожаловать в магазин сервера West Wolves!**",
        description=f"***1. Трек про Леху - {config.PRICES['track']} {config.FROG_EMOJI}***"
                    "Один из легендарных хитов о величайшей лягушке в мире.\n\n"
                    f"***2. Лягушка - {config.PRICES['frog']} {config.FROG_EMOJI}***"
                    "Профессиональная фотография одной из прекрасных представительниц отряда земноводных. "
                    "Собери всю коллекцию, если ты настоящий фанат лягушек.\n\n"
                    f"***3. Случайная мудрая мысль на день- {config.PRICES['cite']} {config.FROG_EMOJI}***"
                    "Кусочек мудрости, который позволит тебе преисполниться и задуматься о вечном.\n\n"
                    f"***4. Случайное фото домашнего любимца - {config.PRICES['animal']} {config.FROG_EMOJI}***"
                    "Фото забавного и милого пушистика: кошки, собаки, попугая, кролика, грызуна. "
                    "А если очень повезет, то ты сможешь увидеть лису!\n\n"
                    f"***5. Случайный мем - {config.PRICES['meme']} {config.FROG_EMOJI}***"
                    "Отборная смешнявая картинка.\n\n"
                    f"***6. Сделать заказ в ресторане «Жабий квак» - {config.PRICES['food']} {config.FROG_EMOJI}***"
                    "Изысканная пища аристократов. Последние пару месяцев ты был вынужден перебиваться "
                    "«Ужином петуха» из лагерного котелка? Теперь побалуй себя!\n\n"
                    f"***7. Случайный саундпад Лехи - {config.PRICES['soundpad']} {config.FROG_EMOJI}***"
                    "Уникальная возможность услышать мудрые высказывания величайшей лягушки в мире.\n\n"
                    f"***8. Скетч с вашим животным/вами в антропоморфном стиле - {config.PRICES['drawing']} {config.FROG_EMOJI}***"
                    "Небольшой арт исключительно для вас от администратора сервера.\n\n"
                    f"***9. Дождь из лягушек - {config.PRICES['rain']} {config.FROG_EMOJI}***"
                    "Устрой апокалипсис! Простри руку твою с жезлом твоим на реки, на потоки и на озера и выведи "
                    "лягух на землю Лаграсскую. Алексей простёр руку свою на воды Камассы; и вышли лягушки и "
                    "покрыли землю Лаграсскую.\n\n"
                    f"***10. Роль «Лягушонок» на 1 месяц - {config.PRICES['role_lite']} {config.FROG_EMOJI}***"
                    f"Донатная роль <@&{config.PREMIUM_ROLE['lite']}>. Первая ступень элитной земноводной иерархии "
                    "сервера. С ней тебе будет доступен ряд небольших привилегий: уникальная роль, приватный "
                    "голосовой чат и дождь из лягушек.\n\n"
                    f"***11. Роль «Легушька» на 1 месяц - {config.PRICES['role']} {config.FROG_EMOJI}***"
                    f"Донатная роль <@&{config.PREMIUM_ROLE['basic']}>, доступная только состоятельным людям и дающая "
                    "доступ в приватный голосовой чат сервера, дождь из лягушек, билет на караван без повозки и "
                    "скетч в антропоморфном стиле, теперь станет твоей.\n\n"
                    f"***12. Банда - {config.PRICES['band']} {config.FROG_EMOJI}***"
                    "Создай свою собственную банду, слава о которой прогремит по всему Дикому Западу. "
                    "Требуется от 7 постоянных участников.\n\n",
        file_path=config.SHOP_ENTRANCE_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def catch(user, amount):
    match amount:
        case amount if amount == 0:
            result = "fault"
        case amount if 1 <= amount <= 2:
            result = "common"
        case amount if 3 <= amount <= 4:
            result = "uncommon"
        case amount if 5 <= amount <= 6:
            result = "epic"
        case amount if amount >= 7:
            result = "legendary"
        case _:
            result = "fault"

    results = {
        "fault": {
            "title": "Увы и ах!",
            "description": f"{user}, ты не поймал ни одной лягушки. "
                           "Они оказались слишком прыткими и ускользнули из твоих пальцев!",
            "file_path": config.CATCH_FAULT_IMAGE
        },
        "common": {
            "title": "Ура!",
            "description": f"Поздравляем тебя, {user}! Ты поймал **{amount}** {utils.numeral(amount)}. "
                           "Это довольно скромный результат, однако ловля лягушек - тяжелый труд, "
                           "поэтому ты можешь гордиться собой.",
            "file_path": config.CATCH_COMMON_IMAGE
        },
        "uncommon": {
            "title": "О, нифигасе, класс!",
            "description": f"Поздравляем тебя, {user}! Ты оказался достаточно умелым ловцом, "
                           f"и поймал **{amount}** {utils.numeral(amount)}.",
            "file_path": config.CATCH_UNCOMMON_IMAGE
        },
        "epic": {
            "title": "Лепота, красота!",
            "description": f"Здорово {user}! Ты поистине превзошел сам себя, далеко не каждому ловцу так везет. "
                           f"Сегодня тебе удалось поймать аж **{amount}** {utils.numeral(amount)}.",
            "file_path": config.CATCH_EPIC_IMAGE
        },
        "legendary": {
            "title": "Какая красотень!",
            "description": f"{user}, сегодня тебе невероятно повезло! Ты поймал "
                           f"целых **{amount}** {utils.numeral(amount)} за один раз. "
                           f"О таком грандиозном улове сложат легенды все жители ближайших лаграсских деревень.",
            "file_path": config.CATCH_LEGENDARY_IMAGE
        }
    }
    embed_message = MessageContainer(
        title=results[result]['title'],
        description=results[result]['description'],
        file_path=results[result]['file_path']
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def cooldown(delta_time):
    embed_message = MessageContainer(
        title="Не так быстро!",
        description=f"Лягушек можно ловить только один раз "
                    f"в **{config.CATCHING_COOLDOWN}** {utils.numeral(config.CATCHING_COOLDOWN, value_type='hours')}. "
                    f"Подожди еще **{utils.from_timestamp(config.CATCHING_COOLDOWN * 3600 - delta_time)}** "
                    f"перед следующей попыткой.",
        file_path=config.COOLDOWN_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def balance(user, user_balance):
    if user_balance == 0:
        description = f"{user}, в твоем пруду пока нет ни одной лягушки. Самое время заняться их ловлей!"
    else:
        description = f"{user}, сейчас у тебя в пруду **{user_balance}** {config.FROG_EMOJI}."
    embed_message = MessageContainer(
        title="Лягушачий баланс",
        description=description,
        file_path=config.BALANCE_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def insufficient_balance():
    embed_message = MessageContainer(
        title="Недостаточно средств",
        description="К сожалению, в твоем пруду слишком мало лягушек, и ты не можешь позволить себе покупку "
                    "данного товара. Недаром говорят, что нищета хуже воровства!",
        file_path=config.TRANSFER_DENIED_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def purchasing_confirmation(item, price):
    embed_message = MessageContainer(
        title="Подтверждение покупки",
        description=f"Вы собираетесь приобрести **{item}** за **{price}** {config.FROG_EMOJI}.",
        file_path=config.SHOP_COUNTER_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def item_purchased(item):
    items = {
        "track": "> **Песня о величайшей лягушке в мире.**",
        "frog": "**Лягушки — эт хорошо. В карман.**",
        "cite": "**Из мудрых уст — и прямиком в блокноты.**",
        "animal": "**Заботьтесь о нем как следует.**",
        "meme": "**Держи краба.**",
        "food": "**Паеш.**",
        "soundpad": "> **У рыб вопрос был к морю, и волн ответил бас:**\n "
                    "> **«Теперь он ваше горе, и будет жить у вас.»**",
        "drawing": "*Сообщение о покупке услуги отправлено администратору.* \n\n"
                   f"Свяжитесь с <@{config.ADMIN_ID}>, чтобы она нарисовала персонально для вас шедевр на века, "
                   "который вы сможете с гордостью повесить на стену.",
        "rain": "*Сообщение о покупке услуги отправлено администратору.* \n\n"
                "Волшебники Изумрудного города уже раскочегаривают свои адские машины, чтобы обрушить "
                "апокалиптический лягушачий дождь на грешный мир. Не спасется никто!",
        "role": "*Теперь вы принадлежите к земноводной элите этого сервера.* \n\n"
                "Лягушек слышите, как квакают? Это другие посвященные, готовые принять в свой тесный круг болотной "
                "элиты, ожидают вас.\n\n"
                "`Роль выдается на 30 календарных дней с момента покупки.`",
        "role_lite": "*Теперь ты лягушонок! Маленький, но очень важный.* \n\n"
                "Теперь вместе со своими земноводными братьями ты отправишься в дивное, объятое мглой чудес болото. "
                "И в этой исконной обители лягушек обретешь новую, славную и чудесную жизнь.\n\n"
                "`Роль выдается на 30 календарных дней с момента покупки.`",
        "band": "*Сообщение о покупке услуги отправлено администратору.* \n\n"
                "Собирай людей под свои знамена. Отныне вы банда! Сообщи администраторам, и они создадут для тебя "
                "и твоих друзей закрытый канал, чат и дадут собственную уникальную роль.",
    }
    service = True if (item in ["drawing", "rain", "role_lite", "role", "band"]) else False

    title = "Премиум-услуга приобретена!" if service else None
    description = items[item]
    if not service:
        file_path = utils.get_random_shop_item(item)
    else:
        file_path = config.SHOP_ITEMS_SERVICES[item]

    if file_path is None:
        title = ERROR_HEADER
        description = ERROR_DESCRIPTION_SHOP
        file_path = config.ERROR_SHOP_IMAGE

    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path,
    )
    return {'content': embed_message.content, 'embed': embed_message.embed, 'file': embed_message.file}


def transfer(other_user, amount):
    embed_message = MessageContainer(
        title="Перевод земноводных средств",
        description=f"Вы собираетесь от чистого сердца подарить **{amount}** {utils.numeral(amount)} "
                    f"пользователю {other_user.mention}.",
        file_path=config.TRANSFER_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def transfer_confirmation(other_user, amount, is_failed=False):
    if not is_failed:
        title = "Перевод произведен успешно"
        description = f"Вы выпустили **{amount}** {utils.numeral(amount)} в пруд, принадлежащий {other_user.mention}."
        file_path = config.TRANSFER_SUCCESS_IMAGE
    else:
        title = "Перевод невозможен"
        description = (f"К сожалению, в твоем пруду слишком мало лягушек, и ты не можешь позволить себе "
                       f"перевести {other_user.mention} целых **{amount}** {utils.numeral(amount)}.")
        file_path = config.TRANSFER_DENIED_IMAGE
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def transfer_denied(reason):
    if reason == "to_bot":
        description = "Вы не можете подарить лягушек боту! Поверьте, он не оценит."
        file_path = config.TRANSFER_FAILED_TO_BOT_IMAGE
    elif reason == "to_self":
        description = "Вы не можете подарить лягушек самому себе, в этом нет никакого смысла!"
        file_path = config.TRANSFER_FAILED_TO_SELF_IMAGE
    elif reason == "non_positive_amount":
        description = "Количество переводимых лягушек должно быть положительным числом."
        file_path = config.TRANSFER_DENIED_IMAGE
    embed_message = MessageContainer(
        title="Перевод невозможен",
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def service_request(user, item):
    services = {
        "drawing": "просит нарисовать для него **авторский рисунок**.",
        "rain": "вызывает **дождь из лягушек**.",
        "role_lite": "приобрел **роль лягушонка**.",
        "role": "приобрел **роль лягушки**.",
        "band": "запрашивает создание собственной **банды** на сервере.",
    }
    embed_message = MessageContainer(
        title="Пользователь приобрел премиум-услугу",
        description=f"Пользователь {user} потратил **{config.PRICES[item]}** {config.FROG_EMOJI}, и {services[item]}",
        file_path=config.SHOP_ITEMS_SERVICES[item]
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def caching_confirmation(files_count_printable):
    if files_count_printable:
        title = "Кэширование завершено"
        description = f"Количество файлов в папках:\n\n{files_count_printable}"
        file_path = config.CACHING_SUCCESSFUL_IMAGE
    else:
        title = ERROR_HEADER
        description = ("Ошибка при кэшировании файлов. Проверьте наличие директории 📁***shop_items*** и всех "
                       "необходимых подпапок с содержимым.")
        file_path = config.ERROR_IMAGE
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def already_has_premium_role(user, premium_role):
    embed_message = MessageContainer(
        title="Роль уже назначена ранее",
        description=f"{user.mention}, ты уже принадлежишь к земноводной элите, обладаешь "
                    f"донатной ролью {premium_role.mention} и живешь в болоте, как царь. Дождись завершения "
                    f"срока подписки перед тем, как совершить покупку.",
        file_path=config.ROLE_LISTING_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def admin():
    embed_message = MessageContainer(
        title="Админка",
        description="Настройки бота, доступные только для администраторов.",
        file_path=config.ADMIN_MENU_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def set_price():
    embed_message = MessageContainer(
        title="Установить новую цену на товар",
        description="Установка цены на товар",
        file_path=config.SET_PRICE_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def set_price_confirmation(is_valid=True):
    if is_valid:
        title = SUCCESS_HEADER
        description = "Новая цена установлена!"
        file_path = config.SUCCESS_OPERATION_IMAGE
    else:
        title = ERROR_HEADER
        description = "Вы установили неправильную цену. Цена должна быть целым положительным числом!"
        file_path = config.ERROR_IMAGE
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def reset_prices_confirmation():
    embed_message = MessageContainer(
        title=SUCCESS_HEADER,
        description="Установлены цены по умолчанию!",
        file_path=config.SUCCESS_OPERATION_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def set_probabilities():
    embed_message = MessageContainer(
        title="Установить вероятности отлова",
        description="Задайте в процентах в открывшейся форме вероятности отлова определенного количества лягушек: \n\n"
                    "Обычный улов — **1-2** лягушки\n"
                    "Редкий улов — **3-4** лягушки\n"
                    "Эпический — **5-6** лягушек\n"
                    "Легендарный — **7-45** лягушек\n\n"
                    "Имейте в виду, что каждая последующая вероятность должна обязательно быть меньше предыдущей!",
        file_path=config.SET_PROBABILITIES_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def set_probabilities_confirmation(is_valid=True):
    if is_valid:
        title = SUCCESS_HEADER
        description = "Новые значения вероятностей отлова установлены!"
        file_path = config.SUCCESS_OPERATION_IMAGE
    else:
        title = ERROR_HEADER
        description = ("Вы ошиблись при установке вероятностей. Внимательно перечитайте требования "
                       "к устанавливаемым значениям.")
        file_path = config.ERROR_IMAGE
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def reset_probabilities_confirmation():
    embed_message = MessageContainer(
        title=SUCCESS_HEADER,
        description="Установлены вероятности по умолчанию!",
        file_path=config.SUCCESS_OPERATION_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def set_cooldown():
    embed_message = MessageContainer(
        title="Установить новую продолжительность кулдауна",
        description="Укажите длительность промежутка между ловлями лягушек. "
                    "Он должен составлять не менее 1, и не более 24 часов.",
        file_path=config.SET_PRICE_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def set_cooldown_confirmation(is_valid=True):
    if is_valid:
        title = SUCCESS_HEADER
        description = "Новое значение кулдауна установлено!"
        file_path = config.SUCCESS_OPERATION_IMAGE
    else:
        title = ERROR_HEADER
        description = ("Вы установили ошиблись при установке кулдауна. "
                       "Внимательно перечитайте требования к устанавливаемым значению")
        file_path = config.ERROR_IMAGE
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def reset_cooldown_confirmation():
    embed_message = MessageContainer(
        title=SUCCESS_HEADER,
        description="Установлена продолжительность кулдауна по умолчанию!",
        file_path=config.SUCCESS_OPERATION_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def post_news():
    embed_message = MessageContainer(
        title="Отправить сообщение от лица бота",
        description=f"Сообщение будет отправлено в новостной канал <#{config.NEWS_CHANNEL_ID}>.",
        file_path=config.NEWS_POST_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def post_news_confirmation():
    embed_message = MessageContainer(
        title=SUCCESS_HEADER,
        description="Сообщение отправлено!",
        file_path=config.SUCCESS_OPERATION_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def news_channel_message(title, description, image_binary_data=None, image_filename=None):
    file_path = image_filename if image_filename else config.NEWS_POST_IMAGE
    embed_message = MessageContainer(
        title=f"**{title}**",
        description=description,
        file_path=file_path,
        image_binary_data=image_binary_data
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def bank_balance():
    embed_message = MessageContainer(
        title="Баланс болотного банка",
        description="Общий объем лягушек в банковском болоте "
                    f"составляет **{sql.get_bank_balance()}** {config.FROG_EMOJI}. "
                    "Именно столько в сумме потратили участники нашего сервера на покупки в магазине!",
        file_path=config.BANK_BALANCE_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def all_users_balances():
    max_users = 100
    embed_messages = []
    all_users_balances_list = sql.get_all_users_balances()
    number_of_users = len(all_users_balances_list)
    if number_of_users == 0:
        embed_message = MessageContainer(
            title="Земноводные балансы всех пользователей",
            description="В это верится с трудом, но в целом мире еще никто не поймал ни одной лягушки :(. "
                        "Либо же все ловцы умудрились одновременно растратить свои состояния.",
            file_path=config.ALL_USERS_BALANCES_IMAGE
        )
        return {'embed': embed_message.embed, 'file': embed_message.file}
    number_of_embeds = (number_of_users + max_users - 1) // max_users
    for i in range(number_of_embeds):
        start = max_users * i
        end = start + max_users
        users_slice = all_users_balances_list[start:end]
        description = "\n".join([
            f"{index + 1}. {user_balance[0]} — **{user_balance[1]}**"
            for index, user_balance in enumerate(users_slice, start=start)
        ])
        title = "Земноводные балансы всех пользователей" if i == 0 else None
        file_path = config.ALL_USERS_BALANCES_IMAGE if i == (number_of_embeds - 1) else None
        if i == 0:
            description = ("Список балансов пользователей сервера, поймавших и имеющих "
                           "в своем пруду хотя бы одну лягушку: \n\n") + description
        embed_message = MessageContainer(
            title=title,
            description=description,
            file_path=file_path
        )
        embed_messages.append(embed_message)
    return {
        'embeds': [embed_message.embed for embed_message in embed_messages],
        'files': [embed_message.file for embed_message in embed_messages]
    }


def gift():
    embed_message = MessageContainer(
        title="Подарить сокровище от админа",
        description="Вы собираетесь от чистого сердца подарить другому пользователю целое состояние - или одну "
                    "лягушку. Главное, что вы хозяин болота и не ограничены ничем!",
        file_path=config.GIFT_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def gift_confirmation(other_user, amount, is_valid=True):
    if not other_user:
        title = ERROR_HEADER
        description = "Перевод невозможен. Пользователя с таким именем нет на нашем сервере."
        file_path = config.ERROR_IMAGE
    elif is_valid:
        title = "Перевод от админа произведен успешно"
        description = (f"Вы выпустили **{amount}** {utils.numeral(int(amount))} в пруд, "
                       f"принадлежащий **{other_user.mention}**.")
        file_path = config.GIFT_SUCCESS_IMAGE
    else:
        title = ERROR_HEADER
        description = "Перевод невозможен. Похоже, вы ошиблись при вводе количества лягушек."
        file_path = config.ERROR_IMAGE
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def role_manage():
    def get_role_owners_description(role_owners, current_time, role_id):
        description = ""
        for i, role_owner in enumerate(role_owners):
            expiration_time = role_owner[1]
            if expiration_time > current_time:
                if expiration_time - current_time < 86400:
                    expire = "истекает **сегодня!**"
                else:
                    expiration_date = utils.from_timestamp(expiration_time, mode="date")
                    expire = f"истекает **{expiration_date}**."
            else:
                expire = "**уже истекла!**"
            description += f"{i}. {role_owner[0]} — {expire}\n"

        if description:
            return (f"Нижеприведенные участники на данный момент обладают "
                    f"донатной ролью <@&{role_id}>:\n\n{description}\n")
        else:
            return (f"Еще ни один участник не смог позволить себе приобрести "
                    f"донатную роль <@&{role_id}>.\n\n")

    current_time = utils.get_timestamp()
    description = ""
    premium_role_lite_owners = sql.get_all_premium_role_owners(lite=True)
    premium_role_owners = sql.get_all_premium_role_owners()
    description += get_role_owners_description(premium_role_lite_owners, current_time, config.PREMIUM_ROLE['lite'])
    description += get_role_owners_description(premium_role_owners, current_time, config.PREMIUM_ROLE['basic'])
    if premium_role_owners or premium_role_lite_owners:
        description += ("*Если в списке имеются участники, чей срок использования роли истек, "
                        "снимите с них роль c помощью соответствующей кнопки.*")

    embed_message = MessageContainer(
        title="Список обладателей донатных ролей",
        description=description,
        file_path=config.ROLE_LISTING_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def role_expired_and_removed(is_expired_role_owners):
    if is_expired_role_owners:
        title = SUCCESS_HEADER
        description = "Участники с просроченными донатными ролями лишились их."
        file_path = config.ROLE_REMOVAL_IMAGE
    else:
        title = ERROR_HEADER
        description = "Участники с просроченной донатной ролью отсутствуют."
        file_path = config.ERROR_IMAGE
    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def reset_database():
    embed_message = MessageContainer(
        title="Обнуление базы данных",
        description="**Шутки кончились.** \n\n "
                    "Вы собираетесь удалить существующую базу данных и заменить ее на обнуленную. "
                    "Это эквивалентно финансовому апокалипсису, дефолту, мировому кризису и прочим "
                    "экономическим бедам вместе взятым. Все пойманные игроками лягушки, весь тяжелый труд на "
                    "протяжении сотен часов, баланс всемирного болотного банка - все это перестанет существовать "
                    "после нажатия на красную кнопку. \n Это ядерная бомба, взорванная в болоте. \n"
                    "Пожалуйста, тысячу раз подумайте о том, что вы собираетесь делать и зачем!\n\n"
                    "*В целях безопасности вы должны ввести корректный путь к файлу базы данных, "
                    "и лишь после этого обнуление и реинициализация будут осуществлены.*",
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def reset_database_confirmation(is_valid=True):
    if not is_valid:
        title = ERROR_HEADER
        description = "Вы ввели неправильный путь к базе данных. Удаление базы данных запрещено!"
        file_path = config.ERROR_IMAGE
    else:
        title = SUCCESS_HEADER
        description = "База данных успешно обнулена и инициализирована повторно."
        file_path = config.SUCCESS_OPERATION_IMAGE

    embed_message = MessageContainer(
        title=title,
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def quiz(question, image_binary_data=None, image_filename=None):
    content = f"<@&{config.QUIZ_PARTICIPANT_ID}>"
    file_path = image_filename if image_filename else config.QUIZ_IMAGE
    embed_message = MessageContainer(
        title="Викторина!",
        description=f"Вопрос к знатокам в зале: **{question}?** \n\n"
                    f"Время размышления - _1 минута_.",
        file_path=file_path,
        image_binary_data=image_binary_data
    )
    return {'content': content, 'embed': embed_message.embed, 'file': embed_message.file}


def quiz_error(reason):
    if reason == "incorrect_prize_amount":
        description = ("Ошибка при создании раунда викторины. Похоже, вы ошиблись при вводе размера награды, "
                       "она должна быть целым положительным числом.")
    elif reason == "no_active_quiz":
        description = ("Викторина еще не начата, либо уже завершилась, либо прошло уже более 30 минут после ее начала, "
                       "и время для вручения приза вышло.")
    elif reason == "in_progress":
        description = "Данное участникам время на размышления еще не вышло."
    elif reason == "to_bot":
        description = "Боты не могут быть ни участниками, ни тем более победителями викторины."
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description=description,
        file_path=config.ERROR_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def quiz_time_up(answer):
    embed_message = MessageContainer(
        title="Викторина",
        description=f"Время на раздумье истекло. \n\nПравильный ответ: **{answer}**.",
        file_path=config.QUIZ_TIME_UP
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def quiz_prize(winner, question, prize_amount, prize_special=False):
    description = (f"{winner.mention},  ты дал верный ответ на вопрос «*{question}*». \n\n"
                   f"Маладэц!\n Твои познания вознаграждены - ты получаешь **{prize_amount}** {config.FROG_EMOJI}.\n")
    file_path = config.QUIZ_PRIZE_BASIC
    if prize_special:
        description += (f"Ответив на столь каверзный вопрос, ты также удостоился специального "
                        f"приза, и это - **{prize_special}**! За его получением обратись к администратору.")
        file_path = config.QUIZ_PRIZE_SPECIAL

    embed_message = MessageContainer(
        title="Чвяк чвяк!",
        description=description,
        file_path=file_path
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def image_url_error():
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description="Изображение по ссылке не может быть получено.\n"
                    "Причиной этого может быть неправильно записанная ссылка, неподходящий формат "
                    "изображения или слишком длительное время загрузки. Вам необходимо заполнить форму заново. "
                    "Если эта ошибка будет повторяться, используйте другую ссылку. Либо запостите сообщение "
                    "со стандартным изображением, оставив поле для ссылки пустым.",
        file_path=config.ERROR_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def other_user_transfer_error():
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description="Вы не можете сделать перевод, поскольку эта транзакция принадлежит не вам!",
        file_path=config.TRANSFER_DENIED_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


def admin_option_only_warning():
    embed_message = MessageContainer(
        title=ERROR_HEADER,
        description="Использовать опции админ-панели могут только администраторы сервера.",
        file_path=config.ERROR_IMAGE
    )
    return {'embed': embed_message.embed, 'file': embed_message.file}


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