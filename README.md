### Test task for remote python developer

Tested on python 3.9, used the alpha python-telegram-bot version

0. Clone the project
1. Fill the token in bot_config.ini
2. Prepare pyton virtual environment, run `pip install -r requirements.txt`
3. Run migrations from "alembic/versions" to prepare the database - `alembic upgrade head`
4. Run `py bot.py`