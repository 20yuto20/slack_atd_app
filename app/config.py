import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    APP_TOKEN = os.getenv("APP_TOKEN")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT")

config = Config()