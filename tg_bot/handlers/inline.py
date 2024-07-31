from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineQuery, InlineQueryResultPhoto, InlineQueryResultCachedPhoto, InlineQueryResultArticle, \
    InputTextMessageContent, Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder

router = Router()


def create_initial_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить в корзину", callback_data="add_to_cart")],
        [InlineKeyboardButton(text="Вернуться назад", callback_data="return_main_menu")],
        [InlineKeyboardButton(text="Открыть корзину", callback_data="open_cart")],
    ])


def create_cart_keyboard(quantity: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="-", callback_data="decrease_quantity"),
            InlineKeyboardButton(text=f"{quantity}", callback_data="quantity"),
            InlineKeyboardButton(text="+", callback_data="increase_quantity"),
        ],
        [InlineKeyboardButton(text="Удалить из корзины", callback_data="remove_from_cart")],
        [InlineKeyboardButton(text="Вернуться назад", callback_data="return_main_menu")],
        [InlineKeyboardButton(text="Открыть корзину", callback_data="open_cart")],
    ])


@router.inline_query()
async def empty_query(query: InlineQuery):
    query_text = query.query.lower()
    if query_text == "кроссовки":
        results = [
            InlineQueryResultArticle(
                id='1',
                title='LV Trainer',
                description='Размеры: 42, 43\nПримерная стоимость: 5.000 ₽',
                thumb_url='https://i.imgur.com/hCLRDDH.png',  # Прямая ссылка на миниатюру
                input_message_content=InputTextMessageContent(
                    message_text='/cd LV Trainer\n'
                ),
            )
        ]
    else:
        results = []
    await query.answer(results=results, cache_time=1)


@router.message(Command('cd'))
async def handle_shop_command(message: Message, command: CommandObject):
    product_name = command.args
    if product_name == "LV Trainer":
        album_builder = MediaGroupBuilder()
        album_builder.add_photo(media="https://i.imgur.com/hCLRDDH.png")
        album_builder.add_photo(media="https://i.imgur.com/MPIWGye.jpeg")
        album_builder.add_photo(media="https://i.imgur.com/cL4dkgb.jpeg")
        album_builder.add_photo(media="https://i.imgur.com/G7s5mg8.jpeg")
        album_builder.add_photo(media="https://i.imgur.com/5SyGTON.jpeg")
        album_builder.add_photo(media="https://i.imgur.com/9ETx4hn.jpeg")
        album_builder.add_photo(media="https://i.imgur.com/EYMINMF.jpeg")
        await message.answer_media_group(media=album_builder.build())
        btn_1 = types.InlineKeyboardButton(text="Добавить в корзину", callback_data="add to cart")
        btn_2 = types.InlineKeyboardButton(text="В главное меню", callback_data="fsdf")
        btn_3 = types.InlineKeyboardButton(text="Открыть корзину", callback_data="fsdf")
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1], [btn_2], [btn_3]])
        await message.answer(
            text=f"Модель: <b>{product_name}</b>\n\nРазмеры: 42, 43\nПримерная стоимость вместе с доставкой: <b>5.000₽</b>",
            reply_markup=keyboard)
    else:
        await message.answer(text="Плохо")


@router.callback_query(lambda call: call.data == "add to cart")
async def handle_add_to_cart(call: CallbackQuery):
    quantity = 1
    new_reply_markup = create_cart_keyboard(quantity)
    await call.message.edit_reply_markup(reply_markup=new_reply_markup)


@router.message(Command('shop'))
async def handle_shop_command(message: Message):
    btn_1 = types.InlineKeyboardButton(text="Кроссовки", switch_inline_query_current_chat='кроссовки')
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1]])
    await message.answer(text="Вот наш ассортимент", reply_markup=keyboard)
