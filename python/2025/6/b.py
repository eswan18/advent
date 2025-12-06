def b(input: str) -> str:
    parts = input.strip().split('\n\n')
    # Sort by the start of each range so we can merge ranges.
    ranges = sorted(
        (Range.from_str(line) for line in parts[0].split('\n')),
        key=lambda r: (r.start, r.end),
    )
    while True:
        found_merge = merge_ranges(ranges)
        if not found_merge:
            break

    return sum(r.size() for r in ranges)
