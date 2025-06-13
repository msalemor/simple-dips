from dataclasses import dataclass
from dataclasses_json import dataclass_json
from uuid import uuid4

from datetime import datetime, timezone
from time import time


@dataclass_json
@dataclass
class AnalysisData:
    content: str


@dataclass_json
@dataclass
class TranscriptionData:
    content: str


@dataclass_json
@dataclass
class Message:
    gid: str = str(uuid4())  # Unique identifier for the message
    type: str = "analysisagent"
    data: AnalysisData | TranscriptionData | None = (
        None  # Data associated with the message, can be None
    )
    ts: str = datetime.isoformat(
        datetime.now(timezone.utc)
    )  # Timestamp of when the message was created
