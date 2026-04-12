import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.algorand_service import algorand_service

result = algorand_service.get_balance()
print(result)
