from enum import Enum


class ModelLibrary(Enum):
    """Enumeration that defines what the model library."""

    SKLEARN = "SKLEARN"
    LIGHTGBM = "LIGHTGBM"
    CATBOOST = "CATBOOST"
    KERAS = "KERAS"
    PYTORCH = "PYTORCH"
    NONE = "NONE"
