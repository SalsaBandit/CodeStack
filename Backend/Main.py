from fastapi import FastAPI
import asyncio
import ollama
from ollama import AsyncClient
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

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

# chunking and file upload logic
file = open("docu.md", "r", encoding="utf-8")
content = file.read()

headers_to_split = [
  ("#", "Project Name"),
  ("##", "Header 2"),
  ("###", "Header 3")
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split)
md_header_splits = markdown_splitter.split_text(content)

text_splitter= RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
splits = text_splitter.split_documents(md_header_splits)

#embedding logic
texts = [doc.page_content for doc in splits]
response = ollama.embed(model = "gemma4:26b", input = texts)
doc_vecs = response['embeddings']

while True:
  inp = input(">>>")
  if inp == "/exit":
    break
  elif len(inp) > 0:
     asyncio.run(chat(inp))

