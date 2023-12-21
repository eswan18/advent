from .mod import ModuleSet


def a(input: str) -> str:
    mod = ModuleSet.build_from_str(input)
    for _ in range(1000):
        mod.press_button()
    return str(mod.low_signals_sent * mod.high_signals_sent)