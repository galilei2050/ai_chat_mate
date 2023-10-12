import asyncio
import logging
import typing
import io
import tempfile
from aiogram import types, dispatcher
from aiogram.dispatcher.handler import SkipHandler

from aiogram.utils.exceptions import TelegramAPIError


from google.cloud import vision
from baski.pattern import retry
from baski.telegram import chat
from baski.concurrent import as_async, as_task


from baski.concurrent import as_task
from baski.telegram import chat, storage, monitoring
from baski.primitives import datetime
from baski.pattern import retry


import core

__all__ = ['PhotoDocumentHandler']


class PhotoDocumentHandler(core.PremiumHandler):
    FEATURE_ID = 'image_msg_in'
    FREE_TRIES = 20

    async def on_message(
            self,
            message: types.Message,
            state: dispatcher.FSMContext,
            *args, **kwargs
    ):
        if message.photo and await self.is_text_document(message.photo[-1]):
            await message.reply('TBD')
            return
            # message.text = await self.text_from_photo(message)

        raise SkipHandler()

    async def is_text_document(self, photo: types.PhotoSize) -> bool:
        labels = await self.get_labels(photo)
        logging.debug(f"Labels for image: {labels}")
        return set([label['label'] for label in labels]) & {'Font', 'Document'}

    async def get_labels(self, photo: types.PhotoSize) -> typing.List[str]:
        with tempfile.TemporaryDirectory() as tempdir:
            write_io: io.FileIO = await retry(
                photo.download,
                exceptions=(TelegramAPIError,),
                destination_dir=tempdir
            )
            write_io.flush()
            with io.FileIO(write_io.name, 'rb') as read_io:
                image = vision.Image(content=read_io.read())
                request = dict(image=image, features=[{'type_': vision.Feature.Type.LABEL_DETECTION}])
                response = await as_async(self.ctx.image_client.annotate_image, request)
                return [{'label': label.description, 'score': label.score} for label in response.label_annotations]
