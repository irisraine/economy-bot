import nextcord
import engine.config as config
from datetime import datetime
import engine.utils as utils


class MessageContainer:
    def __init__(self, title=None, description=None, file_path=None):
        self.__content = None
        self.__embed = None
        if not file_path:
            file_path = config.SEPARATOR
        file_name = file_path.split('/')[-1]
        if file_name.split('.')[-1] in ['jpg', 'jpeg', 'png']:
            self.__embed = nextcord.Embed(
                title=title,
                description=description,
                colour=nextcord.Colour.from_rgb(*config.BASIC_COLOR_CODE),
            )
            image_attachment = f"attachment://{file_name}"
            self.__embed.set_image(url=image_attachment)
        else:
            self.__content = description
        self.__file = nextcord.File(file_path, filename=file_name)

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
    return MessageContainer(
        title="**Добро пожаловать в наш магазинчик на болоте!**",
        description=f"***1. Трек про Леху - {config.PRICES['track']} <:1frg:1286272480083836970>*** "
                        "Один из легендарных хитов из платинового альбома о величайшем повелителе жаб, грозная слава о котором однажды гремела по всему Лаграсу.\n\n"    
                        f"***2. Лягушка - {config.PRICES['frog']} <:1frg:1286272480083836970>***"
                        "Профессиональная фотография одной из прекрасных представительниц отряда земноводных. Собери всю коллекцию, если ты настоящий фанат лягушек.\n\n"                        
                        f"***3. Случайная мудрая мысль на день- {config.PRICES['cite']} <:1frg:1286272480083836970>***"
                        "Кусочек мудрости, который позволит тебе преисполниться и задуматься о вечном.\n\n"                        
                        f"***4. Случайное фото домашнего любимца - {config.PRICES['animal']} <:1frg:1286272480083836970>***"
                        "Фото забавного и милого пушистика. Кошки, собаки, попугаи, кролики, грызуны. А если очень повезет, то ты даже сможешь увидеть лису!\n\n"
                        f"***5. Случайный мем - {config.PRICES['meme']} <:1frg:1286272480083836970>***"
                        "Ржака. Просто ржака. \n\n"
                        f"***6. Сделать заказ в ресторане 'Жабий квак' - {config.PRICES['food']} <:1frg:1286272480083836970>***"
                        "Вкуснейшая и изысканная пища. Настоящий пир! Последние пару месяцев ты был вынужден перебиваться одной лишь дрянной пустой похлебкой из походного котелка? Теперь побалуй себя!\n\n"
                        f"***7. Случайный саундпад Лехи - {config.PRICES['soundpad']} <:1frg:1286272480083836970>***"
                        "Уникальная возможность услышать несколько секунд живой речи величайшего повелителя жаб.\n\n"
                        f"***8. Скетчик с вашим животным/вами в антропоморфном стиле - {config.PRICES['drawing']} <:1frg:1286272480083836970>***"
                        "Профессиональный художник с уникальным видением, стилем и двадцатилетним опытом рисования сотворит художественный шедевр, увековечивающий тебя и твоего домашнего любимца.\n\n"
                        f"***9. Дождь из лягушек - {config.PRICES['rain']} <:1frg:1286272480083836970>***"
                        "Устрой апокалипсис! Простри руку твою с жезлом твоим на реки, на потоки и на озера и выведи лягух на землю Лаграсскую. Алексей простёр руку свою на воды Миссисипи; и вышли лягушки и покрыли землю Лаграсскую.\n\n"
                        f"***10. Ивент - {config.PRICES['event']} <:1frg:1286272480083836970>***"
                        "Стань организатором своего собственного ивента. Давно мечтал о том, чтобы сотни людей поучаствовали в твоем диком и безумном квесте? Сейчас самое время!\n\n"
                        f"***11. Роль 'Легушька' на 1 месяц - {config.PRICES['role']} <:1frg:1286272480083836970>***"
                        "Драгоценная донатная роль <@&1286287383762960384>, доступная только состоятельным людям и дающая доступ в закрытый клуб сервера и множество иных привилегий, теперь станет твоей.\n\n"
                        f"***12. Банда - {config.PRICES['band']} <:1frg:1286272480083836970>***"
                        "Сколоти свою собственную банду, которая будет наводить леденящий ужас на весь Лаграс.\n\n",
        file_path=config.SHOP_ENTRANCE_IMAGE
    )

