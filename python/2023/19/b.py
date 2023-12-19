from itertools import product
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from .rule import Ruleset
from .part import Part
from .range import Range


def b(input: str) -> str:
    rules_section, parts_section = input.split("\n\n")
    ruleset = Ruleset.build_from_str(rules_section)
    
    # Figure out all the ranges of values that will resolve to the same outcome.
    # To do this, we pull all the individual tests, organize them by which field
    # they test, sort them by the threshold value, and create ranges from the space between the value.
    tests = ruleset.all_tests()
    ranges: dict[str, list[Range]] = {}
    for field in "xmas":
        tests_for_field = [test for test in tests if test.field == field]
        tests_for_field.sort(key=lambda test: (test.threshold, int(test.isGt)))
        ranges[field] = []
        for test in tests_for_field:
            if len(ranges[field]) == 0:
                start = 1
            else:
                start = ranges[field][-1].end + 1
            end = test.threshold if test.isGt else test.threshold - 1
            if start > end:
                continue
            r = Range(start, end)
            ranges[field].append(r)
        # Add the remaining numbers up to 4000.
        last = ranges[field][-1]
        if last.end < 4000:
            start = last.end + 1
            end = 4000
            ranges[field].append(Range(start, end))

    accept_counts_for_x = partial(accept_counts, ms=ranges["m"], as_=ranges["a"], ss=ranges["s"], ruleset=ruleset)

    with ProcessPoolExecutor() as executor:
        counts = executor.map(accept_counts_for_x, ranges["x"])
    
    return sum(counts)


# Find all unique combinations of these ranges.
def accept_counts(x_r: Range, ms: list[Range], as_: list[Range], ss: list[Range], ruleset: Ruleset) -> int:
    n_accepted = 0
    for m_r, a_r, s_r in product(ms, as_, ss):
        # Pick the start value of each range as the value for the part.
        x = x_r.start
        m = m_r.start
        a = a_r.start
        s = s_r.start
        part = Part(x, m, a, s)
        if ruleset.route(part):
            # Count how many values are in this combination of ranges.
            n_accepted += (len(x_r) * len(m_r) * len(a_r) * len(s_r))
    return n_accepted