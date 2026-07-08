from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Alert:
    recommendation_id: str
    status: str = "open"          # open / acknowledged / resolved
    channel: str = "log"          # email / dashboard / log
    created_at: Optional[datetime] = None
