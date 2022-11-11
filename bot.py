"""Script entry with whole bot handlers"""

import datetime
import logging
import os

from faker import Faker
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, Application, ConversationHandler, \
    CallbackQueryHandler, MessageHandler, filters, CommandHandler

import randoms
from repository import fetch_insert
from config import read_config
from database import Worker, UserData
from service import write_xls

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

engine: Engine = create_async_engine(read_config("bot_conf.ini").db.DSN)

inline_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Записать работника",
                           callback_data='write_wrkr')]])

NSP = 0  # States variable


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("User in main menu")
    await update.message.reply_text(
        "Вы в главном меню",
        reply_markup=inline_keyboard
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ввод  ФИО отменён")
    return ConversationHandler.END


async def write_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """:returns state to handle user input"""
    await update.callback_query.edit_message_text("Введите вашу фамилию, имя и отчество")
    await update.callback_query.answer()
    return NSP


async def name_surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles users input and preforms file creation and transfer of tmp with last inputs"""
    name_surname_patr = update.message.text
    logger.info("Recieved name-surname-patronymic from %s", update.message.from_user.id)
    birth = randoms.generate_random_date()
    role_id = randoms.random_role_id()
    update_time = datetime.datetime.now()

    new_worker = Worker(
        birth_date=birth,
        name_surname_patronymic=name_surname_patr,
        role_id=role_id,
        updated_at=update_time,
    )
    users_to_write = await fetch_insert(engine, new_worker)
    logger.info("New user saved, data retrieved")
    if not users_to_write:
        await update.message.reply_text("Работников ещё нет, поздравляем, вы первый!")
    else:
        last_joined = [UserData(n, b, r) for n, b, r in users_to_write]
        file_name = write_xls(last_joined)
        # possible aiofiles in case of file io loads
        with open(file_name, 'rb') as doc:
            await update.message.reply_document(
                document=doc,
                filename='LastJoined.xlsx',
                caption='Последние работники',
            )
        os.unlink(file_name)
        logger.info('File sent and deleted')
    await update.message.reply_text("Вы в главном меню", reply_markup=inline_keyboard)
    return ConversationHandler.END


def main():
    """Runs bot until SIG"""
    config = read_config("bot_conf.ini")
    Faker.seed(0)
    app = Application.builder().token(config.bot.API_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(write_worker, pattern='^write_wrkr$')],
        states={
            NSP: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_surname)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(CommandHandler('start', start))
    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
