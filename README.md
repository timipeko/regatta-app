
# Regatta (Fly.io-ready)

Two apps:
- **backend/** → Django + DRF API (`regatta-api`)
- **frontend/** → Vue + Vite static site (`regatta-web`)

## Prereqs
- flyctl, Docker, Python 3.11+, Node 18+

## Deploy backend
cd backend
fly launch --now --copy-config --no-deploy --name regatta-api
fly pg create --name regatta-pg --region ams --initial-cluster-size 1
fly pg attach regatta-pg --app regatta-api
fly secrets set DJANGO_SECRET_KEY=$(openssl rand -hex 32) --app regatta-api
fly secrets set DJANGO_DEBUG=False --app regatta-api
fly secrets set CORS_ALLOWED_ORIGINS=https://regatta-web.fly.dev --app regatta-api
fly secrets set CSRF_TRUSTED_ORIGINS=https://regatta-web.fly.dev --app regatta-api
fly deploy --app regatta-api
fly ssh console --app regatta-api -C "python manage.py migrate && python manage.py seed_demo"

## Deploy frontend
cd ../frontend
npm install
fly launch --now --copy-config --no-deploy --name regatta-web
fly deploy --build-arg VITE_API_BASE=https://regatta-api.fly.dev/api --app regatta-web

Open:
- API docs: https://regatta-api.fly.dev/api/docs/
- Web: https://regatta-web.fly.dev/
