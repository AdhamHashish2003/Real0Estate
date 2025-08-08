from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import fastapi
import requests
from bs4 import BeautifulSoup
class Document(BaseModel):
    url: str
    type: str  # pdf, xlsx, docx, html
    title: Optional[str] = None

class Comp(BaseModel):
    address: str
    unit_mix: Optional[str] = None
    rent_annual: Optional[float] = None
    price: Optional[float] = None
    cap_rate: Optional[float] = None
    source_url: Optional[str] = None

class ScoutOutput(BaseModel):
    documents: List[Document] = Field(default_factory=list)
    comps: List[Comp] = Field(default_factory=list)
    listings: List[Dict[str, Any]] = Field(default_factory=list)
    macro: Dict[str, Any] = Field(default_factory=dict)
    market_notes: Optional[str] = None

class LineItem(BaseModel):
    key: str
    value: Any
    source: Optional[str] = None

class ParserOutput(BaseModel):
    rent_roll: List[Dict[str, Any]] = Field(default_factory=list)
    t12: List[Dict[str, Any]] = Field(default_factory=list)
    assumptions: List[LineItem] = Field(default_factory=list)

class UnderwriteOutput(BaseModel):
    noi: float
    dscr: Optional[float]
    ltv: Optional[float]
    coc: Optional[float]
    irr_5y: Optional[float]
    summary: str
    red_flags: List[str] = Field(default_factory=list)

class DealArtifacts(BaseModel):
    state: str = "QUEUED"
    artifacts: Dict[str, Any] = Field(default_factory=dict)
