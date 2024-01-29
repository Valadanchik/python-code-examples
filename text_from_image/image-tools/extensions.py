import openai
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from config import api_key

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize the OpenAI API client
openai.api_key = api_key
