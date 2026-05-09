from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AIGeneratedSummaryResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    summary_type: str
    prompt_version: str
    input_facts: dict
    generated_text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)