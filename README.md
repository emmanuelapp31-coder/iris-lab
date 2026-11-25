# Iris Lab (Vercel)

Flask API (app.py) + static frontend (public/index.html). Runs on Flask alone: the trained
logistic regression lives in model.json, so no scikit-learn is needed at runtime.

## Run locally
    pip install flask
    python app.py        # http://localhost:5000

## Deploy
Put these files at the ROOT of a GitHub repository, then on vercel.com:
Add New > Project > import the repository > Deploy.
(Vercel detects Flask automatically. Do not change the build settings.)

train.py retrains the model (needs scikit-learn); copy the model.json it writes next to app.py.
