from .farm import UnregionedFarm

def a(input: str) -> str:
    raw_farm =UnregionedFarm.from_str(input)
    farm = raw_farm.to_farm()
    return str(farm.total_price())