import json
from pathlib import Path


class ABStore:

    def __init__(self, log_dir="ab_logs"):
        self.log_dir = Path(log_dir)

    def list_experiments(self):
        return [p.name for p in self.log_dir.glob("*.json")]

    def load(self, experiment_file):
        path = self.log_dir / experiment_file
        return json.loads(path.read_text(encoding="utf-8"))
