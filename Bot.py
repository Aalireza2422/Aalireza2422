import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes


BOT_TOKEN = os.getenv("BOT_TOKEN")
INVITE_LINK = os.getenv("INVITE_LINK", "")


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass


def start_web_server():
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not user or not user.is_premium:
        keyboard = [
            [
                InlineKeyboardButton(
                    "⭐ فعال‌سازی Telegram Premium",
                    url="https://t.me/premium"
                )
            ]
        ]

        await update.message.reply_text(
            "🔒 دسترسی این ربات فقط برای کاربران Telegram Premium فعال است.\n\n"
            "ابتدا Telegram Premium خود را فعال کنید، سپس دوباره /start را بزنید.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    text = "✅ حساب شما Premium است.\n\nبه ربات خوش آمدید!"

    if INVITE_LINK:
        keyboard = [
            [InlineKeyboardButton("🔗 ورود / Join", url=INVITE_LINK)]
        ]

        await update.message.reply_text(
            text + "\n\nبرای ورود به گروه روی دکمه زیر بزنید:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        await update.message.reply_text(
            text + "\n\nلینک ورود هنوز تنظیم نشده است."
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    threading.Thread(target=start_web_server, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    main()
