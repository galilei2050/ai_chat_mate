import logging
import typing
import io
import tempfile
from aiogram import types, dispatcher
from aiogram.dispatcher.handler import SkipHandler

from aiogram.utils.exceptions import TelegramAPIError


from google.cloud import vision
from baski.concurrent import as_async

from baski.concurrent import as_task
from baski.telegram import chat
from baski.pattern import retry


import core
from .text import ChatTextHandler

__all__ = ['PhotoDocumentHandler']


class PhotoDocumentHandler(core.PremiumHandler, ChatTextHandler):
    FEATURE_ID = 'image_msg_in'
    FREE_TRIES = 10

    async def on_message(
            self,
            message: types.Message,
            state: dispatcher.FSMContext,
            *args, **kwargs
    ):
        if not message.photo:
            raise SkipHandler()
        typing_task = as_task(chat.aiogram_retry(message.chat.do, "typing"))
        photo_content = await self.download_photo(message.photo[-1])

        if not await self.is_text_document(photo_content):
            await message.answer("I don't know what to do with this photo. Please, send me a document.")
            raise SkipHandler()
        message.text = await self.get_text(photo_content)
        await super().on_message(message, state, *args, **kwargs)

    async def is_text_document(self, photo_content: io.BytesIO) -> bool:
        labels = await self.get_labels(photo_content)
        logging.debug(f"Labels for image: {labels}")
        return set([label['label'] for label in labels]) & {'Font', 'Document'}

    async def download_photo(self, photo: types.PhotoSize):
        with tempfile.TemporaryDirectory() as tempdir:
            write_io: io.FileIO = await retry(
                photo.download,
                exceptions=(TelegramAPIError,),
                destination_dir=tempdir
            )
            write_io.flush()
            with io.FileIO(write_io.name, 'rb') as read_io:
                return read_io.read()

    async def get_text(self, photo: io.BytesIO) -> typing.List[str]:
        image = vision.Image(content=photo)
        request = dict(image=image, features=[{'type_': vision.Feature.Type.DOCUMENT_TEXT_DETECTION}])
        response = await as_async(self.ctx.image_client.annotate_image, request)
        return response.full_text_annotation.text

    async def get_labels(self, photo: io.BytesIO) -> typing.List[str]:
        image = vision.Image(content=photo)
        request = dict(image=image, features=[{'type_': vision.Feature.Type.LABEL_DETECTION}])
        response = await as_async(self.ctx.image_client.annotate_image, request)
        return [{'label': label.description, 'score': label.score} for label in response.label_annotations]
