import asyncio
import aiohttp
import requests
from time import time

def number_generetor():
    counter = 0
    while True:
        counter += 1
        yield counter

g = number_generetor()

def image(data): 
    filename = 'img_{}.jpeg'.format(next(g))
    with open(filename, 'wb') as file:
        file.write(data)


async def find_img(url, session):
    async with session.get(url, allow_redirects=True) as response:
        img = await response.read()
        image(img) # очень плохая практика использовать синхронные функции в асинхронных
        
        
async def main(n):
    url = 'https://picsum.photos/200/300'
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        for i in range(n):
            task = asyncio.create_task(find_img(url, session))
            tasks.append(task)
            
        await asyncio.gather(*tasks)
        
if __name__ == '__main__':
    asyncio.run(main(int(input())))