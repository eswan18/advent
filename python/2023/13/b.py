from .pattern import Pattern


def b(input: str) -> str:
    patterns = [Pattern.build_from_str(s) for s in input.split("\n\n")]
    scores = [pattern.find_reflect_score(mismatches=1) for pattern in patterns]
    return str(sum(scores))