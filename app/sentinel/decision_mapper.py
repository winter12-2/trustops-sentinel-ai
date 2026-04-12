def map_score_to_threat_level(score: int) -> str:
    if score < 30:
        return "ALLOW"
    elif score < 60:
        return "MONITOR"
    elif score < 80:
        return "QUARANTINE"
    return "ESCALATE"