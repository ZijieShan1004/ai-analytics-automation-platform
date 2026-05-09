from pathlib import Path

import pandas as pd


# Load a dataframe from CSV or Excel.
def load_dataframe(file_path: Path) -> pd.DataFrame:
    extension = file_path.suffix.lower()

    if extension == ".csv":
        return pd.read_csv(file_path)

    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)

    raise ValueError(f"Unsupported file extension: {extension}")