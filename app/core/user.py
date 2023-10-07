from dataclasses import dataclass, field
from baski.telegram import storage
from baski.primitives import datetime

from .exceptions import UserNoPremiumError


@dataclass()
class TelegramUser(storage.TelegramUser):
    last_credits: datetime.datetime = field(default=datetime.datetime.fromtimestamp(0))
    last_donation: datetime.datetime = field(default=datetime.datetime.fromtimestamp(0))

    def is_premium(self):
        return datetime.as_local(self.last_donation + datetime.timedelta(days=30)) > datetime.now()

    def assert_premium(self):
        if not self.is_premium():
            raise UserNoPremiumError()
