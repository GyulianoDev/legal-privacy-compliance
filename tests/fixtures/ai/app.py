from openai import OpenAI
from fastapi import UploadFile
client = OpenAI()
promptHistory = []
vectorStore = {}
