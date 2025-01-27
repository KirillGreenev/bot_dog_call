import multiprocessing

from telethon.sync import TelegramClient
from config import API_ID, API_HASH, PHONE


def add_session() -> None:
    client = TelegramClient(PHONE, API_ID, API_HASH)
    client.start()
    client.disconnect()


def get_members_group(id_group: int, q: multiprocessing.Queue) -> None:
    client = TelegramClient(PHONE, API_ID, API_HASH)
    client.start()

    try:
        channel = client.get_entity(id_group)
        members = ['@' + user.username if user.username else user.first_name for user in
                   client.get_participants(channel)]

        members_filter = [s for s in members if isinstance(s, str)]
        q.put(' '.join(members_filter))
    except Exception as e:
        print(f"Ошибка при получении участников группы: {e}")
    finally:
        client.disconnect()


if __name__ == '__main__':
    add_session()
