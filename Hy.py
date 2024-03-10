from os import environ, getenv
from dotenv import load_dotenv, dotenv_values

load_dotenv()

print(getenv("Gig"))

environ

print(dotenv_values(".env")["Gig"])