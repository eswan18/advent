from .farm import UnregionedFarm

def a(input: str) -> str:
    farm =UnregionedFarm.from_str(input)
    print(farm)
    print(farm.to_farm())