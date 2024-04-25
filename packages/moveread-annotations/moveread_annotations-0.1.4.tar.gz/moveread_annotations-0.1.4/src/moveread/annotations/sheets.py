from pydantic import BaseModel, ConfigDict
from scoresheet_models import ModelID

class SheetMeta(BaseModel):
  model_config = ConfigDict(extra='allow')
  model: ModelID | None = None
