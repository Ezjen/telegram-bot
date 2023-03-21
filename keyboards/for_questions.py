from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def model_select_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Neural Style Transfer")
    kb.button(text="CartoonGAN")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, input_field_placeholder="Choose style transfer model...")
