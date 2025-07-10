# Development Workflow – Django + PostgreSQL inside Docker Compose

> **Audience:** Teammates who are new to Docker. **Goal:** Run, develop, and maintain the project locally with the *least friction*.

---

## Prerequisites

| Tool                         | Tested Version         | What it’s for              |
| ---------------------------- | ---------------------- | -------------------------- |
| **Git**                      | ≥ 2.40                 | Clone & share code ✓       |
| **Docker Desktop**           | ≥ 4.32 (Windows/macOS) |                            |
|   Docker Engine ≥ 24 (Linux) | Runs containers ✓      |                            |
| **Make** (optional)          | any                    | Shortcut commands (see §9) |

> **Tip:** On Windows, enable *WSL 2* integration in Docker Desktop for best performance.

---

## First‑time Setup

```bash
# 1  Clone the repository
$ git clone <repo‑url> drf-server && cd drf-server

# 2  Create your personal environment file
$ cp .env.example .env
#   → Open .env and adjust DB_PASSWORD, SECRET_KEY, etc.

# 3  Build the images & start the stack (first run takes a few minutes)
$ docker-compose up --build

# 4  In another terminal, apply DB migrations & create the admin user
$ docker-compose exec server python manage.py migrate
$ docker-compose exec server python manage.py createsuperuser
```

- Navigate to [**http://localhost:8000**](http://localhost:8000) – you should see Django running.

---

## Daily Development Loop

| Action                     | Command                                        | Notes                                                                            |
| -------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------- |
| **Start stack**            | `docker-compose up`                            | Reuses previous build; quick                                                     |
| **Edit code**              | Use your editor in `server/`                   | Changes auto‑reload via `runserver`                                              |
| **Install new Python lib** | `docker-compose exec server pip install <pkg>` | Then: `docker-compose exec server pip freeze > server/requirements.txt` → commit |
| **Stop stack**             | `Ctrl +C` or `docker-compose down`             | Keeps DB data (volume)                                                           |

> **No rebuild needed** for simple code edits because `server/` is *mounted* inside the container (`volumes:`).

---

## When to Re‑build the Image

Run `` (or `docker-compose build && docker-compose up`) **only if**:

1. You changed **Dockerfile** (base image, system packages, etc.).
2. You modified ``.
3. You updated ``** values** that the *build* relies on (`ARG`/`ENV`).

For anything else (Python code, templates, static files) a rebuild is **not** necessary.

---

## Database & Migrations

| Operation          | Command                                                      |
| ------------------ | ------------------------------------------------------------ |
| Make new migration | `docker-compose exec server python manage.py makemigrations` |
| Apply migrations   | `docker-compose exec server python manage.py migrate`        |
| Open psql prompt   | `docker-compose exec database psql -U $DB_USER $DB_NAME`     |

DB data lives in the named volume `` (see `docker-compose.yml`). It survives `docker-compose down`; delete with `docker volume rm drf-server_postgres_data` if you need a reset.

---

## Updating `pip` Permanently

Add **once** to your `Dockerfile` (before installing requirements):

```Dockerfile
RUN python -m pip install --upgrade pip
```

Then rebuild: `docker-compose build`.

To update *temporarily* inside a running container:

```bash
docker-compose exec server pip install --upgrade pip
```

---

## Cleaning Up

| What                              | Command                  |
| --------------------------------- | ------------------------ |
| Stop & remove containers          | `docker-compose down`    |
| Stop, remove & delete **volumes** | `docker-compose down -v` |
| Remove dangling images            | `docker image prune -f`  |

---

## Optional – Makefile Shortcuts

Create a `Makefile` in the root to shorten commands:

```makefile
up:
	@docker-compose up

down:
	@docker-compose down -v

rebuild:
	@docker-compose up --build

shell:
	@docker-compose exec server bash

migrate:
	@docker-compose exec server python manage.py migrate
```

Now you can run `make up`, `make shell`, etc.

---

## 10  Troubleshooting

| Symptom                      | Fix                                                                                      |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| **Env vars empty**           | Ensure `.env` is in the same folder as `docker-compose.yml` and listed under `env_file:` |
| **DB connection refused**    | Confirm `DB_HOST=database` in `.env`; containers on same network                         |
| **Changes not visible**      | Verify `volumes:` path is correct and `runserver` watching files                         |
| **Port 8000 already in use** | Modify `ports:` mapping, e.g. `"9000:8000"`                                              |

---

## Glossary

- **Image** – template (snapshot) used to create containers.
- **Container** – running instance of an image.
- **Volume** – persistent data storage managed by Docker.
- **Network** – virtual LAN where containers discover each other by service name.
- **Bind mount** – host folder mounted into a container (`./server:/server`).

---

