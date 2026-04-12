from app.models.action_model import ActionRequest
from app.models.decision_model import DecisionResponse
from app.services.risk_scoring import compute_risk_score
from app.services.tavily_service import tavily_service
from app.sentinel.decision_mapper import map_score_to_threat_level
from app.sentinel.safe_transformer import build_safe_transform


def evaluate_action(action: ActionRequest) -> DecisionResponse:
    score, reasons = compute_risk_score(action)

    live_verification = None

    if action.claim_requires_verification and action.content.strip():
        live_verification = tavily_service.verify_claim(action.content)

        if not live_verification.get("verified", False):
            reasons.append("Live verification did not confirm the claim.")
            score += 15
        else:
            reasons.append("Claim checked against live external sources.")
            score -= 10

    if score < 0:
        score = 0

    threat_level = map_score_to_threat_level(score)

    safe_transform = None

    if score < 30:
        decision = "ALLOW"
    elif score <= 60:
        decision = "ALLOW_WITH_REDACTION"
        safe_transform = build_safe_transform(action, reasons)
    elif score < 80:
        decision = "REQUIRE_APPROVAL"
        safe_transform = build_safe_transform(action, reasons)
    else:
        decision = "BLOCK"
        safe_transform = build_safe_transform(action, reasons)

    if not reasons:
        reasons.append("No policy violations detected.")

    return DecisionResponse(
        decision=decision,
        threat_level=threat_level,
        risk_score=score,
        reasons=reasons,
        safe_transform=safe_transform,
        live_verification=live_verification,
    )

# from app.models.action_model import ActionRequest
# from app.models.decision_model import DecisionResponse
# from app.services.risk_scoring import compute_risk_score
# from app.services.tavily_service import tavily_service
# from app.sentinel.decision_mapper import map_score_to_threat_level
# from app.sentinel.safe_transformer import build_safe_transform


# def evaluate_action(action: ActionRequest) -> DecisionResponse:
#     score, reasons = compute_risk_score(action)

#     live_verification = None

#     if action.claim_requires_verification and action.content.strip():
#         live_verification = tavily_service.verify_claim(action.content)

#         if not live_verification.get("verified", False):
#             reasons.append("Live verification did not confirm the claim.")
#             score += 15
#         else:
#             reasons.append("Claim checked against live external sources.")

#     threat_level = map_score_to_threat_level(score)

#     safe_transform = None

#     if score < 30:
#         decision = "ALLOW"
#     elif score <= 60:
#         decision = "ALLOW_WITH_REDACTION"
#         safe_transform = build_safe_transform(action, reasons)
#     elif score < 80:
#         decision = "REQUIRE_APPROVAL"
#         safe_transform = build_safe_transform(action, reasons)
#     else:
#         decision = "BLOCK"
#         safe_transform = build_safe_transform(action, reasons)

#     if not reasons:
#         reasons.append("No policy violations detected.")

#     return DecisionResponse(
#         decision=decision,
#         threat_level=threat_level,
#         risk_score=score,
#         reasons=reasons,
#         safe_transform=safe_transform,
#         live_verification=live_verification,
#     )

# from app.models.action_model import ActionRequest
# from app.models.decision_model import DecisionResponse
# from app.services.risk_scoring import compute_risk_score


# def evaluate_action(action: ActionRequest) -> DecisionResponse:
#     score, reasons = compute_risk_score(action)

#     safe_transform = None

#     if score < 30:
#         decision = "ALLOW"
#     elif score < 60:
#         decision = "ALLOW_WITH_REDACTION"
#         safe_transform = {
#             "remove_attachments": action.attachments,
#             "note": "Proceed only after removing risky attachments or sensitive content."
#         }
#     elif score < 80:
#         decision = "REQUIRE_APPROVAL"
#     else:
#         decision = "BLOCK"

#     if not reasons:
#         reasons.append("No policy violations detected.")

#     return DecisionResponse(
#         decision=decision,
#         risk_score=score,
#         reasons=reasons,
#         safe_transform=safe_transform,
#     )

