from .dimensions import BSIDimensions


class BSIEvaluator:
    def evaluate(self, dataset):
        articles = dataset.articles

        if not articles:
            return BSIDimensions(
                d1=0.0,
                d2=0.0,
                d3=0.0,
                d4=0.0,
                d5=0.0,
                d6=0.0,
                d7=0.0,
            )

        d1 = min(len(articles) / 5.0, 1.0)

        d2 = sum(
            1 for a in articles
            if getattr(a, "abstract", None) and getattr(a, "doi", None)
        ) / len(articles)

        d3 = sum(
            1 for a in articles
            if getattr(a, "title", None) and len(a.title) > 10
        ) / len(articles)

        d4 = d1
        d5 = d2
        d6 = d3
        d7 = (d1 + d2 + d3) / 3.0

        return BSIDimensions(
            d1=d1,
            d2=d2,
            d3=d3,
            d4=d4,
            d5=d5,
            d6=d6,
            d7=d7,
        )
