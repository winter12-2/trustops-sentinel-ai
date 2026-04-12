import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.algorand_service import algorand_service

payload = {
    "decision": "BLOCK",
    "risk_score": 85,
    "reason": "Test transaction"
}

result = algorand_service.send_proof(payload)

print(result)

