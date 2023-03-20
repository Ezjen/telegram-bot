from aiogram import Bot, Dispatcher, types, Router
from aiogram import F
import logging
from config_reader import config
from utils import message_proccesing
from aiogram.filters import Text
from aiogram.filters.command import Command
from pydantic import BaseModel
from typing import Dict
import os
import asyncio


logging.basicConfig(level=logging.INFO)

API_TOKEN = config.API_TOKEN.get_secret_value()
DIR_PATH = config.DIR_PATH.get_secret_value()

bot = Bot(token=API_TOKEN)
router = Router()

# files = os.environ.get("FILES")
files = config.FILES.get_secret_value()


class Flag(BaseModel):
    flag: bool
    content_flag: bool
    style_flag: bool


global shakal_dict
shakal_dict: Dict[int, Flag] = {}


async def main():
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def test(message: types.Message):
        """Test function."""
        kb = [
            [
                types.KeyboardButton(text="Arbitrary Image Stylization"),
                types.KeyboardButton(text="GAN")
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Choose NST model..."
        )

        await message.answer(
            text="Hi, "
            "I'll help you move the style from one photo "
            "to another. To do this, first send me an image "
            "with the content and then send me the image "
            "that you want to transfer the style from. "
            "If you want to replace the loaded picture, "
            "use /cancel and send me a new picture. "
            "When both pictures are loaded, use "
            "/continue and wait a bit until I send you "
            "a picture with the transferred style.", reply_markup=keyboard
        )

    @dp.message(lambda message: message.text == "Arbitrary Image Stylization")
    async def with_puree(message: types.Message):
        await message.reply("A good choice!", reply_markup=types.ReplyKeyboardRemove())

    @dp.message(lambda message: message.text == "GAN")
    async def without_puree(message: types.Message):
        await message.reply("Mama put my GANs in the ground... ", reply_markup=types.ReplyKeyboardRemove())

    @dp.message(F.photo)
    async def photo_processing1(message: types.Message):
        """
        Triggered when the user sends an image and saves it for further processing.
        """

        global shakal_dict
        user_id = message.from_user.id
        if user_id not in shakal_dict:
            shakal_dict[user_id] = Flag(
                flag=True,
                content_flag=False,
                style_flag=False,
            )

    # The bot is waiting for a picture with content from the user.
        if shakal_dict[user_id].flag:
            await bot.download(message.photo[-1],
                               destination=f"{DIR_PATH}/{files}/{user_id}_content.jpg"
                               )
            await message.answer(
                text="I got the first one."
                " Now send me a photo with style or use "
                "the /cancel command to choose "
                "a different content image."
            )
            shakal_dict[user_id].flag = False
            shakal_dict[user_id].content_flag = True

    # The bot is waiting for a picture with style from the user.
        else:
            await bot.download(message.photo[-1],
                               destination=f"{DIR_PATH}/{files}/{user_id}_style.jpg"
                               )
            await message.answer(
                text="I got the second one. Now use the /continue"
                " command or the /cancel command to change"
                " the image style."
            )
            shakal_dict[user_id].flag = True
            shakal_dict[user_id].style_flag = True

    @dp.message(Command("cancel"))
    async def photo_processing2(message: types.Message):
        """Allows the user to select a different image with content or style."""

        global shakal_dict
        user_id = message.from_user.id
    # Let's make sure that there is something to cancel.
        if not shakal_dict[user_id].content_flag:
            await message.answer(
                text="You haven't uploaded the content image yet.")
            return

        if shakal_dict[user_id].flag:
            shakal_dict[user_id].flag = False
        else:
            shakal_dict[user_id].flag = True
        await message.answer(text="Successfully!")

    @dp.message(Command("info"))
    async def creator(message: types.Message):

        link = "https://github.com/Ezjen/telegram-bot"
        await message.answer(
            text="I have been created by Ezjen. " "My code is here: " + link
        )

    @dp.message(Command("continue"))
    async def contin(message: types.Message):
        """Preparing for image processing."""

        # Let's make sure that the user has added both images.
        global shakal_dict
        user_id = message.from_user.id
        await message_proccesing(
            user_id=user_id,
            DIR_PATH=DIR_PATH,
            message=message,
            content_flag=shakal_dict[user_id].content_flag,
            style_flag=shakal_dict[user_id].style_flag,
            files=files,
        )

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
