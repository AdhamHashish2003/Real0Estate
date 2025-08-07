import asyncio
from schemas import ParserOutput, ScoutOutput, UnderwriteOutput
from calculators import annualize_t12, compute_noi, dscr as _dscr, ltv as _ltv, cash_on_cash, simple_irr

class Underwriter:
    async def run(self, parser: ParserOutput, scout: ScoutOutput) -> UnderwriteOutput:
        await asyncio.sleep(0.05)
        ann = annualize_t12(parser.t12)
        vac = _get(parser.assumptions, "VacancyRate", 0.05)
        noi = compute_noi(ann, vacancy_rate=vac)
        comp_prices = [c.price for c in scout.comps if c.price]
        value = sum(comp_prices) / len(comp_prices) if comp_prices else None
        base_rate = (scout.macro.get("eibor") or scout.macro.get("saibor") or 0.06)
        spread = 0.015
        interest_rate = base_rate + spread
        loan_to_value_target = 0.7 if value else None
        loan_amount = (value * loan_to_value_target) if value else None
        annual_debt = (loan_amount * interest_rate) if loan_amount else None
        ltv_val = _ltv(loan_amount, value)
        dscr_val = _dscr(noi, annual_debt)
        annual_cash_flow = (noi - (annual_debt or 0)) if noi else 0
        equity = (value - (loan_amount or 0)) if value else None
        coc = cash_on_cash(annual_cash_flow, equity=equity)
        irr = simple_irr([- (equity or 0)] + [annual_cash_flow]*5 + [(value or 0)*1.03]) if equity else None
        red_flags = []
        if dscr_val and dscr_val < 1.2:
            red_flags.append(f"DSCR low: {dscr_val:.2f}")
        if ltv_val and ltv_val > 0.75:
            red_flags.append(f"LTV high: {ltv_val:.2f}")
        if coc and coc < (scout.macro.get("deposit_rate", 0.03)):
            red_flags.append("Yield below deposit rate")
        summary = (
            f"NOI: {noi:,.0f} | Rate(base+spr): {(base_rate*100):.2f}%+{(spread*100):.2f}% | "
            f"DSCR: {dscr_val:.2f if dscr_val else float('nan')} | LTV: {ltv_val:.2f if ltv_val else float('nan')} | "
            f"CoC: {coc:.2% if coc else 0:.2%}"
        )
        return UnderwriteOutput(noi=noi, dscr=dscr_val, ltv=ltv_val, coc=coc, irr_5y=irr, summary=summary, red_flags=red_flags)

def _get(items, key, default):
    for it in items:
        if getattr(it, 'key', None) == key:
            return it.value
    return default
