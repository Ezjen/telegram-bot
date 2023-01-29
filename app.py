from aiogram import Bot, Dispatcher, executor, types
import logging
from dotenv import load_dotenv
from utils import message_proccesing
from pydantic import BaseModel
from typing import Dict

load_dotenv()
import os


# Configure logging.
logging.basicConfig(level=logging.INFO)
API_TOKEN = os.environ.get("API_TOKEN")
DIR_PATH = os.environ.get("DIR_PATH")
# Initialize bot and dispatcher.
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# # Initialize the net.
# style_model = Net(ngf=128)
# style_model.load_state_dict(torch.load('21styles.model'), False)

# Initializing the flag to distinguish between images content and style.
# Initializing flags to check for images.
files = os.environ.get("FILES")

class Flag(BaseModel):
    flag: bool
    content_flag: bool
    style_flag: bool

global shakal_dict
shakal_dict: Dict[int, Flag] = {}




# def transform(content_root, style_root, im_size):
#     """Function for image transformation."""
#     content_image = tensor_load_rgbimage(content_root, size=im_size,
#                                          keep_asp=True).unsqueeze(0)
#     style = tensor_load_rgbimage(style_root, size=im_size).unsqueeze(0)
#     style = preprocess_batch(style)
#     style_v = Variable(style)
#     content_image = Variable(preprocess_batch(content_image))
#     style_model.setTarget(style_v)
#     output = style_model(content_image)
#     tensor_save_bgrimage(output.data[0], 'result.jpg', False)

    # # Clear the RAM.
    # del content_image
    # del style
    # del style_v
    # del output
    # torch.cuda.empty_cache()
    # gc.collect()


@dp.message_handler(commands=['start'])
async def test(message: types.Message):
    """Test function."""
    await message.answer(text="Hi, "
                              "I'll help you move the style from one photo "
                              "to another. To do this, first send me an image"
                              " with the content (if you suddenly want to "
                              "change it, use the /cancel command and then "
                              "send a new image), and then send me the image"
                              " that you want to transfer the style from "
                              "(you can use the /cancel command here as well). "
                              "After that, I will send you "
                              "a picture with the transferred style. "
                              "This takes a little time.")



@dp.message_handler(content_types=['photo'])
async def photo_processing(message: types.Message):
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
        await message.photo[-1].download(destination_file=f'{DIR_PATH}/{files}/{user_id}_content.jpg')
        await message.answer(text='I got the first one.'
                                  ' Now send me a photo with style or use '
                                  'the /cancel command to choose '
                                  'a different content image.')
        shakal_dict[user_id].flag = False
        shakal_dict[user_id].content_flag = True  # Now the bot knows that the content image exists.

    # The bot is waiting for a picture with style from the user.
    else:
        await message.photo[-1].download(destination_file=f'{DIR_PATH}/{files}/{user_id}_style.jpg')
        await message.answer(text='I got the second one. Now use the /continue'
                                  ' command or the /cancel command to change'
                                  ' the image style.')
        shakal_dict[user_id].flag = True
        shakal_dict[user_id].style_flag = True  # Now the bot knows that the style image exists.


@dp.message_handler(commands=['cancel'])
async def photo_processing(message: types.Message):
    """Allows the user to select a different image with content or style."""

    global shakal_dict
    user_id = message.from_user.id
    # Let's make sure that there is something to cancel.
    if not shakal_dict[user_id].content_flag:
        await message.answer(text="You haven't uploaded the content image yet.")
        return

    if shakal_dict[user_id].flag:
        shakal_dict[user_id].flag = False
    else:
        shakal_dict[user_id].flag = True
    await message.answer(text='Successfully!')



@dp.message_handler(commands=['continue'])
async def contin(message: types.Message):
    """Preparing for image processing."""

    # Let's make sure that the user has added both images.
    global shakal_dict
    user_id = message.from_user.id
    await message_proccesing(user_id=user_id, DIR_PATH=DIR_PATH, message=message, content_flag=shakal_dict[user_id].content_flag, style_flag=shakal_dict[user_id].style_flag, files=files)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)