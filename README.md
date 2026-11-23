# EstateOps — Real Estate Construction Operations Dashboard

A Streamlit portfolio application for monitoring construction delivery across a multi-project real-estate portfolio.

## Features
- Portfolio-level progress and budget KPIs
- Planned-versus-actual progress comparison
- Budget utilisation by project
- Work-package register with schedule variance
- Threshold-based operational alerts
- CSV export of filtered records

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Data
`data/projects.csv` is a **synthetic demonstration dataset**. It is not Godrej Properties data. Replace it with authorised project data before any real operational use.

## Deployment
Create a GitHub repository, push this folder, then create an app at [Streamlit Community Cloud](https://share.streamlit.io/) and select `app.py`.

## Suggested interview discussion
Explain how schedule variance, cost utilisation and exception thresholds help a project manager prioritise site follow-ups. Discuss limitations: progress measurement quality, cost-code mapping, update frequency and false alerts.
