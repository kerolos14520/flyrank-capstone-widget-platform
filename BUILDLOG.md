# Capstone Development Build Log

## Phase 1: Project Setup & Baseline Documentation
- Initialized local Git repository and connected to remote GitHub repository.
- Created baseline repository structure (`README.md`, `capstone.yaml`, `EVIDENCE.md`, `BUILDLOG.md`, `.env.example`).
- Authored initial system architecture diagram and database schema specifications in `README.md`.

## Phase 2: Lead Ingestion Engine & Data Reliability
- Installed core project dependencies (`fastapi`, `uvicorn`, `pydantic`, `email-validator`, `sqlalchemy`, `aiosqlite`, `slowapi`).
- Configured Pydantic submission schemas with anti-spam honeypot verification (`website` hidden field).
- Built IP geolocation service (`app/services/geo_service.py`) using asynchronous `httpx` with dual-provider fallback logic.
- Integrated SQLAlchemy database models (`app/models/submission.py`) and async SQLite persistence layer (`app/core/database.py`).
- Applied rate-limiting middleware (`app/core/limiter.py`) enforcing 10 requests/minute per IP address via `slowapi`.

## Phase 3: Async Side-Effects & Event Notifications
- Created `app/services/webhook_service.py` for dispatching external HTTP POST notifications.
- Attached `BackgroundTasks` execution to `POST /api/v1/submissions` to handle webhook delivery asynchronously without blocking HTTP response lifecycle.

## Phase 4: Widget Configuration & Embed Script Delivery
- Created `Widget` database model (`app/models/widget.py`) and configuration schema (`app/schemas/widget.py`).
- Implemented `GET /api/v1/widgets/{widget_id}/config` to return tenant widget configuration settings.
- Implemented `GET /api/v1/widgets/{widget_id}/embed.js` to dynamically serve cross-origin JavaScript embed scripts.