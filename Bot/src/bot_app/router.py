import re
import json

from . import local_settings


async def router(callback_data, state):
    url_data_list = json.loads(callback_data.data)
    for template, func in local_settings.URLS.items():
        if re.search(template, url_data_list[0]) and url_data_list[1] == func[1]:
            await func[0](callback_data=callback_data, state=state, url_data_list=url_data_list)
