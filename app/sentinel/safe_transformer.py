from app.models.action_model import ActionRequest


def build_safe_transform(action: ActionRequest, reasons: list[str]) -> dict:
    transform: dict = {}

    if action.attachments:
        transform["remove_attachments"] = action.attachments

    if action.contains_pii:
        transform["redact_pii"] = True

    if action.claim_requires_verification:
        transform["replace_claims_with"] = "According to publicly verifiable information reviewed at runtime..."

    transform["note"] = "Sensitive or unverified content should be sanitized before proceeding."

    return transform