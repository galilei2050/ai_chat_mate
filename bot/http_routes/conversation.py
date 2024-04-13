from google.cloud import firestore
from core import OpenAiClient
from pyairtable import Api

open_ai = OpenAiClient()
api = Api('pat9apNtUsG6DD0TU.b45f4ff13db65d5e8861469a8804a5eb043a4ec7bb0478fa40c8307a7c41bfc3')
table = api.table("appv61Zx3hTzrhbPk", 'tblxVDuRS2nPskWXd')


def make_message_from_row(row):
    fields = row.get('fields') or []
    content = f"# Task {fields['ID']:\n\n}"
    lines = '\n'.join([f"{k}:{v}" for k, v in fields.items()])
    return '\n'.join('')

def get_context_messages():
    table.all()

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
    async for text in open_ai.continue_chat(
        user_id=user_id,
        history=history,
        message=last_message.get('content')
    ):
        await ai_doc_ref.set({'content': text}, merge=True)
