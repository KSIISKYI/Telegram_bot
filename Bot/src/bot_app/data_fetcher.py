import aiohttp


async def get_response(url, method, data=None, params=None):
    async with aiohttp.ClientSession() as session:
        if data:
            async with session.__getattribute__(method)(url=url, data=data) as response:
                return await response.json()
        else:
            async with session.__getattribute__(method)(url, params=params) as response:
                return await response.json()
