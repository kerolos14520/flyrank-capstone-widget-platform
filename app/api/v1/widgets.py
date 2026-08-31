from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.widget import Widget
from app.schemas.widget import WidgetConfigResponse

router = APIRouter(prefix="/api/v1/widgets", tags=["Widgets"])

@router.get("/{widget_id}/config", response_model=WidgetConfigResponse)
async def get_widget_config(widget_id: str, db: AsyncSession = Depends(get_db)):
    """
    Returns JSON configuration settings used by the client-side widget loader.
    """
    result = await db.execute(select(Widget).where(Widget.id == widget_id))
    widget = result.scalars().first()

    if not widget:
        # Return fallback configuration for test / demo widget IDs
        return WidgetConfigResponse(
            id=widget_id,
            tenant_id="demo-tenant-123",
            title="Subscribe to Newsletter",
            description="Join our newsletter to receive weekly tech updates.",
            button_text="Subscribe Now",
            form_fields=[
                {"name": "email", "type": "email", "required": True, "label": "Email Address"},
                {"name": "name", "type": "text", "required": False, "label": "Full Name"}
            ]
        )

    return widget

@router.get("/{widget_id}/embed.js")
async def get_embed_script(widget_id: str):
    """
    Serves a dynamically generated standalone JavaScript loader tag for external embedding.
    """
    js_code = f"""
(function() {{
    const widgetId = "{widget_id}";
    const apiBase = window.location.origin;

    console.log("[Widget Loader] Initializing widget ID:", widgetId);

    // Fetch configuration
    fetch(`${{apiBase}}/api/v1/widgets/${{widgetId}}/config`)
        .then(res => res.json())
        .then(config => {{
            const container = document.getElementById("widget-container-" + widgetId);
            if (!container) return;

            container.innerHTML = `
                <div style="border:1px solid #ccc; padding:16px; border-radius:8px; max-width:400px; font-family:sans-serif;">
                    <h3>${{config.title}}</h3>
                    <p>${{config.description || ''}}</p>
                    <form id="widget-form-${{widgetId}}">
                        <input type="email" id="email" placeholder="Your Email" required style="width:100%; margin-bottom:8px; padding:8px; box-sizing:border-box;" />
                        <!-- Honeypot anti-spam field -->
                        <input type="text" name="website" style="display:none !important;" tabindex="-1" autocomplete="off" />
                        <button type="submit" style="width:100%; padding:10px; background:#007bff; color:#fff; border:none; border-radius:4px;">
                            ${{config.button_text}}
                        </button>
                    </form>
                </div>
            `;

            document.getElementById("widget-form-" + widgetId).addEventListener("submit", function(e) {{
                e.preventDefault();
                const email = document.getElementById("email").value;
                
                fetch(`${{apiBase}}/api/v1/submissions`, {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{
                        widget_id: widgetId,
                        email: email
                    }})
                }})
                .then(r => r.json())
                .then(data => alert("Submitted successfully! Submission ID: " + data.submission_id));
            }});
        }});
}})();
    """
    return Response(content=js_code, media_type="application/javascript")