from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot import bot, admins
from tg_bot.db.sqlite import DataBase
from tg_bot.keyboards.settings import WaitingSettings, cancel_settings
from tg_bot.keyboards.subscription import create_subscription_keyboard, start_menu
from tg_bot.keyboards.direct_production import direct_production
from tg_bot.keyboards.self_ransom import self_ransom
from tg_bot.keyboards.waiting_exchange import exchange_kbd, Waiting, confirm_keyboard
from tg_bot.keyboards.delivery import delivery_cnd, goods_delivery, price_kbd
from tg_bot.middlewares.antiflood import AntiFloodMiddleware

router = Router()
router.message.middleware(AntiFloodMiddleware())
CHANNEL_ID = "@vanish_cn"

# Хранение заявок
applications = {}
applications_counter = 0

# Хранение заявок для перевода
applications_translate = {}
applications_translate_counter = 0

db = DataBase()


async def start_message(message: types.Message, name: str, edit: bool):
    keyboard = start_menu()
    text = (f"Привет, <b>{name}</b>.\n"
            f"<b>Спасибо, что выбрали именно нас</b> 🇨🇳 \n\n"
            f"Выбери одно из действий ниже")

    if edit:
        await message.edit_text(text=text, reply_markup=keyboard)
    else:
        await message.answer(text=text, reply_markup=keyboard)


@router.message(Waiting.waiting_exchange)
async def exchange_choose(message: Message, state: FSMContext):
    keyboard = exchange_kbd()
    if message.text.startswith('/'):
        await message.answer("Пожалуйста, <b>введите число</b>, а не команду.")
        return

    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите <b>корректное число</b>.")
        return

    if int(message.text) < 600:
        await message.answer(
            "Минимальная сумма для обмена - <b>600¥.</b>\nПожалуйста, введите сумму <b>больше или равную 600.</b>")
        return

    if int(message.text) > 10000:
        await message.answer(
            "Максимальная сумма для обмена - <b>10.000¥.</b>\nПожалуйста, введите сумму <b>больше или равную 10.000.</b> ")
        return

    amount = int(message.text)
    total = round(amount * db.get_exchange_rate(), 2)
    confirm_kbd = confirm_keyboard()
    await message.answer(
        text=f"Вы ввели <b>{amount}¥</b>.\nКурс юаня: <b>{db.get_exchange_rate()}</b>.\nИтого: <b>{total}₽</b>.\nБудем обменивать?",
        reply_markup=confirm_kbd)
    await state.clear()
    await state.update_data(amount=amount, total=total)


# /start
@router.message(CommandStart())
async def start(message: Message):  # /start
    user_id = message.from_user.id
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    language_code = message.from_user.language_code
    is_bot = message.from_user.is_bot

    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            await start_message(message, name, False)
            existing_user = db.select_user(id=user_id)
            if existing_user is None:
                db.add_user(id=user_id, username=username, first_name=name, last_name=last_name,
                            language_code=language_code, is_bot=is_bot)
                await bot.send_message(chat_id=admins[2],
                                       text=f"👤 <b>Новый пользователь добавлен в базу</b>\n"
                                            f"┌ <b>ID</b>: <code>{user_id or 'Не указан'}</code>\n"
                                            f"├ <b>Username</b>: @{message.from_user.username or 'Не указан'}\n"
                                            f"├ <b>Имя</b>: {name or 'Не указано'}\n"
                                            f"├ <b>Фамилия</b>: {last_name or 'Не указана'}\n"
                                            f"├ <b>Язык</b>: {language_code or 'Не указан'}\n"
                                            f"├ <b>Это бот?</b>: {'Да' if is_bot else 'Нет'}\n"
                                            f"└ <b>Дата первого обращения</b>: {db.select_user(id=user_id)[6]}\n\n"
                                            f"<b>Пользователей в базе</b>: <code>{db.count_users()}</code>")
            else:
                db.update_user(id=user_id, username=username, first_name=name, last_name=last_name,
                               language_code=language_code, is_bot=is_bot)
        else:
            keyboard = create_subscription_keyboard()
            await message.answer(
                text="<b>Подпишись на наш телеграм канал</b>, чтобы использовать функционал бота.",
                reply_markup=keyboard
            )
    except Exception as err:
        await message.answer("Непредвиденная ошибка. \nСвяжитесь с @AustinBur")
        print(err)


