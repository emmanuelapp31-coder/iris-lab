import csv, joblib, pandas as pd
from app import app, FEATURES
c = app.test_client()
assert c.get("/").status_code == 200 and c.get("/health").get_json() == {"status": "ok"}
# parity with the original scikit-learn model on every row of the dataset
m = joblib.load("/home/claude/iris_app/model.joblib")
df = pd.read_csv("iris.csv"); sk = m.predict_proba(df[FEATURES]); worst = 0
for (_, r), p in zip(df.iterrows(), sk):
    out = c.post("/predict", json={k: float(r[k]) for k in FEATURES}).get_json()
    worst = max(worst, max(abs(out["probabilities"][cl] - float(v)) for cl, v in zip(m.classes_, p)))
    assert out["species"] == m.classes_[p.argmax()]
print("max probability difference vs scikit-learn:", worst)
assert worst < 1e-4
assert len(c.get("/api/data").get_json()) == 147 and c.get("/api/info").get_json()["n_total"] == 147
b = c.post("/predict_batch", json={"rows":[dict(zip(FEATURES,[5.1,3.5,1.4,.2])),dict(zip(FEATURES,[6.9,3.1,5.4,2.1]))]}).get_json()
assert [r["species"] for r in b["results"]] == ["setosa","virginica"]
for bad in [{}, {"sepal_length":-1,"sepal_width":3,"petal_length":1,"petal_width":1}, {"sepal_length":"x"}]:
    assert c.post("/predict", json=bad).status_code == 400
assert c.post("/predict_batch", json={"rows":[]}).status_code == 400
print("all tests passed")
