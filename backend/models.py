from sqlalchemy import Column, Integer, String, Text
from database import Base


class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    website_name = Column(String, nullable=False)

    company_name = Column(String)

    website_url = Column(String)

    address = Column(Text)

    mobile_number = Column(String)

    mail = Column(Text)

    core_service = Column(Text)

    target_customer = Column(Text)

    probable_pain_point = Column(Text)

    outreach_opener = Column(Text)