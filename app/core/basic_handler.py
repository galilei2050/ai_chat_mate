import typing
from aiogram import types, dispatcher

from baski.primitives.name import obj_name
from baski.telegram import handlers, chat
from keyboards import dontation_keyboard

from .context import Context
from .user import TelegramUser
from .event_types import MSG_DONATE, FREE_TRIAL

__all__ = ['BasicHandler', 'PremiumHandler']


class BasicHandler(handlers.LogErrorHandler, handlers.TypedHandler):

    def __init__(self, ctx: Context):
        super().__init__()
        self._ctx = ctx

    @property
    def ctx(self) -> Context:
        return self._ctx


class PremiumHandler(handlers.LogErrorHandler, handlers.TypedHandler):
    FEATURE_ID = None
    FREE_TRIES = 20

    def __init__(self, ctx: Context):
        super().__init__()
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
        assert self.FEATURE_ID is not None, f"NAME is not set for handler type {obj_name(self)}"
        user: TelegramUser = kwargs.get('user', None)
        assert user is not None, f"User is not set for handler type {obj_name(self)}"

        if user.is_premium():
            await super().__call__(message, *args, state=state, **kwargs)
            return

        data = await state.get_data({})
        data.setdefault('feature_tries', {})
        tries = data['feature_tries'].setdefault(self.FEATURE_ID, 0)

        payload = {
            "feature": self.FEATURE_ID,
            "tries": tries,
            "free_tries": self.FREE_TRIES
        }

        if tries < self.FREE_TRIES:
            self.ctx.telemetry.add(message.from_user.id, FREE_TRIAL, payload)
            await super().__call__(message, *args, state=state, **kwargs)

            data = await state.get_data({})
            data.setdefault('feature_tries', {})
            data['feature_tries'][self.FEATURE_ID] = tries + 1

            await state.set_data(data)
            return

        answer = msg_donate_for_feature.get(
            message.from_user.language_code,
            msg_donate_for_feature['en']
        )

        if isinstance(message, types.Message):
            await chat.aiogram_retry(message.answer, **answer)
            self.ctx.telemetry.add(message.from_user.id, MSG_DONATE, payload)
        elif isinstance(message, types.CallbackQuery):
            await chat.aiogram_retry(message.message.answer, **answer)
            self.ctx.telemetry.add(message.from_user.id, MSG_DONATE, payload)


msg_donate_for_feature = {
    "en": {
        "text": "This feature is available for users who support the project. "
                "Please make any /donation to unblock this feature and much more: \n\n"
                " 🎙 Voice messages\n"
                " 😆 Large requests\n"
                " 🆕 All new features\n"
                " 🤖 No ads\n"
                "\nPremium features will be available for next 30 days for any donation.",
        "reply_markup": dontation_keyboard()
    },
    "ru": {
        "text": "Эта функция доступна для пользователей, поддерживающих проект. "
                "Пожалуйста, сделайте любое /donation, чтобы разблокировать эту функцию и многое другое: \n"
                " 🎙 Голосовые сообщения\n"
                " 😆 Большой обьем текста в запросе\n"
                " 🆕 Все новые функции\n"
                " 🤖 Без рекламы\n",
        "reply_markup": dontation_keyboard()
    }
}
