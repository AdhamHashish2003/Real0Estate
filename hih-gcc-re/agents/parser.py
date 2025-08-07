import asyncio
from typing import List
from schemas import Document, ParserOutput, LineItem

class DocParser:
    async def run(self, documents: List[Document], region: str) -> ParserOutput:
        await asyncio.sleep(0.05)
        assumptions = [
            LineItem(key="VacancyRate", value=0.05, source="OM.pdf p.7"),
            LineItem(key="ExpenseRatio", value=0.35, source="T12.xlsx"),
            LineItem(key="RentGrowth", value=0.02, source="OM.pdf p.12"),
        ]
        rent_roll = [
            {"unit": "1A", "rent": 6500 if region in ("dubai","abudhabi") else 5000, "sqft": 700},
            {"unit": "1B", "rent": 6800 if region in ("dubai","abudhabi") else 5200, "sqft": 720},
        ]
        t12 = [
            {"month": "2025-05", "income": 133000, "opex": 46000},
            {"month": "2025-06", "income": 134000, "opex": 46250},
            {"month": "2025-07", "income": 135000, "opex": 46500},
        ]
        return ParserOutput(rent_roll=rent_roll, t12=t12, assumptions=assumptions)
