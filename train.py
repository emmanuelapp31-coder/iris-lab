import json, joblib, pandas as pd, numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

df = pd.read_csv("iris.csv").drop_duplicates()
FEATURES = ["sepal_length","sepal_width","petal_length","petal_width"]
X, y = df[FEATURES], df["species"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

models = {
 "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
 "KNN (k=5)": make_pipeline(StandardScaler(), KNeighborsClassifier(5)),
 "SVM (RBF)": make_pipeline(StandardScaler(), SVC()),
 "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
}
cv = StratifiedKFold(5, shuffle=True, random_state=42)
for n, m in models.items():
    s = cross_val_score(m, X_tr, y_tr, cv=cv)
    print(f"{n:22s} CV acc {s.mean():.3f} ± {s.std():.3f}")

best = models["Logistic Regression"].fit(X_tr, y_tr)
pred = best.predict(X_te)
print("\nTest accuracy:", accuracy_score(y_te, pred))
print(classification_report(y_te, pred))
print(confusion_matrix(y_te, pred, labels=best.classes_), best.classes_)

# final model on all data, saved for deployment
final = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X, y)
joblib.dump(final, "model.joblib")

sc, lr = final[0], final[1]
json.dump({"features":FEATURES,"classes":list(lr.classes_),
  "mean":sc.mean_.tolist(),"scale":sc.scale_.tolist(),
  "coef":lr.coef_.tolist(),"intercept":lr.intercept_.tolist()}, open("model_params.json","w"))
print(json.dumps({"mean":sc.mean_.round(4).tolist()}))

json.dump({"classes":[str(c) for c in lr.classes_],"mean":sc.mean_.tolist(),"scale":sc.scale_.tolist(),
           "coef":lr.coef_.tolist(),"intercept":lr.intercept_.tolist()}, open("model.json","w"))
print("wrote model.json")
