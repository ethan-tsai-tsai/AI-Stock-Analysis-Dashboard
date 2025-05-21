import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Set LLM
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL_NAME = 'deepseek/deepseek-chat-v3-0324:free'

client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")
