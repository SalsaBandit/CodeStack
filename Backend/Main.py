from fastapi import FastAPI
import asyncio
from ollama import AsyncClient

app = FastAPI()


stored_mess = []

async def chat(inp):
  stored_mess.append({'role': 'user', 'content': inp})
  response = ""
  async for part in await AsyncClient().chat(model='gemma4:26b', messages=stored_mess, stream=True):
    chunk = part['message']['content']
    print(part['message']['content'], end='', flush=True)
    response = response + chunk
  stored_mess.append({
    'role' : 'assistant',
    'content' : response
  })

  print("")


while True:
  inp = input(">>>")
  if inp == "/exit":
    break
  elif len(inp) > 0:
     asyncio.run(chat(inp))

