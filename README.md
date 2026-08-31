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
                        +---------------------+---------------------+
                        |                                           |
             [Validation & CORS]                   [Rate Limiter & Honeypot]
                        |                                           |
                        +---------------------+---------------------+
                                              |
                                   [Geo Enrichment Fallback]
                            (Provider A -> Provider B -> Fail-Safe)
                                              |
                                   [DB Persistence & Dashboard]
                                              |
                                  [Async Side Effects (Webhook)]

---

## 2. API Endpoints

- `GET /health` - Service health status check.
- `POST /api/v1/submissions` - Lead submission processing with rate limiting, honeypot protection, and geo-enrichment.
- `GET /api/v1/widgets/{widget_id}/config` - Fetches widget JSON structure and custom field settings.
- `GET /api/v1/widgets/{widget_id}/embed.js` - Serves standalone JavaScript loader script for external embedding.

---

## 3. Database & Data Models

### Submissions Table
- `id`: String(36) (Primary Key)
- `widget_id`: String(36) (Indexed)
- `email`: String(255)
- `name`: String(100)
- `data`: JSON
- `ip_address`: String(45)
- `geo_country`: String(100)
- `geo_city`: String(100)
- `created_at`: DateTime

### Widgets Table
- `id`: String(36) (Primary Key)
- `tenant_id`: String(36) (Indexed)
- `title`: String(255)
- `description`: Text
- `button_text`: String(100)
- `form_fields`: JSON
- `created_at`: DateTime

---

## 4. Setup & Running Instructions

```bash
# 1. Clone repository & initialize virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run API server
uvicorn app.main:app --reload --port 8000