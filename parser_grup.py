from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from config import API_ID, API_HASH, PHONE, GROUP_ID


def get_members_grup(id_grup):
    client = TelegramClient(PHONE, API_ID, API_HASH)
    client.start()
    last_date = None
    size_chats = 200

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=size_chats,
        hash=0
    ))

    for chat in result.chats:
        if chat.id == abs(id_grup):
            group = chat
            break
    string = ['@' + user.username if user.username else user.first_name for user in client.get_participants(group)]
    return ' '.join(string)


if __name__ == '__main__':
    print(get_members_grup(GROUP_ID))
