from typing import List, Dict, Any, Optional

def annualize_t12(t12: List[Dict[str, Any]]) -> Dict[str, float]:
    income = sum(m["income"] for m in t12)
    opex = sum(m["opex"] for m in t12)
    months = len(t12) or 1
    factor = 12 / months
    return {"income": income * factor, "opex": opex * factor}

def compute_noi(t12_annual: Dict[str, float], vacancy_rate: float) -> float:
    eff_gross = t12_annual["income"] * (1 - vacancy_rate)
    return eff_gross - t12_annual["opex"]

def dscr(noi: float, annual_debt_service: Optional[float]) -> Optional[float]:
    if not annual_debt_service or annual_debt_service <= 0:
        return None
    return noi / annual_debt_service

def ltv(loan_amount: Optional[float], value: Optional[float]) -> Optional[float]:
    if not loan_amount or not value or value <= 0:
        return None
    return loan_amount / value

def cash_on_cash(annual_cash_flow: float, equity: Optional[float]) -> Optional[float]:
    if not equity or equity <= 0:
        return None
    return annual_cash_flow / equity

def simple_irr(cash_flows: List[float], guess: float = 0.1, iters: int = 64) -> Optional[float]:
    try:
        r = guess
        for _ in range(iters):
            npv = sum(cf / ((1 + r) ** i) for i, cf in enumerate(cash_flows))
            d = sum(-i * cf / ((1 + r) ** (i + 1)) for i, cf in enumerate(cash_flows))
            if abs(d) < 1e-9:
                break
            r -= npv / d
        return r
    except Exception:
        return None
