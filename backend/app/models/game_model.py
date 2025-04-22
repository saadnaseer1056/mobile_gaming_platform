from pydantic import BaseModel
from typing import Optional

class Game(BaseModel):
    game_name: str
    developer: str
    genre: Optional[str]
    platform: str  # Steam Deck, Stadia, Both
