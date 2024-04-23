from aiogram import Bot

from grabber.core.settings import BOT_TOKEN


async def send_message(post_text: str) -> None:
    bot = Bot(token=f"bot{BOT_TOKEN}")
    await bot.send_message(chat_id="@cosplaymaster", text=post_text)
    print(f"Post sent to the channel: {post_text}")
