from datetime import datetime

from pydantic import BaseModel, Field


class InfluxRecord(BaseModel):
    """
    A pydantic model to structure influx records stored
    in the InfluxDB.

    Attributes:
        type (str): Type of metric.
        value (float): Value of metric.
        station (str): Station metric was originally recorded.
        timestamp (datetime): Center of time window of processed metric.
    """

    type: str = Field(description="Type of infrasound record")
    value: float = Field(description="Value of infrasound record")
    station: str = Field(description="Station associated with record")
    timestamp: datetime = Field(description="record timestamp")
