from states import state
from models import message_group
from telethon.sync import TelegramClient

async def get_client(phone: str) -> TelegramClient:
    client = TelegramClient(session=phone, api_id=24963729, api_hash="1bab3b9c3675227b43619d2175bd6990")
    return client

async def get_my_groups(chat_id: int) -> list:
    groups = []
    data = state.get_data(chat_id)
    phone = data.get("PHONE_NUMBER")
    msg_group_list = message_group.MessageGroup.list()
    client: TelegramClient = await get_client(phone)
    if not client.is_connected():
        await client.connect()
    for msg_group in msg_group_list:
        result = await client.get_entity(msg_group[2])
        if result.left == False:
            groups.append(msg_group[2])
    await client.disconnect()
    return groups
