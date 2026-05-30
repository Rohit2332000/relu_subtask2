import json

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import (
    engine,
    Base,
    get_db
)

from models import Company

from schemas import (
    EnrichRequest
)

from scraper import (
    scrape_company
)

from llm import (
    enrich_company
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Company Enrichment API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "Company Enrichment API Running"
    }


@app.post("/enrich")
def enrich_company_endpoint(
    request: EnrichRequest,
    db: Session = Depends(get_db)
):

    try:

        scraped_data = scrape_company(
            request.website_url
        )

        enriched = enrich_company(
            website_url=request.website_url,
            content=scraped_data["content"],
            emails=scraped_data["emails"],
            phones=scraped_data["phones"]
        )

        company = Company(
            website_name=request.website_name,
            website_url=request.website_url,
            company_name=enriched.get(
                "company_name",
                ""
            ),
            address=enriched.get(
                "address",
                ""
            ),
            mobile_number=enriched.get(
                "mobile_number",
                ""
            ),
            mail=json.dumps(
                enriched.get(
                    "mail",
                    []
                )
            ),
            core_service=enriched.get(
                "core_service",
                ""
            ),
            target_customer=enriched.get(
                "target_customer",
                ""
            ),
            probable_pain_point=enriched.get(
                "probable_pain_point",
                ""
            ),
            outreach_opener=enriched.get(
                "outreach_opener",
                ""
            )
        )

        db.add(company)
        db.commit()
        db.refresh(company)

        return {
            "id": company.id,
            "website_name": company.website_name,
            "website_url": company.website_url,
            "company_name": company.company_name,
            "address": company.address,
            "mobile_number": company.mobile_number,
            "mail": json.loads(
                company.mail
            ),
            "core_service": company.core_service,
            "target_customer": company.target_customer,
            "probable_pain_point":
                company.probable_pain_point,
            "outreach_opener":
                company.outreach_opener
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/results")
def get_results(
    db: Session = Depends(get_db)
):

    companies = db.query(
        Company
    ).all()

    results = []

    for company in companies:

        results.append(
            {
                "id": company.id,
                "website_name":
                    company.website_name,
                "website_url":
                    company.website_url,
                "company_name":
                    company.company_name,
                "address":
                    company.address,
                "mobile_number":
                    company.mobile_number,
                "mail":
                    json.loads(
                        company.mail
                    )
                    if company.mail
                    else [],
                "core_service":
                    company.core_service,
                "target_customer":
                    company.target_customer,
                "probable_pain_point":
                    company.probable_pain_point,
                "outreach_opener":
                    company.outreach_opener
            }
        )

    return results


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }