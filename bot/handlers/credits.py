from aiogram import types
from baski.primitives import datetime
from baski.telegram import storage
import core
import keyboards

__all__ = ['CreditsHandler']


class CreditsHandler(core.BasicHandler):

    async def on_message(
            self,
            message: types.Message,
            user: core.TelegramUser,
            *args, **kwargs
    ):
        await self.send_to(message, user, self.ctx.users)
        self.ctx.telemetry.add_message(core.CMD_CREDITS, message, message.from_user)

    @classmethod
    async def send_to(cls, message: types.Message, user: core.TelegramUser, users: storage.UsersStorage):
        answer = msg_credits.get(
            message.from_user.language_code,
            msg_credits['en']
        )
        user.last_credits = datetime.now()
        users.set(user)
        return await message.answer(**answer)


msg_credits = {
    "en": {
        "parse_mode": "MarkdownV2",
        "text": "Your conversation is safe \- the bot is saving only the last ten messages to keep the context of the conversation\."
                "\n\nWe need your help to spread the word about this bot\. Feel free to share it with your friends and colleagues\."
                "\n\n*Be a hero who keep the bot alive\! /donate now, or we face a shutdown*\."
                ,
        "reply_markup": keyboards.dontation_keyboard()
    }
}
