from providers.crossref import CrossrefProvider
from providers.arxiv import ArxivProvider

def providers():

    return [

        CrossrefProvider(),

        ArxivProvider()

    ]
