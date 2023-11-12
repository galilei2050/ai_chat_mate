import typing
import langdetect
import random
import functools

from google.cloud import texttospeech as tts
from langdetect import LangDetectException

from aiogram import dispatcher, types
from baski.telegram import receptionist, chat, monitoring
from baski.concurrent import as_async

import core
from keyboards import VOICE_CB_DATA


def register_voice_handlers(rp: receptionist.Receptionist, ctx: core.Context):
    voice_handler = VoiceHandler(ctx)
    rp.add_button_callback(voice_handler, VOICE_CB_DATA.filter())


class VoiceHandler(core.PremiumHandler):

    FEATURE_ID = 'voice_msg_out'

    async def on_callback(self, callback_query: types.CallbackQuery, state: dispatcher.FSMContext, *args, **kwargs):
        ai_message = callback_query.message
        self.ctx.telemetry.add(callback_query.from_user.id, core.BTN_VOICE_MSG, {})
        await self.send_voice(ai_message, ai_message.text, callback_query.from_user)
        await chat.aiogram_retry(
            callback_query.message.edit_text,
            callback_query.message.text, reply_markup=None
        )

    async def send_voice(self, ai_message: types.Message, text, user: types.User = None):
        await ai_message.chat.do('record_voice')
        try:
            language = langdetect.detect(text)
        except LangDetectException:
            return
        voice = self.get_voice(language)
        if not voice:
            await chat.aiogram_retry(ai_message.answer, f"Sorry, I don't know how to speak {language} yet")
            return
        audio_content = await self.get_audio_content(text, language, voice)
        voice_out = await chat.aiogram_retry(ai_message.reply_voice, audio_content)
        if voice_out:
            self.ctx.telemetry.add_message(monitoring.MESSAGE_OUT, voice_out, user)

    async def get_audio_content(self, text, language, voice):
        synthesis_input = tts.SynthesisInput(text=text)
        voice = tts.VoiceSelectionParams(
            language_code=language, name=voice
        )
        audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.OGG_OPUS, speaking_rate=1.0
        )
        response = await as_async(
            self.ctx.tts_client.synthesize_speech,
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        return response.audio_content

    def get_voice(self, language):
        possible_voices = [v for v in self.available_voices if v.startswith(language)]
        if not possible_voices:
            return None
        wavenet_voices = [v for v in possible_voices if 'Wavenet' in v]
        if wavenet_voices:
            return random.choice(wavenet_voices)
        return random.choice(possible_voices)

    @functools.cached_property
    def available_voices(self) -> typing.List[str]:
        return [v.name for v in self.ctx.tts_client.list_voices().voices if v.ssml_gender == tts.SsmlVoiceGender.MALE]
