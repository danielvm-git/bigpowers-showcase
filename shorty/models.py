"""Data models for shorty."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Link:
    """A stored URL link mapping."""

    code: str
    url: str
    created_at: datetime
    hits: int = 0
