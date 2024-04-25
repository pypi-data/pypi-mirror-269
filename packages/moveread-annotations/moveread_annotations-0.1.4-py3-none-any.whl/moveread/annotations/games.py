from pydantic import BaseModel, ConfigDict, SkipValidation

class Tournament(BaseModel):
  model_config = ConfigDict(extra='forbid')
  name: str | None = None
  group: str | None = None
  round: int | None = None
  board: int | None = None

class Headers(BaseModel):
  model_config = ConfigDict(extra='forbid')
  event: str | None = None
  site: str | None = None
  date: str | None = None
  round: int | None = None
  white: str | None = None
  black: str | None = None
  result: str | None = None

class GameMeta(BaseModel):
  model_config = ConfigDict(extra='forbid')
  tournament: Tournament | None = None
  headers: Headers | None = None
  pgn: SkipValidation[list[str] | None] = None
  early: bool | None = None
  """Whether the `PGN` stops before the game actually finished"""
