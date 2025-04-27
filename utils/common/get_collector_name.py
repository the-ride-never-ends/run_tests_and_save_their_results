from typing import Any

def get_collector_name(collector: Any) -> str:
    return str(collector.__class__.__name__).rstrip("Collector").lower()
