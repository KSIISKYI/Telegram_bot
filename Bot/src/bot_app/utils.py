async def add_back_button_data(buttons_data: dict, state, callback_data):
    async with state.proxy() as data:
        if len(data.__dict__['_data']['menu_stack']) > 1:
            if data.get('menu_stack')[-2] == callback_data.data:
                data.get('menu_stack').pop()
                buttons_data['>>>> Назад <<<<'] = data.get('menu_stack')[-2]
            else:
                buttons_data['>>>> Назад <<<<'] = data.get('menu_stack')[-1]
                data['menu_stack'].append(callback_data.data)
        else:
            buttons_data['>>>> Назад <<<<'] = data.get('menu_stack')[-1]
            data['menu_stack'].append(callback_data.data)


def add_home_button(buttons_data: dict):
    buttons_data['>>>> В головне меню <<<<'] = 'start'
