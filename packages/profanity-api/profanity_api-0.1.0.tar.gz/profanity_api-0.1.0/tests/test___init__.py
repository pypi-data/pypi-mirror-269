import profanity_api


def test_no_profanity():
    results = profanity_api.is_profane(message="This is a non-profane message.")
    assert results is not None
    assert type(results) == profanity_api.ProfanityResults
    assert type(results.is_profane) == bool
    assert results.is_profane is False
    assert results.confidence >= 0.0
    assert results.confidence <= 1.0


def test_profanity():
    results = profanity_api.is_profane(message="This is a fucking profane message.")
    assert results is not None
    assert type(results) == profanity_api.ProfanityResults
    assert type(results.is_profane) == bool
    assert results.is_profane is True
    assert results.confidence >= 0.0
    assert results.confidence <= 1.0
