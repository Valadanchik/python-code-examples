import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
UPLOAD_DIR = "uploads/"
csv_file_path = "Output.csv"
csv_delimiter = "^"
system_prompt_ingredients = "You will be provided with a block of text, and your task is to extract ingredients from it. without any comments | only ingredients or return _ if not found"
system_prompt_energy = "You will be provided with a block of text, and your task is to extract energy value from it. without any comments | only energy value or return _ if not found"
