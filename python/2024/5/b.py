from .orderspec import OrderSpec
from functools import cmp_to_key


def b(input: str) -> str:
    order_spec_input, update_input = input.strip().split("\n\n")
    spec = parse_order_spec(order_spec_input)
    invalid_middle_nums = []

    for update in update_input.split("\n"):
        numbers = [int(x) for x in update.split(',')]
        is_valid = validate(numbers, spec)
        if not is_valid:
            numbers = reorder(numbers, spec)
            middle_num = numbers[len(numbers) // 2]
            invalid_middle_nums.append(middle_num)
    return str(sum(invalid_middle_nums))


def parse_order_spec(input: str) -> OrderSpec:
    spec = OrderSpec()
    for line in input.split("\n"):
        first, second = line.split("|")
        first, second = int(first), int(second)
        spec.pages[second].after.add(first)
        spec.pages[first].before.add(second)
    return spec

def validate(numbers: list[int], spec: OrderSpec) -> bool:
    for i in range(len(numbers)):
        number = numbers[i]
        is_after = set(numbers[:max(i-1, 0)])
        is_before = set(numbers[min(i+1, len(numbers)):])
        expected_after = spec.pages[number].after
        expected_before = spec.pages[number].before
        if is_after.intersection(expected_before):
            return False
        if is_before.intersection(expected_after):
            return False
    return True


def reorder(numbers: list[int], spec: OrderSpec):
    def cmp(a: int, b:int):
        '''Return -1 if a is before b, 1 if b is before a, and 0 if they're the same.'''
        if b in spec.pages[a].before:
            return -1
        if b in spec.pages[a].after:
            return 1
        if a in spec.pages[b].before:
            return 1
        if a in spec.pages[b].after:
            return -1
        return 0
    return sorted(numbers, key=cmp_to_key(cmp))