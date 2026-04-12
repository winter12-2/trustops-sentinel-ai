import json
import hashlib
from datetime import datetime

from algosdk.v2client import algod
from algosdk import mnemonic, transaction

from app.config import settings


class AlgorandService:

    def __init__(self):
        self.algod_address = settings.algorand_algod_address
        self.algod_token = settings.algorand_algod_token
        self.address = settings.algorand_address
        self.mnemonic_phrase = settings.algorand_mnemonic

        self.client = algod.AlgodClient(self.algod_token, self.algod_address)

    def is_configured(self):
        return bool(self.address and self.mnemonic_phrase)

    def get_balance(self):
        try:
            account_info = self.client.account_info(self.address)
            balance = account_info['amount'] / 1e6
            return {
                "success": True,
                "balance": balance
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_hash(self, payload):
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()

    def send_proof(self, payload):
        """
        Sends proof to Algorand blockchain
        """

        if not self.is_configured():
            return {
                "success": False,
                "error": "Algorand not configured"
            }

        try:
            private_key = mnemonic.to_private_key(self.mnemonic_phrase)

            # Step 1 — Create hash
            decision_hash = self.create_hash(payload)

            # Step 2 — Create note payload
            note_data = {
                "app": "TrustOps",
                "hash": decision_hash,
                "decision": payload.get("decision"),
                "risk_score": payload.get("risk_score"),
                "ts": datetime.utcnow().isoformat()
            }

            note_bytes = json.dumps(note_data).encode()

            # Step 3 — Suggested params
            params = self.client.suggested_params()

            # Step 4 — Create transaction (self send)
            txn = transaction.PaymentTxn(
                sender=self.address,
                sp=params,
                receiver=self.address,
                amt=0,
                note=note_bytes
            )

            # Step 5 — Sign & send
            signed_txn = txn.sign(private_key)
            tx_id = self.client.send_transaction(signed_txn)

            return {
                "success": True,
                "tx_id": tx_id,
                "hash": decision_hash,
                "note": note_data
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


algorand_service = AlgorandService()

