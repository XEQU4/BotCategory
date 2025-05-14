# BotCategory

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Aiogram](https://img.shields.io/badge/Aiogram-3.20.0+-green)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Tooling](https://img.shields.io/badge/Tool-uv-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 About the Project

**BotCategory** is a Telegram bot initially developed for a freelance project based on a technical assignment.
Originally, it was designed to support three roles (admin, clients, users who would rent catalog places), but due to budget constraints, only two sides were finalized: **admin** and **clients**.

Clients can:

* Select a **country** (currently: United Arab Emirates 🇦🇪),
* Choose a **city**,
* Browse a **car catalog** and view **contact information** for the car owner.
* Filter cars using **tags**.

Admin can:

* **Add**, **edit**, and **manage** cars in the catalog,
* **Change tags**,
* **Manage rental duration** for the listing spots.

**BotCategory** offers a structured system for renting cars in the UAE through a Telegram interface.

---

## 🚀 Technologies Used

* Python 3
* Aiogram 3
* PostgreSQL
* APScheduler
* Docker

---

## ⚙️ Installation and Launch

### Option 1: Local Launch (via `uv`)

```bash
   pip install -U uv
   uv venv
   uv sync
   uv run bot.py
```

### Option 2: Docker Launch

```bash
   docker-compose up --build
```

---

## 📄 Environment Variables

A `.env.example` template is included for your convenience.
You can simply copy and configure it:

```bash
   cp .env.example .env
```

Example `.env` settings:

```dotenv
# ID of main user
ADMIN_ID=1234567890

# Telegram bot token
BOT_TOKEN="123456789:ABCdefGhIjkLmNoPqRsTuVwXyZ"

# PostgreSQL Database URL
# For local database:
# POSTGRES_URL="postgres://postgres:pass@localhost:5432/postgres"

# For Docker:
POSTGRES_URL="postgres://user:pass@postgres:5432/mydb"
```

---

## 🧪 Testing

The project includes a basic test using `pytest-asyncio` to validate the bot token.

To run tests:

```bash
   docker-compose up --build
```

The test service automatically runs the tests after building.

---

## 📷 Screenshots

### **Client Side:**

![Coming soon!](assets/cstart.png)
![Coming soon!](assets/ccountry.png)
![Coming soon!](assets/ccity.png)
![Coming soon!](assets/ccatalog.png)
![Coming soon!](assets/cinfo.png)
![Coming soon!](assets/ccontacts.png)
![Coming soon!](assets/ctags.png)

### **Admin Side:**

![Coming soon!](assets/astart.png)
![Coming soon!](assets/aadd_car.png)
![Coming soon!](assets/amanage_tags.png)

### **Project Structure and Docker Build:**

![Coming soon!](assets/project_structure.png)
![Coming soon!](assets/docker.png)

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

**Author:** [XEQU](https://github.com/XEQU4)