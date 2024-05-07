from dataclasses import dataclass


class SFType:
    def __str__(self) -> str:
        return self.__class__.__name__

@dataclass
class AutoIncNum(SFType):
    pass

@dataclass
class Formula(SFType):
    formula: str

@dataclass
class Lookup(SFType):
    relationship_label: str
    relationship_name: str
    reference_to: str

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.reference_to})'

@dataclass
class ExtLookup(SFType):
    relationship_label: str
    relationship_name: str
    reference_to: str

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.reference_to})'

@dataclass
class CheckBox(SFType):
    formula: str

@dataclass
class Currency(SFType):
    pass

@dataclass
class Date(SFType):
    pass

@dataclass
class DateTime(SFType):
    pass

@dataclass
class Email(SFType):
    pass

@dataclass
class Geolocation(SFType):
    pass

@dataclass
class Number(SFType):
    scale: int
    precision: int

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.precision}, {self.scale})'

@dataclass
class Percent(SFType):
    pass

@dataclass
class Phone(SFType):
    pass

@dataclass
class Picklist(SFType):
    pass

@dataclass
class PicklistMulti(SFType):
    pass

@dataclass
class Text(SFType):
    length: int

@dataclass
class TextArea(SFType):
    pass

@dataclass
class TextAreaLong(SFType):
    pass

@dataclass
class TextAreaRich(SFType):
    pass

@dataclass
class TextEncrypted(SFType):
    pass

@dataclass
class Time(SFType):
    pass

@dataclass
class URL(SFType):
    pass
