from pydantic import BaseModel, Field
from typing import List


class ActionRequest(BaseModel):
    action_type: str = Field(..., examples=["send_email"])
    user_role: str = Field(default="employee")
    recipients: List[str] = Field(default_factory=list)
    subject: str = ""
    content: str = ""
    attachments: List[str] = Field(default_factory=list)
    contains_pii: bool = False
    is_external: bool = False
    claim_requires_verification: bool = False
