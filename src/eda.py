from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "online_retail_clean.csv"
FIG_DIR = ROOT / "reports" / "figures"


def load_clean(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing cleaned data at {path}")
    df = pd.read_csv(path, parse_dates=["InvoiceDate"])
    return df


def save_fig(name: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / name
    plt.tight_layout()
    plt.savefig(out, dpi=160)
    plt.close()


def plot_monthly_revenue(df: pd.DataFrame) -> None:
    monthly = (
        df.assign(Month=df["InvoiceDate"].dt.to_period("M").dt.to_timestamp())
        .groupby("Month", as_index=False)["TotalPrice"]
        .sum()
    )

    plt.figure(figsize=(10, 4))
    sns.lineplot(data=monthly, x="Month", y="TotalPrice", marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    save_fig("monthly_revenue.png")


def plot_top_countries(df: pd.DataFrame) -> None:
    top = (
        df.groupby("Country", as_index=False)["TotalPrice"]
        .sum()
        .sort_values("TotalPrice", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(8, 5))
    sns.barplot(data=top, x="TotalPrice", y="Country", color="#4C72B0")
    plt.title("Top 10 Countries by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Country")
    save_fig("top_countries.png")


def plot_top_products(df: pd.DataFrame) -> None:
    top = (
        df.groupby("Description", as_index=False)["TotalPrice"]
        .sum()
        .sort_values("TotalPrice", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(8, 5))
    sns.barplot(data=top, x="TotalPrice", y="Description", color="#55A868")
    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Product")
    save_fig("top_products.png")


def main() -> None:
    sns.set_theme(style="whitegrid")
    df = load_clean(DATA_PATH)
    plot_monthly_revenue(df)
    plot_top_countries(df)
    plot_top_products(df)
    print(f"Charts saved to {FIG_DIR}")


if __name__ == "__main__":
    main()
