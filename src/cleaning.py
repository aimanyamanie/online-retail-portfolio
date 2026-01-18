from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "online_retail.xlsx"
OUT_DIR = ROOT / "data" / "processed"
OUT_PATH = OUT_DIR / "online_retail_clean.csv"


def load_raw(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing dataset at {path}")
    return pd.read_excel(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["CustomerID"] = df["CustomerID"].astype("Int64")

    # Remove cancellations and invalid records
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    df = df[df["CustomerID"].notna()]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    df = df.drop_duplicates()
    return df


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = load_raw(RAW_PATH)
    cleaned = clean(raw)
    cleaned.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(cleaned):,} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
