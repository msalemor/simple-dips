from dataclasses_json import dataclass_json
from dataclasses import dataclass

from messages.analysis_data import AnalysisData
from messages.transcription_data import TranscriptionData

from datetime import datetime, timezone
from uuid import uuid4


@dataclass_json
@dataclass
class QueueMessage:
    gid: str = str(uuid4())  # Unique identifier for the message
    type: str = "analysisagent"
    data: AnalysisData | TranscriptionData | None = (
        None  # Data associated with the message, can be None
    )
    ts: str = datetime.isoformat(
        datetime.now(timezone.utc)
    )  # Timestamp of when the message was created
