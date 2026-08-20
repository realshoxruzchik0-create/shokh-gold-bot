from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# Yangilangan HTML va JavaScript (Professional dizayn)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SHOKH GOLD TRADE</title>
    <style>
        body { background: #0e1117; color: white; font-family: Arial, sans-serif; margin: 0; text-align: center; }
        .top-bar { background: #161b22; padding: 15px; font-size: 20px; font-weight: bold; color: #58a6ff; }
        .chart { height: 250px; display: flex; align-items: flex-end; gap: 5px; padding: 10px; border-bottom: 2px solid #30363d; }
        .candle { width: 15px; }
        .white { background: white; }
        .red { background: #ff334b; }
        .controls { padding: 20px; display: flex; gap: 20px; justify-content: center; }
        button { padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .btn-call { background: white; color: black; }
        .btn-put { background: #ff334b; color: white; }
    </style>
</head>
<body>
    <div class="top-bar">Balans: <span id="balance">150000</span> SO'M</div>
    <div class="chart" id="chart"></div>
    <div class="controls">
        <button class="btn-call" onclick="trade('UP')">YUQORIGA (OQ)</button>
        <button class="btn-put" onclick="trade('DOWN')">PASTGA (QIZIL)</button>
    </div>
    
    <script>
        let balance = localStorage.getItem('balance') ? parseInt(localStorage.getItem('balance')) : 150000;
        document.getElementById('balance').innerText = balance;

        function updateBalance(val) {
            balance += val;
            localStorage.setItem('balance', balance);
            document.getElementById('balance').innerText = balance;
        }

        let candles = [];
        function createCandle() {
            let height = Math.floor(Math.random() * 100) + 20;
            let type = Math.random() > 0.45 ? 'white' : 'red'; // Oq chiqish ehtimoli ozroq (qiyinroq)
            candles.push({height, type});
            if(candles.length > 20) candles.shift();
            
            const chart = document.getElementById('chart');
            chart.innerHTML = '';
            candles.forEach(c => {
                let div = document.createElement('div');
                div.className = 'candle ' + c.type;
                div.style.height = c.height + 'px';
                chart.appendChild(div);
            });
        }
        setInterval(createCandle, 1000);

        function trade(dir) {
            let bet = 10000;
            if (balance < bet) { alert("Balans yetarli emas!"); return; }
            updateBalance(-bet);
            
            setTimeout(() => {
                let last = candles[candles.length - 1];
                let win = (dir === 'UP' && last.type === 'white') || (dir === 'DOWN' && last.type === 'red');
                if(win) {
                    updateBalance(bet * 1.9);
                    alert("Yutdingiz! +19,000 SO'M");
                } else {
                    alert("Yutqazdingiz!");
                }
            }, 2000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
