import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_all_data():
    countries = ["ethiopia", "kenya", "nigeria", "sudan", "tanzania"]
    dfs = []

    for c in countries:
        path = BASE_DIR / "data" / f"{c}_clean.csv"

        if path.exists():
            df = pd.read_csv(path)
            df["COUNTRY"] = c.capitalize()
            dfs.append(df)

    return pd.concat(dfs, ignore_index=True)