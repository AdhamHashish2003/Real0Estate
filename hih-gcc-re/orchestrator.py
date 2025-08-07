import asyncio
from typing import Optional
from schemas import ScoutOutput, ParserOutput, UnderwriteOutput
from agents.scout import MarketScout
from agents.parser import DocParser
from agents.underwriter import Underwriter
from storage import Store

class Orchestrator:
    def __init__(self):
        self.q = asyncio.Queue()
        self.scout = MarketScout()
        self.parser = DocParser()
        self.underwriter = Underwriter()
        self.store = Store()
        self._runner_task: Optional[asyncio.Task] = asyncio.create_task(self._runner())

    async def enqueue_job(self, deal_id: str, data_room_url: str, region: str, filters: dict, notes: Optional[str] = None):
        await self.q.put((deal_id, data_room_url, region.lower(), filters, notes))

    async def _runner(self):
        while True:
            deal_id, data_room_url, region, filters, notes = await self.q.get()
            try:
                self.store.update_status(deal_id, state="SCOUTING")
                scout_out: ScoutOutput = await self.scout.run(data_room_url=data_room_url, region=region, filters=filters)
                self.store.save_artifact(deal_id, "listings", scout_out.listings)
                self.store.save_artifact(deal_id, "comps", [c.model_dump() for c in scout_out.comps])
                self.store.save_artifact(deal_id, "macro", scout_out.macro)

                self.store.update_status(deal_id, state="PARSING")
                parser_out: ParserOutput = await self.parser.run(scout_out.documents, region=region)
                self.store.save_artifact(deal_id, "extracted", parser_out.model_dump())

                self.store.update_status(deal_id, state="UNDERWRITING")
                uw_out: UnderwriteOutput = await self.underwriter.run(parser_out, scout_out)
                self.store.save_artifact(deal_id, "underwrite", uw_out.model_dump())

                self.store.update_status(deal_id, state="DONE")
            except Exception as e:
                self.store.update_status(deal_id, state=f"ERROR: {e}")
