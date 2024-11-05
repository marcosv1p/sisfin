import json

from pathlib import Path
from typing import Dict, Optional, Any


class SaveData:
    @staticmethod
    def save(data: Dict[str, str], filename: str) -> None:
        if not Path(f"{filename}.json").exists():
            with open(f"{filename}.json", "+w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            with open(f"{filename}.json", "w", encoding="utf-8") as f:
                f.write()
        
    @staticmethod
    def load(filename) -> Optional[Any]:
        if not Path(f"{filename}.json").exists():
            with open(f"{filename}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(f"{filename}.json", "w", encoding="utf-8") as f:
                f.write()
