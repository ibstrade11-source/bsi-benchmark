from datetime import datetime, timezone
import json
from datetime import datetime
from pathlib import Path
import uuid


class ABLogger:

    def __init__(self, log_dir="ab_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True, parents=True)

    def log(self, experiment_name, results):

        experiment_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        record = {
            "experiment_id": experiment_id,
            "experiment_name": experiment_name,
            "timestamp": timestamp,
            "results": results,
        }

        file_path = self.log_dir / f"{experiment_id}.json"

        file_path.write_text(
            json.dumps(record, indent=2),
            encoding="utf-8"
        )

        return str(file_path)
