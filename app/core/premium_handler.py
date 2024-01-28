import logging
import typing
from aiogram import dispatcher, types

from baski.primitives import datetime
from baski.primitives.name import obj_name
from baski.telegram import chat, handlers
from keyboards import dontation_keyboard
from .event_types import FREE_TRIAL, MSG_DONATE
from .context import Context
from .user import TelegramUser

__all__ = ['PremiumHandler']


TRIES_DATA_FIELD = "feature_last_tries"


class PremiumHandler(handlers.LogErrorHandler, handlers.TypedHandler):

    FEATURE_ID = None
    FREE_TRIES = 20
    PERIOD = datetime.timedelta(days=30)

    def __init__(self, ctx: Context):
        assert self.FEATURE_ID is not None, f"NAME is not set for handler type {obj_name(self)}"
        self._ctx = ctx

    @property
    def ctx(self) -> Context:
        return self._ctx

    async def __call__(
            self,
            message: typing.Union[types.CallbackQuery, types.Message],
            state: dispatcher.FSMContext,
            *args, **kwargs
    ):
        user: TelegramUser = kwargs.get('user', None)
        assert user is not None, f"User is not set for handler type {obj_name(self)}"

        if user.is_premium():
            logging.debug(f"Feature {self.FEATURE_ID} enabled for premium {user.id} user")
            return await super().__call__(message, *args, state=state, **kwargs)
        await self.say_we_are_closed(message)
        return

    async def free_flow(
            self,
            message: typing.Union[types.CallbackQuery, types.Message],
            state: dispatcher.FSMContext,
            *args, **kwargs
    ):
        tries_count = await self.get_tries_count(state)
        telemetry_payload = {
            "feature": self.FEATURE_ID,
            "tries": tries_count,
            "free_tries": self.FREE_TRIES,
            "period": str(self.PERIOD)
        }

        if tries_count < self.FREE_TRIES:
            logging.debug(f"Try {self.FEATURE_ID} by {user.id} user: {tries_count} of {self.FREE_TRIES}")
            self.ctx.telemetry.add(message.from_user.id, FREE_TRIAL, telemetry_payload)
            result = await super().__call__(message, *args, state=state, **kwargs)
            await self.update_tries(state)
            return result
        else:
            self.ctx.telemetry.add(message.from_user.id, MSG_DONATE, telemetry_payload)

            ask_donation_answer = {
                "text": self.get_donate_to_unblock_text(message.from_user.language_code),
                "reply_markup": dontation_keyboard(),
            }

            if isinstance(message, types.Message):
                await chat.aiogram_retry(message.answer, **ask_donation_answer)
            elif isinstance(message, types.CallbackQuery):
                await chat.aiogram_retry(message.message.answer, **ask_donation_answer)
            else:
                raise TypeError(f"Unknown message type {type(message)}")
            return False

    async def say_we_are_closed(self, message: types.Message):
        """
        Function tell user that the project is closed and thank him for using it
        """
        await message.answer(
            "🤖 Sorry, but this project is closed. Unfortunately, we didn't find a way to make it profitable. "
            "Thank you for using it. "
        )

    async def update_tries(self, state: dispatcher.FSMContext):
        data = await state.get_data({})
        data.setdefault(TRIES_DATA_FIELD, {})
        tries = data[TRIES_DATA_FIELD].setdefault(self.FEATURE_ID, [])
        last_time_point = datetime.now() - self.PERIOD
        data[TRIES_DATA_FIELD][self.FEATURE_ID] = (
                [t for t in tries if t['timestamp'] > last_time_point] +
                [dict(feature_id=self.FEATURE_ID, timestamp=datetime.now())]
        )
        await state.set_data(data)

    async def get_tries_count(self, state: dispatcher.FSMContext):
        data = await state.get_data({})
        data.setdefault(TRIES_DATA_FIELD, {})
        tries = data[TRIES_DATA_FIELD].setdefault(self.FEATURE_ID, [])
        last_time_point = datetime.now() - self.PERIOD
        return len([1 for t in tries if t['timestamp'] > last_time_point])

    def get_donate_to_unblock_text(self, language_code):
        return self.why_feature_not_available_text(language_code) + self.get_pemium_benefits_text(language_code)

    def why_feature_not_available_text(self, language_code):
        return msg_donate_for_feature.get(
            language_code,
            msg_donate_for_feature['en']
        )

    @classmethod
    def get_pemium_benefits_text(cls, language_code):
        return msg_premium_benefits.get(
            language_code,
            msg_premium_benefits['en']
        )


msg_premium_benefits = {
    "en":
        " 🎙 Voice messages\n"
        " 🖼️ Image requests\n"
        " 😆 Large requests\n"
        " 🆕 All new features\n"
        " 💬 Unlimited text messages\n"
        " 🤖 No ads\n"
        "\nPremium features will be available for next 30 days for any donation.",
    "ru":
        " 🎙 Голосовые сообщения\n"
        " 🖼️ Распознавание текста в изображениях\n"
        " 😆 Большой объем текста в запросе\n"
        " 🆕 Все новые функции\n"
        " 🤖 Без рекламы\n"
        "Эти фишки будут доступны следующие 30 дней для любого пожертвования",
}

msg_donate_for_feature = {
    "en":
        "This feature is available for users who support the project. "
        "Please make any /donation to unblock this feature and much more: \n\n",

    "ru":
        "Эта функция доступна для пользователей, поддерживающих проект. "
        "Пожалуйста, сделайте любое /donation, чтобы разблокировать эту функцию и многое другое: \n\n"
}