def catch(user, amount):
    match amount:
        case amount if amount == 0:
            result = "fault"
        case amount if 1 <= amount <= 2:
            result = "common"
        case amount if 3 <= amount <= 4:
            result = "uncommon"
        case amount if 5 <= amount <= 6:
            result = "rare"
        case amount if amount >= 7:
            result = "legendary"
        case _:
            result = "fault"

    results = {
        "fault": {
            "title": "Это фиаско, братан...",
            "description": f"{user}, ты не поймал ни одной лягушки :( "
                           f"Они оказались слишком прыткими и ускользнули из твоих пальцев!",
            "file_path": config.CATCH_FAULT_IMAGE
        },
        "common": {
            "title": "Успех!",
            "description": f"Поздравляем тебя, {user}! Ты поймал {amount} {utils.numeral(amount)}. "
                           f"Это довольно скромный результат, однако ловля лягушек - тяжелый труд, "
                           f"так что ты по праву можешь гордиться собой.",
            "file_path": config.CATCH_COMMON_IMAGE
        },
        "uncommon": {
            "title": "Удача!",
            "description": f"Поздравляем тебя, {user}! Ты оказался достаточно умелым ловцом, "
                           f"и поймал {amount} {utils.numeral(amount)}",
            "file_path": config.CATCH_UNCOMMON_IMAGE
        },
        "rare": {
            "title": "Впечатляющий результат!",
            "description": f"Здорово {user}! Ты поистине превзошел сам себя, далеко не каждому ловцу так везет. "
                           f"Сегодня тебе удалось поймать аж {amount} {utils.numeral(amount)}",
            "file_path": config.CATCH_RARE_IMAGE
        },
        "legendary": {
            "title": "Грандиозное событие!",
            "description": f"{user}, тебе сегодня невероятно повезло! Ты поймал аж {amount} {utils.numeral(amount)} "
                           f"за один раз. О таком грандиозном улове сложат легенды все жители ближайших "
                           f"рыбацких деревень.",
            "file_path": config.CATCH_LEGENDARY_IMAGE
        }
    }
    return MessageContainer(
        title=results[result]['title'],
        description=results[result]['description'],
        file_path=results[result]['file_path']
    )

def cooldown(delta_time):
    return MessageContainer(
        title="Не так быстро!",
        description=f"Лягушек можно ловить только один раз в 10 секунд. "
                    f"Подожди еще **{datetime.fromtimestamp(config.CATCHING_COOLDOWN - delta_time).strftime('%H:%M:%S')}** перед следующей попыткой",
        file_path=config.COOLDOWN_IMAGE
    )

def balance(user, user_balance):
    if user_balance == 0:
        description = f"{user}, на твоем счету пока еще нет ни одной лягушки. Самое время заняться их ловлей!"
    else:
        description = f"{user}, сейчас у тебя на счету **{user_balance}** <:1frg:1286272480083836970>."
    return MessageContainer(
        title="Лягушачий баланс",
        description=description,
        file_path=config.BALANCE_IMAGE
    )

def insufficient_balance():
    return MessageContainer(
        title="Недостаточно средств",
        description=f"К сожалению, в твоем болоте слишком мало лягушек, и ты не можешь позволить себе покупку столь дорогостоящего товара. Недаром говорят, что нищета хуже воровства!",
        file_path=config.COOLDOWN_IMAGE
    )

def balance_bank():
    pass

def buying_confirmation(item, price):
    return MessageContainer(
        title="Подтверждение покупки",
        description=f"Вы собираетесь приобрести **{item}** за **{price}** <:1frg:1286272480083836970>",
        file_path=config.SHOP_COUNTER_IMAGE
    )

