
__all__ = [ 'ChatManagerError', 'UserNoPremiumError']


class ChatManagerError(RuntimeError):
    pass


class UserNoPremiumError(ChatManagerError):
    pass
