from emoji import emojize
from typing import Dict
from pydantic import BaseModel
from config_reader import config
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.for_questions import model_select_kb
from utils import message_proccesing


class Flag(BaseModel):
    flag: bool
    content_flag: bool
    style_flag: bool


global shakal_dict
shakal_dict: Dict[int, Flag] = {}

DIR_PATH = config.DIR_PATH.get_secret_value()
files = config.FILES.get_secret_value()


router = Router()
bot = Bot(token=config.API_TOKEN.get_secret_value())


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(emojize("Hi! I can change the style of your image :smiling_face_with_sunglasses:\n"
                                 "To continue, choose a style transfer method:\n"
                                 ":green_circle: Neural Style Transfer is the technique of blending style "
                                 "from a style reference image :milky_way: "
                                 "into a content image :cityscape: keeping its content intact :night_with_stars:\n"
                                 ":green_circle: CartoonGAN is a generative adversarial network (GAN) for cartoon stylization of a content image :cityscape:\n"
                                 "There are 4 styles available:\n"
                                 "Makoto Shinkai :comet:, Hayao Miyazaki :castle:, "
                                 "Mamoru Hosoda :hourglass_not_done: and Paprika :hot_pepper:\n"),
                         reply_markup=model_select_kb()
                         )


@router.message(Text(text="Neural Style Transfer", ignore_case=True))
async def answer_nst(message: Message):
    await message.answer(emojize("A good choice! :winking_face:\n"
                                 "Now just send me the content image :cityscape: and the style reference image :milky_way:\n"
                                 "If you want to replace the loaded picture, "
                                 "use /cancel and send me a new picture\n"
                                 "When all pictures are loaded, use "
                                 "/continue and wait a bit until I send you "
                                 "a picture with the transferred style :night_with_stars:\n"),
                         reply_markup=ReplyKeyboardRemove()
                         )


@router.message(Text(text="CartoonGAN", ignore_case=True))
async def answer_gan(message: Message):
    await message.answer(emojize("A good choice! :slightly_smiling_face:\n"
                                 "Now just send me the content image :cityscape: and choose one of the proposed styles\n"
                                 "If you want to replace the loaded picture, "
                                 "use /cancel and send me a new picture\n"
                                 "When all pictures are loaded, use "
                                 "/continue and wait a bit until I send you "
                                 "a picture with the transferred style :night_with_stars:\n"),
                         reply_markup=ReplyKeyboardRemove()
                         )


@router.message(F.photo)
async def photo_processing1(message: Message):
    global shakal_dict
    user_id = message.from_user.id
    if user_id not in shakal_dict:
        shakal_dict[user_id] = Flag(
            flag=True,
            content_flag=False,
            style_flag=False,
        )

    if shakal_dict[user_id].flag:
        await bot.download(message.photo[-1], f"{DIR_PATH}/{files}/{user_id}_content.jpg")
        await message.answer(emojize("I got the content image :cityscape:\n"
                                     " Now send me the style reference image :milky_way: or use "
                                     "the /cancel command to choose "
                                     "a different content image :cityscape:")
                             )
        shakal_dict[user_id].flag = False
        shakal_dict[user_id].content_flag = True

    # The bot is waiting for a picture with style from the user.
    else:
        await bot.download(message.photo[-1], f"{DIR_PATH}/{files}/{user_id}_style.jpg")
        await message.answer(emojize("I got the style reference image :milky_way:\n"
                                     "Now use the /continue command or use the /cancel command to choose"
                                     "a different style reference image :milky_way:")
                             )
        shakal_dict[user_id].flag = True
        shakal_dict[user_id].style_flag = True


@router.message(Command("cancel"))
async def photo_processing2(message: Message):
    global shakal_dict
    user_id = message.from_user.id

    if not shakal_dict[user_id].content_flag:
        await message.answer(emojize("You haven't uploaded the content image yet :thinking_face:"))
        return

    if shakal_dict[user_id].flag:
        shakal_dict[user_id].flag = False
    else:
        shakal_dict[user_id].flag = True
    await message.answer(emojize("Successfully! check_mark_button:"))


@router.message(Command("info"))
async def creator(message: Message):
    link = "https://github.com/Ezjen/telegram-bot"
    dlslink = "https://dls.samcs.ru/en/dls"
    await message.answer(emojize("I have been created by Ezjen :nerd_face:\n"
                                 "My code is here: " + link + "\n"
                                 "MIPT Deep Learning School is here: " + dlslink))


@router.message(Command("continue"))
async def contin(message: Message):

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
