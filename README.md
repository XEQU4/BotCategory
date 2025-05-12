# BaseTelegramBot
![CI](https://github.com/XEQU4/BaseTelegramBot/actions/workflows/ci.yml/badge.svg)

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Aiogram](https://img.shields.io/badge/Aiogram-3.20.0+-green)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)

A Telegram bot developed for a freelance client to manage user categories through Telegram.
Built with asynchronous PostgreSQL integration and designed with scalability in mind.

## 🔧 Tech Stack

- **Aiogram 3.20.0+**
- **PostgreSQL** via `asyncpg`
- **Loguru** — advanced logging system
- **pytz**, **python-dotenv**, **sqlalchemy** (minimally used)
- **uv** — modern Python package manager

## 🛠️ Dependencies

```properties
aiofiles==24.1.0
aiogram==3.20.0.post0
aiohappyeyeballs==2.6.1
aiohttp==3.11.18
aiosignal==1.3.2
annotated-types==0.7.0
apscheduler==3.11.0
async-timeout==5.0.1
asyncpg==0.30.0
attrs==25.3.0
certifi==2025.4.26
colorama==0.4.6
dotenv==0.9.9
exceptiongroup==1.3.0
frozenlist==1.6.0
greenlet==3.2.2
idna==3.10
iniconfig==2.1.0
loguru==0.7.3
magic-filter==1.0.12
multidict==6.4.3
packaging==25.0
pluggy==1.5.0
propcache==0.3.1
pydantic==2.11.4
pydantic-core==2.33.2
pytest==8.3.5
pytest-asyncio==0.26.0
python-dotenv==1.1.0
sqlalchemy==2.0.40
tomli==2.2.1
typing-extensions==4.13.2
typing-inspection==0.4.0
tzdata==2025.2
tzlocal==5.3.1
win32-setctime==1.2.0
yarl==1.20.0
```

## 🔄 Features

- ✅ /start command that shows different menus depending on user role (admin or regular user)
- ✅ Admin Panel via bot commands (admin ID is configured in .env)
- ✅ User Interaction Handling using ReplyKeyboards and InlineKeyboards
- ✅ Dynamic Category Management:\
       Admins can create, edit, and delete categories\
       Users can browse and select categories
- ✅ State Management with Finite State Machine (FSM) for smoother multi-step flows
- ✅ PostgreSQL Database to store users and categories
- ✅ Auto Database Migration — tables are created automatically if missing
- ✅ Scheduler (APScheduler)
- ✅ Structured Logging with Loguru for easy debugging
- ✅ Environment Variables usage for secure configuration (.env)
- ✅ CI Integration with GitHub Actions (pytest runs on every push)
- ✅ Testing Suite (basic unit tests with pytest-asyncio)


## 📚 .env File

```dotenv
   # ID of main user
   ADMIN_ID=admin_id

   # Telegram bot token
   BOT_TOKEN="your_bot_token"

   # PostgreSQL connection string
   POSTGRES_URL="postgres://<user>:<password>@<hostname>:<port>/<your_database>"
```

### PostgreSQL in Docker
Use `postgres` as the hostname, not `localhost`, for PostgreSQL as well.

> **✅ Correct:** ```POSTGRES_URL="postgres://postgres:your_password@postgres:5432/your_database"```

🔐 The `username` and `password` in POSTGRES_URL must match those specified in your `docker-compose.yml` file:

```yml
   environment:
      POSTGRES_USER:postgres
      POSTGRES_PASSWORD:your_password
      POSTGRES_DB:your_database
```

If you use different credentials locally, ensure the `.env` file uses the Docker-specific ones when running via Docker Compose.

## 🚀 Running the Project (Without Docker)

1. Install [uv](https://github.com/astral-sh/uv):
   ```bash
   pip install -U uv
   ```
2. Create a virtual environment:
   ```bash
   uv venv
   ```
3. Activate the virtual environment:
   ```bash
   .venv/Scripts/activate
   ```
4. Install dependencies:
   ```bash
   uv sync
   ```
5. Configure your `.env` file (see above)
6. Run PostgreSQL (manually create the DB)
7. Start the bot:
   ```bash
   python ./bot.py
   ```

## 🧪 Testing

Basic tests are included using `pytest` and `pytest-asyncio`.

---

> For **unit tests**, use fake (non-functional) values:
> 
> In `ADMINS` - any integers, e.g. `111111111/222222222`\
> In `BOT_TOKEN` - any string in token format, e.g. `123456789:fake-token`
> ```dotenv
>    ADMINS=111111111/222222222
>    BOT_TOKEN="123456789:fake-token"
> ```
> ❗ These values won't work with the Telegram API — they're used only for testing purposes.

---

### 🧼 Run Locally (via uv)

```bash
   uv pip install pytest
   uv run pytest
   ```

## ✅ Project Status

The project was initially created for a freelance client with potential future expansion in mind.
You may encounter placeholder modules or extra utility functions prepared for scaling and upgrades.

## 📝 License

MIT License. See [LICENSE](./LICENSE) for more information.

---

**Author:** [XEQU](https://github.com/XEQU4)