# Проверка подписки на канал
@router.callback_query(lambda call: call.data == "subscription verification")
async def verification(call: CallbackQuery):
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    name = call.from_user.first_name
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            await start_message(call.message, name, True)
            await call.answer(text="Спасибо за подписку!")
        else:
            await call.answer(text="Вы не подписаны на канал.")
    except Exception as err:
        await call.message.answer("Непредвиденная ошибка. \nСвяжитесь с @AustinBur")


# Прямое производство
@router.callback_query(lambda call: call.data == "direct production")
async def direct_prod(call: CallbackQuery):
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    keyboard = direct_production()
    media = "AgACAgIAAxkBAAIBnmaeIG14srZiWmFa-zGoJI_q4O7rAAKL8DEb_SvwSFbhx0Fri0E3AQADAgADcwADNQQ"
    caption = """
- Находим для Вас прямое производство в Китае под ваш запрос.\n
<b>- Преимущества связи с прямым производством</b>:\n
    <b>1)</b> Самая низкая цена на рынке (можно ее снизить еще больше, посредством торга, это также входит в эту услугу)
    <b>2)</b>  Различные новинки и предложения от фабрик для вас (Сможете продавать уникальный товар, который еще не вошел в большой оборот)
    <b>3)</b>  У вас останется контакт этого производства и вы сможете лично общаться, а также продолжать сотрудничество.

- <b>Для кого подходит?</b> 

    • Для людей уже с опытом в товарном бизнесе, которые хотят получить лучшие цены на свои товары.

    • Для людей, которые хотят выйти сразу с лучшими ценами на рынок и составить конкуренцию другим продавцам.

Оставляй заявку на <b><u>БЕСПЛАТНУЮ</u></b> консультацию

На консультации мы разберем твою проблему и поможем найти выход из твоей ситуации"""
    await call.message.answer_photo(photo=media, caption=caption, reply_markup=keyboard)
    await call.message.delete()
    await call.answer()


# Возвращение в меню после прямых производств
@router.callback_query(lambda call: call.data == "return start menu")
async def return_start(call: CallbackQuery):
    name = call.from_user.first_name
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    await start_message(call.message, name, False)
    await call.message.delete()
    await call.answer()


# Бесплатная консультация
@router.callback_query(lambda call: call.data == "free consultation")
async def free_selection(call: CallbackQuery):
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    if db.get_open_application_id(user_id):
        await call.answer("Вы уже отправили заявку.\nПожалуйста, дождитесь ответа модератора.", show_alert=True)
        return

    user = call.from_user
    db.add_application(user_id, user.username, user.first_name, user.last_name, user.language_code)
    application_id = db.get_open_application_id(user_id)

    user_info = (
        f"🆓 <b>Новая заявка на бесплатную консультацию #{application_id}</b>\n\n"
        f"┌<b>ID</b>: <code>{user.id}</code>\n"
        f"├<b>Имя</b>: {user.first_name or 'Не указано'}\n"
        f"├<b>Фамилия</b>: {user.last_name or 'Не указана'}\n"
        f"├<b>Username</b>: @{user.username or 'Не указан'}\n"
        f"└<b>Язык</b>: {user.language_code or 'Не указан'}\n"
    )

    btn_1 = types.InlineKeyboardButton(text="Закрыть заявку", callback_data=f"close_application:{application_id}")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1]])

    await bot.send_message(chat_id=admins[2], text=user_info, reply_markup=keyboard)
    await call.answer("Заявка успешно подана. Ожидайте ответа!", show_alert=True)


# Закрытие заявок на бесплатную консультацию
@router.callback_query(lambda call: call.data.startswith("close_application:"))
async def close_application(call: CallbackQuery):
    application_id = int(call.data.split(":")[1])
    db.close_application(application_id)
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    await call.message.edit_text(f"<s>{call.message.text}</s>\n\n<b>Статус:</b> Заявка закрыта.")
    await call.answer("Заявка закрыта.", show_alert=True)


