# Capstone Project Evidence & Verification Report

## Project Overview
- **Project Name:** Embeddable Widget & Lead-Capture Platform
- **Repository:** https://github.com/kerolos14520/flyrank-capstone-widget-platform
- **Framework:** FastAPI (Python 3.14)
- **Database:** SQLite (Async via SQLAlchemy & aiosqlite)

---

## Verified Endpoints & Functionality

### 1. Health Check
- **Endpoint:** `GET /health`
- **Status:** `200 OK`
- **Output:** `{"status": "ok", "service": "Widget Platform API"}`

### 2. Lead Submission & Anti-Spam
- **Endpoint:** `POST /api/v1/submissions`
- **Features Tested:**
  - Pydantic validation (Email check via `email-validator`).
  - Honeypot check (Silent rejection on filled hidden fields).
  - Client IP extraction & Geo-IP fallback execution.
  - Asynchronous SQLite record persistence.
  - Rate Limiting (`10 requests/minute` enforced via `slowapi`, returning `429` on exceed).

### 3. Background Tasks & Webhooks
- **Service:** `app/services/webhook_service.py`
- **Execution:** Dispatches non-blocking POST payloads to external endpoints upon valid submission without degrading HTTP response latency.

### 4. Widget Config & Embed Script Delivery
- **Config Endpoint:** `GET /api/v1/widgets/{widget_id}/config`
- **Embed JS Endpoint:** `GET /api/v1/widgets/{widget_id}/embed.js`
- **Status:** Dynamically generates valid JavaScript and JSON configurations for cross-origin integration.

---

## Test Verification Output
```bash
# Health check response
curl -X GET "[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)"

# Widget config response
curl -X GET "[http://127.0.0.1:8000/api/v1/widgets/demo-123/config](http://127.0.0.1:8000/api/v1/widgets/demo-123/config)"