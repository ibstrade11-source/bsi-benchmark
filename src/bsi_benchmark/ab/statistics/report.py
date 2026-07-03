import json
from pathlib import Path


class StatisticsReport:

    def write(self, summary, path):

        Path(path).write_text(
            json.dumps(summary, indent=2),
            encoding="utf-8",
        )
