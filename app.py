import csv, json, math, os
from flask import Flask, request, jsonify, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

with open(os.path.join(BASE, "model.json")) as f:
    M = json.load(f)                      # trained logistic regression parameters

def _load_data():
    seen, rows = set(), []
    with open(os.path.join(BASE, "iris.csv"), newline="") as f:
        for r in csv.DictReader(f):
            row = [float(r[k]) for k in FEATURES] + [r["species"]]
            if tuple(row) not in seen:
                seen.add(tuple(row)); rows.append(row)
    return rows
DATA = _load_data()

def probabilities(x):
    z = [(v - m) / s for v, m, s in zip(x, M["mean"], M["scale"])]
    logits = [sum(w * zi for w, zi in zip(ws, z)) + b for ws, b in zip(M["coef"], M["intercept"])]
    mx = max(logits); e = [math.exp(l - mx) for l in logits]; t = sum(e)
    return [v / t for v in e]

def result(x):
    p = probabilities(x)
    return {"species": M["classes"][p.index(max(p))],
            "probabilities": {c: round(v, 4) for c, v in zip(M["classes"], p)}}

def parse_row(d):
    x = [float(d[k]) for k in FEATURES]          # KeyError/TypeError/ValueError -> caller
    if any(not (0 < v <= 15) for v in x):
        raise ValueError("range")
    return x

app = Flask(__name__)

@app.get("/")
def index():                                      # on Vercel, public/index.html is served by the CDN instead
    return send_from_directory(os.path.join(BASE, "public"), "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/data")
def api_data():
    return jsonify(DATA)

@app.get("/api/info")
def api_info():
    with open(os.path.join(BASE, "metrics.json")) as f:
        return jsonify(json.load(f))

@app.post("/predict")
def predict():
    try:
        x = parse_row(request.get_json(silent=True) or {})
    except (KeyError, TypeError, ValueError):
        return jsonify(error=f"Send numeric fields {FEATURES}, each between 0 and 15 cm"), 400
    return jsonify(result(x))

@app.post("/predict_batch")
def predict_batch():
    rows = (request.get_json(silent=True) or {}).get("rows")
    if not isinstance(rows, list) or not rows or len(rows) > 1000:
        return jsonify(error="Send 1 to 1000 rows"), 400
    try:
        xs = [parse_row(r) for r in rows]
    except (KeyError, TypeError, ValueError):
        return jsonify(error="Every row needs four numeric measurements between 0 and 15 cm"), 400
    return jsonify(results=[result(x) for x in xs])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
