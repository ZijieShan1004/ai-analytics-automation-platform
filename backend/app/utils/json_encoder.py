import math
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import numpy as np
import pandas as pd


# Convert values into JSON-safe Python objects.
def to_json_safe(value):
    if isinstance(value, dict):
        return {str(key): to_json_safe(item) for key, item in value.items()}

    if isinstance(value, list | tuple | set):
        return [to_json_safe(item) for item in value]

    if isinstance(value, UUID):
        return str(value)

    if isinstance(value, datetime | date):
        return value.isoformat()

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        numeric_value = float(value)
        return None if math.isnan(numeric_value) or math.isinf(numeric_value) else numeric_value

    if isinstance(value, np.ndarray):
        return [to_json_safe(item) for item in value.tolist()]

    if pd.isna(value):
        return None

    return value