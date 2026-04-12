from app.models.action_model import ActionRequest


def compute_risk_score(action: ActionRequest) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    if action.is_external and action.attachments:
        score += 50
        reasons.append("External action includes attachment.")

    if action.contains_pii and action.is_external:
        score += 40
        reasons.append("PII detected in externally directed content.")

    if action.claim_requires_verification:
        score += 25
        reasons.append("Content contains a claim that requires live verification.")

    if len(action.recipients) > 25 and action.is_external:
        score += 20
        reasons.append("Bulk external send exceeds threshold.")

    if action.user_role.lower() not in {"manager", "admin"} and action.is_external:
        score += 10
        reasons.append("Non-privileged user attempting external action.")

    return score, reasons