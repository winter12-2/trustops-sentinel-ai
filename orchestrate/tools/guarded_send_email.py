import requests
from typing import List, Dict, Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def guarded_send_email(
    action_type: str,
    user_role: str,
    recipients: List[str],
    subject: str,
    content: str,
    attachments: List[str],
    contains_pii: bool,
    is_external: bool,
    claim_requires_verification: bool,
) -> Dict[str, Any]:
    """
    Evaluates a potentially sensitive outbound action before execution.
    Calls the TrustOps Sentinel AI backend and returns a structured decision.
    """

    payload = {
        "action_type": action_type,
        "user_role": user_role,
        "recipients": recipients,
        "subject": subject,
        "content": content,
        "attachments": attachments,
        "contains_pii": contains_pii,
        "is_external": is_external,
        "claim_requires_verification": claim_requires_verification,
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/evaluate-action",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to evaluate action: {str(e)}",
        }

    decision = result.get("decision")

    if decision == "BLOCK":
        return {
            "status": "blocked",
            "message": "Action blocked before execution.",
            "decision": result,
        }

    if decision == "REQUIRE_APPROVAL":
        return {
            "status": "approval_required",
            "message": "Action requires approval before execution.",
            "decision": result,
        }

    if decision == "ALLOW_WITH_REDACTION":
        return {
            "status": "allowed_with_redaction",
            "message": "Action can proceed only after applying the safe transform.",
            "decision": result,
        }

    return {
        "status": "allowed",
        "message": "Action allowed.",
        "decision": result,
    }