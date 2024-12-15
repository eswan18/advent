from .warehouse import Warehouse


def a(input: str) -> str:
    warehouse_str, move_str = input.strip().split("\n\n")
    warehouse = Warehouse.from_str(warehouse_str)
    move_str = move_str.replace('\n', '')
    for move in move_str:
        warehouse.make_move(move)
    
    return str(warehouse.sum_of_box_coords())
