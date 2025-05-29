from telethon import TelegramClient, events
import emoji

api_id = 20355326
api_hash = '741c61b70925f8e421f646f847d74e70'
target_chat_id = 1098185428

client = TelegramClient('autodel_session', api_id, api_hash)

def contains_other_emoji_than_laugh(text):
    # Проверяем эмодзи в тексте
    for char in text:
        if char in emoji.EMOJI_DATA and char != "😂":
            return True
    return False

async def check_and_delete(message):
    text = message.raw_text or ""

    # Удалить, если есть медиа
    if message.media:
        await message.delete()
        return

    # Удалить, если есть эмодзи, кроме 😂
    if contains_other_emoji_than_laugh(text):
        await message.delete()
        return

    # Оставляем текст и любые количества 😂
    # (никаких удалений здесь)

@client.on(events.NewMessage(chats=target_chat_id))
async def on_new_message(event):
    await check_and_delete(event.message)

@client.on(events.MessageEdited(chats=target_chat_id))
async def on_message_edited(event):
    await check_and_delete(event.message)

async def main():
    await client.start()
    print("Бот запущен и фильтрует сообщения по правилам.")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
