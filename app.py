from flask import Flask, render_template, abort
app = Flask(__name__)

TXT_PATH = "lotteries.txt"

def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def read_lotteries(path):
    lines = read_lines(path)
    result = []
    for line in lines:
        # Split into up to 3 parts: id | amount | date (missing parts become "")
        parts = (line.split("|") + ["", ""])[:3]
        item = {
            "id": parts[0].strip(),
            "amount": parts[1].strip(),
            "date": parts[2].strip()
        }
        result.append(item)
    return result

def find_lottery(lotteries, lot_id):
    for l in lotteries:
        if l["id"] == str(lot_id):
            return l
    return None

@app.route("/")
def index():
    lotteries = read_lotteries(TXT_PATH)
    return render_template("home.html", lotteries=lotteries)

@app.route("/lottery/<lot_id>")
def lottery_detail(lot_id):
    lotteries = read_lotteries(TXT_PATH)
    item = find_lottery(lotteries, lot_id)
    if not item:
        abort(404)
    return render_template("lotterypage.html", lottery=item)

@app.route("/login")
@app.route("/register")
def login():
    return render_template("login.html")

@app.route("/info")
def info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=True)
