import enum

class DistanceUnit(enum.Enum):
    KM = "km"
    M = "m"
    NM = "nm"
    MI = "mi"
    YD = "yd"
    FT = "ft"

    @classmethod
    def values(cls):
        return [unit.value for unit in cls]

if __name__ == "__main__":
    print(DistanceUnit.values())

