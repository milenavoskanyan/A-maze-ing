from typing import Any, Tuple
from my_exceptions import ConfigError
from pydantic import BaseModel, Field, NonNegativeInt, ValidationError, model_validator

class Validator(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: Tuple[NonNegativeInt, NonNegativeInt]
    exit: Tuple[NonNegativeInt, NonNegativeInt]

    @model_validator(mode="before")
    def semantic_validation(self) -> 'Validator':
        w_entry, h_entry = self.entry
        w_exit, h_exit = self.exit
        if w_entry == w_exit and h_entry == h_exit:
            raise ConfigError(f"ENTRY and EXIT cannot be the same: {self.entry} and {self.exit}")
        if w_entry < 0 or w_entry >= self.width or h_entry < 0 or h_entry >= self.height:
            raise ConfigError(f"Invalid value for ENTRY: {self.entry}")
        if w_exit < 0 or w_exit >= self.width or h_exit < 0 or h_exit >= self.height:
            raise ConfigError(f"Invalid value for EXIT: {self.exit}")
        
        return self
