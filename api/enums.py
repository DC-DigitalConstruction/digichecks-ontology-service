from enum import Enum


class PermitType(Enum):
    GCN_PERMIT = ('GCN', 'http://data.example.com/f93d5b3b-004c-4a28-8c7d-519d8e22d89d')
    BAT_PERMIT = ('Bats', 'http://data.example.com/eda64fee-9d20-4418-95db-da363ad1a1bf')
    POWER_PERMIT = ('Power', 'http://data.example.com/5652c456-b009-44c7-bce4-dc9e718dfd54')
    BUILDING_PERMIT = ('Building', 'http://data.example.com/0c2cd519-cd8d-442a-89bc-d8390349f90c')
    AUSTRIAN_PERMIT = ('AustrianBuildingPermit', 'http://data.example.com/0c2cd519-cd8d-442a-89bc-d8390349f90c')

    @property
    def type(self):
        return self.value[0]

    @property
    def uri(self):
        return self.value[1]
    
    @classmethod
    def from_type(cls, type_str: str):
        for permit in cls:
            if permit.type == type_str:
                return permit
        raise ValueError(f'No PermitType with type \'{type_str}\' found.')
