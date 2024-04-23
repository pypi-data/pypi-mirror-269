from .. import SheetModel
from .id import ModelID
from .fcde import FCDE
from .llobregat23 import LLOBREGAT23

models: dict[ModelID, SheetModel] = dict(
    fcde=FCDE, llobregat23=LLOBREGAT23
)