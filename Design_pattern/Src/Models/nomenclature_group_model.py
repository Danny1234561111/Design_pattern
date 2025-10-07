from Src.Core.validator import validator
from Src.Core.entity_model import entity_model
class nomenclature_group_model(entity_model):
    def __eq__(self, other):
        if isinstance(other, nomenclature_group_model):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)
    def __init__(self):
        pass