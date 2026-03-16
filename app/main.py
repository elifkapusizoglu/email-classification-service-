"""
Email Classification Service
AI-powered email triage for Elliott Tool Technologies - Project Spark
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import anthropic
import json
import os

app = FastAPI(
    title="Email Classification Service",
    description="AI-powered email classification API for Elliott Tool Technologies (Project Spark)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ── Schemas ──────────────────────────────────────────────────────────────────

class EmailInput(BaseModel):
    sender: str = Field(..., description="Email sender address or name", example="john.doe@example.com")
    subject: str = Field(..., description="Email subject line", example="Urgent: Order #12345 delayed")
    body: str = Field(..., description="Full email body text", example="Hi, my order has not arrived yet...")

class ClassificationResult(BaseModel):
    category: str = Field(..., description="Primary classification category")
    subcategory: Optional[str] = Field(None, description="Optional subcategory for more detail")
    priority: str = Field(..., description="Priority level: LOW | MEDIUM | HIGH | URGENT")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")
    suggested_action: str = Field(..., description="Recommended next step for the CXS team")
    summary: str = Field(..., description="One-sentence summary of the email")

# ── Categories ────────────────────────────────────────────────────────────────

CATEGORIES = """
Available categories:
- ORDER_STATUS: Questions about order tracking, shipping, delivery times
- RETURNS_REFUNDS: Return requests, refund inquiries, exchange requests
- PRODUCT_INQUIRY: Questions about product specs, availability, compatibility
- COMPLAINT: Negative feedback, complaints about products or service
- BILLING_PAYMENT: Invoice issues, payment problems, pricing disputes
- TECHNICAL_SUPPORT: Product usage help, troubleshooting, defect reports
- SALES_LEAD: New business inquiries, bulk orders, partnership requests
- SPAM_IRRELEVANT: Spam, marketing emails, irrelevant messages
- OTHER: Anything that doesn't fit the above categories
"""

# ── Classification Logic ──────────────────────────────────────────────────────

def classify_email(sender: str, subject: str, body: str) -> ClassificationResult:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""You are an email classification assistant for Elliott Tool Technologies, a B2B industrial tools company.
Classify the following incoming customer email into structured data.

{CATEGORIES}

Priority levels:
- URGENT: Requires same-day response (angry customer, legal threat, critical outage)
- HIGH: Respond within 4 hours
- MEDIUM: Respond within 24 hours
- LOW: Respond within 48-72 hours

Email:
Sender: {sender}
Subject: {subject}
Body: {body}

Respond ONLY with a valid JSON object, no markdown, no explanation:
{{
  "category": "...",
  "subcategory": "...",
  "priority": "...",
  "confidence": 0.0,
  "suggested_action": "...",
  "summary": "..."
}}"""

    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    data = json.loads(raw)

    return ClassificationResult(**data)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "Email Classification Service", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

@app.post("/classify", response_model=ClassificationResult, tags=["Classification"])
def classify(email: EmailInput):
    """
    Classify an incoming email into a structured category.

    Accepts sender, subject, and body — returns category, priority,
    confidence score, suggested action, and summary.
    """
    try:
        result = classify_email(email.sender, email.subject, email.body)
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