# Самовыкуп
@router.callback_query(lambda call: call.data == "self ransom")
async def direct_prod(call: CallbackQuery):
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    keyboard = self_ransom()
    photo_path = "AgACAgIAAxkBAAIBk2aeH-ckntW8M-pSMmTJnAXHm8nbAAKJ8DEb_SvwSMnDI8JW8dBEAQADAgADcwADNQQ"
    doc_path = "BQACAgIAAxkBAAIBpGaeIMvrKOwCud7e7ur2hiCiaA92AAIiTwAC_SvwSPCGlU49AAGNJTUE"
    caption = '''
- Мы осуществляем выкуп ваших товаров с <b><u>ЛЮБЫХ</u></b> китайских маркетплейсов.
(<b>POIZON, TaoBao, 1688 и другие</b>). Главное - <u>указать ссылки</u> в бланке заказов.

- Чтобы ознакомиться с условиями самовыкупа, нажми кнопку "<b>Условия самовыкупа</b>".

- Для инструкции по созданию бланка заказа для самовыкупа посмотрите видео, нажав кнопку "<b>Видео-инструкция</b>".

- После заполнения бланка нажмите кнопку "<b>Отправить бланк заказов</b>"'''
    await call.message.answer_photo(photo=photo_path, caption=caption)
    await call.message.answer_document(document=doc_path, reply_markup=keyboard)
    await call.message.delete()
    await call.answer()


# Возвращение в меню после самовыкупа
@router.callback_query(lambda call: call.data == "return start menu after self ransom")
async def return_start(call: CallbackQuery):
    name = call.from_user.first_name
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    await start_message(call.message, name, False)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
    await call.message.delete()
    await call.answer()


# Обмен юаней
@router.callback_query(lambda call: call.data == "exchange")
async def exchange(call: CallbackQuery, state: FSMContext):
    keyboard = exchange_kbd()
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    await call.message.edit_text(
        text=f'Обмен осуществляется <b>от 600¥</b>\nВведите сколько <b>¥</b> хотите получить.\nПисать нужно <b>слитно</b>. <i>Например: "14372"</i>\n\nКурс юаня: <b>{db.get_exchange_rate()}</b>',
        reply_markup=keyboard)
    await state.set_state(Waiting.waiting_exchange)
    await call.answer()


# Возвращение в меню после обмена юаней
@router.callback_query(lambda call: call.data == "return start menu after exchange")
async def return_start(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    name = call.from_user.first_name
    await start_message(call.message, name, False)
    await call.message.edit_text(text=call.message.text)
    await call.answer()


# Одобрение обмена
@router.callback_query(lambda call: call.data == "confirm exchange")
async def confirm_exchange(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount")
    total = data.get("total")
    name = call.from_user.first_name

    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    if db.get_open_exchange_application_id(user_id):
        await state.clear()
        await start_message(call.message, name, True)
        await call.answer(text="Вы уже отправили заявку.\nПожалуйста, дождитесь ответа модератора.", show_alert=True)
        return

    user = call.from_user
    db.add_exchange_application(user_id=user_id, username=user.username, first_name=user.first_name,
                                last_name=user.last_name, language_code=user.language_code, amount=amount,
                                rate=db.get_exchange_rate(), total=total)
    application_id = db.get_open_exchange_application_id(user_id)
    user_info = (
        f"🔁 <b>Новая заявка на обмен юаней #{application_id}</b> 🇨🇳\n\n"
        f"┌<b>ID</b>: <code>{user.id}</code>\n"
        f"├<b>Имя</b>: {user.first_name}\n"
        f"├<b>Фамилия</b>: {user.last_name or 'Не указана'}\n"
        f"└<b>Username</b>: @{user.username or 'Не указан'}\n\n"
        f"Юаней: <b>{amount}¥</b>\n"
        f"Курс юаня: <b>{db.get_exchange_rate()}</b>\n"
        f"Рублей: <b>{total}₽</b>"
    )
    btn_1 = types.InlineKeyboardButton(text="Закрыть заявку",
                                       callback_data=f"close_exchange_application:{application_id}")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1]])

    await bot.send_message(chat_id=admins[2], text=user_info, reply_markup=keyboard)
    await state.clear()
    await call.message.edit_text(
        text=f"Вы ввели <b>{amount}¥</b>.\nКурс юаня: <b>{db.get_exchange_rate()}</b>.\nИтого: <b>{total}₽</b>.\nОжидайте сообщения от модератора.")
    await start_message(call.message, name, False)
    await call.answer("Заявка на обмен успешно подана. Ожидайте ответа!", show_alert=True)


