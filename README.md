# Digital Bevy – API‑Driven Mini Web App

Full‑stack mini app using Django + DRF + PostgreSQL (backend) and React (Vite) frontend.

## Features
- Enter a keyword → fetch GitHub repo data (via GitHub Search API)
- Store results in PostgreSQL
- List stored results with pagination, ordering, and basic filters
- Clean, modular code + error handling

## Tech Stack
- Backend: Django, DRF, PostgreSQL
- Frontend: React + Vite
- Hosting: Render/Heroku (sample configs included)

## Local Setup (Windows-friendly, no virtualenv required)

### Backend
```cmd
cd backend
pip install -r requirements.txt
copy .env.example .env
REM edit .env with your DB credentials
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Frontend
```cmd
cd ../frontend
npm install
npm run dev
```

## API Usage
- POST `/api/search/` body `{ "keyword": "django", "page": 1, "per_page": 10 }`
- GET  `/api/repos/?page=1&page_size=10&ordering=-stars&keyword=django`

## Deployment (Render)
1. Create PostgreSQL instance on Render and copy credentials.
2. Create a Web Service from `/backend` with:
   - Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start: `gunicorn backend.wsgi:application --preload --workers=2 --bind 0.0.0.0:$PORT`
3. Set env vars: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DB_*`, optional `GITHUB_TOKEN`.
4. Deploy frontend on Netlify/Vercel. Set `VITE_API_BASE=https://your-backend.onrender.com`.

## Notes
- Rate limits: without `GITHUB_TOKEN` you may hit 60 req/hr. Add token for higher limits.
- Security: In production, set `DEBUG=False` and restrict CORS/ALLOWED_HOSTS.
