import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, render_template_string
import threading
import asyncio
import os

TOKEN = "8952524440:AAEEgqQQEBvkF6pToofDC7XqXZvT_RR_ZBM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SHOKH GOLD OPTION</title>
    <style>
        body { background: #0f141f; color: white; text-align: center; padding: 20px; font-family: Arial; }
        .balance-card { background: #1a2233; padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #2a364f; }
        .balance { font-size: 26px; color: #00e676; font-weight: bold; }
        .chart-box { background: #141b2b; height: 180px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; color: #ffcc00; border: 1px solid #2a364f; margin-bottom: 20px; }
        button { width: 100%; padding: 15px; margin: 8px 0; border: none; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; }
        .up { background: #00e676; color: #000; }
        .down { background: #ff334b; color: white; }
    </style>
</head>
<body>
    <h2>SHOKH GOLD OPTION</h2>
    <div class="balance-card">
        <div>Balans:</div>
        <div class="balance" id="balance">100,000 SO'M</div>
    </div>
    <div class="chart-box" id="chartValue">EUR/USD: 1.08450 📈</div>
    <button class="up" onclick="trade('UP')">YUQORIGA (CALL) 🟢</button>
    <button class="down" onclick="trade('DOWN')">PASTGA (PUT) 🔴</button>

    <script>
        let balance = 100000;
        setInterval(() => {
            let val = (1.08450 + (Math.random() * 0.0004 - 0.0002)).toFixed(5);
            document.getElementById('chartValue').innerText = "EUR/USD: " + val + " 📈";
        }, 1500);

        function trade(type) {
            let amount = 10000;
            if(balance < amount) { alert("Balans yetarli emas!"); return; }
            balance -= amount;
            setTimeout(() => {
                let win = Math.random() > 0.45;
                if(win) {
                    let profit = amount * 1.85;
                    balance += profit;
                    alert("Tabriklayman! Yutdingiz: +" + profit + " SO'M");
                } else {
                    alert("Afsuski, yutqazdingiz.");
                }
                document.getElementById('balance').innerText = balance.toLocaleString() + " SO'M";
            }, 2000);
            document.getElementById('balance').innerText = balance.toLocaleString() + " SO'M";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    web_app_url = "https://shokh-gold-bot.onrender.com"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 Savdoni Boshlash", web_app=WebAppInfo(url=web_app_url))]
    ])
    await message.answer("SHOKH GOLD OPTION platformasiga xush kelibsiz! Savdoni boshlash uchun quyidagi tugmani bosing:", reply_markup=kb)

async def main():
    threading.Thread(target=run_flask, daemon=True).start()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
