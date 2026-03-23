from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8741953371:AAFz3PJ8meWt_ySjXN30y41dxQhZfRGszEk"
ADMINS = [6562354897]
RESTRICTED_TOPICS = []

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    topic_id = msg.message_thread_id
    user_id = msg.from_user.id

    print("Message in topic:", topic_id, "from user:", user_id)

    if user_id not in ADMINS and ((topic_id in RESTRICTED_TOPICS) or (topic_id is None and "main" in RESTRICTED_TOPICS)):
        try:
            await msg.delete()
        except Exception as e:
            print("Failed to delete:", e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is ready!")

async def lock_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        await update.message.reply_text("❌ Not allowed")
        return

    topic_id = update.message.message_thread_id
    if not topic_id:
        await update.message.reply_text("⚠️ Use inside a topic")
        return

    if topic_id not in RESTRICTED_TOPICS:
        RESTRICTED_TOPICS.append(topic_id)
        await update.message.reply_text(f"🔒 Locked: {topic_id}")

async def unlock_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        await update.message.reply_text("❌ Not allowed")
        return

    topic_id = update.message.message_thread_id
    if not topic_id:
        await update.message.reply_text("⚠️ Use inside a topic")
        return

    if topic_id in RESTRICTED_TOPICS:
        RESTRICTED_TOPICS.remove(topic_id)
        await update.message.reply_text(f"🔓 Unlocked: {topic_id}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("locktopic", lock_topic))
app.add_handler(CommandHandler("unlocktopic", unlock_topic))
app.add_handler(MessageHandler(~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling()