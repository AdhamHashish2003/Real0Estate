import asyncio
from typing import Dict, Any, List
from schemas import Comp

async def fetch_listings(region: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    await asyncio.sleep(0.05)
    if region == "dubai":
        return [
            {"address": "Dubai Marina, Marina Gate 1", "city": "Dubai", "district": "Dubai Marina", "price": 2200000, "currency": "AED", "beds": 2, "baths": 2, "sqft": 1200, "url": "https://example.com/bayut/123", "source": "bayut"},
            {"address": "Business Bay, Executive Towers", "city": "Dubai", "district": "Business Bay", "price": 1800000, "currency": "AED", "beds": 1, "baths": 2, "sqft": 950, "url": "https://example.com/propertyfinder/456", "source": "propertyfinder"},
        ]
    if region == "abudhabi":
        return [
            {"address": "Yas Island, Ansam", "city": "Abu Dhabi", "district": "Yas Island", "price": 1500000, "currency": "AED", "beds": 1, "baths": 2, "sqft": 880, "url": "https://example.com/dubizzle/789", "source": "dubizzle"},
        ]
    return [
        {"address": "Al Olaya, Riyadh", "city": "Riyadh", "district": "Al Olaya", "price": 1200000, "currency": "SAR", "beds": 3, "baths": 3, "sqft": 1600, "url": "https://example.com/aqar/111", "source": "aqar"},
        {"address": "Corniche, Jeddah", "city": "Jeddah", "district": "Corniche", "price": 900000, "currency": "SAR", "beds": 2, "baths": 2, "sqft": 1100, "url": "https://example.com/propertyfinderksa/222", "source": "propertyfinder_ksa"},
    ]

def pick_comps(listings: List[Dict[str, Any]]) -> List[Comp]:
    comps: List[Comp] = []
    for li in listings:
        price = li.get("price")
        sqft = li.get("sqft") or 0
        cap = None
        if price and sqft:
            cap = 0.05
        comps.append(Comp(address=f"{li.get('district')}, {li.get('city')}", rent_annual=None, price=price, cap_rate=cap, source_url=li.get("url")))
    return comps
