import asyncio
from http import HTTPStatus
from typing import Annotated, List
from uuid import uuid4

from fastapi import BackgroundTasks, Depends, HTTPException, routing
from firebase_admin.auth import UserInfo
from google.cloud import firestore
from pydantic import BaseModel

from baski.primitives import datetime
from core import THREADS, WEB_USERS
from .jwt_token import get_user
from .conversation import next_message

router = routing.APIRouter(prefix="/thread", tags=['Threads related stuff'])
firestore_client = firestore.AsyncClient()


class Message(BaseModel):
    uuid: str
    role: str
    content: str
    created_at: datetime.datetime | None = None


class Thread(BaseModel):
    uuid: str
    title: str
    created_at: datetime.datetime


async def get_user_doc(
        user: Annotated[UserInfo, Depends(get_user)],
) -> firestore.AsyncDocumentReference:
    user_doc_ref: firestore.DocumentReference = firestore_client.collection(WEB_USERS).document(user.uid)
    await user_doc_ref.set({
        'provider_id': user.provider_id,
        'email': user.email,
        'display_name': user.display_name
    }, merge=True)
    return user_doc_ref


async def get_thread_doc(
        thread_id: str,
        user: Annotated[firestore.AsyncDocumentReference, Depends(get_user_doc)]
) -> firestore.AsyncDocumentReference:
    thread_doc_ref = user.collection(THREADS).document(thread_id)
    return thread_doc_ref


@router.get('/', response_model=List[Thread])
async def get_list_of_threads(
        user: Annotated[firestore.AsyncDocumentReference, Depends(get_user_doc)]
):
    """
    Get a list of the threads for the user
    """
    query = user.collection(THREADS).order_by('created_at', direction="DESCENDING")
    threads = [doc.to_dict() async for doc in query.stream()]
    if not threads:
        threads = [await create_new_thread(user)]
    return threads


@router.post('/', response_model=Thread)
async def create_new_thread(
        user: Annotated[firestore.AsyncDocumentReference, Depends(get_user_doc)]
):
    """
    Create new thread for a user
    """
    new_thread = Thread(
        uuid=str(uuid4()),
        title="New thread",
        created_at=datetime.now()
    )
    first_message = Message(
        uuid=str(uuid4()),
        role='assistant',
        content="I'm your friendly assistant. How can I help?",
        created_at=datetime.now()
    )
    _, doc_ref = await user.collection(THREADS).add(new_thread.dict(), document_id=new_thread.uuid)
    await doc_ref.collection('messages').add(first_message.dict(), document_id=first_message.uuid)
    return new_thread


@router.get("/{thread_id}", response_model=List[Message])
async def get_messages(
        thread_doc_ref: Annotated[firestore.AsyncDocumentReference, Depends(get_thread_doc)]
):
    """
    Return list of the messages in thread
    """
    query = thread_doc_ref.collection('messages').order_by('created_at')
    messages = [doc.to_dict() async for doc in query.stream()]
    if not messages:
        raise HTTPException(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    return messages


@router.post('/{thread_id}')
async def add_message(
        message: Message,
        user: Annotated[UserInfo, Depends(get_user)],
        background_tasks: BackgroundTasks,
        thread_doc_ref: Annotated[firestore.AsyncDocumentReference, Depends(get_thread_doc)],
        status_code=HTTPStatus.ACCEPTED,
):
    """
    Add a new message to the thread and kick off AI answer flow
    """
    message.created_at = message.created_at or datetime.now()
    message.role = 'user'
    message.uuid = str(uuid4())
    messages = thread_doc_ref.collection('messages')
    ai_message = Message(
        uuid=str(uuid4()),
        role='assistant',
        content="...",
        created_at=datetime.now()
    )
    title, new_title, num_words = '', '', 2
    while len(new_title) < 12:
        title = new_title
        new_title = ' '.join(message.content.split(' ')[:num_words] + ['...'])
        num_words+=1

    _, (_, message_doc_ref), (_, ai_doc_ref) = await asyncio.gather(
        thread_doc_ref.set({'title': title}, merge=True),
        messages.add(message.dict(), document_id=str(message.uuid)),
        messages.add(ai_message.dict(), document_id=str(ai_message.uuid))
    )
    background_tasks.add_task(next_message, user.uid, thread_doc_ref, ai_doc_ref)
