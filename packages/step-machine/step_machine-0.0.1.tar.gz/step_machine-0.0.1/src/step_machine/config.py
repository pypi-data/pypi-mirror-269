from typing import Optional

from pydantic import BaseModel


class HistoryConfig(BaseModel):
    type: str
    config: dict


class SMConfig(BaseModel):
    project_name: str
    py: Optional[str] = None
    history_backend: HistoryConfig
