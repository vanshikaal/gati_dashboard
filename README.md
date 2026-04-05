# GATI Healthcare Dashboard — Deployment Guide

## Deploy to Render (free, ~5 minutes)

### Step 1 — Push to GitHub
1. Create a new GitHub repository (public or private)
2. Upload this entire `gati_dashboard/` folder to it
3. Commit and push

### Step 2 — Connect to Render
1. Go to https://render.com and sign up (free)
2. Click **New → Web Service**
3. Connect your GitHub repository
4. Set these fields:
   - **Name**: gati-healthcare-dashboard (or anything you like)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server`
5. Click **Create Web Service**

Render will build and deploy. Your dashboard will be live at:
`https://your-service-name.onrender.com`

---

## Run Locally

```bash
cd gati_dashboard
pip install -r requirements.txt
python app.py
```

Then open: http://localhost:8050

---

## Updating the Dashboard

When Vanshika needs changes:
1. Share the updated `app.py` file
2. Replace in your GitHub repo
3. Render auto-redeploys in ~2 minutes

---

## File Structure

```
gati_dashboard/
├── app.py              ← Complete dashboard (all data embedded)
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

All data is embedded directly in `app.py` — no CSV file needed on the server.
The Germany map fetches GeoJSON from GitHub at startup. If the fetch fails,
the map automatically falls back to a bubble-map representation.

---

## Data Notes

- Source: StepStone Germany, 31 Jan – 10 Mar 2026
- n = 29,045 job postings
- Occupational classification: ISCO-08 (ILO)
- Employer classification: ISIC Rev. 4 (UN Statistics Division)
- 35.1% of records carry state-level geographic tags
