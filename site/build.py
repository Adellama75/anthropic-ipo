"""Fill site/template.html with data from data/ and write site/index.html."""
import json
import pathlib
import pandas as pd

root = pathlib.Path(__file__).resolve().parent.parent
p = pd.read_csv(root / "data/paths.csv", index_col=0)
comps = pd.read_csv(root / "data/comparables.csv")
ctx = pd.read_csv(root / "data/market_context.csv", index_col=0)

data = {"series": {t: [None if pd.isna(v) else round(v, 1) for v in p[t]] for t in p},
        "names": dict(zip(comps.ticker, comps.name)), "years": dict(zip(comps.ticker, comps.ipo_date.str[:4]))}

NOW_3M, NOW_12M = 6.1, 11.9  # Nasdaq trailing returns on 2026-10-27, from notebook 02
ctx["dist"] = ((ctx.nasdaq_3m_before - NOW_3M) ** 2 + (ctx.nasdaq_12m_before - NOW_12M) ** 2) ** 0.5
nn = ctx.drop("SPCX").nsmallest(7, "dist")
fmt = lambda v: f'<td class="{"pos" if v >= 0 else "neg"}">{"+" if v >= 0 else "−"}{abs(v):.0f}%</td>'
rows = "".join(
    f"<tr><td>{data['names'][t]} ({data['years'][t]})</td><td>{r.nasdaq_12m_before:+.0f}%</td>"
    + fmt(r.day1) + fmt(r.stock_1y_from_offer) + fmt((p[t].iloc[252] / p[t].iloc[0] - 1) * 100) + "</tr>"
    for t, r in nn.iterrows())

html = (root / "site/template.html").read_text()
quotes = (root / "site/quotes.html").read_text() if (root / "site/quotes.html").exists() else ""
html = html.replace("__DATA__", json.dumps(data, separators=(",", ":"))).replace("__NN_ROWS__", rows).replace("__QUOTES__", quotes)
(root / "site/index.html").write_text(html)
