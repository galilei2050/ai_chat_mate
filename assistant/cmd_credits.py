import random
from aiogram import types
from .telegram import dp
from .i_can_break import sorry_if_exception


FEEDBACK_URL = "https://3qugszanpzk.typeform.com/to/ifCEiciG"
GITHUB_URL = "https://github.com/vgalilei/ai_chat_mate"
CREDITS_PROBABILITY = 0.01


async def maybe_send_credits(message: types.Message, *args, **kwargs):
    if message.chat.type != 'private' or random.random() > CREDITS_PROBABILITY:
        return
    await send_credits(message)


@dp.message_handler(commands=["credits"])
@sorry_if_exception()
async def send_credits(message: types.Message, *args, **kwargs):
    answer = msg_credits.get(
        message.from_user.language_code,
        msg_credits['en']
    )
    await message.answer(**answer)


msg_credits = {
    "en": {
        "parse_mode": "MarkdownV2",
        "text": "This bot is developed by @galilei\. "
                "You are more than welcome to reach out with a suggestion or complain\."
                "\n\nYour conversation is safe \- "
                "bot never stores any of your messages without your explicit permission\. "
                "The code is open\. Feel free to review the GitHub page\. "
                "\n\nIf this bot is useful for you it will be useful for your friends\. "
                "\n*Please don't hesitate to share it*",
        "reply_markup": types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton("🔗 Source code", url=GITHUB_URL),
                    types.InlineKeyboardButton("💬 Leave feedback", url=FEEDBACK_URL)
                ]
            ])
    },
    "ru": {
        "parse_mode": "MarkdownV2",
        "text": "«Этот бот разработан @galilei\. "
                "Вы всегда можете обратиться с предложением или жалобой\. "
                "\n\nВаш разговор в безопасности \— "
                "бот никогда не сохраняет ваши сообщения без вашего явного разрешения\. "
                "Код открыт\. Посетите страницу проекта на GitHub"
                "\n\nЕсли этот бот полезен для вас\, он будет полезен и для ваших друзей\. "
                "Пожалуйста\, не стесняйтесь поделиться им c друзьями и коллегами",
        "reply_markup": types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton("🔗 Исходный код", url=GITHUB_URL),
                    types.InlineKeyboardButton("💬 Поделиться идеей", url=FEEDBACK_URL)
                ]
            ])
    }
}
