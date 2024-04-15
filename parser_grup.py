from telethon.sync import TelegramClient
from config import API_ID, API_HASH, PHONE


def add_session():
    client = TelegramClient(PHONE, API_ID, API_HASH)
    client.start()
    client.disconnect()


def get_members_grup(id_grup, q):
    client = TelegramClient(PHONE, API_ID, API_HASH)
    client.start()
    channel = client.get_entity(id_grup)
    string = ['@' + user.username if user.username else user.first_name for user in client.get_participants(channel)]
    client.disconnect()
    q.put(' '.join(string))


if __name__ == '__main__':
    add_session()