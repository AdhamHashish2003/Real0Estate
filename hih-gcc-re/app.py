from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator import Orchestrator
from storage import Store
from typing import Optional

orchestrator = Orchestrator()
store = Store()

class AnalyzeReq(BaseModel):
    deal_id: str
    data_room_url: str
    region: str  # "dubai" | "abudhabi" | "ksa"
    filters: dict | None = None
    notes: Optional[str] = None

class StatusResp(BaseModel):
    deal_id: str
    state: str
    artifacts: dict

def make_app() -> FastAPI:
    app = FastAPI(title="Hashish Investment Holding — GCC RE Intelligence")

    @app.post("/analyze")
    async def analyze(req: AnalyzeReq):
        if store.exists(req.deal_id):
            raise HTTPException(409, "deal_id already exists")
        store.init_deal(req.deal_id)
        await orchestrator.enqueue_job(
            deal_id=req.deal_id,
            data_room_url=req.data_room_url,
            region=req.region,
            filters=req.filters or {},
            notes=req.notes,
        )
        return {"ok": True, "deal_id": req.deal_id}

    @app.get("/status/{deal_id}", response_model=StatusResp)
    async def status(deal_id: str):
        s = store.get_status(deal_id)
        if not s:
            raise HTTPException(404, "unknown deal_id")
        return StatusResp(**s)

    return app
