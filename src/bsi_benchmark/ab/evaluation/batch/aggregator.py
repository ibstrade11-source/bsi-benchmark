class ABBatchAggregator:

    def aggregate(self, results):
        n = len(results)

        if n == 0:
            return {"error": "empty dataset"}

        bsi_deltas = []
        eig_deltas = []

        for r in results:
            base = r["baseline"]
            bsi = r["with_bsi"]

            # baseline has no score, so assume 0 comparison baseline
            bsi_deltas.append(bsi.get("bsi_score", 0))

            eig_deltas.append(bsi.get("eig_score", 0))

        return {
            "count": n,
            "avg_bsi": sum(bsi_deltas) / n,
            "avg_eig": sum(eig_deltas) / n,
            "max_bsi": max(bsi_deltas),
            "min_bsi": min(bsi_deltas),
        }
