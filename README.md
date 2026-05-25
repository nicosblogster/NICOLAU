<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/10ufea4QyAwX_BT4_5sEDjwWiNufcNvOy

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

## Machine Learning with GitHub Actions

This repository now includes a simple machine learning training example using Python and scikit-learn.

### Files added

- `train.py`: trains an Iris classifier and writes artifacts to `models/`
- `requirements.txt`: Python dependencies
- `.github/workflows/train-model.yml`: workflow to train in GitHub Actions

### Run training locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python train.py
```

### Run training on GitHub

1. Push to the `main` branch, or
2. Open **Actions** tab and trigger **Train ML Model** with **Run workflow**.

After it runs, download the `iris-model-artifacts` artifact from the workflow run page.