def item_purchased(item):
    items = {
        "track": "> **Песня о легендарном предводителе жаб.**",
        "frog": "**Лягушки — эт хорошо. В карман.**",
        "cite": "**Из мудрых уст — и прямиком в блокноты.**",
        "animal": "**Заботьтесь о нем как следует.**",
        "meme": "**Держи краба.**",
        "food": "**Паеш.**",
        "soundpad": "> **У рыб был вопрос к морю, и отвечал волн бас:**\n > **«Теперь он ваше горе, и будет жить у вас.»**",
        "drawing": "*Сообщение о покупке услуги отправлено администратору.* \n\nСвяжитесь с <@1058616492758941787>, чтобы она нарисовала персонально для вас шедевр, который вы сможете с гордостью повесить на стену.",
        "rain": "*Сообщение о покупке услуги отправлено администратору.* \n\nВолшебники Изумрудного города уже прогревают свои адские машины, чтобы обрушить апокалиптический лягушачий дождь на грешный мир. Не спасется никто!",
        "event": "*Сообщение о покупке услуги отправлено администратору.* \n\nДело за малым - изложите @ свои безумные планы, и на ближайшее время весь сервер поучаствует в вашем авторском приключении",
        "role": "*Теперь вы принадлежите к земноводной элите этого сервера.* Слышите звук? Это перед вами раскрылись потаенные двери, где вас уже ждут другие посвященные.",
        "band": "*Сообщение о покупке услуги отправлено администратору.* \nСобирай людей под свои знамена. Отныне вы банда! Сообщи администраторам, и они создадут для тебя и твоих друзей закрытый канал, чат и собственную уникальную роль.",
    }
    service = True if (item in ["drawing", "rain", "event", "role", "band"]) else False

    title = "Премиум-услуга приобретена!" if service else None
    if not service:
        file_path = utils.get_random_shop_item_filepath(item)
    else:
        file_path = config.SHOP_ITEMS_SERVICES[item]

    return MessageContainer(
        title=title,
        description=items[item],
        file_path=file_path,
    )

def transfer(other_user, amount):
    return MessageContainer(
        title="Перевод земноводных средств",
        description=f"Вы собираетесь от чистого сердца подарить {amount} {utils.numeral(amount)} пользователю {other_user.mention}.",
        file_path=config.TRANSFER_IMAGE
    )

def transfer_successful(other_user, amount):
    return MessageContainer(
        title="Перевод произведен успешно",
        description=f"Вы выпустили {amount} {utils.numeral(amount)} в болото, принадлежащее {other_user.mention}.",
        file_path=config.TRANSFER_SUCCESS_IMAGE
    )

def transfer_denied(other_user, amount):
    return MessageContainer(
        title="Перевод невозможен",
        description=f"К сожалению, в твоем болоте слишком мало лягушек, и ты не можешь позволить себе перевести {other_user.mention} целых {amount} {utils.numeral(amount)}. Если хочешь исправить эту ситуацию, пойди и займись их ловлей.",
        file_path=config.TRANSFER_DENIED_IMAGE
    )

def transfer_failed(reason):
    if reason == "to_bot":
        description = "Вы не можете подарить лягушек боту! Поверьте, он не оценит."
        file_path=config.TRANSFER_FAILED_TO_BOT_IMAGE
    elif reason == "to_self":
        description = f"Вы не можете подарить лягушек самому себе, в этом нет никакого смысла!"
        file_path = config.TRANSFER_FAILED_TO_SELF_IMAGE
    return MessageContainer(
        title="Перевод невозможен",
        description=description,
        file_path=file_path
    )

def caching_successful(files_count_printable):
    return MessageContainer(
        title="Кэширование завершено",
        description=f"Количество файлов в папках:\n\n{files_count_printable}"
    )

def admin_panel():
    return MessageContainer(
        title="Админка",
        description=f"Настройки бота, доступные только для администраторов",
        file_path=config.ADMIN_PANEL_IMAGE
    )

def not_applied_yet():
    return MessageContainer(
        title="В разработке",
        description=f"Эта функция будет добавлена несколько позднее. Имейте терпение.",
    )
