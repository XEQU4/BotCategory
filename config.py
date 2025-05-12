from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: str = os.getenv("BOT_TOKEN")  # Bot token
ADMIN_ID: int = int(os.getenv("ADMIN_ID"))  # Id of main user
DSN = os.getenv("POSTGRES_URL")  # Postgres datas: postgres://<user>:<password>@<host>:<port>/<database>

COUNTRIES_AND_CITIES = {
    "UAE": ["Dubai", "Abu Dhabi", "Shardijah"],
    "Saudi Arabia": ["Riyadh", "Jeddah"],
    "Qatar": ["Doha"],
    "Bahrain": ["Al Manama"],
    "Oman": ["Muscat"],
}

CITIES = ["Dubai", "Abu Dhabi", "Shardijah", "Riyadh", "Jeddah", "Al Manama", "Muscat", "Doha"]

TEXT_CAPTION_CAR = """
<b>{}</b>

COUNTRY: {}
CITY: {}
YEAR OF MANUFACTURE: {}
RENTAL SERVICES: {}
ABOUT THE CAR: {}
"""  # Car INFO text sample

SAMPLE_MEDIA_GROUP_PATH = "bot_media/sample_media.png"
WELCOME_IMAGE_FOR_CLIENTS_PATH = "bot_media/hello_client.png"
CLIENT_CITIES_PATH = "bot_media/client_city.png"
CLIENT_COUNTRIES_PATH = "bot_media/client_country.png"
