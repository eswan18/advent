from .warehouse import BigWarehouse


def b(input: str) -> str:
    warehouse_str, move_str = input.strip().split("\n\n")
    warehouse = BigWarehouse.from_str(warehouse_str)
    move_str = move_str.replace("\n", "")
    for move in move_str:
        warehouse.make_move(move)

    return str(warehouse.sum_of_box_coords())
