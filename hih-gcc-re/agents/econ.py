import asyncio
from typing import Dict

async def fetch_macro(region: str) -> Dict[str, float]:
    await asyncio.sleep(0.02)
    if region in ("dubai", "abudhabi"):
        return {"eibor": 0.054, "inflation": 0.025, "deposit_rate": 0.03, "oil": 82.0}
    return {"saibor": 0.056, "inflation": 0.023, "deposit_rate": 0.032, "oil": 82.0}
