import asyncio
from typing import List, Dict, Any
from schemas import Document, ScoutOutput
from agents.sources_gcc import fetch_listings, pick_comps
from agents.econ import fetch_macro

class MarketScout:
    async def run(self, data_room_url: str, region: str, filters: Dict[str, Any]) -> ScoutOutput:
        await asyncio.sleep(0.05)
        docs: List[Document] = [
            Document(url=f"{data_room_url}/OM.pdf", type="pdf", title="Offering Memorandum"),
            Document(url=f"{data_room_url}/RentRoll.xlsx", type="xlsx", title="Rent Roll"),
            Document(url=f"{data_room_url}/T12.xlsx", type="xlsx", title="T-12"),
        ]
        listings = await fetch_listings(region=region, filters=filters)
        comps = pick_comps(listings)
        macro = await fetch_macro(region)
        return ScoutOutput(documents=docs, comps=comps, listings=listings, macro=macro, market_notes=f"{region} listings={len(listings)}")
