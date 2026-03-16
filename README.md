# 📧 Email Classification Service

An AI-powered REST API that automatically classifies incoming customer emails into structured categories — built for Elliott Tool Technologies' **Project Spark** initiative.

## Overview

The service accepts three inputs (sender, subject, body) and returns a structured JSON response with category, priority, confidence score, suggested action, and a one-sentence summary. Designed to be called by internal tooling (Sales Email Parser) with zero integration overhead on the contractor side.

```
POST /classify
{
  "sender": "john.doe@acme.com",
  "subject": "Order #12345 still hasn't arrived",
  "body": "Hi, I placed an order 10 days ago..."
}
```

```json
{
  "category": "ORDER_STATUS",
  "subcategory": "Shipping Delay",
  "priority": "HIGH",
  "confidence": 0.95,
  "suggested_action": "Check order tracking and reply with updated ETA",
  "summary": "Customer inquiring about delayed order #12345"
}
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| AI Model | Claude 3.5 Haiku (Anthropic) |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Testing | Pytest |

---

## Categories

| Category | Description |
|---|---|
| `ORDER_STATUS` | Tracking, shipping, delivery inquiries |
| `RETURNS_REFUNDS` | Return/refund/exchange requests |
| `PRODUCT_INQUIRY` | Specs, availability, compatibility questions |
| `COMPLAINT` | Negative feedback, service complaints |
| `BILLING_PAYMENT` | Invoice issues, payment disputes |
| `TECHNICAL_SUPPORT` | Troubleshooting, defect reports |
| `SALES_LEAD` | New business, bulk orders, partnerships |
| `SPAM_IRRELEVANT` | Spam and off-topic messages |
| `OTHER` | Catch-all for unclassified emails |

---

## Getting Started

### 1. Clone & Install

```bash
git clone https://github.com/elifkapusizoglu/email-classification-service.git
cd email-classification-service
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run

```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Test

```bash
pytest tests/ -v
```

---

## API Reference

### `POST /classify`

Classify a single email.

**Request Body:**

```json
{
  "sender": "string (required)",
  "subject": "string (required)",
  "body": "string (required)"
}
```

**Response:**

```json
{
  "category": "ORDER_STATUS",
  "subcategory": "Shipping Delay",
  "priority": "HIGH",
  "confidence": 0.95,
  "suggested_action": "Check order tracking system and provide ETA",
  "summary": "Customer asking about delayed shipment for order #12345"
}
```

**Priority Levels:**

| Priority | SLA |
|---|---|
| `URGENT` | Same-day response |
| `HIGH` | Within 4 hours |
| `MEDIUM` | Within 24 hours |
| `LOW` | Within 48–72 hours |

### `GET /health`

Returns service health status.

### Interactive Docs

Visit `http://localhost:8000/docs` for the full Swagger UI.

---

## Project Structure

```
email-classification-service/
├── app/
│   └── main.py          # FastAPI app, schemas, classification logic
├── tests/
│   └── test_main.py     # Unit & integration tests
├── .env.example         # Environment variable template
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Author

**Elif Kapusüzoğlu** — Computer Vision & AI Engineer  
[GitHub](https://github.com/elifkapusizoglu) · [Upwork](https://www.upwork.com)
