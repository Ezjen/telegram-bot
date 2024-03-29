import tensorflow_hub as hub
import tensorflow as tf
import os
from emoji import emojize
from aiogram import types
from aiogram.types import FSInputFile

model_link = ("https://tfhub.dev/google/magenta/" +
              "arbitrary-image-stylization-v1-256/2")
NST_model = hub.load(model_link)


def get_data(img_path: str):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img


async def message_proccesing(user_id: int,
                             DIR_PATH: str,
                             message: types.Message,
                             content_flag: bool,
                             style_flag: bool,
                             files: str):
    if not os.path.exists(f'{DIR_PATH}/{files}'):
        os.mkdir(f'{DIR_PATH}/{files}')
    if not (content_flag * style_flag):  # Conjunction
        await message.answer(emojize("You haven't uploaded all images yet :thinking_face:"))
        return

    else:
        await message.answer(emojize("Processing has started :pregnant_woman:\n"
                             "Just wait for a little bit..."),
                             reply_markup=types.ReplyKeyboardRemove())
        content_image = get_data(f'{DIR_PATH}/{files}/{user_id}_content.jpg')
        style_image = get_data(f'{DIR_PATH}/{files}/{user_id}_style.jpg')
        style_image = tf.image.resize(style_image, (256, 256))
        generated_image = NST_model(tf.constant(
            content_image), tf.constant(style_image))[0]
        tf.keras.utils.save_img(
            f'{DIR_PATH}/{files}/{user_id}_result.jpg', generated_image[0])
        ans = FSInputFile(f'{DIR_PATH}/{files}/{user_id}_result.jpg')
        await message.answer_photo(ans, caption=emojize("Done! :check_mark_button:"))
