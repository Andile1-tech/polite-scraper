from src.normalizer import normalize_price


def test_normalize_price():
    assert normalize_price("£51.77") == 51.77


def test_normalize_price_with_encoding_issue():
    assert normalize_price("Â£51.77") == 51.77
