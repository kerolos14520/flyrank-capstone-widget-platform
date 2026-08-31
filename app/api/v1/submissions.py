from fastapi import APIRouter, status, Request, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.services.geo_service import resolve_ip_location
from app.services.webhook_service import send_webhook_notification
from app.core.database import get_db
from app.models.submission import Submission
from app.core.limiter import limiter
import uuid

router = APIRouter(prefix="/api/v1/submissions", tags=["Submissions"])

@router.post("", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_submission(
    request: Request,
    payload: SubmissionCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # 1. Anti-Spam Honeypot Check
    if payload.website_hp:
        return SubmissionResponse(
            status="success",
            submission_id=str(uuid.uuid4()),
            message="Submission received successfully"
        )
    
    # 2. Extract Client IP
    client_ip = request.client.host if request.client else "127.0.0.1"
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()

    # 3. Geo-Enrichment Fallback Execution
    geo_data = await resolve_ip_location(client_ip)
    
    # 4. Save Record to Database
    new_submission = Submission(
        widget_id=payload.widget_id,
        email=payload.email,
        name=payload.name,
        data=payload.data,
        ip_address=client_ip,
        geo_country=geo_data.get("country"),
        geo_city=geo_data.get("city")
    )
    
    db.add(new_submission)
    await db.commit()
    await db.refresh(new_submission)

    # 5. Dispatch Non-Blocking Background Webhook Task
    webhook_payload = {
        "event": "submission.created",
        "submission_id": new_submission.id,
        "widget_id": new_submission.widget_id,
        "email": new_submission.email,
        "location": f"{new_submission.geo_city}, {new_submission.geo_country}"
    }
    
    # Test webhook endpoint (HTTPBin echoes POST requests)
    target_webhook = "https://httpbin.org/post"
    background_tasks.add_task(send_webhook_notification, target_webhook, webhook_payload)

    return SubmissionResponse(
        status="success",
        submission_id=new_submission.id,
        message="Submission accepted and background notification scheduled"
    )