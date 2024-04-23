from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Sport(str, ExtendedEnum):
    NBA = "NBA"
    NFL = "NFL"
    NHL = "NHL"
    MLB = "MLB"
    EPL = "EPL"
