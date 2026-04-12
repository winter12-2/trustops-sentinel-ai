from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# class DecisionResponse(BaseModel):
#     decision: str = Field(..., examples=["ALLOW", "ALLOW_WITH_REDACTION", "REQUIRE_APPROVAL", "BLOCK"])
#     risk_score: int
#     reasons: List[str]
#     safe_transform: Optional[Dict[str, Any]] = None




class DecisionResponse(BaseModel):
    decision: str = Field(..., examples=["ALLOW", "ALLOW_WITH_REDACTION", "REQUIRE_APPROVAL", "BLOCK"])
    threat_level: str = Field(..., examples=["ALLOW", "MONITOR", "QUARANTINE", "ESCALATE"])
    risk_score: int
    reasons: List[str]
    safe_transform: Optional[Dict[str, Any]] = None
    live_verification: Optional[Dict[str, Any]] = None