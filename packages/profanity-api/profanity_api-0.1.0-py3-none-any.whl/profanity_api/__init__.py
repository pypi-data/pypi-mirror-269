import objectrest


class ProfanityResults:
    def __init__(self, data: dict):
        self._data = data

    @property
    def is_profane(self) -> bool:
        return self._data["isProfanity"]

    @property
    def confidence(self) -> float:
        return self._data["score"]


def is_profane(message: str) -> ProfanityResults:
    response = objectrest.post(
        "https://vector.profanity.dev",
        headers={"Content-Type": "application/json"},
        json={"message": message},
    )
    response.raise_for_status()

    data = response.json()
    return ProfanityResults(data=data)
