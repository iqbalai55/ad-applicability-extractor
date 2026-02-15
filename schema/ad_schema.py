from typing import List, Optional
from pydantic import BaseModel

class ApplicabilityRules(BaseModel):
    aircraft_models: List[str]
    msn_constraints: Optional[List[str]] = None
    excluded_if_modifications: List[str] = []
    required_modifications: List[str] = []

class ADModel(BaseModel):
    ad_id: str
    applicability_rules: ApplicabilityRules
