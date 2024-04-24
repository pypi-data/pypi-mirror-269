"""SQLAlchemy models for NHSBT"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, MetaData, Boolean

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class UKTPatient(Base):
    __tablename__ = "ukt_patients"

    uktssa_no = Column(Integer, primary_key=True, autoincrement=False)
    surname = Column(String(50))
    forename = Column(String(50))
    sex = Column(String(1))
    post_code = Column(String(10))
    new_nhs_no = Column(Integer)
    chi_no = Column(Integer)
    hsc_no = Column(Integer)
    rr_no = Column(Integer)
    ukt_date_death = Column(DateTime)
    ukt_date_birth = Column(DateTime)


class UKTTransplant(Base):
    __tablename__ = "ukt_transplants"

    registration_id = Column(String(12), primary_key=True)
    uktssa_no = Column(Integer)
    transplant_id = Column(Integer)
    transplant_type = Column(String(10))
    transplant_organ = Column(String(50))
    transplant_unit = Column(String(50))
    rr_no = Column(Integer)
    transplant_date = Column(DateTime)
    ukt_fail_date = Column(DateTime)
    registration_date = Column(DateTime)
    registration_date_type = Column(String(12))
    registration_end_date = Column(DateTime)
    registration_end_status = Column(String(12))
    transplant_consideration = Column(String(20))
    transplant_dialysis = Column(String(12))
    transplant_relationship = Column(String(20))
    transplant_sex = Column(String(12))
    cause_of_failure = Column(String(10))
    cause_of_failure_text = Column(String(500))
    cit_mins = Column(String(10))
    hla_mismatch = Column(String(10))
    ukt_suspension = Column(Boolean)
