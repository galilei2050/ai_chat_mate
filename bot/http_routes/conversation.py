from google.cloud import firestore
from core import OpenAiClient


open_ai =  OpenAiClient()


async def next_message(
        user_id: str,
        thread_doc_ref: firestore.AsyncDocumentReference,
        ai_doc_ref: firestore.AsyncDocumentReference,
):
    query = thread_doc_ref.collection('messages').order_by('created_at')
    history = [doc.to_dict() async for doc in query.stream()]
    assert len(history) > 2, "History must be more than 2 messages "
    history, last_message, ai_message = history[:-3], history[-2], history[-1]
    history = [{'role': doc['role'], 'content': doc['content']} for doc in history]
    async for text in open_ai.continue_chat(
        user_id=user_id,
        history=history,
        message=last_message.get('content')
    ):
        await ai_doc_ref.set({'content': text}, merge=True)
