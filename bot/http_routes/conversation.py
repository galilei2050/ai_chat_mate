import logging
import typing
from collections import defaultdict
from google.cloud import firestore

from baski.concurrent import as_async
from baski.env import get_env
from core import OpenAiClient
from pyairtable import Api


open_ai = OpenAiClient(
    system_prompt="""You are analyst at the event "AI Wonderland Hackathon". 
You will be given the list of the projects submitted.
Speaking about projects you MUST include only information provided. 
You help navigate through projects submitted. 
You MUST answer to the question in last message
"""
)

api = Api(get_env('AIRTABLE_API_KEY'))
table = api.table("appuwvnCtzRPPciXd", 'tblXrCEriiEaS1TKe')

context_message = {
    "role": "user",
    "content": "Bellow there are list of the projects:"
}


def make_message_from_row(row):
    fields = row.get('fields') or {}
    if not fields:
        return None
    header = f"# Project {fields['Project Name']}:\n"
    lines = [f"{k}:  {v}" for k, v in fields.items()]
    return {
        'role': 'user',
        'content': '\n'.join([header] + lines)
    }


async def get_additional_context():
    rows = await as_async(table.all)
    additional_context = [context_message] + [m for m in [make_message_from_row(row) for row in rows] if m]
    return additional_context


async def next_message(
        user_id: str,
        thread_doc_ref: firestore.AsyncDocumentReference,
        ai_doc_ref: firestore.AsyncDocumentReference,
):
    query = thread_doc_ref.collection('messages').order_by('created_at')
    history = [doc.to_dict() async for doc in query.stream()]
    assert len(history) > 2, "History must be more than 2 messages "
    history, last_message, ai_message = history[-10:-3], history[-2], history[-1]
    history = [{'role': doc['role'], 'content': doc['content']} for doc in history]
    additional_context = await get_additional_context()
    logging.info(f"Call GPT for message {ai_doc_ref.id}")
    async for text in open_ai.continue_chat(
            user_id=user_id,
            history=additional_context + history,
            message=last_message.get('content')
    ):
        logging.info(f"Update text in message {ai_doc_ref.id}")
        await ai_doc_ref.set({'content': text}, merge=True)
