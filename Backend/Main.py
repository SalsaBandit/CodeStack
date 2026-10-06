from fastapi import FastAPI
import asyncio
from ollama import AsyncClient

app = FastAPI()



async def chat():
  message = {'role': 'user', 'content': input()}
  async for part in await AsyncClient().chat(model='gemma4:26b', messages=[message], stream=True):
    print(part['message']['content'], end='', flush=True)
asyncio.run(chat())

