import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from agents.brain import think
from agents.planner import create_plan
from agents.executor import execute
from agents.memory import (
    save_memory,
    load_memory
)

from tools.helper import split_message

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🤖 OpenClaw Telegram Agent Ready

Commands:
/start
/status
/reset
"""

    await update.message.reply_text(text)

# =========================
# STATUS
# =========================

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Autonomous Agent Online"
    )

# =========================
# RESET
# =========================

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_chat.id)

    save_memory(user_id, [])

    await update.message.reply_text(
        "🧠 Memory cleared"
    )

# =========================
# CHAT
# =========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_chat.id)

    user_text = update.message.text

    history = load_memory(user_id)

    plan = create_plan(user_text)

    history.append({
        "role": "user",
        "content": user_text
    })

    messages = [
        {
            "role": "system",
            "content": plan
        },
        *history
    ]

    try:

        reply = think(messages)

        history.append({
            "role": "assistant",
            "content": reply
        })

        save_memory(user_id, history)

        chunks = split_message(reply)

        for chunk in chunks:

            await update.message.reply_text(chunk)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error: {str(e)}"
        )

# =========================
# MAIN
# =========================

def main():

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("reset", reset))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    print("🤖 OpenClaw Agent Running...")

    app.run_polling()

if __name__ == "__main__":
    main()
