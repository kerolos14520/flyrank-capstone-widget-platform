# Embeddable Widget & Lead-Capture Platform

## 1. Executive Summary & Architecture Overview
An enterprise-ready platform enabling tenants to create embeddable lead-capture widgets via script tags on external websites. Incoming submissions are validated, rate-limited, enriched with IP geolocation fallback chains, and stored securely.

### Component Flow Architecture
[Widget Owner] ---> (Auth API) ---> [Database & Tenant Management]
|
[External Website] <-- (GET Config & JS) -----+
|
[Visitor Submission] ---> (POST /api/v1/submissions)
|
+-----------+-----------+
|                       |
[Validation & CORS]    [Rate Limiter & Honeypot]
|                       |
+-----------+-----------+
|
[Geo Enrichment Fallback]
(Provider A -> Provider B -> Fail-Safe)
|
[DB Persistence & Dashboard]
|
[Async Side Effects (Mail/Webhook)]


---

## 2. Database & Data Models

### Tenants Table
- `id`: UUID (Primary Key)
- `email`: VARCHAR(255) (Unique)
- `password_hash`: VARCHAR(255)
- `created_at`: TIMESTAMP

### Widgets Table
- `id`: UUID (Primary Key)
- `tenant_id`: UUID (Foreign Key -> Tenants.id)
- `type`: VARCHAR(50)
- `title`: VARCHAR(255)
- `description`: TEXT
- `form_fields`: JSONB
- `button_text`: VARCHAR(100)
- `created_at`: TIMESTAMP

### Submissions Table
- `id`: UUID (Primary Key)
- `widget_id`: UUID (Foreign Key -> Widgets.id)
- `tenant_id`: UUID (Foreign Key -> Tenants.id)
- `payload`: JSONB
- `ip_address`: VARCHAR(45)
- `geo_country`: VARCHAR(100) (Nullable)
- `geo_city`: VARCHAR(100) (Nullable)
- `created_at`: TIMESTAMP

---

## 3. Explicit Non-Goals
- No custom CDN configuration or domain registration.
- No visual drag-and-drop widget page builder.
- No live production SMTP delivery (mocked/logged safely via Mailpit/Console).

---

## 4. Setup & Running Instructions
```bash
# 1. Clone repository & initialize virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run API server
uvicorn app.main:app --reload --port 8000