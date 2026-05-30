from pydantic import BaseModel, Field
from typing import List


class CompanyCreate(BaseModel):

    website_name: str = ""

    website_url: str

    company_name: str = ""

    address: str = ""

    mobile_number: str = ""

    mail: List[str] = []

    core_service: str = ""

    target_customer: str = ""

    probable_pain_point: str = ""

    outreach_opener: str = ""


class CompanyResponse(BaseModel):

    id: int

    website_name: str

    website_url: str

    company_name: str

    address: str

    mobile_number: str

    mail: List[str]

    core_service: str

    target_customer: str

    probable_pain_point: str

    outreach_opener: str

    class Config:
        from_attributes = True


class EnrichRequest(BaseModel):

    website_name: str = Field(
        ...,
        description="User supplied website name"
    )

    website_url: str = Field(
        ...,
        description="Company URL"
    )