# Mini Project Management System

Scaffold for the screening task. This repo contains a minimal Django backend with GraphQL (Graphene) and Docker configuration.

Quick start (Docker):

1. Copy `.env.example` to `.env` and adjust values.
2. Start services:

```powershell
docker-compose up --build -d
```

3. Run migrations and create superuser:

```powershell
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

4. Open GraphiQL at: http://localhost:8000/graphql/

Backend files are under `backend/`.

Planned next steps:
- Create the React + TypeScript frontend (Vite + Tailwind + Apollo)
- Add tests and CI
- Harden settings and production Docker setup
