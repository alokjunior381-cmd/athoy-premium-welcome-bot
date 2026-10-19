import os
import html
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
CHANNEL_LINK = os.environ["CHANNEL_LINK"]

def make_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "🚀 JOIN OUR CHANNEL",
            url=CHANNEL_LINK
        )
    ]])

def welcome(name):
    name = html.escape(name or "বন্ধু")
    return (
        "✨ <b>WELCOME TO OUR COMMUNITY</b> ✨\n\n"
        f"হ্যালো, <b>{name}</b>! ❤️\n\n"
        "আমাদের সঙ্গে যুক্ত হওয়ার জন্য ধন্যবাদ। 🥰\n\n"
        "💎 আমাদের চ্যানেলে নিয়মিত আপডেট পাবে।\n\n"
        "🔥 Stay Connected • Stay Awesome!"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        welcome(update.effective_user.first_name),
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard()
    )

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    event = update.chat_member
    if not event or event.chat.type != "channel":
        return

    old = event.old_chat_member.status
    new = event.new_chat_member.status

    if old not in ("left", "kicked"):
        return
    if new not in ("member", "administrator", "creator"):
        return

    user = event.new_chat_member.user
    if user.is_bot
