from datetime import datetime
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):

    status: str = Field(..., description="Overall service status, e.g. 'ok'.")
    timestamp: datetime = Field(
        ..., description="Server time at the moment of the check."
    )
