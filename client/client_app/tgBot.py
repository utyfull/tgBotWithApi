import asyncio
import logging
import sys
from os import getenv
from help_tools import helping_methods
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

sys.path.insert(0, '/home/utyfull/Desktop/projects/tgBotWithApi/client/serverConnect')
from dbConnect import connect_to_Server

TOKEN = getenv("BOT_TOKEN")

form_router = Router()


class Form(StatesGroup):
    start_key = State()
    valid_key = State()
    invalid_key = State()
    valid_team = State()
    input_team = State()
    valid_team = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.start_key)
    com_list = [KeyboardButton=(text="Write key"), KeyboardButton=(text="Generate key")]
    await message.answer(
        "Hi there! Write your key or generate it.",
        reply_markup=ReplyKeyboardMarkup()
    )


@form_router.message(Form.start_key)
async def check_key(message: Message, state: FSMContext) -> None:
    await state.update_data(key=message.text)
    if connect_to_Server.check_key(message.Text) == "YES":
        await state.set_state(Form.valid_key)
        await message.reply(
            "Cool, the next step is write people you want to send notifications. Please, write users or use last team",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await state.set_state(Form.invalid_key)
        await message.reply(
            "You've wrote wrong key! Try again or generate new key.",
            reply_markup=ReplyKeyboardMarkup()
        )


@form_router.message(Form.invalid_key, F.text.casefold() == "")
async def check_key(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.start_key)
    await message.answer(
        "Write your key again!",
        reply_markup=ReplyKeyboardRemove()
    )


@form_router.message(Form.start_key, Form.invalid_key, F.text.casefold() == "")
async def gen_key(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.valid_key)
    key = helping_methods.new_key()
    await message.answer(
        f"Your key is {key}\n Please remember it.\n 
        The next step is write people you want to send notifications. Please, write users or use last team",
        reply_markup=ReplyKeyboardMarkup()
    )


@form_router.message(Form.valid_key, F.text.cesefold() == "Write users")
async def choose_team(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.input_team)
    await message.reply(
        "Please, write users with this format -> (@abc@wfs)",
        reply_markup=ReplyKeyboardRemove()
    )

@form_router.message(Form.input_team)
async def check_team(message: Message, state: FSMContext) -> None:
    team = message.Text
    if helping_methods.check_team_valid(team) == "VALID":
        await state.set_state(Form.valid_team)
        await message.reply(
            "Your team is valid, the next step is write message"
        )
    else:
        await state.set_state(Form.valid_key)
        await message.reply(
            "Team format is invalid! Try again",
            reply_markup=ReplyKeyboardRemove
        )

@form_router.message(Form.valid_team)
async def send_notif(message: Message, state: FSMContext) -> None:
    user_message = message.Text
    await message.reply(
        "Notifications have been sent. See you later!!!"
    )


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())