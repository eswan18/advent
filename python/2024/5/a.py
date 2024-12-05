from .orderspec import OrderSpec


def a(input: str) -> str:
    order_spec_input, update_input = input.strip().split("\n\n")
    spec = parse_order_spec(order_spec_input)
    valid_middle_nums = []

    for update in update_input.split("\n"):
        numbers = [int(x) for x in update.split(',')]
        is_valid = validate(numbers, spec)
        if is_valid:
            middle_num = numbers[len(numbers) // 2]
            valid_middle_nums.append(middle_num)
    return str(sum(valid_middle_nums))


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