import io
import random
import tempfile

from aiogram import types, dispatcher
from aiogram.utils.exceptions import TelegramAPIError

from baski.telegram import chat, storage
from baski.primitives import datetime
from baski.pattern import retry

import core
from .credits import CreditsHandler

__all__ = ['ChatHandler']

from .text import ChatTextHandler

CREDITS_COOLDOWN = datetime.timedelta(days=5)
CREDITS_PROBABILITY = 0.05


class ChatHandler(core.PremiumHandler, ChatTextHandler):
    FEATURE_ID = 'normal_chat'
    FREE_TRIES = 3
    PERIOD = datetime.timedelta(minutes=60)

    async def on_message(
            self,
            message: types.Message,
            state: dispatcher.FSMContext,
            *args, **kwargs
    ):
        if message.voice:
            message.text = await self.text_from_voice(message)
        user: storage.TelegramUser = kwargs.get('user')

        await super().on_message(message, state, *args, **kwargs)
        await self.maybe_show_credits(message, user)

    async def maybe_show_credits(
            self,
            message: types.Message,
            user: core.TelegramUser,
            *args, **kwargs
    ):
        if datetime.now() - datetime.as_local(user.last_credits) < CREDITS_COOLDOWN:
            return
        if random.random() > CREDITS_PROBABILITY:
            return
        credits_message = await CreditsHandler.send_to(message, user, self.ctx.users)
        self.ctx.telemetry.add_message(core.SHOW_CREDITS, credits_message, message.from_user)

    async def text_from_voice(self, message):
        with tempfile.TemporaryDirectory() as tempdir:
            placeholder = await chat.aiogram_retry(message.reply, "🎙 Transcribing voice message...")
            await message.chat.do("typing")
            buffer = await retry(
                message.voice.download,
                exceptions=(TelegramAPIError,),
                destination_dir=tempdir
            )
            buffer.flush()
            with io.FileIO(buffer.name, 'rb') as read_buffer:
                text = await self.ctx.openai.transcribe(user_id=message.from_user.id, audio=read_buffer)
                await chat.aiogram_retry(placeholder.edit_text, f"🎙 Transcription is: \"{text}\"")
                return text

    def why_feature_not_available_text(self, language_code):
        return msg_cool_down.get(
            language_code,
            msg_cool_down['en']
        )


msg_cool_down = {
    "en":
        f"I'm tired. Now I can only process {ChatHandler.FREE_TRIES} messages per hour."
        "Please wait some time or make any /donation to unblock unlimited messaging and much more: \n\n",

    "ru":
        f"Много запросов. Я могу обрабатывать {ChatHandler.FREE_TRIES} сообщений каждый час."
        "Пожалуйста подождите какое-то время или сделайте любое /donation, чтобы общаться сколько угодно а так же: \n\n"
}