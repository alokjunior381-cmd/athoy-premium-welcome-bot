
import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.constants import ChatMemberStatus
from telegram.request import HTTPXRequest
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
CHANNEL_LINK = os.environ["CHANNEL_LINK"]
WEBHOOK_PATH = os.environ["WEBHOOK_PATH"].strip("/")
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
BASE_URL = os.environ["RENDER_EXTERNAL_URL"].rstrip("/")
PORT = int(os.environ.get("PORT", "10000"))

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)]
])

WELCOME_TEXT = (
    "🎉 <b>Welcome to ATHOY PREMIUM!</b>\n\n"
    "❤️ আমাদের চ্যানেলে যোগ দেওয়ার জন্য ধন্যবাদ।\n"
    "🔥 নতুন আপডেট পেতে নিচের বাটনে চাপ দাও।"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message:
        await update.effective_message.reply_text(
            WELCOME_TEXT,
            reply_markup=keyboard,
            parse_mode="HTML",
        )


async def private_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_message:
        await update.effective_message.reply_text(
            "👋 ধন্যবাদ! আমাদের চ্যানেলে যোগ দিতে নিচের বাটনে চাপ দাও।",
            reply_markup=keyboard,
        )


async def member_update(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    change = update.chat_member
    if not change:
        return

    old_status = change.old_chat_member.status
    new_status = change.new_chat_member.status

    joined_statuses = {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    }

    if old_status not in joined_statuses and new_status in joined_statuses:
        user = change.new_chat_member.user
        name = (
            user.full_name
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        message = (
            f"🎉 <b>নতুন সদস্যকে স্বাগতম!</b>\n\n"
            f"👤 নাম: {name}\n"
            f"📢 ATHOY PREMIUM চ্যানেলে স্বাগতম ❤️"
        )

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            parse_mode="HTML",
            reply_markup=keyboard,
        )


def main():
    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30,
    )

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND,
            private_message,
        )
    )
    app.add_handler(
        ChatMemberHandler(member_update, ChatMemberHandler.CHAT_MEMBER)
    )

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=WEBHOOK_PATH,
        webhook_url=f"{BASE_URL}/{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET,
        allowed_updates=["message", "chat_member"],
        bootstrap_retries=-1,
    )


if __name__ == "__main__":
    main()
