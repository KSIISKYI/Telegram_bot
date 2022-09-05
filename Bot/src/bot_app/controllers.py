import json

from Bot.src.bot_app import data_fetcher, keyboards, app, utils, states


def initializer(text: str):
    def decorator(func):
        async def wrapper(**kwargs):
            response = await data_fetcher.get_response(*kwargs['url_data_list'])
            buttons_data = await func(response)
            await utils.add_back_button_data(buttons_data, kwargs['state'], kwargs['callback_data'])
            utils.add_home_button(buttons_data)
            buttons = keyboards.generate_button(buttons_data)
            await app.bot.send_message(kwargs['callback_data']['from']['id'], f'*{text}*', reply_markup=buttons, parse_mode="Markdown")

        return wrapper

    return decorator


@initializer(text='Доступні категорії:')
async def show_categories(response):
    """Контролер який відповідає за відображення списку доступних категорій слів"""

    return {category['name']: json.dumps(category['link']) for category in response}


@initializer(text='Виберіть:')
async def show_category_detail(response):
    """Контролер який відповідає за відображення доступних можливостей конкретної категорії"""

    return {m: json.dumps(link) for m, link in response['menu_list'].items()}


@initializer(text='Список слів:')
async def show_words(response):
    """Контролер який відповідає за відображення слів по конкретній категорії"""

    return {word['eng_word']: json.dumps(word['link']) for word in response}


@initializer(text='Доступні вправи:')
async def show_exercise(response):
    """Контролер який відповідає за відображення списку вправ до даної категорії"""

    return {label: json.dumps(url) for label, url in response.items()}


async def show_lang(callback_data, state, url_data_list):
    """Контролер який відповідає за відображення доступних мов"""
    response = await data_fetcher.get_response(*url_data_list)
    if text := response.get('text'):
        buttons_data = {'>>>> В головне меню <<<<': 'start'}
    else:
        buttons_data = {k: json.dumps(v) for k, v in response.items()}
        utils.add_home_button(buttons_data)
        text = 'Виберіть мову:'
        await utils.add_back_button_data(buttons_data, state, callback_data)
    buttons = keyboards.generate_button(buttons_data)
    await app.bot.send_message(callback_data['from']['id'], f'*{text}*', reply_markup=buttons,
                               parse_mode="Markdown")


async def add_word(callback_data, state, url_data_list):
    """Контролер який відповідає за додання нового слова"""

    await state.finish()
    await states.AddWord.end_word.set()
    async with state.proxy() as data:
        data['url_data_list'] = url_data_list
    await app.bot.send_message(callback_data['from']['id'], 'Запишіть слово')


async def check_word(callback_data, state, url_data_list):
    """Контролер який відповідає за перевірку слова"""

    await state.finish()
    await states.GameStates.random_word.set()
    async with state.proxy() as data:
        data['pre_callback_data'] = await data_fetcher.get_response(*url_data_list)
    await app.bot.send_message(callback_data['from']['id'], f'Запишіть переклад слова <u>{data["pre_callback_data"]["word"]}</u>', parse_mode="HTML")
