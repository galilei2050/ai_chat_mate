from aiogram import types
from aiogram.utils import callback_data
from aiogram.utils.callback_data import CallbackData

DONATION_CB_DATA = callback_data.CallbackData("donation", "amount")
VOICE_CB_DATA = CallbackData("voice_message")


def assistant_message_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("🎙 Voice message", callback_data=VOICE_CB_DATA.new())
            ]
        ]
    )


def dontation_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=text, callback_data=DONATION_CB_DATA.new(amount=amount))
                for text, amount in [('$1 🕯️', '100'), ('5$ ☕', '500'), ('10$ 🥪', '1000'), ('$25 💳', '2500')]
            ]
        ]
    )
