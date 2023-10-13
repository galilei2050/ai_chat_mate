import io
import random
import openai
import asyncio
import tempfile
import typing

from aiogram import types, dispatcher
from aiogram.utils.exceptions import MessageNotModified, RetryAfter, TelegramAPIError

from baski.concurrent import as_task
from baski.telegram import chat, storage, monitoring
from baski.primitives import datetime
from baski.pattern import retry

import core
from .credits import CreditsHandler
from keyboards import assistant_message_keyboard


__all__ = ['ChatHandler', 'ChatTextHandler']


CHAT_HISTORY_LENGTH = 7
CHAT_HISTORY_COOLDOWN = datetime.timedelta(minutes=30)
CREDITS_COOLDOWN = datetime.timedelta(days=5)
CREDITS_PROBABILITY = 0.05
MAX_MESSAGE_SIZE = 4096
LARGE_REQUEST_DONATE_MESSAGE = (
    f"The basic model is unable to handle large requests. \n"
    f"To proceed with your request, make a /donation to unblock large requests."
)


class ChatTextHandler(core.BasicHandler):

    async def on_message(
            self,
            message: types.Message,
            state: dispatcher.FSMContext,
            *args, **kwargs
    ):
        assert message.text, f"Message has no text"
        user: storage.TelegramUser = kwargs.get('user')
        self.ctx.telemetry.add_message(monitoring.MESSAGE_IN, message, message.from_user)
        typing_task = as_task(chat.aiogram_retry(message.chat.do, "typing"))
        async with state.proxy() as proxy:
            history = chat.ChatHistory(proxy)
            history.from_user(message)
            try:
                await typing_task
                answers = await self.answer_to_text(user, message, history)
                for answer in answers:
                    history.from_ai(answer)
                    self.ctx.telemetry.add_message(monitoring.MESSAGE_OUT, answer, message.from_user)

            except openai.error.InvalidRequestError as e:
                await chat.aiogram_retry(message.answer, LARGE_REQUEST_DONATE_MESSAGE)
                self.ctx.telemetry.add_message(core.LARGE_MESSAGE, message, message.from_user)

    async def answer_to_text(self, user: core.TelegramUser, message, history: chat.ChatHistory):
        answers: typing.List[types.Message] = []
        last_answer_began = 0
        letters_written = 0
        async for text in self.ctx.openai.continue_chat(
                user_id=user.id,
                history=history.last(CHAT_HISTORY_LENGTH, fmt="openai", fr=datetime.now() - CHAT_HISTORY_COOLDOWN),
                message=message.text,
                use_large=user.is_premium()):
            try:
                if not answers:
                    if text:
                        answer = await chat.aiogram_retry(message.answer, text)
                        if answer:
                            answers.append(answer)
                            letters_written = len(text)
                    continue

                if len(text) - last_answer_began > MAX_MESSAGE_SIZE:
                    await chat.aiogram_retry(
                        answers[-1].edit_text,
                        text=answers[-1].text, reply_markup=assistant_message_keyboard()
                    )
                    last_answer_began = letters_written
                    answer = await chat.aiogram_retry(message.answer, text[letters_written:])
                    if answer:
                        answers.append(answer)
                else:
                    if answers[-1].text != text[last_answer_began:]:
                        answers[-1] = await chat.aiogram_retry(answers[-1].edit_text, text=text[last_answer_began:])
                letters_written = len(text)
                await chat.aiogram_retry(message.chat.do, "typing")
            except MessageNotModified as e:
                pass
            except RetryAfter:
                await asyncio.sleep(1)
        if answers:
            await chat.aiogram_retry(
                answers[-1].edit_text,
                text=answers[-1].text, reply_markup=assistant_message_keyboard()
            )
        return answers


class ChatHandler(ChatTextHandler):

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
