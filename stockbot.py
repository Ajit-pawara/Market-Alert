from apscheduler.schedulers.background import BackgroundScheduler
import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yfinance as yf

# Replace this with your bot token
TOKEN = "7519487301:AAErz2i2rVZgiMzN0S248slCtrFm53oIMGs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I’m your Stock Bot!\n\nCommands:\n"
        "/topgainers - Show today's top movers\n"
        "/analyse GENUSPOWER - Analyse a stock"
    )

async def top_gainers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gainers = {
        "GENUSPOWER": "+5.8%",
        "ELECTCAST": "+6.2%",
        "TATAPOWER": "+4.9%",
    }
    msg = "📈 *Today's Top Gainers:*\n"
    for stock, gain in gainers.items():
        msg += f"🔹 {stock}: {gain}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Usage: /analyse STOCKNAME")
        return
    try:
        stock = context.args[0].upper() + ".NS"
        ticker = yf.Ticker(stock)
        data = ticker.history(period="5d")
        current = data['Close'].iloc[-1]
        previous = data['Close'].iloc[-2]
        change = ((current - previous) / previous) * 100
        msg = f"🔍 {stock} Analysis:\nPrice: ₹{current:.2f}\nChange: {change:.2f}%"
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text("⚠️ Could not fetch data. Check the stock name or internet.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("topgainers", top_gainers))
    app.add_handler(CommandHandler("analyse", analyse))

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: app.create_task(daily_stock_alert(app.bot)),
        'cron',
        hour=9, minute=15
    )
    scheduler.start()

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
async def daily_stock_alert(context: ContextTypes.DEFAULT_TYPE):
    chat_id = "YOUR_CHAT_ID"  # Replace this with your personal chat ID
    message = (
        "🌅 *Morning Stock Alert*\n"
        "Top Movers:\n"
        "🔸 GENUSPOWER: +5.8%\n"
        "🔸 ELECTCAST: +6.2%\n"
        "🔸 TATAPOWER: +4.9%\n"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
