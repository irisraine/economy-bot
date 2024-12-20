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
