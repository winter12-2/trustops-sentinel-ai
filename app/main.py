from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.models.action_model import ActionRequest
from app.services.redis_service import redis_service
from app.services.tavily_service import tavily_service
from app.services.mysql_service import (
    get_action_logs,
    get_incidents,
    insert_action_log,
    insert_incident,
)
from app.services.policy_engine import evaluate_action
from app.services.algorand_service import algorand_service


app = FastAPI(title=settings.app_name)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse(
        {
            "status": "ok",
            "app": settings.app_name,
        }
    )


@app.get("/redis-test")
def redis_test() -> JSONResponse:
    sample_payload = {
        "project": settings.app_name,
        "layer": "memory",
        "status": "connected",
    }

    redis_service.set_value("test:string", "TrustOps AI")
    redis_service.set_json("test:json", sample_payload)

    return JSONResponse(
        {
            "redis_working": redis_service.ping(),
            "string_value": redis_service.get_value("test:string"),
            "json_value": redis_service.get_json("test:json"),
        }
    )


@app.get("/tavily-test")
def tavily_test(q: str = "latest Redis enterprise AI security news") -> JSONResponse:
    result = tavily_service.search(query=q, max_results=3)
    return JSONResponse(result)


@app.get("/add-incident")
def add_incident():
    insert_incident(
        title="Test Incident",
        description="Redis + Tavily working",
        severity="Low",
    )
    return {"status": "inserted"}


@app.get("/incidents")
def list_incidents():
    return get_incidents()


@app.post("/evaluate-action")
def evaluate_action_endpoint(action: ActionRequest):
    result = evaluate_action(action)

    # Redis logging
    redis_service.push_event(
        "stream:actions",
        {
            "action_type": action.action_type,
            "user_role": action.user_role,
            "decision": result.decision,
            "threat_level": result.threat_level,
            "risk_score": str(result.risk_score),
        },
    )

    # MySQL logging (unchanged)
    insert_action_log(action, result)

    # Algorand proof (kept completely separate from MySQL)
    blockchain_payload = {
        "action_type": action.action_type,
        "user_role": action.user_role,
        "recipients": action.recipients,
        "subject": action.subject,
        "decision": result.decision,
        "threat_level": result.threat_level,
        "risk_score": result.risk_score,
        "reasons": result.reasons,
    }

    blockchain_result = algorand_service.send_proof(blockchain_payload)

    response = result.model_dump()
    response["blockchain"] = blockchain_result

    return response


@app.get("/action-logs")
def action_logs():
    return get_action_logs()


@app.get("/algorand-health")
def algorand_health():
    return {
        "configured": algorand_service.is_configured(),
        "address": settings.algorand_address,
        "algod_address": settings.algorand_algod_address,
    }


@app.get("/algorand-balance")
def algorand_balance():
    return algorand_service.get_balance()

