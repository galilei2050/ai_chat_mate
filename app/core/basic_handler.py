import typing
from aiogram import types, dispatcher

from baski.primitives.name import obj_name
from baski.telegram import handlers, chat
from keyboards import dontation_keyboard

from .context import Context
from .user import TelegramUser

__all__ = ['BasicHandler', 'PremiumHandler']


class BasicHandler(handlers.LogErrorHandler, handlers.TypedHandler):

    def __init__(self, ctx: Context):
        super().__init__()
        self._ctx = ctx

    @property
    def ctx(self) -> Context:
        return self._ctx


class PremiumHandler(object):
    FEATURE_ID = None
    FREE_TRIES = 10

    async def __call__(
            self,
            message: typing.Union[types.CallbackQuery, types.Message],
            state: dispatcher.FSMContext,
            user: TelegramUser,
            *args, **kwargs
    ):
        assert self.FEATURE_ID is not None, f"NAME is not set for handler type {obj_name(self)}"
        if user.is_premium():
            await super().__call__(message, *args, state=state, user=user, **kwargs)
            return

        data = await state.get_data({})
        data.setdefault('feature_tries', {})
        feature_tries = data['feature_tries']
        tries = feature_tries.setdefault(self.FEATURE_ID, 0)
        feature_tries[self.FEATURE_ID] = tries + 1
        await state.set_data(data)

        if tries < self.FREE_TRIES:
            await super().__call__(message, *args, state=state, user=user, **kwargs)
            return

        answer = msg_donate_for_feature.get(
            message.from_user.language_code,
            msg_donate_for_feature['en']
        )

        if isinstance(message, types.Message):
            await chat.aiogram_retry(message.answer, **answer)
        elif isinstance(message, types.CallbackQuery):
            await chat.aiogram_retry(message.message.answer, **answer)


msg_donate_for_feature = {
    "en": {
        "text": "This feature is available for users who support the project. "
                "Please make any /donation to unblock this feature and much more: \n\n"
                " 🎙 Voice messages\n"
                " 😆 Large requests\n"
                " 🆕 All new features\n"
                " 🤖 No ads\n"
                "\n Premium features will be available for next 30 days for any donation.",
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
