from .request import ABRequest
from .response import ABResponse


class ABSession:

    def __init__(self):
        self.history: list[ABResponse] = []

    def add(self, request: ABRequest, result: dict):

        response = ABResponse(
            provider=request.provider,
            query=request.query,
            use_bsi=request.use_bsi,
            result=result,
        )

        self.history.append(response)

        return response
