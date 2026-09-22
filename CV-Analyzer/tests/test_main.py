from src.main import compute_match_score


def test_compute_match_score_basic():
    cv = "Python developer with SQL, Flask, and Docker experience"
    job = "Looking for a Python developer with SQL and Docker skills"

    score = compute_match_score(cv, job)

    assert score > 0
    assert score <= 100


def test_compute_match_score_exact_match():
    cv = "python sql docker flask"
    job = "python sql docker flask"

    assert compute_match_score(cv, job) == 100.0
