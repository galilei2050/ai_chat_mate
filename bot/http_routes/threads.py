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
    messages: typing.List[Message]
    created_at: datetime.datetime


@router.get('/', response_model=typing.List[Thread])
def get_list_of_threads():
    """
    Get a list of the threads for the user
    """
    return []


@router.post('/', response_model=Thread)
def create_new_thread(user = Depends(get_user)):
    """
    Create new thread for a user
    """
    print(f"create thread for user {user}")
    return Thread(id='fake', messages=[], created_at=datetime.now())


@router.get("/{thread_id}", response_model=typing.List[Message])
def get_messages():
    """
    Return list of the messages in thread
    """
    return []


@router.post('/{thread_id}')
def add_message():
    """
    Add a new message to the thread and kick off AI answer flow
    """
    return {}
