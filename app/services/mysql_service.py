import mysql.connector
import json
from app.config import settings
from app.models.action_model import ActionRequest
from app.models.decision_model import DecisionResponse

def get_connection():
    return mysql.connector.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database
    )


def insert_incident(title: str, description: str, severity: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO incidents (title, description, severity)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (title, description, severity))
    conn.commit()

    cursor.close()
    conn.close()


def get_incidents():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM incidents")
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

# def insert_action_log(action: ActionRequest, decision: DecisionResponse):
#     conn = get_connection()
#     cursor = conn.cursor()

#     query = """
#     INSERT INTO actions (
#         action_type, user_role, recipients, subject, content, attachments,
#         contains_pii, is_external, claim_requires_verification,
#         decision, risk_score, reasons
#     )
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """

#     values = (
#         action.action_type,
#         action.user_role,
#         json.dumps(action.recipients),
#         action.subject,
#         action.content,
#         json.dumps(action.attachments),
#         action.contains_pii,
#         action.is_external,
#         action.claim_requires_verification,
#         decision.decision,
#         decision.risk_score,
#         json.dumps(decision.reasons),
#     )

#     cursor.execute(query, values)
#     conn.commit()

#     cursor.close()
#     conn.close()

def insert_action_log(action: ActionRequest, decision: DecisionResponse):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO actions (
        action_type, user_role, recipients, subject, content, attachments,
        contains_pii, is_external, claim_requires_verification,
        decision, threat_level, risk_score, reasons, live_verification, safe_transform
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        action.action_type,
        action.user_role,
        json.dumps(action.recipients),
        action.subject,
        action.content,
        json.dumps(action.attachments),
        action.contains_pii,
        action.is_external,
        action.claim_requires_verification,
        decision.decision,
        decision.threat_level,  # ✅ NEW
        decision.risk_score,
        json.dumps(decision.reasons),
        json.dumps(decision.live_verification),  # ✅ NEW
        json.dumps(decision.safe_transform),     # ✅ NEW
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

def get_action_logs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM actions ORDER BY created_at DESC")
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results