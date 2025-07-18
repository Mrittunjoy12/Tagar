PK     #(�Z�/x  x     main.pyfrom telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import smtplib
from email.mime.text import MIMEText
import random
import string
import json
import os

TOKEN = "7699490123:AAE7jD59d0jYgfbLa0ixP3EfXEXtjPuhbGQ"
ADMIN_ID = 7352578881

# Verification storage
users_file = "users.json"
verifications = {}

def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(users_file, "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

def generate_code():
    return ''.join(random.choices(string.digits, k=6))

def send_email(receiver, code):
    sender = "freelancingzone.office@gmail.com"
    password = "apes mcdm wxhl xvbe"
    message = MIMEText(f"Your verification code is: {code}")
    message["Subject"] = "Verification Code"
    message["From"] = sender
    message["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(message)

async def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id in users:
        await update.message.reply_text("✅ আপনি ইতোমধ্যে রেজিস্ট্রেশন করেছেন!")
    else:
        await update.message.reply_text("✉️ আপনার ইমেইল লিখুন রেজিস্ট্রেশনের জন্য")
        context.user_data["awaiting_email"] = True

async def handle_message(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    text = update.message.text

    if context.user_data.get("awaiting_email"):
        email = text.strip()
        code = generate_code()
        verifications[user_id] = {"email": email, "code": code}
        send_email(email, code)
        context.user_data["awaiting_email"] = False
        context.user_data["awaiting_code"] = True
        await update.message.reply_text("📨 একটি ভেরিফিকেশন কোড পাঠানো হয়েছে। কোডটি এখানে লিখুন।")
    elif context.user_data.get("awaiting_code"):
        if user_id in verifications and text == verifications[user_id]["code"]:
            email = verifications[user_id]["email"]
            users[user_id] = {"email": email}
            save_users(users)
            context.user_data["awaiting_code"] = False
            await update.message.reply_text("✅ রেজিস্ট্রেশন সম্পন্ন হয়েছে!")
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"🆕 নতুন রেজিস্ট্রেশন: {user_id} | {email}")
        else:
            await update.message.reply_text("❌ ভুল কোড। আবার চেষ্টা করুন।")
    else:
        await update.message.reply_text("⚠️ দয়া করে /start কমান্ড দিন।")

async def refer(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id not in users:
        await update.message.reply_text("❗ আগে রেজিস্ট্রেশন করুন /start দিয়ে।")
        return
    referral_link = f"https://t.me/{context.bot.username}?start={user_id}"
    await update.message.reply_text(f"🤝 আপনার রেফারেল লিংক:
{referral_link}")

async def all_users(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ আপনি এই কমান্ড ব্যবহার করতে পারবেন না।")
        return

    msg = "📋 রেজিস্টার্ড ইউজার:

"
    for uid, data in users.items():
        msg += f"🆔 {uid} | 📧 {data['email']}
"
    await update.message.reply_text(msg)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("refer", refer))
    app.add_handler(CommandHandler("users", all_users))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()PK     #(�Z�}o&   &      requirements.txtpython-telegram-bot==20.3
Flask==2.3.2PK     #(�Z�/x  x             ��    main.pyPK     #(�Z�}o&   &              ���  requirements.txtPK      s   �    