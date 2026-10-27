"""Fetch post-IPO price paths for comparable IPOs and index them to the offer price."""
import pandas as pd
import yfinance as yf

HORIZONS = {"day 1": 0, "1 month": 21, "3 months": 63, "6 months": 126, "1 year": 252}


def load_comparables(path="data/comparables.csv"):
    return pd.read_csv(path, parse_dates=["ipo_date"])


def price_path(ticker, ipo_date, offer_price, days=252):
    """Closes for the first `days` trading days, as % of the offer price (offer = 100).

    Yahoo back-adjusts history for splits, so the offer price is adjusted the same way.
    """
    t = yf.Ticker(ticker)
    end = ipo_date + pd.Timedelta(days=int(days * 1.6) + 10)
    hist = t.history(start=ipo_date, end=end, auto_adjust=False)["Close"]
    hist.index = hist.index.tz_localize(None)
    splits = t.splits
    splits.index = splits.index.tz_localize(None)
    split_factor = splits[splits.index > ipo_date].prod() if len(splits) else 1.0
    offer_adj = offer_price / split_factor
    path = (hist.iloc[: days + 1] / offer_adj * 100).reset_index(drop=True)
    return path


def build_paths(comps, days=252):
    """Wide DataFrame: rows = trading day since IPO (0 = first close), columns = ticker."""
    paths = {}
    for row in comps.itertuples():
        try:
            paths[row.ticker] = price_path(row.ticker, row.ipo_date, row.offer_price, days)
        except Exception as e:  # delisted / renamed tickers shouldn't kill the whole run
            print(f"skipping {row.ticker}: {e}")
    return pd.DataFrame(paths)


def summary(paths):
    """Return vs offer price at each horizon (NaN if the IPO is too recent)."""
    out = pd.DataFrame({h: paths.iloc[d] - 100 if d < len(paths) else None
                        for h, d in HORIZONS.items()}).round(1)
    out["peak"] = (paths.max() - 100).round(1)
    out["peak day"] = paths.idxmax()
    return out


def rebase_to_first_close(paths):
    """Same paths, but as % of the first-day close: what you'd see buying at the end of day 1."""
    return paths / paths.iloc[0] * 100
