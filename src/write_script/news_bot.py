import os
import feedparser

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

RSS_SOURCES = {
    "威脅情資": "https://feeds.feedburner.com/TheHackersNews",
    "漏洞警報": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
    "資安快訊": "https://www.bleepingcomputer.com/feed/",
    "國際時事": "https://news.google.com/rss/search?q=world&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
}


def get_news(category):
    rss_url = RSS_SOURCES.get(category)
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        return "目前抓不到新聞，請稍後再試。"

    news_list = []

    for i, entry in enumerate(feed.entries[:5], start=1):
        title = entry.title
        link = entry.link

        news_list.append(f"{i}. 📰 {title}\n🔗 {link}")

    return f"【{category}】最新消息\n\n" + "\n\n".join(news_list)


def summarize_news(category):
    rss_url = RSS_SOURCES.get(category)
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        return "目前抓不到新聞，請稍後再試。"

    titles = []

    for i, entry in enumerate(feed.entries[:5], start=1):
        titles.append(f"{i}. {entry.title}")

    news_text = "\n".join(titles)

    return f"""【{category} 摘要】

一、今日重點摘要
以下是目前較值得注意的消息標題：

{news_text}

二、值得注意的趨勢
可留意是否出現新漏洞、勒索軟體、APT 攻擊、資料外洩、供應鏈攻擊或重大國際事件。

三、我應該關注什麼
建議優先點開與「CVE、漏洞利用、勒索病毒、APT、資料外洩、惡意軟體、供應鏈」相關的消息深入閱讀。
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """你好，我是你的 Threat Intelligence Bot 🤖

你可以輸入：

威脅情資
漏洞警報
資安快訊
國際時事
威脅摘要
漏洞摘要
資安摘要
國際摘要
"""
    await update.message.reply_text(message)


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    print("收到一則新訊息：", user_text)

    if user_text == "威脅情資":
        await update.message.reply_text(get_news("威脅情資"))
        return

    if user_text == "漏洞警報":
        await update.message.reply_text(get_news("漏洞警報"))
        return

    if user_text == "資安快訊":
        await update.message.reply_text(get_news("資安快訊"))
        return

    if user_text == "國際時事":
        await update.message.reply_text(get_news("國際時事"))
        return

    if user_text == "威脅摘要":
        await update.message.reply_text(summarize_news("威脅情資"))
        return

    if user_text == "漏洞摘要":
        await update.message.reply_text(summarize_news("漏洞警報"))
        return

    if user_text == "資安摘要":
        await update.message.reply_text(summarize_news("資安快訊"))
        return

    if user_text == "國際摘要":
        await update.message.reply_text(summarize_news("國際時事"))
        return

    await update.message.reply_text(
        "目前支援指令：\n\n"
        "威脅情資\n"
        "漏洞警報\n"
        "資安快訊\n"
        "國際時事\n"
        "威脅摘要\n"
        "漏洞摘要\n"
        "資安摘要\n"
        "國際摘要"
    )


if not TELEGRAM_TOKEN:
    raise ValueError("找不到 TELEGRAM_TOKEN，請在 Render 的 Environment Variables 設定。")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Threat Intelligence Telegram Bot 已啟動")

app.run_polling()