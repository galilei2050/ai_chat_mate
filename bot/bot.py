import argparse
import typing

from functools import cached_property, lru_cache
from google.cloud import texttospeech as tts, pubsub, storage as cloud_storage, vision
from aiogram import types
from aiogram.dispatcher import storage as aiogram_storage

from baski.env import get_env, project_id
from baski.server import aiogram_server
from baski.telegram import storage, filters, handlers, middleware, monitoring

import handlers as app_handlers, core


class ChatMateBot(aiogram_server.TelegramServer):

    @cached_property
    def users(self):
        return storage.UsersStorage(self.db.collection('telegram_users'), core.TelegramUser)

    @cached_property
    def fsm_storage(self) -> aiogram_storage.BaseStorage:
        return storage.FirebaseStorage(self.db)

    @cached_property
    def openai_clinet(self):
        return core.OpenAiClient(telemetry=self.telemetry)

    @cached_property
    def telemetry(self):
        return monitoring.MessageTelemetry(self.pubsub, self.args['project_id'], publish=self.args['cloud'])

    @cached_property
    def context(self):
        return core.Context(
            db=self.db,
            pubsub=self.pubsub,
            openai=self.openai_clinet,
            users=self.users,
            telemetry=self.telemetry,
            tts_client=tts.TextToSpeechClient(),
            image_client=vision.ImageAnnotatorClient(client_options={'quota_project_id': str(project_id())}),
        )

    @cached_property
    def cloud_storage(self):
        return cloud_storage.Client()

    @cached_property
    def pubsub(self):
        return pubsub.PublisherClient()

    def register_handlers(self):
        app_handlers.register_voice_handlers(self.receptionist, self.context)

        self.receptionist.add_error_handler(handlers.SaySorryHandler())
        self.receptionist.add_message_handler(app_handlers.ClearHandler(self.context), commands=['clear'])
        self.receptionist.add_message_handler(app_handlers.StartHandler(self.context), commands=['start'])
        self.receptionist.add_message_handler(app_handlers.CreditsHandler(self.context), commands=['credits'])
        self.receptionist.add_message_handler(
            app_handlers.PhotoDocumentHandler(self.context),
            chat_type='private',
            content_types=[types.ContentType.PHOTO],
        )
        self.receptionist.add_message_handler(
            app_handlers.ChatHandler(self.context),
            chat_type='private',
            content_types=[types.ContentType.TEXT, types.ContentType.VOICE]
        )

    def web_routes(self) -> typing.List:
        return []

    @lru_cache()
    def filters(self) -> typing.List:
        attribution_topic = self.context.pubsub.topic_path(project_id(), core.ATTRIBUTION)
        filters.Attribution.setup_firestore(self.db.collection(core.ATTRIBUTION))
        filters.Attribution.setup_pubsub(attribution_topic, self.context.pubsub)

        filters.User.setup(self.users)
        return [
            filters.User,
            filters.Attribution,
        ]

    def middlewares(self) -> typing.List:
        return [
            middleware.UnprocessedMiddleware(
                storage_client=self.cloud_storage,
                storage_bucket='assistant-idk',
                telemetry=self.context.telemetry
            ),
            middleware.BlocklistMiddleware(
                blocklist=[]
            )
        ]


if __name__ == '__main__':
    ChatMateBot().run()
