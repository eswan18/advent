from .farm import UnregionedFarm, Region, Point

def b(input: str) -> str:
    raw_farm =UnregionedFarm.from_str(input)
    farm = raw_farm.to_farm()
    return str(farm.total_price_by_sides())