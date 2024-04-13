import typing
from baski.primitives import datetime
from fastapi import routing, Depends
from pydantic import BaseModel
from .jwt_token import get_user

router = routing.APIRouter(prefix="/thread", tags=['Threads related stuff'])


class Message(BaseModel):
    uuid: str
    role: str
    content: str


class Thread(BaseModel):
    id: str
    title: str
    messages: typing.List[Message]
    created_at: datetime.datetime


@router.get('/', response_model=typing.List[Thread])
async def get_list_of_threads(user=Depends(get_user)):
    """
    Get a list of the threads for the user
    """
    return [
        Thread(id='fake', messages=[], created_at=datetime.now())
    ]


@router.post('/', response_model=Thread)
async def create_new_thread(user=Depends(get_user)):
    """
    Create new thread for a user
    """
    print(f"create thread for user {user}")
    return Thread(id='fake', title="New thread", messages=[], created_at=datetime.now())


@router.get("/{thread_id}", response_model=typing.List[Message])
async def get_messages(thread_id: str, user=Depends(get_user)):
    """
    Return list of the messages in thread
    """
    return [
        Message(uuid='sdf', role='user', content='my message')
    ]


@router.post('/{thread_id}')
async def add_message(message: Message, user=Depends(get_user)):
    """
    Add a new message to the thread and kick off AI answer flow
    """
    return
