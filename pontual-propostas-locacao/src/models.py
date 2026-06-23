from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Any


@dataclass
class PropertyData:
    lease_type: str
    address: str
    proposed_rent: str
    residents_count: int
    fees_notes: str = ""


@dataclass
class PersonalReference:
    name: str
    phone: str


@dataclass
class OwnedProperty:
    address: str
    iptu_registration: str


@dataclass
class VehicleData:
    vehicle_type: str
    model_year: str
    plate: str


@dataclass
class ApplicantData:
    full_name: str
    birth_date: date
    profession: str
    rg_info: str
    cpf: str
    phone: str
    email: str
    marital_status: str
    sex: str
    nationality: str
    father_name: str
    mother_name: str
    spouse_name: str
    spouse_cpf: str
    work_card: str
    current_address: str
    previous_address: str
    years_current_address: str
    years_previous_address: str
    residence_status: str
    landlord_contact: str
    company_name: str
    company_address: str
    company_phone: str
    department: str
    employment_time: str
    monthly_income: str
    occupation_type: str
    company_participation: str
    state_registration: str
    other_income: str
    extra_income: str
    other_residents: str
    pets: str
    has_properties: bool
    properties: list[OwnedProperty]
    has_vehicles: bool
    vehicles: list[VehicleData]
    references: list[PersonalReference]


@dataclass
class GuarantorData:
    full_name: str
    birth_date: date
    rg_info: str
    cpf: str
    sex: str
    marital_status: str
    nationality: str
    father_name: str
    mother_name: str
    work_card: str
    spouse_details: str
    current_address: str
    residence_status: str
    company_details: str
    profession: str
    employment_time: str
    monthly_income: str
    other_income: str
    occupation_type: str
    properties: str
    vehicles: str
    references: str


@dataclass
class DeliveryData:
    preferred_channel: str
    destination: str


@dataclass
class UploadedDocument:
    label: str
    filename: str
    saved_path: str
    size_bytes: int


@dataclass
class ProposalSubmission:
    property_data: PropertyData
    applicant_data: ApplicantData
    delivery_data: DeliveryData
    guarantor_data: GuarantorData | None = None
    documents: list[UploadedDocument] = field(default_factory=list)
    protocol: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    pdf_path: str | None = None
    package_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["created_at"] = self.created_at.isoformat()
        payload["applicant_data"]["birth_date"] = self.applicant_data.birth_date.isoformat()
        if self.guarantor_data:
            payload["guarantor_data"]["birth_date"] = self.guarantor_data.birth_date.isoformat()
        return payload
