import datetime
import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from .app import dp, bot
from .messages import WELCOME_MESSAGE
from . import keyboards, router, states, local_settings, data_fetcher, controllers


@dp.message_handler(commands=('start', 'help'), state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await states.MenuManager.menu.set()
    async with state.proxy() as data:
        data['menu_stack'] = list()
        data['menu_stack'].append('start')

    data_buttons = {'Вибрати категорію слів': json.dumps([local_settings.SHOW_CATEGORIES_URL, 'get']),
                    'Додати слово': json.dumps([local_settings.ADD_WORD, 'post'])}

    buttons = keyboards.generate_button(data_buttons)
    await bot.send_message(message['from']['id'], WELCOME_MESSAGE, reply_markup=buttons)


@dp.callback_query_handler(lambda c: c.data not in [], state=states.MenuManager.menu)
async def delegator(callback_query: types.CallbackQuery, state: FSMContext):
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S"), callback_query.data)
    if callback_query.data == 'start':
        await send_welcome(callback_query, state)
    else:
        await router.router(callback_query, state)


# ======================== add word ============================

# приймаємо англійське слово
@dp.message_handler(state=states.AddWord.end_word)
async def load_eng_word(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['word'] = {}
        data['word']['eng_word'] = message.text
    await states.AddWord.next()
    await message.reply('Впишіть переклад')


# приймаємо укр слово
@dp.message_handler(state=states.AddWord.ukr_word)
async def load_ukr_word(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['word']['ukr_word'] = message.text
    await states.AddWord.next()
    await message.reply(
        'Запишіть id категорії:\n1 - Іменник\n2 - Дієслово\n3 - Прикметник\n4 - Прислівник\n5 - Займенник')


# приймаємо категорію
@dp.message_handler(state=states.AddWord.category)
async def load_category(message: types.Message, state: FSMContext):
    d = None
    async with state.proxy() as data:
        data['word']['category'] = int(message.text)
        d = data
    await state.finish()

    url = d['url_data_list'][0]
    method = d['url_data_list'][1]
    r = await data_fetcher.get_response(url=url, method=method, data=d['word'])

    await states.MenuManager.menu.set()
    buttons = keyboards.generate_button({'На головну': 'start'})

    await bot.send_message(message['from']['id'], '*Успішне додання*', reply_markup=buttons, parse_mode='Markdown')


# ==================== check word ==================


@dp.message_handler(state=states.GameStates.random_word)
async def check_word(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    response = None
    async with state.proxy() as data:
        params = [('answer', answer)]
        response = await data_fetcher.get_response(*data['pre_callback_data']['button_check']['link'], params=params)
    if result := response["Result"] == 'Неправильно':
        result = f'<b>{response["Result"]}</b>, правильна відповідь: <u>{response["translated_word"]}</u>'
    else:
        result = f"<b>{response['Result']}</b>"
    if not response.get('button_next'):
        await state.finish()
        await states.MenuManager.menu.set()
        buttons = keyboards.generate_button({'На головну': 'start'})
        await bot.send_message(message['from']['id'],
                               f'{result}\n\n{response["button"]["text"]}',
                               reply_markup=buttons,
                               parse_mode='HTML')
    else:
        async with state.proxy() as data:
            response = await data_fetcher.get_response(*response['button_next']['link'])
            data['pre_callback_data'] = response
        await bot.send_message(message['from']['id'],
                               f'{result}\n\nЗапишіть переклад слова <u>{response["word"]}</u>',
                               parse_mode="HTML")