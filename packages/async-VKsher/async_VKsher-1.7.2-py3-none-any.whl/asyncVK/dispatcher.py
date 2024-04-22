from typing import Any


class Dispatcher:
    def __init__(self, event: dict, bot, text: str = None, user_id: int = None, peer_id: int = None,
                 post_id: int = None, owner_id: int = None, reply_text: str = None, reply_user_id: int = None,
                 reply_peer_id: int = None, chain_data: Any = None):
        self.bot = bot
        self.user_id = user_id
        self.peer_id = peer_id
        self.chat_id = peer_id - 2000000000
        self.post_id = post_id
        self.owner_id = owner_id
        self.event = event
        self.text = text
        self.reply_text = reply_text
        self.reply_user_id = reply_user_id
        self.reply_peer_id = reply_peer_id
        self.chain_data = chain_data

    async def answer(self, text: str = None, attachment: str = None, keyboard: str = None) -> None:
        await self.bot.execute("messages.send", message=text, user_id=self.user_id,
                               random_id=0, attachment=attachment, keyboard=keyboard)

    async def send_message(self, text: str = None, attachment: str = None, keyboard: str = None) -> None:
        await self.bot.execute("messages.send", message=text, peer_id=self.peer_id,
                               random_id=0, attachment=attachment, keyboard=keyboard)

    async def send_comment(self, text: str = None, attachment: str = None) -> None:
        await self.bot.execute("wall.createComment",
                               owner_id=self.owner_id, post_id=self.post_id, message=text, attachment=attachment)

    async def mark_as_read(self) -> None:
        await self.bot.execute("messages.markAsRead", peer_id=self.peer_id)

    async def set_typing_status(self, typing_status: str = "typing") -> None:
        await self.bot.execute("messages.setActivity", peer_id=self.peer_id, type=typing_status)

    async def kick_user(self, member_id: int) -> None:
        await self.bot.execute("messages.removeChatUser", chat_id=self.chat_id, member_id=member_id)

    async def edit_chat_name(self, title: str) -> None:
        await self.bot.execute("messages.editChat", chat_id=self.chat_id, title=title)


def get_dispatcher_by_event(bot, event: dict, event_params: dict, chain_data: Any) -> Dispatcher:
    text = event_params["text"]
    user_id = event_params["user_id"]
    peer_id = event_params["peer_id"]
    post_id = event_params["post_id"]
    owner_id = event_params["owner_id"]
    reply_message = event_params["reply_message"]

    return Dispatcher(event=event, bot=bot, text=text, user_id=user_id, peer_id=peer_id,
                      post_id=post_id, owner_id=owner_id, reply_text=reply_message.get("text"),
                      reply_peer_id=reply_message.get("peer_id"), reply_user_id=reply_message.get("user_id"),
                      chain_data=chain_data)