# Отмена обмена
@router.callback_query(lambda call: call.data == "cancel exchange")
async def cancel_exchange(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    name = call.from_user.first_name
    await start_message(call.message, name, True)
    await call.answer("Обмен отменён")


# Закрытие заявки на обмен
@router.callback_query(lambda call: call.data.startswith("close_exchange_application:"))
async def close_exchange_application(call: CallbackQuery):
    application_id = int(call.data.split(":")[1])
    db.close_exchange_application(application_id)
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    await call.message.edit_text(f"<s>{call.message.text}</s>\n\n<b>Статус:</b> Заявка закрыта.")
    await call.answer("Заявка закрыта.", show_alert=True)


# Доставка-условия
@router.callback_query(lambda call: call.data == "delivery condition")
async def delivery_condition(call: CallbackQuery):
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    keyboard = delivery_cnd()
    await call.message.edit_text(text="<b>С чем желаете ознакомиться?</b>\n\nВыберите один из пунктов ниже",
                                 reply_markup=keyboard)
    await call.answer()


# Доставка
@router.callback_query(lambda call: call.data == "delivery")
async def delivery(call: CallbackQuery):
    keyboard = goods_delivery()
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    text = """
<b>Карго:</b> Доставка осуществляется в Санкт-Петербург, после чего я отправляю ваши посылки через <b>СДЭК</b>. Благодаря заключенному договору с СДЭК, стоимость доставки будет максимально низкой.

Этот вариант доставки рекомендуется для <b>маленьких партий</b> или <b>поштучных заказов</b>. Для больших партий с весом более 50 кг мы можем расширить ассортимент выбора карго-доставки. Если вам требуется другой вид карго-доставки, пожалуйста, <b>свяжитесь со мной</b> для получения дополнительной информации.

<b>Важно:</b> Карго-доставка является <b>серым ввозом</b>, что означает неофициальный ввоз товаров. Если вы хотите перевезти ценный груз, я рекомендую воспользоваться <b>страховкой</b>, которая составляет 5% от общей стоимости товара.

"""
    await call.message.edit_text(text=text, reply_markup=keyboard)
    await call.answer()


# Возвращения назад после доставки
@router.callback_query(lambda call: call.data == "return delivery_cnd after delivery")
async def return_delivery_cnd(call: CallbackQuery):
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    await delivery_condition(call)
    await call.answer()


# Возвращения в меню после доставки
@router.callback_query(lambda call: call.data == "return start menu after delivery")
async def return_start_menu(call: CallbackQuery):
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    await start_message(call.message, call.from_user.first_name, True)
    await call.answer()


# Стоимость
@router.callback_query(lambda call: call.data == "price_delivery")
async def price_delivery(call: CallbackQuery):
    keyboard = price_kbd()
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    text = """
<b>Стоимость:</b> 45 ¥ за 1 кг.

Если вес вашего заказа менее 0,5 кг, расчет будет производиться как <b>0,5 × 45 ¥ = 22,5 ¥</b>.

<b>Срок доставки:</b> 15-20 дней с момента отправки.

<b>Отправка</b> осуществляется раз в неделю.

Для того чтобы ваш заказ был отправлен со склада, <b>необходимо написать мне</b> о том, что ваша посылка прибыла на склад.

Нажмите на кнопку ниже, чтобы <b>посмотреть видео-инструкцию</b> о том, как отследить свою посылку.
"""
    await call.message.edit_text(text=text, reply_markup=keyboard)
    await call.answer()


# Возвращения в меню после стоимости
@router.callback_query(lambda call: call.data == "return start menu after delivery_cnd")
async def return_start_menu(call: CallbackQuery):
    user_id = call.from_user.id
    db.update_last_interaction(user_id)
    await start_message(call.message, call.from_user.first_name, True)
    await call.answer()


# ToDo -----------------------------------------------


# /change_course
@router.message(Command("change_course"))
async def change(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in admins:
        await message.answer("У Вас нет прав для использования этой команды!")
        return

    await message.answer(
        text=f"Текущий курс: <b>{db.get_exchange_rate()}</b>.\n\nВведите новый курс юаня.\n<i>Например: 13.5</i>",
        reply_markup=cancel_settings())
    await state.set_state(WaitingSettings.waiting_settings)


@router.message(WaitingSettings.waiting_settings)
async def change_settings(message: Message, state: FSMContext):
    try:
        new_course = float(message.text)
        db.update_exchange_rate(new_rate=new_course)
        await message.answer(f"Курс юаня успешно обновлён: <b>{db.get_exchange_rate()}</b>")
        await state.clear()
    except ValueError:
        await message.answer(text="Пожалуйста, введите корректное число.\nНапример: 13.5")


@router.callback_query(lambda call: call.data == "cancel settings")
async def cancel_st(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text=f"Отменено, текущий курс юаня: <b>{db.get_exchange_rate()}</b>")
    await call.answer("Отменено")


# ToDo -----------------------------------------------


# /view_open_applications
@router.message(Command("view_open_applications"))
async def view_open_applications(message: Message):
    # Извлекаем все открытые заявки
    open_applications = db.get_all_open_applications()
    if message.from_user.id not in admins:
        await message.answer("У Вас нет прав для использования этой команды!")
        return

    if not open_applications:
        await message.answer("В данный момент нет открытых заявок на бесплатную консультацию.")
        return

    # Форматируем каждую заявку
    formatted_apps = []
    for app in open_applications:
        app_id = app[0]
        user_id = app[1]
        username = app[2] or "Не указан"
        first_name = app[3] or "Не указано"
        last_name = app[4] or "Не указана"
        language_code = app[5] or "Не указан"
        created_at = app[6]

        formatted_apps.append(
            f"🆓 Заявка #{app_id}\n"
            f"┌<b>ID пользователя</b>: <code>{user_id}</code>\n"
            f"├<b>Имя</b>: {first_name}\n"
            f"├<b>Фамилия</b>: {last_name}\n"
            f"├<b>Username</b>: @{username}\n"
            f"├<b>Язык</b>: {language_code}\n"
            f"└<b>Дата создания</b>: {created_at}\n"
            f"------------------------------"
        )

    # Отправляем сообщение с заявками
    formatted_message = "\n".join(formatted_apps)
    await message.answer(f"<b>Открытые заявки:</b>\n\n{formatted_message}")


# ToDo -----------------------------------------------


# /view_open_exchange_applications
@router.message(Command("view_open_exchange_applications"))
async def view_open_xchange_applications(message: Message):
    if message.from_user.id not in admins:
        await message.answer("У Вас нет прав для использования этой команды!")
        return
    # Извлекаем все открытые заявки
    open_applications = db.get_open_exchange_applications()

    if not open_applications:
        await message.answer("В данный момент нет открытых заявок на обмен юаней.")
        return

    # Форматируем каждую заявку
    formatted_apps = []
    for app in open_applications:
        app_id = app[0]
        user_id = app[1]
        username = app[2] or "Не указан"
        first_name = app[3] or "Не указано"
        last_name = app[4] or "Не указана"
        language_code = app[5] or "Не указан"
        amount = app[6]
        rate = app[7]
        total = app[8]
        created_at = app[10]

        formatted_apps.append(
            f"🔁 Заявка #{app_id}\n"
            f"┌<b>ID пользователя</b>: <code>{user_id}</code>\n"
            f"├<b>Имя</b>: {first_name}\n"
            f"├<b>Фамилия</b>: {last_name}\n"
            f"├<b>Username</b>: @{username}\n"
            f"├<b>Язык</b>: {language_code}\n"
            f"└<b>Дата создания</b>: {created_at}\n\n"
            f"Сумма: <b>{amount}¥</b>\n"
            f"Курс юаня: <b>{rate}</b>\n"
            f"Итого: <b>{total}₽</b>\n"
            f"------------------------------"
        )

    # Отправляем сообщение с заявками
    formatted_message = "\n".join(formatted_apps)
    await message.answer(f"<b>Открытые заявки:</b>\n\n{formatted_message}")


# ToDo -----------------------------------------------


# /stats
@router.message(Command("stats"))
async def stats(message: Message):
    if message.from_user.id not in admins:
        await message.answer("У Вас нет прав для использования этой команды!")
        return
    user_count = db.count_users()
    total_consultations = db.count_application()
    open_consultations = db.count_open_applications()
    closed_consultations = total_consultations - open_consultations

    total_exchanges = db.count_all_exchange_applications()
    open_exchanges = db.count_open_exchange_applications()
    closed_exchanges = total_exchanges - open_exchanges

    stats_message = (
        f"<b>📊 Статистика бота</b>\n\n"
        f"👤 <b>Пользователей в базе</b>: {user_count}\n\n"
        f"🆓 <b>Заявки на бесплатную консультацию</b>:\n"
        f"┌ Всего: {total_consultations}\n"
        f"├ Открытые: {open_consultations}📂\n"
        f"└ Закрытые: {closed_consultations}🔒\n\n"
        f"🔁 <b>Заявки на обмен валюты:</b>\n"
        f"┌ Всего: {total_exchanges}\n"
        f"├ Открытые: {open_exchanges}📂\n"
        f"└ Закрытые: {closed_exchanges}🔒\n"
    )

    await message.answer(text=stats_message)
