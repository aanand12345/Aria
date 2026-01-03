import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from openai import OpenAI

app = FastAPI()
TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
client = OpenAI(api_key=OPENROUTER_KEY, base_url="https://openrouter.ai/api/v1")

application = Application.builder().token(TOKEN).build()

async def ai_reply(text):
    resp = client.chat.completions.create(model="deepseek/deepseek-r1", messages=[
        {"role": "system", "content": "तुम Aria हो। Hindi/English friendly AI।"},
        {"role": "user", "content": text}
    ])
    return resp.choices[0].message.content

@application.message(Command("start"))
async def start(update: Update, context):
    await update.message.reply_text("नमस्ते! Aria यहाँ हूँ 😊")

@application.message(filters.TEXT & ~filters.COMMAND)
async def chat(update: Update, context):
    reply = await ai_reply(update.message.text)
    await update.message.reply_text(reply)

@app.post("/")
async def webhook(request: Request):
    update = Update.de_json(await request.json(), application.bot)
    await application.process_update(update)
    return {"ok": True}

@app.get("/")
def home():
    return "Aria Bot Live!"
