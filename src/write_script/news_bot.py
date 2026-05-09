import os
import feedparser

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

RSS_SOURCES = {
    "資安新聞": "https://news.google.com/rss/search?q=Cybersecurity&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "國際時事": "https://news.google.com/rss/search?q=world&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
}

def get_news(category):
    rss_url = RSS_SOURCES.get(category)

    feed = feedparser.parse(rss_url)

    news = []

    for i, entry in enumerate(feed.entries[:5], start=1):
        news.append(f"{i}. {entry.title}")

    return "\n\n".join(news)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("AI 新聞 Bot 已啟動")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "資安新聞":
        await update.message.reply_text(get_news("資安新聞"))
        return

    if text == "國際時事":
        await update.message.reply_text(get_news("國際時事"))
        return

    await update.message.reply_text("請輸入：資安新聞 或 國際時事")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

print("Bot 啟動")

app.run_polling()